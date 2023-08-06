''' verlat.py module offers you the `latest` function, that gives you all information about the latest release of a project on PyPI
'''

import requests
import logging


def latest(project_name: str) -> dict:
    '''Fetches all information about the latest version of a package on PyPI

    Args:
        project_name (str): the name of package whose info you want

    Returns:
        dict: a dictionary containing all the important keys like 

        - author
        - author_email
        - description
        - home_page
        - keywords
        - summary 
        - version
        - release_url

    '''
    if not project_name:
        project_name = input('Enter package name\n>>> ')
    try:
        url = f'https://pypi.org/pypi/{project_name}/json'
        package = requests.get(url).json()
        return package['info']

    except Exception as err:
        logging.debug(err)
        logging.warning(f'Could not fetch details for {project_name}')
