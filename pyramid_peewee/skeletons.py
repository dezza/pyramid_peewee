import peewee
import copy

__all__ = ["AdapterSkeleton", "DatabaseSkeleton"]

class AdapterSkeleton(object):
    def dispatch(self, db_type):
        if db_type == "sqlite" or db_type == "sqlite3":
            return peewee.SqliteAdapter
        elif db_type == "mysql":
            return peewee.MySQLAdapter
        elif db_type == "postgres" or db_type == "postgresql":
            return peewee.PostgresqlAdapter
        else:
            raise NotImplementedError("%s is not support. support: sqlite, mysql, postgresql" % db_type)

    def concrete(self, db_type):
        db_type = db_type.lower()
        return self.dispatch(db_type)() # return instance

    reserved_tables = [] #

class DatabaseSkeleton(peewee.Database): #TODO: add help message (when calling any method before concrete())
    def dispatch(self, db_type):
        if db_type == "sqlite" or db_type == "sqlite3":
            return peewee.SqliteDatabase
        elif db_type == "mysql":
            return peewee.MySQLDatabase
        elif db_type == "postgres" or db_type == "postgresql":
            return peewee.PostgresqlDatabase
        else:
            raise NotImplementedError("%s is not support. support: sqlite, mysql, postgresql" % db_type)

    def concrete(self, db_type, fields=None, _connect_kwargs=None):
        kwargs = copy.copy(self.connect_kwargs)
        if _connect_kwargs:
            kwargs.update(_connect_kwargs)

        dbclass = self.dispatch(db_type.lower())
        dbname = self.database
        if fields:
            return dbclass(dbname, fields=fields, **kwargs) #return instance
        return dbclass(dbname, **kwargs) #return instance

    def rename(self, new_name):
        self.database = new_name

    def __init__(self, database, **connect_kwargs):
        super(DatabaseSkeleton, self).__init__(AdapterSkeleton(), database, **connect_kwargs)
