import peewee
import sys
#from .skeletons import AdapterSkeleton
from .skeletons import DatabaseSkeleton
import playhouse.signals


class ModelPool(object):
    def __init__(self):
        self.registerd_models = []
        self._consumed_models = []

    def add(self, model):
        self.registerd_models.append(model)

    def consume(self):
        r = []
        pool = self.registerd_models
        while pool:
            model = pool.pop()
            # if not model._is_basemodel():
            self._consumed_models.append(model)
            r.append(model)
        return r

    @property
    def consumed_models(self):
        return (m for m in self._consumed_models if not m._is_basemodel())

    @property
    def is_consumed(self):
        return not bool(self.registerd_models)


class ModelManagement(object):
    def __init__(self, pool, dummy_name):
        self.pool = pool
        self.database = DatabaseSkeleton(dummy_name)

    def get_base(self):
        pool = self.pool
        _database = self.database

        #class ModelMetaWithPool(peewee.BaseModel):
        #peewee.BaseModel is Metaclass
        class ModelMetaWithPool(peewee.BaseModel):
            def __new__(cls, name, bases, attrs):
                cls = super(ModelMetaWithPool, cls).__new__(cls, name,
                                                            bases, attrs)
                pool.add(cls)
                return cls

        #class BaseModel(peewee.Model, metaclass=ModelMetaWithPool):
        class BaseModel(playhouse.signals.Model, metaclass=ModelMetaWithPool):
            @classmethod
            def _is_basemodel(cls):
                return cls == BaseModel

            class Meta:
                database = _database

        return BaseModel

    def is_setuped(self):
        return not hasattr(self.database, "concrete")

    def setup(self, db_type, new_name, fields=None, connect_kwargs=None):
        print(connect_kwargs)
        ## sinot mde effect
        self.database.rename(new_name)
        database = self.database.concrete(db_type, fields,
                                          connect_kwargs or {})
        for m in self.pool.consume():
            m._meta.database = database
        self.database = database  # over write

    def drop_all(self):
        if not self.is_setuped:
            raise Exception("please. self.setup(db_type, new_name)")

        for m in self.pool.consumed_models:
            m.drop_table()

    def populate(self, force=False):
        if not self.is_setuped:
            raise Exception("please. self.setup(db_type, new_name)")

        if force:
            for m in self.pool.consumed_models:
                m.drop_table()
                m.create_table()
        else:
            for m in self.pool.consumed_models:
                if not m.table_exists():
                    m.create_table()

    @property
    def models(self):
        if self.pool.is_consumed:
            return list(self.pool.consumed_models)
        else:
            ## TODO:using logger?
            print("WARNING: THIS IS FUCKING ABOUT TO BREAK! \
                   OPEN YOUR FUCKING BASE.PY AND GET YOURSELF TOGETHER!")
            sys.stderr.write("theese models are not concreted, yet")
            sys.stderr.write("\n\t+ ")
            sys.stderr.write("\n\t+ ".join(repr(m) for m in self.pool.registerd_models))
            sys.stderr.write("\nplease. self.setup(db_type, new_name)\n")
            return self.pool.registerd_models


def get_management(dummy_name="*dummy*"):
    pool = ModelPool()
    return ModelManagement(pool, dummy_name)
