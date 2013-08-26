import os
import sys
import peewee
import unittest

class BaseTest(unittest.TestCase):
    def get_management(self):
        from pyramid_peewee.base import get_management
        return get_management()

    def define_model(self, base):
        class Foo(base):
            name = peewee.CharField()

        return Foo

    def assert_populate(self, management, clean=True):
        try:
            dbname = management.database.database
            sys.stderr.write("\tcreate db: %s\n" % dbname)
            management.populate()
            self.assertTrue(os.path.exists(dbname))
        finally:
            if clean and os.path.exists(dbname):
                os.remove(dbname)

    def test_models_management_before_setup(self):
        m = self.get_management()
        base = m.get_base()
        Foo = self.define_model(base)

        self.assertEquals(m.models, [base, Foo])

    def test_models_management_after_setup(self):
        m = self.get_management()
        base = m.get_base()
        Foo = self.define_model(base)

        m.setup("sqlite", "*dbname*")

        self.assertEquals(m.models, [Foo]) # for populate, base class is noneed

    def test_model_database_before_setup(self):
        m = self.get_management()
        base = m.get_base()
        Foo = self.define_model(base)

        from pyramid_peewee.skeletons import DatabaseSkeleton
        self.assertTrue(isinstance(base._meta.database, DatabaseSkeleton))
        self.assertTrue(isinstance(Foo._meta.database, DatabaseSkeleton))

    def test_model_database_after_setup(self):
        m = self.get_management()
        base = m.get_base()
        Foo = self.define_model(base)

        m.setup("sqlite", "*dbname*")

        self.assertTrue(isinstance(base._meta.database, peewee.SqliteDatabase))
        self.assertTrue(isinstance(Foo._meta.database, peewee.SqliteDatabase))

    def test_model_database_after_setup_mysql(self):
        m = self.get_management()
        base = m.get_base()
        Foo = self.define_model(base)

        m.setup("mysql", "*dbname*")

        self.assertTrue(isinstance(base._meta.database, peewee.MySQLDatabase))
        self.assertTrue(isinstance(Foo._meta.database, peewee.MySQLDatabase))

    def test_model_database_after_setup_postgresql(self):
        m = self.get_management()
        base = m.get_base()
        Foo = self.define_model(base)

        m.setup("postgresql", "*dbname*")

        self.assertTrue(isinstance(base._meta.database, peewee.PostgresqlDatabase))
        self.assertTrue(isinstance(Foo._meta.database, peewee.PostgresqlDatabase))

    ## check sqlite3 only
    def test_populate(self):
        m = self.get_management()
        base = m.get_base()
        Foo = self.define_model(base)

        m.setup("sqlite", "test.db")
        self.assert_populate(m)

    def test_populate_memory_db(self): ## TODO:fix
        m = self.get_management()
        base = m.get_base()
        Foo = self.define_model(base)

        m.setup("sqlite", ":memory:")
        self.assertRaises(AssertionError, lambda : self.assert_populate(m))

    def test_populate_multiple_times(self):
        m = self.get_management()
        base = m.get_base()
        Foo = self.define_model(base)
        
        m.setup("sqlite", "test2.db")
        self.assert_populate(m, clean=False)
        self.assert_populate(m)


##TODO:drop_all
##TODO:check content of db
