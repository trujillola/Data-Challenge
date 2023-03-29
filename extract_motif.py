# Librairies
import os
import cv2
import math
import Levenshtein  # une bibliothèque Python pour calculer la distance de Levenshtein
import easyocr
import numpy as np

## Objectif : Extraction des motifs
file_name = 'motifs_legende/legende_rapports/15-3-2/leg_15-3-2.png'
dossier = "save_legend/15-3-2/"
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

def ocr_img(file_name : str) -> tuple :
    # here you can use any other language you want
    reader = easyocr.Reader(['en'])

    # using the read text function generating the text from image
    output = reader.readtext(file_name)

    return output


def correction_word(word : str, dictionnaire : dict) -> str:
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
def word_and_coord(output, dictionnaire : dict, proba_seuil : float):
    dict_mot_coord = {}

    for word_legend in output:
        coord, txt, proba = word_legend
        
        x_min, y_min = [int(min(idx)) for idx in zip(*coord)]
        x_max, y_max = [int(max(idx)) for idx in zip(*coord)]

        # Correction du mot selon la probabilité
        nouveau_mot = correction_word(txt, dictionnaire) if proba < proba_seuil else txt
        
        dict_mot_coord[nouveau_mot] = {
            "proba" : proba,
            "x_min" : x_min,
            "x_max" : x_max,
            "y_min" : y_min,
            "y_max" : y_max
        }

    return dict_mot_coord


# ## Récupérer les rectangles
def get_rect(file_name):
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
def assign_legend_pattern(dict_mot_coord : dict, dict_rect : dict):
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


def assign_pattern_legend(dict_mot_rect : dict, dict_mot_coord : dict, dict_rect : dict):
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


def save_patterns(dossier, dict_rect : dict, dict_rect_mot : dict, img, convex_contours : list):
    if not os.path.exists(dossier):
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

    # Afficher l'image avec les rectangles extraits
    cv2.imwrite(f"{dossier}full_legend.jpg", img)

def main(file_name : str, dossier : str, proba_seuil : float = 0.6):
    # OCR sur l'image
    output = ocr_img(file_name)

    # Récupérer les mots et leurs coordonnées (les mots sont corrigés)
    dict_mot_coord = word_and_coord(output, dictionnaire, proba_seuil)

    # Récupérer les rectangles potentiels et leurs informations
    convex_contours, dict_rect, img = get_rect(file_name)

    # On associe à chaque mot le rectangle le plus proche
    dict_mot_rect, dict_mot_coord = assign_legend_pattern(dict_mot_coord, dict_rect)

    # A partir de l'association précédente, on déduit les noms de légendes pour chaque rectangle
    dict_rect_mot = assign_pattern_legend(dict_mot_rect, dict_mot_coord, dict_rect)

    # On enregistre les motifs dans le chemin souhaité
    save_patterns(dossier, dict_rect, dict_rect_mot, img, convex_contours)    


main(file_name, dossier)