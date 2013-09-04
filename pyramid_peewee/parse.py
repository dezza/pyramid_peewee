## parse
from urllib import parse as urlparse

"""
[sqlite]
url = sqlite:///%(here)s/devdata.db
url = sqlite:
[mysql]
url = mysql://pyramid:pyramid@localhost/pyramid
[postgres]
url = postgresql://foo:bar@localhost:5432/mydatabase
"""


def setup_from_url_factory(setup_function):
    def get_options(parsed, opts):
        r = opts or {}
        if parsed.username:
            r["user"] = parsed.username
        if parsed.password:
            r["passwd"] = parsed.password
        if parsed.port:
            r["port"] = parsed.port
        return r

    def _get_path(parsed):
        if parsed.scheme == "sqlite" and parsed.path == "":
            return ":memory:"
        else:
            return parsed.path

    def setup_from_url(url, opts=None):
        parsed = urlparse.urlparse(url)
        return setup_function(parsed.scheme, _get_path(parsed),
                              connect_kwargs=get_options(parsed, opts))
    return setup_from_url
