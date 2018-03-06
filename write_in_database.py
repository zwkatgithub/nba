from sqlalchemy.orm import sessionmaker
from model import Player, Base
from sqlalchemy import create_engine
import json
from constdata import sqlUrl



engine = create_engine(sqlUrl, encoding='utf-8')
Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)

session = DBSession()

dataFile = './data/all_players'

if __name__ == '__main__':
    with open(dataFile,'r') as f:

        for line in f.readlines():
            for obj in json.loads(line.strip()):
                player = Player(obj['Player'],obj['From'],obj['To'],
                    obj['Pos'],obj['Height'],obj['Weight'],
                    obj['Birth'],obj['College'],obj['Link'])
                session.add(player)
        session.commit()
    session.close()