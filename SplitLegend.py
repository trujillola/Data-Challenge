import cv2
from PIL import Image
import numpy as np
import pytesseract



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

text = pytesseract.image_to_string(blur,)
print(text)

# Trouver les contours des rectangles dans l'image
contours, hierarchy = cv2.findContours(blur, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Extraire les rectangles de l'image en utilisant les contours trouvés
for contour in contours:
    # Calculer l'aire du contour
    area = cv2.contourArea(contour)
   
    # Ignorer les contours trop petits ou trop grands
    if area < 2000 or area > 80000:
         continue

    print(area)  

    # Trouver le rectangle qui englobe le contour
    rect = cv2.minAreaRect(contour)
    box = cv2.boxPoints(rect)
    box = box.astype('int')
    # print(box)

    # Dessiner le rectangle sur l'image originale
    cv2.drawContours(img, [box], 0, (0, 0, 255), 2)

# Afficher l'image avec les rectangles extraits
cv2.imshow('Legende avec les rectangles extraits', img)
cv2.waitKey(0)
cv2.destroyAllWindows()