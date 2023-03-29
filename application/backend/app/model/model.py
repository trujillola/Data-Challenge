#  
from joblib import dump, load
from app.objects.manager import Lithologie
from codecarbon import EmissionsTracker
from PIL import Image
import os
import pandas as pd
import numpy as np
import glob
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import openpyxl
from openpyxl.chart import PieChart, Reference


class ResNetModel:
    """
        Create an ResNetModel object and methods to interact with it
    """

    model : None
    model_filepath : str
    data_dir : str = "./app/data/results/"
    # class_labels : list = ['anhydrite', 'calcareous_dolomite', 'chalk', 'chert', 'clay', 'coal_lignite', 'conglomerate', 'dolomite', 'dolomitic_limestone', 'fossiliferous', 'glauconite', 'gypsum', 'limestone', 'marl', 'metamorphic', 'pyrite', 'salt', 'sand', 'shale', 'silt', 'tuff']
    class_labels : list = ['coal_lignite', 'marl', 'marl_limestone', 'sand', 'sand_clay']
    
    def __init__(self, model_file_name : str):
        """
            Initialize the model
            args : model file path 
        """
        self.model_filepath = model_file_name
        self.model = tf.keras.models.load_model(self.model_filepath, compile=False)
        self.model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    def predict(self, stones_directory : str):
        """
            Predict the lithology composition and measure the blocks heights
        """ 
        heights = {m: [] for m in self.class_labels}
        class_predictions = {m: 0 for m in self.class_labels}
        # Get the list of images
        image_files = glob.glob(stones_directory + "/*.png")
        for image_file in image_files:
            # Find image height
            img_original_size = Image.open(image_file)
            height = img_original_size.height
            valeur_relative = height / 100

            # Do the class prediction 
            img = load_img(image_file, target_size=(224, 224))
            x = img_to_array(img)
            x = np.expand_dims(x, axis=0)
            x = preprocess_input(x)
            preds = self.model.predict(x)
            class_idx = np.argmax(preds[0])
            predicted_label = self.class_labels[class_idx]
            class_predictions[predicted_label] += 1
            heights[predicted_label].append(valeur_relative)
        return class_predictions, heights

    def create_excel(self, litho_dir : str, heights : dict, class_predictions : dict):
        """
            Create an excel file with the composition of the well
        """
        # Trouver la classe prédite qui a été choisie le plus grand nombre de fois
        most_predicted_class = max(class_predictions, key=class_predictions.get)
        # Trouver le nombre de fois que cette classe a été choisie
        most_predictions_count = class_predictions[most_predicted_class]

        # Créer le tableur Excel
        wb = openpyxl.Workbook()
        ws = wb.active


        # Ajouter les hauteurs relatives pour chaque matériau dans le tableur
        for i, m in enumerate(self.class_labels):
            # Ajouter le nom du matériau dans la première colonne
            ws.cell(row=i+2, column=1, value=m)

            # Ajouter les hauteurs relatives dans les colonnes suivantes
            for j, h in enumerate(heights[m]):
                ws.cell(row=i+2, column=j+2, value=h)

        # Ajouter la ligne des totaux en bas
        #for j in range(2, 7):
        #10 etant le nb de fois qu'un matériau est prédit
        for j in range(2, most_predictions_count+2):
            sub_sum = sum(ws.cell(row=i, column=j).value or 0 for i in range(2, len(self.class_labels)+2))
            ws.cell(row=len(self.class_labels)+2, column=j, value=sub_sum)

        # Ajouter la colonne des totaux
        for i in range(2, len(self.class_labels)+3):
            sub_sum = sum(ws.cell(row=i, column=j).value or 0 for j in range(2,  len(self.class_labels)))
            ws.cell(row=i, column=most_predictions_count+2, value=sub_sum)

        # Ajouter la colonne des pourcentages
        for i in range(2, len(self.class_labels)+2):
            total = ws.cell(row=len(self.class_labels)+2, column=most_predictions_count+2).value
            percent = sum(ws.cell(row=i, column=j).value or 0 for j in range(2, most_predictions_count+2)) / ws.cell(row=len(self.class_labels)+2, column=most_predictions_count+2).value
            ws.cell(row=i, column=most_predictions_count+3, value=percent).number_format = '0.00%'

        #génération du graphique camembert
        # Créer le graphique camembert
        chart = PieChart()
        chart.title = "Pourcentage Lithologie"

        # Ajouter les données du graphique
        labels = Reference(ws, min_col=1, min_row=2, max_row=len(self.class_labels)+1)
        data = Reference(ws, min_col=most_predictions_count+3, min_row=1, max_row=len(self.class_labels)+1)
        chart.add_data(data, titles_from_data=True)
        chart.set_categories(labels)

        # Ajouter le graphique au tableur
        ws.add_chart(chart, "J2")

        # Enregistrer le tableur Excel
        wb.save(litho_dir+"resultats.xlsx")

        return 1

    def get_composition_from_excel(self,litho_dir : str):
        composition_dict = {}
        res_path = litho_dir+"resultats.xlsx"
        # Nom de la feuille dans le fichier Excel
        nom_feuille = "Sheet"

        # Lire le fichier Excel en utilisant pandas
        df = pd.read_excel(res_path, sheet_name=nom_feuille)

        # Cette colonne sera toujours en premièr, et donc s'appellera toujours comme ca
        # Nom de la colonne que vous voulez retourner
        nom_colonne = "Unnamed: 0"

        # Sélectionner la colonne spécifique en utilisant le nom de la colonne
        df[nom_colonne] = df[nom_colonne].dropna()
        list_nom = df[nom_colonne].to_list()
        # Supprime le denrier élément de la liste
        # Comme on ajoute une ligne à la fin du tableau pour les totaux, cela sera toujours de cette configuration aussi
        list_nom.pop()
        # print(df)

        # Afficher la colonne
        # print(list_nom)

        # Supprimer toutes les colonnes qui contiennent plus de 5 NaN
        df = df.dropna(thresh=len(df)-(len(list_nom) - 1) , axis = 1)

        # Sélectionner la dernière colonne restante
        list_nombre = df.iloc[:, -2].to_list()
        list_nombre.pop()
        # print(list_nombre)
        return list_nom, list_nombre
    
    def composition(self,file_name : str):
        """
            Get the composition of the well based on a file

            Args: file is a File object

            Returns: the dictionnary of the compositions
        """ 
        litho = Lithologie(file_name)
        litho.split_litho()
        stones_directory = litho.litho_stones_dir
        class_predictions, heights = self.predict(stones_directory)
        print('******************************')
        print(class_predictions)
        print('******************************')
        print(heights)
        print('******************************')
        self.create_excel(litho.litho_dir,heights,class_predictions)
        noms, valeurs = self.get_composition_from_excel(litho.litho_dir)
        print("noms, valuers = ", noms, "valeurs ", valeurs)
        return noms, valeurs
    



   