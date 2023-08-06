import os
from . import __version__


class Config(object):
    # Above all enters the flask app, below does not.
    # Would those settings belong here or should they be somewhere else, i.e.
    # a specific dtool lookup server configuration file?
    # This option allows a client to submit direct mongo-syntaxed queries
    # to the underlying mongo database. Externally managed privileges will
    # be enforced as usual by embedding such queries in accompanying logical
    # 'and' clauses, see utils._preprocess_privileges() and
    #  utils._dict_to_mongo_query().
    ALLOW_DIRECT_QUERY = os.environ.get('DTOOL_LOOKUP_SERVER_ALLOW_DIRECT_QUERY',
                                        'True').lower() in ['true', '1', 'y', 'yes', 'on']
    # This option allows a client to submit direct mongo-syntaxed aggregations
    # to the underlying mongo database. As above, externally managed privileges
    # will still apply to the initial '$match' stage of the aggregation
    # pipeline (see utils._dict_to_mongo_aggregation()), but can be easiliy
    # circumvented in subsequent aggregation stages. Further notice that
    # aggregation stages allow write access to the database, thus this option
    # should only be enabled if some privileges are configured a the MongoDB
    # level as well.
    ALLOW_DIRECT_AGGREGATION = os.environ.get('DTOOL_LOOKUP_SERVER_ALLOW_DIRECT_AGGREGATION',
                                              'False').lower() in ['true', '1', 'y', 'yes', 'on']

    @classmethod
    def to_dict(cls):
        """Convert plugin configuration into dict."""
        exclusions = []  # config keys to exclude
        d = {'version': __version__}
        for k, v in cls.__dict__.items():
            # select only capitalized fields
            if k.upper() == k and k not in exclusions:
                d[k.lower()] = v
        return d
