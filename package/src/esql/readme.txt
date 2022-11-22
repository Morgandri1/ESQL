
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


