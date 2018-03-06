#per game, Totals, per 36 minutes, per 100 poss, advanced, playoffs per game, playoffs per 36 minutes, playoffs per 100 poss, playoffs advanced, College
import requests
from bs4 import BeautifulSoup
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Base, Player, PlayerData
from constdata import sqlUrl

dataFile = "./data/all_players"
doNotSpider = ['Player News','Full Site Menu', 'Transactions']



def getUrls(file):
    links = []
    with open(file,'r') as f:
        for line in f.readlines():
            #every line is a list
            for obj in json.loads(line.strip()):
                links.append(obj['Link'])
    return links

def getUrl(session, id):
    return session.query(Player).filter_by(id=id).first().link

def getTableNameAndID(soup):
    """
        return : {name:id, ...}
    """
    ul = soup.find('ul',class_="in_list inpage")
    lis = ul.findAll('li')
    names = [(li.get_text(),li.a['href'].replace('#',"")) 
        for li in lis if li.get_text() not in doNotSpider]
    return dict(names)

def getTable(soup, tableId):
    """
        return : table
    """
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
    result = dict()engine = create_engine(sqlurl, encoding='utf-8')
    Base.metadata.create_all(engine)
    DBsession = sessionmaker(bind=engine)
    session = DBsession()
    result['Head'] = ths
    result['Body'] = trdata
    return result

def getSoup(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.text,'lxml')
    return soup
    
if __name__ == '__main__':
    
    engine = create_engine(sqlurl, encoding='utf-8')
    Base.metadata.create_all(engine)
    DBsession = sessionmaker(bind=engine)
    session = DBsession()

    for player in session.query. 
    urls = getUrls(dataFile)

    for url in urls:
        soup = getSoup(url)
        name_id = getTableNameAndID(soup)
        for name, ID in name_id.items():
            


    

    

        

            

