from .parse import setup_from_url_factory
from .base import get_management # for convinient

def _get_opts(settings):
    opts = {}
    if "peewee.threadlocals" in settings:
        opts["threadlocals"] = settings["peewee.threadlocals"]
    if "peewee.autocommits" in settings:
        opts["autocommits"] = settings["peewee.autocommits"]
    return opts

def peewee_management_setup_from_config(config, peewee_management):
    settings = config.registry.settings
    opts = _get_opts(settings)

    if "peewee.url" in settings:
        setup_from_url_factory(peewee_management.setup)(settings["peewee.url"], opts)
    else:
        dbname = settings["peewee.dbname"]
        dbtype = settings["peewee.db_type"]
        peewee_management.setup(dbtype, dbname, opts)

def includeme(config):
    config.add_directive("peewee_management_setup_from_config", peewee_management_setup_from_config)
