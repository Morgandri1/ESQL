import sqlalchemy.exc as exc
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Guild(Base):
    __tablename__ = "guild"

    id = Column('id', Integer, primary_key=True)
    xpl = Column('xpl', Integer, default=32)
    xpMultiplier = Column('xpMultiplier', Integer, default=1)
    raidXP = Column('raidXP', Integer, default=1)
    faxp = Column('faxp', Integer, default=1)
    sexp = Column('sexp', Integer, default=1)
    gxp = Column('gxp', Integer, default=1)
    cwa = Column('cwa', String)
    password = Column('password', String)
    tpm = Column('tpm', Integer, default=1)
    cxp = Column('cxp', Integer, default=1)
    rc = Column('rc', Integer)
    ac = Column('ac', Integer)
    gc = Column('gc', Integer)
    ec = Column('ec', Integer)
    coc = Column('coc', Integer)
    lc = Column('lc', Integer)

    def __init__(self, id):
        self.id = id

    def add_verifiers(self, *verifiers):
        for verifier in verifiers:
            # Makes sure the verifiers being added have not already been added.
            if len(db.query(GuildVerifier).filter(GuildVerifier.verifier_id == verifier).filter(GuildVerifier.guild_id == self.id).all()) > 0:
                continue

            v = GuildVerifier()
            v.verifier_id = verifier
            v.guild_id = self.id

            db.add(v)

            update()

    def remove_verifiers(self, *verifiers):
        for verifier in verifiers:
            try:
                v = db.query(GuildVerifier).filter(GuildVerifier.verifier == verifier).one()

                db.remove(v)

                update()
            except exc.NoResultFound as e:
                print(e)

    def verifiers(self):
        verifiers = []
        for v in db.query(GuildVerifier).filter(GuildVerifier.guild_id == self.id).all():
            verifiers.append(v.verifier_id)
        return verifiers

class GuildVerifier(Base):
    __tablename__ = "guild_verifier"

    id = Column('id', Integer, primary_key=True)
    guild_id = Column('guild_id', Integer)
    verifier_id = Column('verifier_id', Integer)

engine = create_engine('sqlite:///database.db')
Base.metadata.create_all(bind=engine)
db = sessionmaker(bind=engine)()

def update():
    db.commit()

def get_guild(guild_id) -> Guild:
    guild_id = int(guild_id)
    try:
        return db.query(Guild).filter(Guild.id == guild_id).one()
    except exc.NoResultFound as e:
        print(e, "Creating guild table...")
        return create_guild(guild_id)

def create_guild(guild_id):
    try:
        print(f'1{guild_id}')
        guild = Guild(guild_id)

        db.add(guild)

        update()

        return guild
    except exc.IntegrityError as e: # Occurs when an object has the same key id as an object already in the table.
        print(e)
        return None

def remove_guild(guild_id):
    try:
        db.remove(db.query(Guild).filter(Guild.id == guild_id).one())
        update()
        return True
    except exc.NoResultFound as e:
        print(e)
        return False