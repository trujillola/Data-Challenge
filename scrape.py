from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import time

class ScrapeContent:

    def __init__(self):
        s=Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=s)

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



s = ScrapeContent()
for name in ["15/2-1", "15/3-2", "15/3-4", "15/3-5", "15/3-6", "15/5-4", "15/6-1", "15/6-2", "15/6-6", "15/8-1", "15/9-1", "15/9-3", "15/9-8", "15/9-9", "15/9-10", "15/12-1", "15/12-2", "15/12-3", "15/12-4"]:
    print(s.getContent(name))
    print()
s.close()