from app.objects.manager import FileManager, File
from fastapi import UploadFile
from app.model.model import OCRmodel
import numpy as np
import pandas as pd
import os

class Launcher:
    """
        Used to interact with the data, Models and files
    """

    file_manager : FileManager
    model : OCRmodel

    def __init__(self):
        """
            Initialize the launcher object and train the model if it doesn't exist
            params : file path of model and list of Wines
        """ 
        self.file_manager = FileManager()

    def get_composition(self, file : File):
        """
            Get the composition of the well based on a file

            Args: file is a File object

            Returns: the dictionnary of the compositions
        """ 
        return self.model.composition(file)

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


    