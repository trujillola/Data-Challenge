
from pdf2image import convert_from_path
from PIL import Image
import cv2
import numpy as np
import fitz

# Class that search the column into the file
class searchColumn():

    def __init__(self):
        pass

    def findColumn(self, filename):
        # Search the correct page with the outlines
        OUTLINES = ['Composite Log', 'Composite log', 'Completion log', 'Completion Log']

        doc = fitz.open(filename)
        toc = doc.get_toc()
        for outline in toc:
            for o in OUTLINES:
                if outline[1] == o or o in outline[1]:
                    page_num = outline[2]
                    break
        
        # Convert pdf into image
        Image.MAX_IMAGE_PIXELS = None
        page = convert_from_path(filename, first_page=page_num, last_page=page_num, transparent=True)[0]

        # Cropping the image to have less image to search into
        w, h = page.size
        reduced_page = page.crop((int(w*0.42), 2500, int(w*0.5), 6000))


        # Part that search lines into the pdf
        im = cv2.cvtColor(np.array(reduced_page), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)

        kernel_size = 5
        blur_gray = cv2.GaussianBlur(gray,(kernel_size, kernel_size),0)

        low_threshold = 50
        high_threshold = 200
        edges = cv2.Canny(blur_gray, low_threshold, high_threshold)

        rho = 1  # distance resolution in pixels of the Hough grid
        theta = np.pi / 180  # angular resolution in radians of the Hough grid
        threshold = 15  # minimum number of votes (intersections in Hough grid cell)
        min_line_length = 50  # minimum number of pixels making up a line
        max_line_gap = 20  # maximum gap in pixels between connectable line segments
        line_image = np.copy(im) * 0  # creating a blank to draw lines on

        # Run Hough on edge detected image
        # Output "lines" is an array containing endpoints of detected line segments
        lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]), min_line_length, max_line_gap)


        # Keep vertical lines
        precision = 20
        x1_old,y1_old,x2_old,y2_old = 0,0,0,0
        lines = sorted(lines, key=lambda row: row[0][0])
        good_lines = []
        color_lines = []
        for line in lines:
            for x1,y1,x2,y2 in line:
                if abs(x1-x1_old)>10 and abs(x1-x2) < precision and abs(y1-y2)>250: #enlève les traits trop poche et garde les traits verticaux
                    if abs(x1-x1_old)>30:
                        cv2.line(line_image,(x1,y1),(x2,y2),(0,255,0),5)
                    else:
                        cv2.line(line_image,(x1,y1),(x2,y2),(0,0,255),5)
                    x1_old,y1_old,x2_old,y2_old = x1,y1,x2,y2
                    good_lines.append(line)
                    color_lines.append(0)


        # Search for potential columns
        col_list = []
        for i in range(0, len(good_lines)):
            for j in range(i+1, len(good_lines)):
                if abs(good_lines[i][0][0] - good_lines[j][0][0]) > 60 and abs(good_lines[i][0][0] - good_lines[j][0][0]) < 80:
                    color_lines[i] = 1
                    color_lines[j] = 1
                    col_list.append((good_lines[i][0][0], good_lines[j][0][0]))


        # Get all potential columns
        i=1
        newImageList = []
        for x1, x2 in col_list:
            test_img = reduced_page.crop((x1-1, 0, x2+1, 1000))
            newImageList.append(test_img)
            #test_img.save("litho/good_col/"+str(i)+"_1.png")
            i+=1

        return newImageList

# Example
"""sc = searchColumn()
img = sc.findColumn("NO_Quad_15/15_2-1/15_2-1__WELL__15-02-01_PB-706-0386.pdf")"""