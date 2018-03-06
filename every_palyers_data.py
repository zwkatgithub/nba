#per game, Totals, per 36 minutes, per 100 poss, advanced, playoffs per game, playoffs per 36 minutes, playoffs per 100 poss, playoffs advanced, College
import requests
from bs4 import BeautifulSoup
import json

dataFile = "./data/all_players"
doNotSpider = ['Player News','Full Site Menu', 'Transactions']

def getLinks(file):
    links = []
    with open(file,'r') as f:
        for line in f.readlines():
            #every line is a list
            for obj in json.loads(line.strip()):
                links.append(obj['Link'])
    return links

def getTableNameAndID(soup):
    ul = soup.find('ul',class_="in_list inpage")
    lis = ul.findAll('li')
    names = [(li.get_text(),li.a['href'].replace('#',"")) 
        for li in lis if li.get_text() not in doNotSpider]
    return dict(names)

def getTable(soup, tableId):
    div = soup.find('div',id = tableId)
    if div is None:
        return None
    table = div.find('table')
    return table
def processTrWithTh(tr):
    result = []
    result.append(tr.th.a.get_text())
    for td in tr.findAll('td'):
        result.append(td.get_text())
    return result
def processRegularTable(table):
    ths = [th.get_text() for th in table.thead.tr.findAll('th')]
    trs = table.tbody.findAll("td")
    trdata = []
    for tr in trs:
        row = processTrWithTh(tr)
        assert len(row) == len(ths)
        trdata.append(row)
        
    

    

        

            

