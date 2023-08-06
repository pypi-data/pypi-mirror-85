"""
Functions accessing the Firebase Real-time Database.
"""
from typing import Union

from firebase_admin import db


def read_site_key_name(site_key: str):
    """Return the value of name from the RTDB site key node."""
    return db.reference(f"{site_key}/name").get()


def read_site_key_timezone(site_key: str):
    """Return the value of timezone from the RTDB site key node."""
    return db.reference(f"{site_key}/timezone").get()


def read_all_site_key_locations(site_key: str) -> Union[dict, None]:
    """Return a dictionary of all site key locations"""
    # noinspection PyTypeChecker
    return db.reference(f"{site_key}/locations").get()


def read_all_site_key_users(site_key: str) -> Union[dict, None]:
    """Return a dictionary of all site key users"""
    # noinspection PyTypeChecker
    return db.reference(f"{site_key}/users").get()
