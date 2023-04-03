from app.objects.manager import FileManager, Lithologie, ScrapeContent
from fastapi import UploadFile, File
from app.model.model import ResNetModel
import numpy as np
import pandas as pd
import os
from PIL import Image

class Launcher:
    """
        Used to interact with the data, Models and files
    """

    file_manager : FileManager
    model : ResNetModel
    info: dict

    def __init__(self):
        """
            Initialize the launcher object and train the model if it doesn't exist
            params : file path of model and list of Wines
        """ 
        self.file_manager = FileManager()
        self.model = ResNetModel("./app/model/model_demo.h5")
        self.infos = {}

    def get_composition(self, file_name : str):
        """
            Get the composition of the well based on a file

            Args: file is a File object

            Returns: the dictionnary of the compositions
        """ 
        return self.model.composition(file_name)

    def get_files_list(self):
        """
            Get the list of files

            Returns: the list of files
        """ 
        return self.file_manager.get_files_list()

    def upload_file(self, uploaded_file : UploadFile):
        """
            Adds a line of data to the csv file (and update the datasets??)

            Args:
                wine (Wine): An object of type wine to add to the csv file
            
            Returns:
                bool: True if the data was added, False otherwise.
        """
        
        return self.file_manager.upload_file(uploaded_file)


    def get_well_position(self, file_name : str):
        """
            Get the position of the well based on a file

            Args: file is a File object

            Returns: the dictionnary of the position
        """ 
        if(self.infos == {}):
            #self.infos = Lithologie(file_name).infos
            self.infos = ScrapeContent().getContent(file_name.split("__")[0])
        position = {"NS" : self.infos["NS degrees"], "EW" : self.infos["EW degrees"]}
        return position 

    def get_well_description(self, file_name : str):
        """
            Get the position of the well based on a file

            Args: file is a File object

            Returns: the dictionnary of the position
        """ 
        if(self.infos == {}):
            self.infos = ScrapeContent().getContent(file_name.split("__")[0])
        position = {"depth" : self.infos["Total depth (MD) [m RKB]"], "description" : self.infos["general"]}
        return position 

    def crop_image(self, min: int, max: int):
        # Chargement de l'image PNG
        img = Image.open('./app/data/litho_front_metres.png')

        #si sur le front on entre 400 et 450 alors on prend le crop du (0,295)
        #si sur le front on entre 450 et 500 alors on prend le crop du (275,568)

        # Délimitations des lignes à extraire (en pixels)
        lines = [(0, 295), (275, 568)]

        # Boucle sur les délimitations de lignes pour extraire les sous-images
        for i, (start, end) in enumerate(lines):
            # Découpage de l'image
            line_img = img.crop((0, start, img.width, end))
        print("-----------------------")
        print("min = ", min)
        # Enregistrement de la sous-image dans un fichier PNG
        if(min == 400):
            line_img.save(f'./app/data/split_depth-{0}.png')
        else:
            line_img.save(f'./app/data/split_depth-{1}.png')
            #line_img.save(f'split_depth-{i}.png')
        return 0