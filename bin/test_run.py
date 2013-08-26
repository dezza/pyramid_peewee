from datetime import datetime
from pyramid_peewee import get_management
import peewee as pw

Management = get_management()
Base = Management.get_base()

class SpellBook(Base):
    title = pw.CharField()
    published_at = pw.DateTimeField()

class Spell(Base):
    book = pw.ForeignKeyField(SpellBook)
    name = pw.CharField()

def main(dbtype, dbname, kwargs=None):
    print(("dbtype:%s,  dbname:%s" % (dbtype, dbname)))
    Management.setup(dbtype, dbname, **(kwargs or {}))
    Management.populate()

    book = SpellBook.create(title="foo", published_at=datetime.now())
    fire = Spell.create(book=book, name='curse of fucking',title="fire")

    selected_book = SpellBook.get()
    print((list(Spell.filter(book=selected_book))))
    Management.drop_all()

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 5: #fixme
        dbtype, dbname, kwargs = sys.argv[1], sys.argv[2], dict(user=sys.argv[3], passwd=sys.argv[4])
    elif len(sys.argv) < 3:
        dbtype, dbname,  kwargs = "sqlite", ":memory:", {}
    else:
        dbtype, dbname, kwargs = sys.argv[1], sys.argv[2], {}
    main(dbtype, dbname, kwargs)
