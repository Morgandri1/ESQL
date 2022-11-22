import sqlalchemy.exc as exc
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Guild(Base):
    __tablename__ = "guild"

    id = Column('id', Integer, primary_key=True)

    def add_test(self, *items):
        for item in items:
            if len(db.query(Guildtest).filter(Guildtest.test_id == item).filter(Guildtest.guild_id == self.id).all()) > 0:
                continue

            i = Guildtest()
            i.test_id = item
            i.guild_id = self.id

            db.add(i)

            update()

    def remove_test(self, *items):
        for item in items:
            try:
                i = db.query(Guildtest).filter(Guildtest.item == item).one()

                db.remove(i)

                update()
            except exc.NoResultFound as e:
                return "No result"

    def test(self):
        test = []
        for v in db.query(Guildtest).filter(Guildtest.guild_id == self.id).all():
            test.append(v.test_id)
        return test
                
class Guildtest(Base):
    __tablename__ = "guild_test"

    id = Column('id', Integer, primary_key=True)
    guild_id = Column('guild_id', Integer)
    test_id = Column('test_id', Integer)
                


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

        