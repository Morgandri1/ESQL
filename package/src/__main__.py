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
from sqlalchemy import create_engine, Column, Integer, String, Float
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
            for string in strings:
                input(string)
                default = string["default"]
                f.write(f"        {string} = Column('{string}', String, default={default})\n")
            for integer in integers:
                default = integer["data"]["default"]
                f.write(f"        {integer} = Column('{integer}', Integer, default={default})\n")
            for float in floats:
                default = float["data"]["default"]
                f.write(f"        {float} = Column('{float}', Float, default={default})\n")
            for boolean in booleans:
                default = boolean["data"]["default"]
                f.write(f"        {boolean} = Column('{boolean}', Boolean, default={default})\n")
            f.close
    def start(self):
        banner("ESQL", blue)
        print("Welcome to ESQL, the easy SQL database builder!")
        print(
            """
    1. add dataset by value (ex: 123, "table")
            """
        )
        option = input("what would you like to do? ")
        if option == "1":
            self.table = input("what would you like to name the table? ")
            self.add_dataset_by_value()
        else:
            print("invalid option")
            self.start()

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
            value = input("what would you like to set the defualt value to? ")
            self.strings[name] = {"defualt": value}
            self.add_dataset_by_value()
        elif option == "2":
            name = input("what would you like to name the integer? ")
            value = input("what would you like to set the defualt value to? ")
            self.integers[name] = {"defualt": value}
            self.add_dataset_by_value()
        elif option == "3":
            name = input("what would you like to name the float? ")
            value = input("what would you like to set the defualt value to? ")
            self.floats[name] = {"defualt": value}
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
            self.booleans[name] = {"defualt": value}
            self.add_dataset_by_value()
        elif option == "5":
            name = input("what would you like to name the list? ")
            self.lists.append(name)
            self.add_dataset_by_value()
        elif option == "6":
            self.write(self.table, self.strings, self.integers, self.floats, self.booleans, self.lists)

if argv[0] == "-c" or "--create":
    ESQL()
