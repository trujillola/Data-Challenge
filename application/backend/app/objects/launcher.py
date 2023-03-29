from app.objects.manager import FileManager, Lithologie, DataLoader, LegendExtraction
from fastapi import UploadFile, File
from app.model.model import ResNetModel, SiameseNetwork
import numpy as np
import pandas as pd
import os
import random
import tensorflow as tf
from tensorflow.keras.optimizers import Adam


class Launcher:
    """
        Used to interact with the data, Models and files
    """

    file_manager : FileManager
    path_separator = os.path.sep
    model : SiameseNetwork
    lithologie : Lithologie
    legend_extractor : LegendExtraction

    # Environment settings
    LOAD_DATA = True
    IS_EXPERIMENT = False
    train_name = 'train'
    train_path = './app/data/train.txt'
    test_name = 'test'
    test_path = './app/data/test.txt'
    WIDTH = HEIGHT = 124
    CEELS = 1
    loss_type = "binary_crossentropy"
    validation_size = 0.2
    early_stopping = True
    seeds = [0]
    lr = [0.00005]
    batch_size = [32]
    epochs = [10]
    patience = [5]
    min_delta = [0.1]
    output_path = './app/model/'
    data_path = './app/data/results/'
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

    def __init__(self):
        """
            Initialize the launcher object and train the model if it doesn't exist
            params : file path of model and list of Wines
        """ 
        self.file_manager = FileManager()
        self.legend_extractor = LegendExtraction()
        self.lithologie = Lithologie()
        
        # files paths
        self.dataloader = DataLoader(self.WIDTH, self.HEIGHT, self.CEELS, self.data_path, self.output_path)
        
        # A path for the weights
        load_weights_path = os.path.join(self.output_path, 'weights.h5')

        # Construct the model
        self.model = SiameseNetwork(seed=self.seeds[0], width=self.WIDTH, height=self.HEIGHT, cells=self.CEELS, loss=self.loss_type, metrics=['accuracy'],
                                optimizer=Adam(lr=self.lr[0]), dropout_rate=0.4)
        
        # Get the weights of the model
        self.model._load_weights(load_weights_path)

    def get_composition(self, well_name : str):
        """
            Get the composition of the well based on a file

            Args: file is a File object

            Returns: the dictionnary of the compositions
        """ 
        
        # Extract the patterns from the legend
        legend_path = os.path.join(self.data_path, well_name, "legend.png")

        legend_output_folder = os.path.join(self.data_path, well_name, "legend/")
        self.legend_extractor.extract_patterns_from_legend(legend_path, legend_output_folder)

        # Get the dictionnary with the legend images
        legend_patterns = self.dataloader.load_from_dir(well_name, legend=True)

        # Extract the patterns from the lithology
        litho_path = os.path.join(self.data_path, well_name, "completion_log.png")
        litho_output_path = os.path.join(self.data_path, well_name, "stones/")

        self.lithologie.split_litho(well_name, litho_path, litho_output_path)
        print("Legend : ",legend_patterns)

        # Get the dictionnary with the litho images
        litho = self.dataloader.load_from_dir(well_name, legend=False)

        # Get the prediction for each image
        litho_predictions = {}
        for key in litho:
            print(key)
            # litho_predictions[key] = self.model.predict_stone_class(litho[key], legend_patterns)
        """_summary_

        Returns:
            _type_: _description_
        """        
        return {"oui": 1, "non" : 2}

    def run_siamese(self) : 
        """
            Run the siamese network
        """
        self.model.run_siamese(self.train_name, self.test_name, self.WIDTH, self.HEIGHT, self.CEELS, self.loss_type, self.validation_size, self.early_stopping)


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
        infos = Lithologie().get_litho_infos(file_name)
        position = {"NS" : infos["NS degrees"], "EW" : infos["EW degrees"]}
        return position 

    def get_well_description(self, file_name : str):
        """
            Get the position of the well based on a file

            Args: file is a File object

            Returns: the dictionnary of the position
        """ 
        infos = Lithologie().get_litho_infos(file_name)
        position = {"depth" : infos["Total depth (MD) [m RKB]"], "description" : infos["general"]}
        return position 