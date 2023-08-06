#!/usr/bin/env python3
"""
    Interacts with MegaFon
"""

import logging

from . import balance
from . import credentials

def main(login=None, password=None, do_check_balance=False, do_check_remainings=False, debug=False):

    if debug:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO
    
    logging.basicConfig(level=loglevel)
    logging.debug("Validating credentials..")

    if not login or not password:
        env_credentials = credentials.get_from_env()
        login = env_credentials['login']
        password = env_credentials['password']

    logging.debug("Uniforming login")
    uniformed_login = credentials.uniform_login(login)
    logging.debug("Login: '%s' -> '%s'" % (login, uniformed_login) )

    connection = balance.APIConnection(login=uniformed_login, password=password)

    if do_check_balance:
        logging.debug("Check balance command invoked")
        connection.sign_in()
        connection.get_balance()

    elif do_check_remainings:
        logging.debug("Check internet subscription remainings command invoked")
        connection.sign_in()
        connection.get_internet_remainings()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.error("Not implemented.")
