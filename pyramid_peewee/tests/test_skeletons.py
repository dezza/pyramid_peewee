import unittest
import peewee

class SkeltonAdapterTest(unittest.TestCase):
    def make_skeleton(self):
        from pyramid_peewee.skeletons import AdapterSkeleton
        return AdapterSkeleton()

    def test_dispatch(self):
        skeleton = self.make_skeleton()

        self.assertEqual(skeleton.dispatch("sqlite"), peewee.SqliteAdapter)
        self.assertEqual(skeleton.dispatch("mysql"), peewee.MySQLAdapter)
        self.assertEqual(skeleton.dispatch("postgres"), peewee.PostgresqlAdapter)
        self.assertRaises(NotImplementedError, lambda : skeleton.dispatch("foo"))

    def test_concrete(self):
        skeleton = self.make_skeleton()
        db = skeleton.concrete("sqlite")
        self.assertTrue(isinstance(db, peewee.SqliteAdapter))
        self.assertFalse(isinstance(db, skeleton.__class__))

class SkeltonDatabaseTest(unittest.TestCase):
    def make_skeleton(self):
        from pyramid_peewee.skeletons import DatabaseSkeleton
        return DatabaseSkeleton("dbname")

    def test_dispatch(self):
        skeleton = self.make_skeleton()

        self.assertEqual(skeleton.dispatch("sqlite"), peewee.SqliteDatabase)
        self.assertEqual(skeleton.dispatch("mysql"), peewee.MySQLDatabase)
        self.assertEqual(skeleton.dispatch("postgres"), peewee.PostgresqlDatabase)
        self.assertRaises(NotImplementedError, lambda : skeleton.dispatch("foo"))
        
    def test_concrete(self):
        skeleton = self.make_skeleton()
        db = skeleton.concrete("sqlite")
        self.assertTrue(isinstance(db, peewee.SqliteDatabase))
        self.assertFalse(isinstance(db, skeleton.__class__))
