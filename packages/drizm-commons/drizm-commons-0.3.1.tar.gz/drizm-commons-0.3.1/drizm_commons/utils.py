import os
import pathlib
import shutil
from collections import OrderedDict
from functools import wraps
from typing import Union, Optional, Iterable
from urllib.parse import urlparse
from uuid import UUID


def get_application_root() -> str:
    """ Get the root path of the running application """
    return os.environ.get("PYTHONPATH").split(os.pathsep)[0]


def is_dunder(name: str) -> bool:
    """ Check whether a string is a dunder function name """
    if (name[:2] and name[-2:]) in ("__",):
        return True
    return False


def all_items_equal(iterable: Iterable) -> bool:
    """ Check whether all items in a non-hashable iterable are equal """
    if isinstance(iterable, (list, tuple)):
        return True if len(set(iterable)) == 1 else False
    raise TypeError("Only list and tuples may be processed")


def all_nested_zipped_equal(iterable: Iterable[Iterable]) -> bool:
    """
    Check whether all items at the same indexes
    in a nested iterable are equal.

    Example\n
    mylist = [[1, 2], [1, 2], [1, 2]]\n
    Would check\n
    mylist[0][0] == mylist[1][0] == mylist[2][0]
    """
    return all(
        [all_items_equal(subiter) for subiter in zip(*iterable)]
    )


def uuid4_is_valid(uuid: str) -> bool:
    """ Check whether a given string is a valid UUIDv4 """
    try:
        val = UUID(uuid, version=4)
    except ValueError:
        return False
    return val.hex == uuid


def exclude_keys(dictionary: dict, keys: Iterable) -> dict:
    """ Return a new dict - the specified keys """
    return {
        k: v for k, v in dictionary.items() if k not in keys
    }


def all_keys_present(dictionary: dict, keys: Iterable) -> bool:
    """ Check whether all specified keys are present in the dict """
    return all(k in dictionary.keys() for k in keys)


def all_items_present(list_: Union[list, tuple], values: Iterable) -> bool:
    """ Check whether all provided values are present in the list """
    return all(k in list_ for k in values)


def url_is_http(url: str) -> bool:
    """ Check whether a URL is valid HTTP """
    if url.startswith("http") or url.startswith("https"):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc, result.path])
        except (AttributeError, TypeError):
            return False
    return False


def memoize(fn):
    """
    Caches the last passed parameter,
    until a new one is provided.\n
    Only works for function with a single positional param.

    Probably not thread-safe, so use with caution.
    """
    # use a dict for mutability
    cache = OrderedDict()

    @wraps(fn)
    def mem_f(arg=None):
        if arg:
            cache[0] = arg
        try:
            res = fn(cache[0])
        except KeyError:
            raise TypeError(
                f"Function {fn.__name__} missing positional argument"
            ) from None
        else:
            return res

    return mem_f


class AttrDict(dict):
    """ A dictionary whose keys can be accessed like attributes """
    __slots__ = []

    def __getattr__(self, item):
        return super(AttrDict, self).__getitem__(item)


class _TfvarsParser:
    """ A parser class for *.tfvars files """
    def __init__(self, path: pathlib.Path) -> None:
        self.path = path

    def read(self) -> dict:
        with open(self.path, "r") as fin:
            c = fin.readlines()
        extract = lambda i: [
            el.strip() for el in [line.split("=")[i] for line in c]
        ]
        keys = extract(0)
        vals = [line[1:-1] for line in extract(1)]
        kvpairs = {k: v for k, v in zip(keys, vals)}
        return kvpairs


class Tfvars:
    """ Wrapper for a parsed *.tfvars file """
    def __init__(self, /, path: Union[str, pathlib.Path]) -> None:
        if not isinstance(path, pathlib.Path):
            path = pathlib.Path(path)
        if not path.exists():
            raise FileNotFoundError(f"The directory {path} does not exist")
        self.path = path
        self.vars = AttrDict(**_TfvarsParser(path).read())


# this is necessary because we can only subclass the concrete implementation
class Path(type(pathlib.Path())):
    def rmdir(self, recursive: Optional[bool] = True) -> None:
        if recursive:
            shutil.rmtree(self)
        else:
            super(Path, self).rmdir()


__all__ = [
    "is_dunder", "get_application_root", "uuid4_is_valid",
    "all_items_equal", "all_nested_zipped_equal", "all_items_present",
    "exclude_keys", "all_keys_present", "url_is_http",
    "AttrDict", "Tfvars", "Path", "memoize"
]
