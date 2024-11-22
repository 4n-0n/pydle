# noinspection PyUnresolvedReferences
from asyncio import Future
from functools import cmp_to_key
from . import connection, protocol, client, features
from .client import Error, NotInChannel, AlreadyInChannel, BasicClient, ClientPool
from .features.ircv3.cap import NEGOTIATING as CAPABILITY_NEGOTIATING, FAILED as CAPABILITY_FAILED, \
    NEGOTIATED as CAPABILITY_NEGOTIATED

import asyncio
# And use asyncio.coroutine where it was used, although it's better to switch to async def
# However, since 'coroutine' decorator is removed, you would actually need to:
from functools import wraps

def coroutine(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

__name__ = 'pydle'
__version__ = '0.9.4rc1'
__version_info__ = (0, 9, 4)
__license__ = 'BSD'


def featurize(*features):
    """ Put features into proper MRO order. """

    def compare_subclass(left, right):
        if issubclass(left, right):
            return -1
        if issubclass(right, left):
            return 1
        return 0

    sorted_features = sorted(features, key=cmp_to_key(compare_subclass))
    name = 'FeaturizedClient[{features}]'.format(
        features=', '.join(feature.__name__ for feature in sorted_features))
    return type(name, tuple(sorted_features), {})


class Client(featurize(*features.ALL)):
    """ A fully featured IRC client. """
    ...


class MinimalClient(featurize(*features.LITE)):
    """ A cut-down, less-featured IRC client. """
    ...
