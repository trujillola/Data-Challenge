from dataclasses import dataclass
import pandas as pd
import os
from sklearn.model_selection import train_test_split


@dataclass
class File():
    """
        Describe the File Class
    """


    def __init__(self):
        """
            Initailize a new Wine Class with its parameters
        """
        return
    


class Datasets:
    """
        Describe the Datasets Class
    """

    X_train : list
    y_train : list
    X_test : list
    y_test : list

    def __init__(self, data):
        """
            Initialize a new Dataset with its parameters
        """
        data = ...

        # Select the target variable column    
        y = ...

        # Select the columns corresponding to the features describing the wine
        X = ...

        # Split the dataset into training and test sets
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.33, random_state=42)
      


@dataclass
class FileManager:
    """
        Class used to interact with files
    """

    file_names : list()
    dir : str = "./app/data/NO_Quad_15"

    def __init__(self):
        """
            Initialize a new Class
            params : str of file path
        """
        self.file_names = self.get_files_list()

    def get_file(self):
        """
        """
        return
    
    def upload_file(self, file):
        """
        """
        return
    
    def get_files_list(self):
        """
            Browse the files in the directory and returns a list of their names
        """
        list_files = []
        for directory in os.listdir(self.dir):
            for file in os.listdir(self.dir + "/" + directory):
                list_files.append(file)
        return list_files