''' Get to know the latest version of a python package on PyPI '''

__version__ = "0.0.1"

import requests
import logging


def latest(package_name: str) -> str:
    if not package_name:
        package_name = input('Enter package name\n>>> ')
    try:
        url = f'https://pypi.org/pypi/{package_name}/json'
        package = requests.get(url).json()
        return package['info']['version']

    except Exception as err:
        logging.debug(err)
        print('Error Occured! ( see debug logs for more info )')
