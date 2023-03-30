from dataclasses import dataclass
import glob
import shutil
from fastapi import UploadFile, File
import pandas as pd
import os
from sklearn.model_selection import train_test_split
import cv2
import numpy as np
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import time
import pickle
import tqdm
from PIL import Image, ImageOps
# Librairies
import os
import cv2
import math
import Levenshtein  # une bibliothèque Python pour calculer la distance de Levenshtein
import easyocr
import numpy as np
from selenium.webdriver.chrome.options import Options

class ScrapeContent:

    def __init__(self):


        #driver_exe = 'chromedriver'
        options = Options()
        options.add_argument("--headless")
        # self.driver = webdriver.Chrome(driver_exe, options=options)

        s=Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=s, options=options)


        self.driver.get("https://factpages.npd.no/en/wellbore/PageView/Exploration/All")

    def getContent(self, report_name):
        report_name = report_name.replace("_", "/")
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        nav = soup.find("ul", {"class": "uk-nav uk-nav-parent-icon uk-nav-sub"})
        li_list = nav.find_all("li")
        link = ""
        for li in li_list:
            if li.text.strip() == report_name:
                link = li.find("a")['href']
                break

        if link == "":
            return None

        self.driver.get(link)
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')

        div_table = soup.find("table", {"class": "general-info-table"})
        tr_list = div_table.find_all("tr")
        contents_name = ['NS degrees', 'EW degrees', 'Total depth (MD) [m RKB]']
        content_json = {}
        for tr in tr_list:
            td_list = tr.find_all("td")
            if td_list != []:
                for content in contents_name:
                    if content in td_list[0].text:
                        content_json[content] = td_list[1].text.strip()

        li_history = soup.find("li", {"id": "wellbore-history"})
        while li_history == None:
            time.sleep(1)
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            li_history = soup.find("li", {"id": "wellbore-history"})

        span_list = li_history.find_all("span")

        content_json["general"] = ""
        get_next = False
        for span in span_list:
            if "Operations and results" in span.text:
                break
            elif get_next:
                content_json["general"] += span.text.strip()
            else:
                get_next = "General" in span.text
        
        return content_json
        
    def close(self):
        self.driver.quit()


class DataLoader(object):
    """
    Class for loading data from image files
    """
    def __init__(self, width, height, cells, data_path, output_path):
        """
        Proper width and height for each image.
        """
        self.width = width
        self.height = height
        self.cells = cells
        self.data_path = data_path
        self.output_path = output_path

    def _open_image(self, path):
        """
        Using the Image library we open the image in the given path. The path must lead to a .jpg file.
        We then resize it to 105x105 like in the paper (the dataset contains 250x250 images.)

        Returns the image as a numpy array.
        """
        image = Image.open(path)
        image = ImageOps.grayscale(image)
        image = image.resize((self.width, self.height))
        data = np.asarray(image)
        data = np.array(data, dtype='float64')
        return data

    def convert_image_to_array(self, image_name, image_num, data_path, predict=False):
        """
        Given a person, image number and datapath, returns a numpy array which represents the image.
        predict - whether this function is called during training or testing. If called when training, we must reshape
        the images since the given dataset is not in the correct dimensions.
        """
        max_zeros = 4
        # image_num = '0' * max_zeros + image_num
        # image_num = image_num[-max_zeros:]
        # image_path = os.path.join(data_path, 'stones', f'{image_num}.png')
        image_data = self._open_image(image_name)
        if not predict:
            image_data = image_data.reshape(self.width, self.height, self.cells)
        return image_data

    def load(self, set_name):
        """
        Writes into the given output_path the images from the data_path.
        dataset_type = train or test
        """
        file_path = os.path.join(self.data_path, f'{set_name}.txt')
        print(file_path)
        print('Loading dataset...')
        x_first = []
        x_second = []
        y = []
        names = []
        with open(file_path, 'r') as file:
            lines = file.readlines()
        for line in tqdm.tqdm(lines):
            line = line.split()
            if len(line) == 4:  # Class 0 - non-identical
                names.append(line)
                first_stone_name, first_image_num, second_stone_name, second_image_num = line[0], line[1], line[2], \
                                                                                           line[3]
                first_image = self.convert_image_to_array(stone=first_stone_name, image_num=first_image_num, data_path=self.data_path)
                second_image = self.convert_image_to_array(stone=second_stone_name,
                                                           image_num=second_image_num,
                                                           data_path=self.data_path)
                x_first.append(first_image)
                x_second.append(second_image)
                y.append(0)
            elif len(line) == 3:  # Class 1 - identical
                names.append(line)
                stone_name, first_image_num, second_image_num = line[0], line[1], line[2]
                first_image = self.convert_image_to_array(stone=stone_name,
                                                          image_num=first_image_num,
                                                          data_path=self.data_path)
                second_image = self.convert_image_to_array(stone=stone_name,
                                                           image_num=second_image_num,
                                                           data_path=self.data_path)
                x_first.append(first_image)
                x_second.append(second_image)
                y.append(1)
            elif len(line) == 1:
                print(f'line with a single value: {line}')
        print('Done loading dataset')
        with open(self.output_path, 'wb') as f:
            pickle.dump([[x_first, x_second], y, names], f)

    def load_from_dir(self, well_name : str, legend : bool):
        """
            Load the legend of the well
        """
        if not legend:
            path = os.path.join(self.data_path, well_name, 'stones/')
        else :
            path = os.path.join(self.data_path, well_name, 'legend/')
        print(path)
        result_dict = dict()
        images = glob.glob(path+"*.png")
        for image in os.listdir(path):
            image_name = image.split(".")[0]
            image_data = self._open_image(path+image)
            result_dict[image_name] = image_data
        print(result_dict)
        return result_dict

print("Loaded data loader")




@dataclass
class Lithologie():
    """
        Describe the lithologie Class
    """

    scrapper : ScrapeContent
    infos : dict

    def __init__(self):
        """
            Initailize a new Wine Class with its parameters
        """
        self.scrapper = ScrapeContent()
        
    def get_litho_infos(self,litho_name):
        """
            Returns the litho infos
        """
        return self.scrapper.getContent(litho_name.split("__")[0])
    
    def split_litho(self,litho_name, litho_path, litho_stones_dir):
        """
            Returns the litho images
        """ 
        image = cv2.imread(litho_path)
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

        # Fuse rectangles that are too small and follow each other
        # cnts = self.fuse_small_rectangles(cnts)

        for c in cnts:
            cv2.drawContours(result, [c], 0, (36,255,12), 1)


        # Delete stone directory and recreate it directory to store cropped images
        if os.path.exists(litho_stones_dir):
            for file_name in os.listdir(litho_stones_dir):
                file = litho_stones_dir + file_name
                os.remove(file)
        else : 
            os.makedirs(litho_stones_dir)
        
        # # Find maximum and minimum of x coordinates 
        x_start = 0
        x_end = image.shape[1]

        # Find maximum and minimum of y coordinates for each block of stones
        y_top = cnts[0][0][0][1]
        y_end = image.shape[0]
        cv2.imwrite(litho_stones_dir+str(0)+".png", image[y_top:y_end, x_start:x_end])
        for i in range(len(cnts)-1):
            y_end = cnts[i][0][0][1]
            y_top= cnts[i+1][0][0][1]
            cv2.imwrite(litho_stones_dir+str(i+1)+".png", image[y_top:y_end, x_start:x_end])
        y_end = cnts[len(cnts)-1][0][0][1]
        y_top = 1
        if y_end - y_top > 0:
            cv2.imwrite(litho_stones_dir+str(len(cnts))+".png", image[y_top:y_end, x_start:x_end])


@dataclass
class FileManager:
    """
        Class used to interact with files
    """

    file_names : list()

    def __init__(self):
        """
            Initialize a new Class
            params : str of file path
        """
        self.file_names = self.get_files_list()
    
    def upload_file(self, path : str, uploaded_file : bytes = File(...)):
        """
            Upload a file to the directory
            - columns 
            - legend
        """
        print(uploaded_file)
        # file_directory = uploaded_file.filename.split("__")[0]
        if not os.path.exists(path):
            os.mkdir(path)
        file_location = path+uploaded_file.filename
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(uploaded_file.file, file_object)
        return {"info": f"file '{uploaded_file.filename}' saved at '{file_location}'"}
    
    def get_files_list(self, dir : str = "./app/data/results/"):
        """
            Browse the files in the directory and returns a list of their names
        """
        list_files = []
        for directory in os.listdir(dir):
            if "completion_log.png" in os.listdir(dir + "/" + directory) and "legend.png" in os.listdir(dir + "/" + directory):
                list_files.append(directory)
        return list_files
    
class LegendExtraction():
        
    ## Objectif : Extraction des motifs
    dictionnaire = list(set([
        'pyrite', 'to', 'limestone', 'Marl', 'glauconite', 'bitumen', 
        'dolomite', 'mico', 'nannofossil', 'fine', 'grained', 
        'coarse', 'ooze', 'sand', 'sandstone', 'siderite',
        'clasts', 'flame', 'dewatering' ,'deflected', 'around', 'nodular'
        'diamict', 'diamictite', 'with', 'silt', 'clay',
        'matrix', 'foraminifer', 'silty', 'sandy', 'calcareous',
        'clayey', 'conglomerate', 'diatom', 'siltstone', 'breccia',
        'radiolarian', 'volcanic', 'ash', 'or', 'tuff', 'chalk',
        'claystone', 'silt-sized', 'sand-sized', 'serpentine','limestone',
        'chert', 'sand-silt-clay', 'sheared', 'phacoidal'
        'rock', 'lignite', 'sand', 'anhydrite', 'dolomite',
        'chalk', 'clay', 'claystone', 'coal', 'coal lignite',
        'conglomerate', 'dolomite', 'dolomitic', 'gypsum',
        'igneous', 'limestone', 'marl', 'marlstone', 'rock', 'salt',
        'clay', 'sandstone', 'fining-upward', 'trend', 'calcite', ''
        'shale', 'silt', 'siltstone', 'tuff']))


    def __init__(self):
        pass      

    def ocr_img(self,file_name : str) -> tuple :
        # here you can use any other language you want
        reader = easyocr.Reader(['en'])

        # using the read text function generating the text from image
        output = reader.readtext(file_name)

        return output


    def correction_word(self, word : str, dictionnaire : dict) -> str:
        """ 
        Correction du mot à partir du dictionnaire et de la distance de Lichtenstein 
        si la probabilité calculé avec easyocr n'est pas fiable
        Args:
            word (str): mot à changer
            dictionnaire (dict): dictionnaire des mots existants
        Returns:
            str: mot corrigé
        """
        liste_mots = word.split()
        liste_mots = [mot.lower() for mot in liste_mots]
        lst_sentence = []
        for mot in liste_mots:
            distances = {}
            for legende_mot in dictionnaire:
                distances[legende_mot] = Levenshtein.distance(mot, legende_mot)
            
            if np.min(list(distances.values())) > 5:
                lst_sentence.append(mot)
            else :
                lst_sentence.append(min(distances, key=distances.get))
        
        return ' '.join(lst_sentence)

    # A partir de la sortie de l'ocr et du dictionnaire, on récupère la position
    # des mots et on les corrige si nécessaire
    def word_and_coord(self, output, dictionnaire : dict, proba_seuil : float):
        dict_mot_coord = {}

        for word_legend in output:
            coord, txt, proba = word_legend
            
            x_min, y_min = [int(min(idx)) for idx in zip(*coord)]
            x_max, y_max = [int(max(idx)) for idx in zip(*coord)]

            # Correction du mot selon la probabilité
            nouveau_mot = self.correction_word(txt, dictionnaire) if proba < proba_seuil else txt
            
            dict_mot_coord[nouveau_mot] = {
                "proba" : proba,
                "x_min" : x_min,
                "x_max" : x_max,
                "y_min" : y_min,
                "y_max" : y_max
            }

        return dict_mot_coord


    # ## Récupérer les rectangles
    def get_rect(self, file_name):
        img = cv2.imread(file_name)

        # Convertir l'image en niveaux de gris
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Appliquer un flou gaussien pour réduire le bruit
        blur = cv2.GaussianBlur(gray, (5, 5), 0)

        # Appliquer une binarisation adaptative pour mettre en évidence les contours
        thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)

        # Trouver les contours de l'image
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        dict_rect = {}
        convex_contours = []
        j = 0

        lst_aire_w_h = []
        lst_h, lst_w, lst_aire, lst_center_point = [], [], [], []
        # Extraire les rectangles de l'image en utilisant les contours trouvés

        for contour in contours:
            # Récupérer les contours convexes
            hull = cv2.convexHull(contour)
            area = cv2.contourArea(hull)

            # Les accepter selon un aire minimum
            if area > 1000 and area < 10000 :
                # Créer un rectangle à partir de l'élément convexe
                x, y, w, h = cv2.boundingRect(hull)
                
                lst_aire_w_h.append({
                    "aire" : area,
                    "rect" : (x, y, w, h),
                    "hull" : hull
                })
                
                lst_h.append(h)
                lst_w.append(w)
                lst_aire.append(area)
                lst_center_point.append((x + w//2, y + h //2))
                
        # Calculer la médiane des aires
        med_h = np.median(lst_h)
        med_w = np.median(lst_w)
        med_aire = np.median(lst_aire) 

        for aire_w_h in lst_aire_w_h:
            x, y, w, h = aire_w_h["rect"]
            aire = aire_w_h["aire"]
            hull = aire_w_h["hull"]
            
            if (h > med_h*6//7) and (w > med_w*6//7) and (aire > med_aire*6//7):
                nom_fichier = f"rect_{j}"
                dict_rect[nom_fichier] = (x, y, w, h)
                convex_contours.append(hull)
                j += 1
        
        return convex_contours, dict_rect, img


    # Attribuer à chaque rectangle la légende qui lui va
    def assign_legend_pattern(self, dict_mot_coord : dict, dict_rect : dict):
        # Pour chaque mot : trouver la boite la plus proche
        dict_mot_rect = {}

        dict_mot_coord_copy = dict_mot_coord.copy()

        for mot, coord in dict_mot_coord_copy.items():    
            # mot = xmin et ymax
            x_mot, y_mot = coord["x_min"], coord["y_max"]

            lst_distance_boite = []
            
            for key_rect in dict_rect.keys():
                x, y, w, h = dict_rect[key_rect]
                x_box, y_box = x + w, y + h // 2
                
                dist_eucli = math.sqrt((y_box - y_mot)**2 + (x_box - x_mot)**2)
                lst_distance_boite.append(dist_eucli)
            
            # On trouve la clé du rectangle qui nous concerne
            dict_mot_coord[mot]["dist_rect"] = np.min(lst_distance_boite)
            dict_mot_coord[mot]["rect"] = list(dict_rect.keys())[np.argmin(lst_distance_boite)]
            
            dict_mot_rect[mot] = list(dict_rect.keys())[np.argmin(lst_distance_boite)]

        del(dict_mot_coord_copy)

        return dict_mot_rect, dict_mot_coord


    def assign_pattern_legend(self, dict_mot_rect : dict, dict_mot_coord : dict, dict_rect : dict):
        dict_rect_mot = {}
        for word, rect in dict_mot_rect.items():
            word_y_min = dict_mot_coord[word]["y_min"]
            word_y_max = dict_mot_coord[word]["y_max"]
            rect_y_min = dict_rect[rect][1]
            rect_y_max = dict_rect[rect][1]+dict_rect[rect][3] # = (x, y, w, h)
            
            if word_y_max < rect_y_max + 20 and rect_y_min - 20 < word_y_min:
                if rect in dict_rect_mot.keys():
                    dict_rect_mot[rect] += " " + word
                else:
                    dict_rect_mot[rect] = word
        
        return dict_rect_mot


    def save_patterns(self, dossier, dict_rect : dict, dict_rect_mot : dict, img, convex_contours : list):
        if not os.path.exists(dossier):
            os.makedirs(dossier)
        else : 
            shutil.rmtree(dossier)
            os.makedirs(dossier)
        
        acc = 0

        for key_rect in dict_rect.keys():
            x, y, w, h = dict_rect[key_rect]
            
            if key_rect in dict_rect_mot:
                nom = dict_rect_mot[key_rect]
            else : 
                nom = f"unknow_{acc}"
                acc += 1
            
            # On enregistre la sous partie qu'on souhaite
            cv2.imwrite(f"{dossier}{nom}.jpg", img[y:y+h, x:x+w])
            
        # Dessiner les contours simplifiés sur l'image originale
        cv2.drawContours(img, convex_contours, -1, (255, 0, 0), 2)

        print(f"Il y a {len(dict_rect.keys())} motifs dans cette légende")

        # # Afficher l'image avec les rectangles extraits
        # cv2.imwrite(f"{dossier}full_legend.jpg", img)

    def extract_patterns_from_legend(self, file_name : str, dossier : str, proba_seuil : float = 0.6):
        # OCR sur l'image
        output = self.ocr_img(file_name)

        # Récupérer les mots et leurs coordonnées (les mots sont corrigés)
        dict_mot_coord = self.word_and_coord(output, self.dictionnaire, proba_seuil)

        # Récupérer les rectangles potentiels et leurs informations
        convex_contours, dict_rect, img = self.get_rect(file_name)

        # On associe à chaque mot le rectangle le plus proche
        dict_mot_rect, dict_mot_coord = self.assign_legend_pattern(dict_mot_coord, dict_rect)

        # A partir de l'association précédente, on déduit les noms de légendes pour chaque rectangle
        dict_rect_mot = self.assign_pattern_legend(dict_mot_rect, dict_mot_coord, dict_rect)

        # On enregistre les motifs dans le chemin souhaité
        self.save_patterns(dossier, dict_rect, dict_rect_mot, img, convex_contours)    


