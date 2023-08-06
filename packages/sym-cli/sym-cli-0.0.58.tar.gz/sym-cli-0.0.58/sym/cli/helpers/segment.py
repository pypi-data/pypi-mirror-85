from getpass import getuser
from os import uname
from uuid import uuid4

import analytics

from ..version import __version__
from .config import Config


def _context():
    u = uname()
    return {
        "app": {"name": "sym-cli", "version": __version__},
        "os": {"name": u.sysname, "version": u.release},
    }


def _user_id():
    return f"{Config.get_org()}:{Config.get_email()}"


def _identity_kwargs():
    try:
        return {"user_id": _user_id(), "context": _context()}
    except KeyError:
        return {"anonymous_id": str(uuid4()), "context": _context()}


def identify():
    traits = {"username": getuser()}

    for attr in ("org", "email"):
        try:
            traits[attr] = Config.instance()[attr]
        except KeyError:
            pass

    kwargs = _identity_kwargs()
    analytics.identify(traits=traits, **kwargs)
    if "user_id" in kwargs:
        analytics.group(group_id=Config.get_org(), **kwargs)


def track(event, **properties):
    analytics.track(event=event, properties=properties, **_identity_kwargs())
