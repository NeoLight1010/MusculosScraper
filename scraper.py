from bs4 import BeautifulSoup
from selenium import webdriver
import os
import requests
import json

this_path = os.path.dirname(__file__)
driver_path = os.path.join(this_path, 'chromedriver/chromedriver.exe')
browser = webdriver.Chrome(executable_path=driver_path)

all_cat = [
    "DESCRIPCIÓN",
    "ORIGEN",
    "INSERCIÓN",
    "FUNCIÓN",
    "IMAGEN"
]

def get_lines(string):
    lines = []
    for line in string.splitlines():
        lines.append(line.strip())
        
    return lines
    
def find_category(lines, category, all_cat):
    description = []
    in_cat = False
    
    for line in lines:
        if line == category:
            in_cat = True
            continue
        
        if line in all_cat:
            in_cat = False
            continue
        
        if in_cat:
            description.append(line)
        
    if len(description) > 1:
        return description
    else:
        return description[0]

def start_scraping():
    base_url = "https://www.ugr.es/~dlcruz/musculos/listamuscabc.htm"

    # Get HTML from url
    html_page = requests.get(base_url).text

    soup = BeautifulSoup(html_page, "html.parser")
    trs = soup.find_all("tr")

    # Find <p> tags.
    ps = []
    for tr in trs:
        ps.extend(tr.find_all("p", {"class": "MsoNormal"}))

    # Find <a> tags (that contain muscles)
    anchors = []
    for p in ps:
        found = p.find("a")
        if found:
            anchors.append(found)

    # Delete invalid anchors.
    for i, anchor in enumerate(anchors):
        if len(anchor.text.strip()) < 2:
            anchors.pop(i)

    # Get info from each muscle.
    muscles = {}
    for anchor in anchors:
        muscle_url = "https://www.ugr.es/~dlcruz/musculos/" + anchor['href']

        try:
            browser.get(muscle_url)

            title = browser.title
            body_text = browser.find_element_by_tag_name("body").text

            body_text = get_lines(body_text)

            muscles[title] = {}

            for category in all_cat:
                muscles[title][category] = find_category(body_text, category, all_cat)
        except:
            pass

    with open('results.json', 'w+') as fp:
        json.dump(muscles, fp, indent=2)

    browser.quit()

if __name__ == "__main__":
    start_scraping()
    