import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import json

baseUrl = 'https://www.basketball-reference.com/leagues/NBA_{0}_advanced.html'
years = [str(2007+y) for y in range(10)]
head = ['pos', 'per', 'ts_pct', 'orb_pct','drb_pct', 'trb_pct', 'ast_pct','stl_pct','blk_pct', 
        'tov_pct', 'usg_pct', 'ows','dws','ws','obpm','dbpm']

#table = {var[i]:[] for i in range(len(var))}
rows = []
for year in years:
    print('processing '+year+' ...')
    html = requests.get(baseUrl.format(year))
    soup = BeautifulSoup(html.text, 'lxml')
    trs = soup.findAll('tr', class_='full_table')
    for tr in trs:
        tds = tr.findAll('td')[1:]
        row = [td.get_text() if td.get_text()!='' else None for td in tds if td['data-stat'] in head]
        rows.append(row)
rows.insert(0,head)
with open('./data/nba_data.txt','w') as f:
    f.write(json.dumps(rows))

            
