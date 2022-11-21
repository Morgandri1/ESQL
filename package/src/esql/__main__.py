from sys import argv
from CopperUI import *

class ESQL:
    def __init__(self):
        self.start()

    table = None
    strings = {}
    integers = {}
    floats = {}
    booleans = {}
    lists = []

    def write(self, file, strings, integers, floats, booleans, lists):
        template_start = f"""import sqlalchemy.exc as exc
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Guild(Base):
    __tablename__ = "guild"

    id = Column('id', Integer, primary_key=True)
"""

        template_end = f"""
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

        """
        with open(f"{file}.py", "w") as f:
            f.write(template_start)
            f.close
        with open(f"{file}.py", "a+") as f:
            for s in strings:
                default = strings[s]["default"]
                f.write(f"    {s} = Column('{s}', String, default='{str(default)}')\n")
            for i in integers:
                default = integers[i]["default"]
                f.write(f"    {i} = Column('{i}', Integer, default={int(default)})\n")
            for fl in floats:
                default = floats[fl]["default"]
                f.write(f"    {fl} = Column('{fl}', Float, default={float(default)})\n")
            for b in booleans:
                default = booleans[b]["default"]
                f.write(f"    {b} = Column('{b}', Boolean, default={bool(default)})\n")
            f.write("\n\n"+template_end)
            f.close
    def start(self):
        banner("ESQL", blue)
        print("Welcome to ESQL, the easy SQL database builder!")
        self.table = input("what would you like to name the database file? (ex. db.py) ")
        if self.table.endswith(".py"):
            self.table = self.table[:-3]
        print(self.table)
        self.add_dataset_by_value()

    def add_dataset_by_value(self):
        print("created new dataset default")
        print(
            """
    1. add string
    2. add integer
    3. add float
    4. add boolean
    5. add list
    6. finish up
        """
        )
        option = input("what would you like to do? ")
        if option == "1":
            name = input("what would you like to name the string? ")
            value = input("what would you like to set the default value to? ")
            self.strings[name] = {"default": value}
            self.add_dataset_by_value()
        elif option == "2":
            name = input("what would you like to name the integer? ")
            value = input("what would you like to set the default value to? ")
            self.integers[name] = {"default": value}
            self.add_dataset_by_value()
        elif option == "3":
            name = input("what would you like to name the float? ")
            value = input("what would you like to set the default value to? ")
            self.floats[name] = {"default": value}
            self.add_dataset_by_value()
        elif option == "4":
            name = input("what would you like to name the boolean? ")
            value = input("what you like True or False? (case sensitive) ")
            if not value == "True" or value == "False":
                print("invalid value")
                self.add_dataset_by_value()
            if value == "True":
                value = True
            if value == "False":
                value = False
            self.booleans[name] = {"default": value}
            self.add_dataset_by_value()
        elif option == "5":
            return print("We're sorry, but lists are not supported yet. please check back next feature update!")
            name = input("what would you like to name the list? ")
            self.lists.append(name)
            self.add_dataset_by_value()
        elif option == "6":
            self.write(self.table, self.strings, self.integers, self.floats, self.booleans, self.lists)
