import pandas as pd
import json
import numpy



def readData(dataFile):
    with open(dataFile, 'r') as f:
        table = json.load(f)
    return pd.DataFrame(table[1:],columns=table[0]).fillna(0.0)

if __name__ == '__main__':
    dataFile = './data/nba_data.txt'
    data = readData(dataFile)
    x = np.array(data.iloc[:,1:])
    y = np.array(data.iloc[:,0])
    
