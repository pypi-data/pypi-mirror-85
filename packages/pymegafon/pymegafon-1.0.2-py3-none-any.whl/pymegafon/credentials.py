#!/usr/bin/env python3
"""
    Validates and/or retrieves credentials
"""

import os

def get_from_env():
    """
        Looks up for credentials in the environment
    """

    login = os.environ.get("MEGAFON_LOGIN", None)
    password = os.environ.get("MEGAFON_PASSWORD", None)

    if not login or not password:
        raise Exception("Couldn't find credentials in MEGAFON_LOGIN and MEGAFON_PASSWORD variables.")

    return {"login": login, "password": password}

def uniform_login(login):
    """
        Returns login in the proper format
    """

    only_digits = ''.join(filter(str.isdigit, login))

    if len(only_digits) != 11:
        raise Exception("Login should contain 11 digits.")

    formatted = '+{} {}{}{} {}{}{} {}{}{}{}'.format(*only_digits)

    return formatted

