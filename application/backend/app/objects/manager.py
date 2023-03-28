from dataclasses import dataclass
from fastapi import UploadFile, File
import pandas as pd
import os
from sklearn.model_selection import train_test_split
import cv2


@dataclass
class Lithologie():
    """
        Describe the lithologie Class
    """

    litho_name : str
    litho_dir : str
    litho_stones_dir : str
    documents_dir : str = "./app/data/NO_Quad_15/"
    results_dir : str = "./app/data/results/"
    
    def __init__(self, litho_name):
        """
            Initailize a new Wine Class with its parameters
        """
        self.litho_name = litho_name
        self.litho_dir = self.results_dir+litho_name.split("__")[0]+"/"
        self.litho_stones_dir = self.litho_dir+"stones/"
        

    def split_litho(self):
        """
            Returns the litho images
        """        
        print(self.litho_dir)
        image = cv2.imread(self.litho_dir+'completion_log.png')
        result = image.copy()

        # Convert to grayscale and apply Otsu's thresholding
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray,0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        # Detect horizontal lines
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40,1))
        detect_horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=1)
        detect_horizontal = cv2.dilate(detect_horizontal,horizontal_kernel,iterations = 1)
        cnts = cv2.findContours(detect_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        for c in cnts:
            cv2.drawContours(result, [c], 0, (36,255,12), 1)

        # Save the split image
        cv2.imwrite(self.litho_dir+"split.png", result)

        # Delete stone directory and recreate it directory to store cropped images
        if os.path.exists(self.litho_stones_dir):
            for file_name in os.listdir(self.litho_stones_dir):
                file = self.litho_stones_dir + file_name
                os.remove(file)
        else : 
            os.makedirs(self.litho_stones_dir)
        
        # # Find maximum and minimum of x coordinates 
        x_start = 0
        x_end = image.shape[1]

        # Find maximum and minimum of y coordinates for each block of stones
        y_top = cnts[0][0][0][1]
        y_end = image.shape[0]
        cv2.imwrite(self.litho_stones_dir+str(0)+".png", image[y_top:y_end, x_start:x_end])
        for i in range(len(cnts)-1):
            y_end = cnts[i][0][0][1]
            y_top= cnts[i+1][0][0][1]
            cv2.imwrite(self.litho_stones_dir+str(i+1)+".png", image[y_top:y_end, x_start:x_end])
        y_end = cnts[len(cnts)-1][0][0][1]
        y_top = 1
        if y_end - y_top > 0:
            cv2.imwrite(self.litho_stones_dir+str(len(cnts))+".png", image[y_top:y_end, x_start:x_end])


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
    
    def upload_file(self, uploaded_file : UploadFile):
        """
        """
        file_directory = uploaded_file.filename.split("__")[0]
        if not os.path.exists(self.dir+"/"+file_directory):
            os.mkdir(self.dir+"/"+file_directory)
        file_location = self.dir+"/"+file_directory+"/"+uploaded_file.filename
        with open(file_location, "wb+") as file_object:
            file_object.write(uploaded_file.file.read())
        return {"info": f"file '{uploaded_file.filename}' saved at '{file_location}'"}
    
    def get_files_list(self):
        """
            Browse the files in the directory and returns a list of their names
        """
        list_files = []
        for directory in os.listdir(self.dir):
            for file in os.listdir(self.dir + "/" + directory):
                list_files.append(file)
        return list_files