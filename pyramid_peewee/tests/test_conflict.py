import peewee
import unittest

class ConflictTest(unittest.TestCase):
    def get_management(self):
        from pyramid_peewee.base import get_management
        return get_management()


    def test_conflict(self): #fixme
        m = self.get_management()
        base = m.get_base()

        class Foo(base):
            name = peewee.CharField()
            
        class Foo(base):
            name = peewee.CharField()

        m.setup("sqlite", ":memory:")
        m.populate()
