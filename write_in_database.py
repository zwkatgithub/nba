from sqlalchemy.orm import sessionmaker
from model import Player, Base, PlayerData
from sqlalchemy import create_engine
import json
from constdata import sqlUrl
from process import readData


engine = create_engine(sqlUrl, encoding='utf-8')
Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)

session = DBSession()

dataFile = './data/nba_data3.txt'

if __name__ == '__main__':
    
    data = readData(dataFile)
    for i in range(len(data)):
        
        args = []
        row = data.iloc[i,:]
        player = session.query(Player).filter_by(link = row[-1]).first()
        if player is None:
            continue
        args.append(player.id)
        args.append(row[0])
        for j in row[1:-1]:
            args.append(float(j))
        print(args)
        playerData = PlayerData(*args)
        session.add(playerData)
    session.commit()
    session.close()
