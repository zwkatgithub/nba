from multiprocessing import Pool
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import os
import time
from selenium.common.exceptions import NoSuchElementException, TimeoutException

chrome_options = Options()
chrome_options.add_argument('--headless')
baseUrl = "https://www.basketball-reference.com/players/"
css_selector = "ul.alphabet.bullets-inline"
logFile = "./data/log"

def getLink(driver, index):
    if chr(index+97) != 'x': 
        li = driver.find_element_by_css_selector(css_selector).find_elements_by_tag_name('li')[index]
        return li.find_element_by_tag_name('a')
    return None

def spider(index_range):
    players = []
    index = str(os.getpid())
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(baseUrl)
    print(index+" start")
    
    for link in index_range:
        a = getLink(driver, link)
        if a is None:
            continue
        a.click()
        print(index+" "+chr(97+link))
        try:
            table = driver.find_element_by_id('players')
        except NoSuchElementException:
            with open(logFile, 'a') as log:
                log.write(time.ctime()+' '+chr(97+link)+"NoSuchElementException\n")
            continue
        except TimeoutException:
            with open(logFile, 'a') as log:
                log.write(time.ctime()+' '+chr(97+link)+'TimeoutException\n')
            continue
        tbody = table.find_element_by_tag_name('tbody')
        trs = tbody.find_elements_by_tag_name('tr')
        for tr in trs:
            tds = tr.find_elements_by_tag_name('td')
            player = dict(zip(['From',"To","Pos","Height","Weight","Birth","College"],
                [td.text for td in tds]))
            plink = tr.find_element_by_tag_name('th').find_element_by_tag_name('a')
            player['Player'] = plink.text
            print(index+" "+plink.text)
            player['Link'] = plink.get_attribute("href")
            players.append(player)
        driver.back()
    driver.close()
    with open(dataFile,'a') as file:
        file.write(json.dumps(players)+'\n')
    return None
            
result = []           


dataFile = "./data/all_players"
try:
    print("Start")
    p = Pool(26)
    index_ranges = [list(range(i,i+1)) for i in range(0,26)]
    #index_ranges=[[1],[2]]
    print(index_ranges)
    for i in range(26):
        result.append(p.apply_async(spider, args=(index_ranges[i],)))
    p.close()
    p.join()
    print("End")
except Exception:
    with open(logFile, 'a') as log:
        log.write(time.ctime()+" "+"end")

# resList = []
# for res in result:
#     resList.append(res.get())
# with open(dataFile,'w') as file:
#     file.write('\n'.join(resList))