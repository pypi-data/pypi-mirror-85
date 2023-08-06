import json
import os

from dtool_lookup_server import mongo, MONGO_COLLECTION

from . import __version__

AFFIRMATIVE_EXPRESSIONS = ['true', '1', 'y', 'yes', 'on']


class Config(object):
    # If enabled, the underlying database will offer dependency graph views on
    # the server's default collection. Those views offer on-the-fly-generated
    # collections of undirected per-dataset adjacency lists in order to
    # facilitate searching dataset dependeny graphs in both directions.
    # See https://docs.mongodb.com/manual/core/views/.
    ENABLE_DEPENDENCY_VIEW = os.environ.get('DTOOL_LOOKUP_SERVER_ENABLE_DEPENDENCY_VIEW',
                                            'True').lower() in AFFIRMATIVE_EXPRESSIONS

    # Generated dependency views are named by current UTC datetime in ISO format, prefixed by
    MONGO_DEPENDENCY_VIEW_PREFIX = os.environ.get('DTOOL_LOOKUP_SERVER_MONGO_DEPENDENCY_VIEW_PREFIX', 'dep:')

    # name of bookkeeping collection for cached dependency views
    MONGO_DEPENDENCY_VIEW_BOOKKEEPING = os.environ.get('DTOOL_LOOKUP_SERVER_MONGO_DEPENDENCY_VIEW_BOOKKEEPING', 'dep_views')

    # maximum number of cached views
    MONGO_DEPENDENCY_VIEW_CACHE_SIZE = int(os.environ.get('DTOOL_LOOKUP_SERVER_MONGO_DEPENDENCY_VIEW_CACHE_SIZE', '10'))

    # Enforce rebuilding dependency views at each query.
    FORCE_REBUILD_DEPENDENCY_VIEW = os.environ.get('DTOOL_LOOKUP_SERVER_FORCE_REBUILD_DEPENDENCY_VIEW',
                                                   'False').lower() in AFFIRMATIVE_EXPRESSIONS

    # Specify a key or multiple possible keys that hold unidirectional
    # dependency information in form of parents' UUIDs. The syntax must be
    # a single key or a JSON-formatted list of keys.
    # Nested fields are separated by a dot (.)
    DEPENDENCY_KEYS = [
        'readme.derived_from.uuid',
        'annotations.source_dataset_uuid'
    ]

    dep_key = os.environ.get('DTOOL_LOOKUP_SERVER_DEPENDENCY_KEYS', '')
    if len(dep_key) > 0:
        try:
            DEPENDENCY_KEYS = json.loads(dep_key)
        except json.JSONDecodeError:  # assume only one key, plain string
            DEPENDENCY_KEYS = [dep_key]

    # Allow clients to submit dynamic dependency keys and evoke the generation
    # of cached dependency views:
    DYNAMIC_DEPENDENCY_KEYS = os.environ.get('DTOOL_LOOKUP_SERVER_DYNAMIC_DEPENDENCY_KEYS',
                                             'True').lower() in AFFIRMATIVE_EXPRESSIONS

    @classmethod
    def to_dict(cls):
        """Convert server configuration into dict."""
        d = {'version': __version__}
        for k, v in cls.__dict__.items():
            # select only capitalized fields
            if k.upper() == k:
                d[k.lower()] = v
        return d
