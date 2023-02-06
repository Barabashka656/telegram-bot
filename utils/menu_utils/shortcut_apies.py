from loader import shortcut_object
from pyshorteners.exceptions import (
    ShorteningErrorException,
    # ExpandingErrorException,
    # BadAPIResponseException
)
shortcut_services = ("tinyurl", "chilpit",
                     "clckru", "dagd",
                     "isgd"
                     )


def tinyurl(url: str, create: bool = True) -> tuple:
    try:
        if create:
            return (False, shortcut_object.tinyurl.short(url))
        return (False, shortcut_object.tinyurl.expand(url))
    except ShorteningErrorException as e:
        return e.args
    except Exception as e:
        print("exception")
        return e.args


def chilpit(url: str, create: bool = True) -> tuple:
    try:
        if create:
            return (False, shortcut_object.chilpit.short(url))
        return (False, shortcut_object.chilpit.expand(url))
    except ShorteningErrorException as e:
        return e.args
    except Exception as e:
        print("exception")
        return e.args


def clckru(url: str, create: bool = True) -> tuple:
    try:
        if create:
            return (False, shortcut_object.clckru.short(url))
        return (False, 'error clckru cannot be expanded with alesha')
    except ShorteningErrorException as e:
        return e.args
    except Exception as e:
        print("exception")
        return e.args


def dagd(url: str, create: bool = True) -> tuple:
    try:
        if create:
            return (False, shortcut_object.dagd.short(url))
        return (False, 'error dagd cannot be expanded with alesha')
    except ShorteningErrorException as e:
        return e.args
    except Exception as e:
        print("exception")
        return e.args


def isgd(url: str, create: bool = True, code: str | None = None) -> str:  # TODO: ADD support for code
    try:
        if create:
            return (False, shortcut_object.isgd.short(url))
        return (False, 'error isgd cannot be expanded with alesha')
    except ShorteningErrorException as e:
        return e.args
    except Exception as e:
        print("exception")
        return e.args
