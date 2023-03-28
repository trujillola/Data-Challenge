## TODO
# 1. Clean up code
# 2. Add comments
# 3. Check si la ligne est assez longue pour être considérée comme une délimitation
# 4. Gérer le cas où la légende contient des lignes horizontales

import cv2
import os

dir = './NO_Quad_15/15_3-4/'

image = cv2.imread(dir+'completion_log.png')

result = image.copy()
# Convert to grayscale and apply Otsu's thresholding
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray,0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

cv2.imwrite(dir+"thresh.png", thresh)

# Detect horizontal lines
horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40,1))
detect_horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=1)
detect_horizontal = cv2.dilate(detect_horizontal,horizontal_kernel,iterations = 1)
cnts = cv2.findContours(detect_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    cv2.drawContours(result, [c], 0, (36,255,12), 1)

cv2.imwrite(dir+"split.png", result)


## CROP IMAGES

#Create directory to store cropped images
if not os.path.exists(dir+"stones/"):
    os.makedirs(dir+"stones/")

# # Find maximum and minimum of x coordinates 
x_start = 0
x_end = image.shape[1]
# Find maximum and minimum of y coordinates for each block of stones
y_top = cnts[0][0][0][1]
y_end = image.shape[0]
cv2.imwrite(dir+"stones/"+str(0)+".png", image[y_top:y_end, x_start:x_end])
for i in range(len(cnts)-1):
    y_end = cnts[i][0][0][1]
    y_top= cnts[i+1][0][0][1]
    cv2.imwrite(dir+"stones/"+str(i+1)+".png", image[y_top:y_end, x_start:x_end])
y_end = cnts[len(cnts)-1][0][0][1]
y_top = 1
if y_end - y_top > 0:
    cv2.imwrite(dir+str(len(cnts))+".png", image[y_top:y_end, x_start:x_end])
