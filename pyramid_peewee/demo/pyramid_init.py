from pyramid.config import Configurator
import sqlahelper

"""
appname = demo
"""
from demo.models import get_management 

""" e.g. in development.ini

peewee.url = :memory:
peewee.db_type = sqlite

or 

peewee.url = %(here)s/peewee.db
peewee.db_type = sqlite

"""
def main(global_conf, **settings):
    config = Configurator(settings=settings)
    config.include("pyramid_peewee")

    peewee_management = get_management()
    config.setup_from_config(peewee_management)
    peewee_management.populate()

    return config.make_wsgi_app()
