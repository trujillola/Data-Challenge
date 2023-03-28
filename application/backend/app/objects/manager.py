from dataclasses import dataclass
from fastapi import UploadFile, File
import pandas as pd
import os
from sklearn.model_selection import train_test_split
import cv2

from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import time

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



@dataclass
class Lithologie():
    """
        Describe the lithologie Class
    """

    litho_name : str
    litho_dir : str
    litho_stones_dir : str
    scrapper : ScrapeContent
    infos : dict
    documents_dir : str = "./app/data/NO_Quad_15/"
    results_dir : str = "./app/data/results/"
    
    def __init__(self, litho_name):
        """
            Initailize a new Wine Class with its parameters
        """
        self.litho_name = litho_name
        self.litho_dir = self.results_dir+litho_name.split("__")[0]+"/"
        self.litho_stones_dir = self.litho_dir+"stones/"
        self.scrapper = ScrapeContent()
        print(self.scrapper.getContent(litho_name.split("__")[0]))
        self.infos = self.scrapper.getContent(litho_name.split("__")[0])
        

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