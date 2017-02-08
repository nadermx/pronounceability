from pony.orm import *
from datetime import datetime

db = Database()

class Word(db.Entity):
    word = Required(unicode, unique=True)
    pronounceability = Required(float)
    dt_created = Required(datetime, default=datetime.utcnow())



db.bind('sqlite', 'database.sqlite', create_db=True)
# db.bind('postgres', user='', password='', host='', database='')
db.generate_mapping(create_tables=True)