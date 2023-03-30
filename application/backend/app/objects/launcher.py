import pickle
from app.objects.manager import FileManager,ExcelManager, Lithologie, DataLoader, LegendExtraction
from fastapi import UploadFile, File
from app.model.model import ResNetModel, SiameseNetwork
import numpy as np
import pandas as pd
import os
import random
import cv2
import tensorflow as tf
from tensorflow.keras.optimizers import Adam
import imagesize

class Launcher:
    """
        Used to interact with the data, Models and files
    """

    file_manager : FileManager
    excel_manager : ExcelManager
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
        self.excel_manager = ExcelManager()
        
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

        # Get the dictionnary with the litho images
        litho = self.dataloader.load_from_dir(well_name, legend=False)

    
        # Get the prediction for each image
        litho_predictions = {}
        for bloc_idx in litho:
            
            print("litho", bloc_idx)
            names = []
            x_first = []
            x_second = []
            y = []
            max_prediction_info = []
            for name, pattern in legend_patterns.items():
                # print("litho", bloc_idx, "pattern", name)
                line = [name]
                names.append(line)
                x_first.append(litho[bloc_idx])
                x_second.append(pattern)
                y.append(1)
            with open("./app/data/results/predictions.pickle", 'wb') as f:
                pickle.dump([[x_first, x_second], y, names], f)
            with open("./app/data/results/predictions.pickle", 'rb') as f:
                x_pred, y_pred, names = pickle.load(f)
            x_pred[0] = np.array(x_pred[0], dtype='float64')
            x_pred[1] = np.array(x_pred[1], dtype='float64')
            predictions = self.model.siamese_net.predict(x_pred)

            max = 0
            max_idx = 0
            for idx, prediction in enumerate(predictions):
                if prediction > max:
                    max = prediction
                    max_idx = idx
           
            max_prediction_info = [names[max_idx][0], max[0]]
            litho_predictions[bloc_idx] = max_prediction_info

        classes = self.get_classes(legend_patterns)
        # Compute the class_predictions and heights
        class_predictions, heights = self.get_infos(litho_predictions, classes, well_name)
        
        # Compute the percentages
        self.excel_manager.create_excel(litho_path, heights, class_predictions, classes)

        # Return the percentages
        return self.excel_manager.get_composition_from_excel(litho_path)

    def get_classes(self, legend_patterns):
        classes = []
        for name, pattern in legend_patterns.items():
            classes.append(name)
        return classes
    
    def get_infos(self,litho_predictions, classes, well_name):
        # Number of times a class has been predicted
        class_predictions = {m: 0 for m in classes}
        # Dictionary of the cumulatives heights for each class
        heights = {m: [] for m in classes}
        for id, prediction in litho_predictions.items():
            class_predictions[prediction[0]] += 1
            path = "./app/data/results/"+well_name+"/stones/"+id+".png"
            im = cv2.imread(path)
            w, height, c =  im.shape
            valeur_relative = height / 100
            heights[prediction[0]].append(valeur_relative)
        return class_predictions, heights
        
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