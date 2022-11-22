from sys import argv
from CopperUI import *

readme = """
Hello! Thanks for using ESQL.

you may be looking for implimentation help, so here it is!

move the generated file to your project directory, and import it.

then, you can get your guild's table by using the get_guild(*guild_id*) function. (guild ID needs to be a string.)

usually it's gonna look like this:

    from esql import *

    db = get_guild(str(guild.id))

here's how to get the rest of your info:

    db.<variable name> # this will get you any simple variable. (int, str, bool, float.)
    db.<list name> # this will get you any list. lists are methods, so remember your parentheses! it returns as a python list, so you can iterate over it to your heart's content.

creating a new guild is easy:

    create_guild(str(guild.id))
    # or, you can load the guld if there's a chance the table already exists. if it doesnt, it'll create it automatically.
    db = get_guild(str(guild.id))

each list has an add method and a remove method. they can be called the same way as your list. (db.add_<list_name>(item), db.remove_<list_name>(item))


"""

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
            for l in lists:
                f.write(f"""
    def add_{l}(self, *items):
        for item in items:
            if len(db.query(Guild{l}).filter(Guild{l}.{l}_id == item).filter(Guild{l}.guild_id == self.id).all()) > 0:
                continue

            i = Guild{l}()
            i.{l}_id = item
            i.guild_id = self.id

            db.add(i)

            update()

    def remove_{l}(self, *items):
        for item in items:
            try:
                i = db.query(Guild{l}).filter(Guild{l}.item == item).one()

                db.remove(i)

                update()
            except exc.NoResultFound as e:
                return "No result"

    def {l}(self):
        {l} = []
        for v in db.query(Guild{l}).filter(Guild{l}.guild_id == self.id).all():
            {l}.append(v.{l}_id)
        return {l}
                """)
            for l in lists:
                f.write(f"""
class Guild{l}(Base):
    __tablename__ = "guild_{l}"

    id = Column('id', Integer, primary_key=True)
    guild_id = Column('guild_id', Integer)
    {l}_id = Column('{l}_id', Integer)
                """)
            f.write("\n\n"+template_end)
            f.close
        with open("readme.txt", "w") as f:
            f.write(readme)
    def start(self):
        clearscreen()
        banner("ESQL", blue)
        print("Welcome to ESQL, the easy SQL database builder!")
        self.table = input("what would you like to name the database file? (ex. db.py) ")
        if self.table.endswith(".py"):
            self.table = self.table[:-3]
        print(self.table)
        self.add_dataset_by_value()

    def add_dataset_by_value(self):
        clearscreen()
        banner("ESQL", blue)
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
            name = input("what would you like to name the list? ")
            self.lists.append(name)
            self.add_dataset_by_value()
        elif option == "6":
            self.write(self.table, self.strings, self.integers, self.floats, self.booleans, self.lists)

try:
    if sys.argv[1] == "-c":
        ESQL()
    else:
        print("invalid argument")
except IndexError:
    ESQL()