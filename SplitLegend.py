import cv2
from PIL import Image
import numpy as np
import pytesseract
import matplotlib.pyplot as plt
from imutils.object_detection import non_max_suppression
import os

dir = './NO_Quad_15/15_3-4/'

image = cv2.imread(dir+'legend.png')

dst = cv2.detailEnhance(image, sigma_s=10, sigma_r=0.15)

#Improve image quality
im1 = cv2.imwrite(dir+"legend_improved.png",dst)

# Charger l'image de la légende
img = cv2.imread(dir+"legend_improved.png")

# Convertir l'image en niveaux de gris
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Appliquer une binarisation pour convertir l'image en noir et blanc
thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)

blur = cv2.GaussianBlur(thresh, (5, 5), 0)

cv2.morphologyEx(image, cv2.MORPH_OPEN,np.ones((5,5),np.uint8))

# Trouver les contours des rectangles dans l'image
contours, hierarchy = cv2.findContours(blur, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#Template 
# template = cv2.imread(dir+'template.png', cv2.IMREAD_GRAYSCALE)
# pattern = cv2.imread(dir+'template.png')

#METHODE AVEC SIFT

# # Initialiser le détecteur de caractéristiques SIFT
# sift = cv2.SIFT_create()

# # Détecter les keypoints et les descripteurs pour l'image et le pattern
# img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# pattern_gray = cv2.cvtColor(pattern, cv2.COLOR_BGR2GRAY)

# kp1, des1 = sift.detectAndCompute(img_gray, None)
# kp2, des2 = sift.detectAndCompute(pattern, None)

# # Initialiser le matcher FLANN (Fast Library for Approximate Nearest Neighbors)
# FLANN_INDEX_KDTREE = 1
# index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
# search_params = dict(checks=50)

# flann = cv2.FlannBasedMatcher(index_params, search_params)

# # Trouver les correspondances entre les descripteurs de l'image et ceux du pattern
# matches = flann.knnMatch(des1, des2, k=2)

# # Faire correspondre les keypoints de l'image avec ceux du pattern
# good_matches = []
# for m, n in matches:
#     if m.distance < 0.7 * n.distance:
#         good_matches.append(m)

# src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
# dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

# # Trouver la transformation homographique entre les keypoints de l'image et ceux du pattern
# H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

# # Trouver les coins du pattern dans l'image
# h, w, d = pattern.shape
# pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
# dst = cv2.perspectiveTransform(pts, H)

# # Dessiner un contour autour des coins du pattern dans l'image
# cv2.polylines(img, [np.int32(dst)], True, (0, 0, 255), 3)
# cv2.imshow('img', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# METHODE AVEC MATCHTEMPLATE
# res = cv2.matchTemplate(thresh,template,cv2.TM_SQDIFF_NORMED)
# loc = np.where( res <= 0.6)
# loc = list(zip(*loc[::-1]))
# w,h = template.shape[::-1]
# occurrences = list()
# for i in range(4):
#     min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
#     if max_val > 0.8:
#         occurrences.append(max_loc)
#         res[max_loc[1]:max_loc[1]+h, max_loc[0]:max_loc[0]+w] = 0

# for pt in occurrences:
#     cv2.rectangle(img, pt,(pt[0]+w, pt[1] +h), (0, 0, 255), 2)
# cv2.imshow('Template', img)
# cv2.waitKey(0)


# Extraire les rectangles de l'image en utilisant les contours trouvés

#Création directory
if not os.path.exists(dir+'legende/'):
    os.makedirs(dir+'legende/')

boxes = []
i = 0
for contour in contours:

    # Calculer l'aire du contour
    area = cv2.contourArea(contour)
   
    # Ignorer les contours trop petits ou trop grands
    if area < 4000 or area > 80000:
         continue

    # Trouver le rectangle qui englobe le contour
    rect = cv2.minAreaRect(contour)
    box = cv2.boxPoints(rect)
    box = box.astype('int')

    # Enregistrer l'image du rectangle
    print("oui")
    x, y, w, h = cv2.boundingRect(contour)
    roi = img[y:y + h, x:x + w]
    cv2.imwrite(dir+'legende/'+str(i)+'.png', roi)

    i = i + 1
    # Dessiner le rectangle sur l'image
    cv2.drawContours(img, [box], 0, (0, 0, 255), 2)
    

# Afficher l'image avec les rectangles extraits
cv2.imshow('Legende avec les rectangles extraits', img)
cv2.waitKey(0)
cv2.destroyAllWindows()