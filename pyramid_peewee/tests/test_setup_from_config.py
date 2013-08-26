import unittest
import peewee 
import threading
class AssertThreadLocalsMixin(object):
    def assert_threadlocals_false(self, database):
        self.assertTrue(isinstance(database, peewee.SqliteDatabase))
        # mangling in peewee.Database
        self.assertEquals(getattr(database, "_Database__local").__name__,  "DummyLocal")
        
    def assert_threadlocals_true(self, database):
        self.assertTrue(isinstance(database, peewee.SqliteDatabase))
        # mangling in peewee.Database
        self.assertTrue(getattr(database, "_Database__local"), threading.local().__class__)
    
class FromConfigATest(AssertThreadLocalsMixin, unittest.TestCase):
    def _get_management(self):
        from pyramid_peewee import get_management
        return get_management()

    def _callFUT(self, _settings, _management):
        class config(object):
            class _registry(object):
                settings = _settings
            registry = _registry
        from pyramid_peewee import peewee_management_setup_from_config
        peewee_management_setup_from_config(config, _management)
        
    def test_threadlocals_none(self):
        management = self._get_management()
        self._callFUT({"peewee.url": "sqlite://"}, management)
        self.assert_threadlocals_false(management.database)

    def test_threadlocals_true(self):
        management = self._get_management()
        self._callFUT({"peewee.url": "sqlite://", 
                       "peewee.threadlocals": True}, management)
        self.assert_threadlocals_true(management.database)
        
        
