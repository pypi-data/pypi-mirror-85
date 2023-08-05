# Helpers

## Requirements
* Python
* Django
* Django Rest Framework
* DRF spectacular ("https://pypi.org/project/drf-spectacular/")


## Installation

```
$ pip install tonicapp-helpers
```

Add the application to your project's `INSTALLED_APPS` in `settings.py`.

```
INSTALLED_APPS = [
    ...
    'helpers',
]
```


## Source

```
https://pypi.org/project/tonicapp-helpers/
```


## Update Library

```
python3 setup.py sdist
```

```
python3 -m twine upload dist/*
Enter your username: ******
Enter your password: ******
```


# Version updates
From v1.0 to v2.0 the support to drf_spectacular library was removed (the file schema_parameters was removed).
