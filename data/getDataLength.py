import json
import sys

with open("all_players",'r') as f:
    res = []
    for line in f.readlines():
        for obj in json.loads(line.strip()):
            res.append(obj[sys.argv[1]])
print(max([len(r) for r in res]))
