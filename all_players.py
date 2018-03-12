from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json

chrome_options = Options()
chrome_options.add_argument('--headless')

driver = webdriver.Chrome(chrome_options=chrome_options)

dataFile = "./data/all_players"

baseUrl = "https://www.basketball-reference.com/players/"

css_selector = "ul.alphabet.bullets-inline"

driver.get(baseUrl)
print("1")

lis = driver.find_element_by_css_selector(css_selector).find_elements_by_tag_name('li')

def getLink(index):
    lis = driver.find_element_by_css_selector(css_selector).find_elements_by_tag_name('li')
    for i,li in enumerate(lis):
        if li.text != 'X' and i==index:
                return li.find_element_by_tag_name('a')
    return None

print("2")
players = []
for link in range(len(lis)):
    print("process link "+chr(97+link))
    a = getLink(link)
    if a is not None:
        a.click()
    else:
        continue
    table = driver.find_element_by_id('players')
    tbody = table.find_element_by_tag_name("tbody")
    trs = tbody.find_elements_by_tag_name('tr')

    for tr in trs:
        player = dict()
        th = tr.find_element_by_tag_name('th')
        player['Player'] = th.find_element_by_tag_name('a').text
        print("     process player "+th.text)
        player['Link'] = th.find_element_by_tag_name('a').get_attribute('href')
        tds = tr.find_elements_by_tag_name('td')
        z = zip(['From',"To","Pos","Height","Weight","Birth","College"],[td.text for td in tds])
        for ele in z:
            player[ele[0]] = ele[1]
        players.append(player.copy())
    driver.back()
with open(dataFile,"w") as file:
    json.dump(players,file)

driver.close()
driver.quit()