import unittest 

class ParseFromUrlTest(unittest.TestCase):
    def _callFUT(self):
        from pyramid_peewee.parse import setup_from_url_factory
        def identity(db_type, path, options):
            options["db_type"] = db_type
            options["path"] = path
            return options
        return setup_from_url_factory(identity)

    def test_sqlite(self):
        parse_function = self._callFUT()
        self.assertEquals(
            parse_function("sqlite:///foo/testdata.db"), 
            dict(db_type="sqlite", path="/foo/testdata.db")
            )

    def test_sliqte_memory(self):
        parse_function = self._callFUT()
        self.assertEquals(
            parse_function("sqlite://"), 
            dict(db_type="sqlite", path=":memory:")
            )
        
    def test_mysql(self):
        parse_function = self._callFUT()
        self.assertEquals(
            parse_function("mysql://pyramid:pyramid@localhost/pyramid"), 
            dict(db_type="mysql", path="/pyramid", 
                 user="pyramid", passwd="pyramid")
            )


    def test_postgresql(self):
        parse_function = self._callFUT()
        self.assertEquals(
            parse_function("postgresql://foo:bar@localhost:5432/mydatabase"), 
            dict(db_type="postgresql", path="/mydatabase", 
                 user="foo", passwd="bar", port=5432)
            )
