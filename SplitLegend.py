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
boxes = []
for contour in contours:
    # Calculer l'aire du contour
    area = cv2.contourArea(contour)
   
    # Ignorer les contours trop petits ou trop grands
    if area < 4000 or area > 80000:
         continue

    # print(area)  

    # Trouver le rectangle qui englobe le contour
    rect = cv2.minAreaRect(contour)
    box = cv2.boxPoints(rect)
    box = box.astype('int')
    print(box)
    boxes.append(box)
    
    # Dessiner le rectangle sur l'image originale

box_width = boxes[0][0][1] - boxes[0][2][1]
box_height = boxes[0][2][1] - boxes[0][1][1]
x_extreme_start = boxes[0][0][0]
x_extreme_end = boxes[1][0]
y_extreme_start = boxes[0][1]
y_extreme_end = boxes[2][1]

for box in boxes : 
    box[1][0] = box[1][1] + box_width * 3
    cv2.drawContours(img, [box], 0, (0, 0, 255), 2)

print(box_width)
print(box_height)
print(x_extreme_start)
print(x_extreme_end)
print(y_extreme_start)
print(y_extreme_end)

# Afficher l'image avec les rectangles extraits
cv2.imshow('Legende avec les rectangles extraits', img)
cv2.waitKey(0)
cv2.destroyAllWindows()