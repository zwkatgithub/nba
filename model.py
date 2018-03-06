from sqlalchemy import Column, String, Integer, ForeignKey
#from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from constdata import MAX_LINK_LENGTH, MAX_COLLEGE_LENGTH,DEFAULT_LENGTH ,MAX_BIRTH_LENGTH, MAX_NAME_LENGTH, MAX_FROM_TO_LENGTH

Base = declarative_base()

class Player(Base):
    __tablename__ = 'player'

    id  = Column(Integer, primary_key=True)
    name = Column(String(MAX_NAME_LENGTH))
    from_ = Column(String(MAX_FROM_TO_LENGTH))
    to = Column(String(MAX_FROM_TO_LENGTH))
    pos = Column(String(DEFAULT_LENGTH))
    height = Column(String(DEFAULT_LENGTH))
    weight = Column(String(DEFAULT_LENGTH))
    birth = Column(String(MAX_BIRTH_LENGTH))
    college = Column(String(MAX_COLLEGE_LENGTH))
    link = Column(String(MAX_LINK_LENGTH))

    def __init__(self, name,from_,to,pos,height,
        weight, birth, college, link):
        (self.name, self.from_, self.to, self.pos, 
        self.height, self.weight, self.birth, self.college, self.link) = (
        name, from_, to, pos, height, weight, birth, college, link)

    def __repr__(self):
        return '< %r, %r>' % (self.id, self.name)

class PlayerData(Base):
    __tablename__ = 'playerdata'

    id  = Column(Integer, primary_key=True)
    playerId = Column(Integer, ForeignKey(Player.id))
    

