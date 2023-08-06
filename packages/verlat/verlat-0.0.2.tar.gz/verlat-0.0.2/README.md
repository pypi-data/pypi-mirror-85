# verlat

Get to know the latest version of a python package on PyPI.

Use code written by other people and save your time.

Be Dry! You don't need to reinvent the wheel.

## Installation

```shell
pip install verlat
```

## Usage

```python
from verlat import latest
proj = latest('project_name')
print(f'Version is {proj["version"]}')
print(f'Link {proj["release_url"]}')
```

## Docs for the `latest` function

Fetches all information about the latest version of a package on PyPI

```text
        **Args:**
            project_name (str): the name of package whose info you want
        **Returns:**
            dict: a dictionary containing all the important keys like
            - author
            - author_email
            - description
            - home_page
            - keywords
            - summary
            - version
            - release_url
```

Yeah! Its that simple!
