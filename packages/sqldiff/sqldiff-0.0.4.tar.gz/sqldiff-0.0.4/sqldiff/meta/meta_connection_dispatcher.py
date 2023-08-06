import importlib
import sys
from collections import namedtuple

import pkg_resources
from packaging import version

meta_registry = []

ConnectionMeta = namedtuple('ConnectionMeta', 'driver_name min_version max_version meta_func')


def dbmeta(driver_name, min_version=None, max_version=None):
    def decorator(func):
        meta_registry.append(ConnectionMeta(driver_name, min_version, max_version, func))
        return func
    return decorator


def check_obj(obj):
    # inspec.get()
    mod = importlib.util.module_from_spec(obj)
    base, _sep, _stem = mod.__name__.partition('.')
    return sys.modules[base]


# https://stackoverflow.com/questions/2020014/get-fully-qualified-class-name-of-an-object-in-python
def fullname(o):
    # o.__module__ + "." + o.__class__.__qualname__ is an example in
    # this context of H.L. Mencken's "neat, plausible, and wrong."
    # Python makes no guarantees as to whether the __module__ special
    # attribute is defined, so we take a more circumspect approach.
    # Alas, the module name is explicitly excluded from __qualname__
    # in Python 3.
    module = o.__class__.__module__
    if module is None or module==str.__class__.__module__:
        return o.__class__.__name__  # Avoid reporting __builtin__
    else:
        return module + '.' + o.__class__.__name__


def get_meta_provider(connection_obj):
    connection_fullname = fullname(connection_obj)
    pkg_name = connection_fullname.split('.')[0]
    pkg_version = pkg_resources.get_distribution(pkg_name).version
    for i in meta_registry:
        if pkg_name==i.driver_name and (
                not i.min_version or version.parse(pkg_version) >= version.parse(i.min_version)) and (
                not i.max_version or version.parse(pkg_version) <= version.parse(i.max_version)):
            return i.meta_func
    raise TypeError('No metadata provider defined for provided connection.')
