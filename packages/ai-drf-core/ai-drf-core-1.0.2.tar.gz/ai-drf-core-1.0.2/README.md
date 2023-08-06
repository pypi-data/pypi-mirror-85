# Overview:
This package contains various useful helper functions for the django REST framework.

**ATTENTION: This package is deprecated. All functionality will live on in the [ai-django-core](https://pypi.org/project/ai-django-core/) package.
Please install it with the drf-extension enabled. More details in the changelog.**

# Installation:
- Add a requirement to your requirements.txt:

    `ai-drf-core`

- Add module to `INSTALLED_APPS`:

    `ai-drf`

- Run migrations

# Contribute

- Clone the project locally
- Create a new branch for your feature
- Change the dependency in your requirements.txt to a local (editable) one that points to your local file system:
    ```
    -e /Users/myuser/workspace/ai-drf-core
    ```
- Ensure the code passes the tests
- Run:

    `python setup.py develop`

- Create a pull request

# Publish to PyPI

- Run:

    `python setup.py sdist upload`

If you run into trouble, please create a file in your home directory: ~/.pypirc

```
[distutils]
index-servers =
    pypi

[pypi]
repository: https://upload.pypi.org/legacy/
username:
password:
```


# Tests

- Check coverage

    `pytest --cov=ai-drf-core`

- Run tests

    `pytest`
