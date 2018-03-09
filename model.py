from sqlalchemy import Column, String, Integer, ForeignKey, Float
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
head = ['pos', 'per', 'ts_pct', 'orb_pct','drb_pct', 'trb_pct', 'ast_pct','stl_pct','blk_pct', 
        'tov_pct', 'usg_pct', 'ows','dws','ws','obpm','dbpm']
class PlayerData(Base):
    __tablename__ = 'playerdata'

    id  = Column(Integer, primary_key=True)
    playerID = Column(Integer)
    pos = Column(String(DEFAULT_LENGTH+1))
    per = Column(Float)
    ts_pct = Column(Float)
    orb_pct = Column(Float)
    drb_pct = Column(Float)
    trb_pct = Column(Float)
    ast_pct = Column(Float)
    stl_pct = Column(Float)
    blk_pct = Column(Float)
    tov_pct = Column(Float)
    usg_pct = Column(Float)
    ows = Column(Float)
    dws = Column(Float)
    ws = Column(Float)
    obpm = Column(Float)
    dbpm = Column(Float)

    def __repr__(self):
        return '<%r, %r>' % (self.id, self.playerID)
    def __init__(self, playerID, pos, per,ts_pct, orb_pct, drb_pct, 
        trb_pct, ast_pct, stl_pct, blk_pct, tov_pct, 
        usg_pct, ows, dws,ws,obpm, dbpm):
        
        (self.playerID, self.pos, self.per, self.ts_pct, self.orb_pct, self.drb_pct, 
            self.trb_pct, self.ast_pct, self.stl_pct, self.blk_pct, self.tov_pct, 
            self.usg_pct, self.ows, self.dws, self.ws, self.obpm, self.dbpm) = (
                playerID,
                pos, per, ts_pct, orb_pct, drb_pct, trb_pct, ast_pct, stl_pct,
                blk_pct, tov_pct, usg_pct, ows, dws, ws,obpm, dbpm
            )


    

