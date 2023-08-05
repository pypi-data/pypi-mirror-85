# Django Commons
[![PyPI version](https://badge.fury.io/py/drizm-django-commons.svg)](https://badge.fury.io/py/drizm-django-commons)

This package includes shared code used by
the Drizm organizations development team.  

It is not intended for public usage but you
may still download, redistribute or 
modify it to your liking.

## Installation

Install:  
>pip install drizm-django-commons

Once installed through pip, include
the app in your settings.py like so:  
INSTALLED_APPS += ["drizm_django_commons"]  

In order to use the applications
manage.py commands you must include the
app at the top of the INSTALLED_APPS list.

Import like so:  
import drizm_django_commons

## Documentation

pass

## Changelog

### 0.2.1

- Added HrefModelSerializer which will
serialize primary keys to hyperlinks
- Moved testing.py dependencies to
drizm-commons package utilities
