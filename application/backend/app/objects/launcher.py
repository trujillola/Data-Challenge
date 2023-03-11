from app.objects.manager import FileManager, Datasets, File
from app.model.model import OCRmodel
import numpy as np
import pandas as pd
import os

class Launcher:
    """
        Used to interact with the data, Models and files
    """

    file_manager : FileManager
    datasets : Datasets
    model : OCRmodel

    def __init__(self,data_file_name : str = "/data/Wines.csv", save_file_name : str = "/data/random_forest.joblib"):
        """
            Initialize the launcher object and train the model if it doesn't exist
            params : file path of model and list of Wines
        """ 


    def get_composition(self, file : File):
        """
            Get the composition of the well based on a file

            Args: file is a File object

            Returns: the dictionnary of the compositions
        """ 
        return self.model.composition(file)


    def upload_file(self, file : File):
        """
            Adds a line of data to the csv file (and update the datasets??)

            Args:
                wine (Wine): An object of type wine to add to the csv file
            
            Returns:
                bool: True if the data was added, False otherwise.
        """
        result = self.file_manager.write_data(file)
        self.datasets = Datasets(self.file_manager.read_data())
        return result


    