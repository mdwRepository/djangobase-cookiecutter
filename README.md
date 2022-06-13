# Djangobase Cookiecutter

![mdwRepository](mdwRepository.svg)
![Framework](django.svg)
![Project](djangobase-cookiecutter.svg)

Cookiecutter template for jumpstarting for Django projects based on https://github.com/acdh-oeaw/djangobase-cookiecutter

## Features

-   For Django 3.2
-   Works with Python 3.9

# DSE-Static-Cookiecutter

[Cookiecutter](https://github.com/cookiecutter/cookiecutter) template djangobaseproject-based django-project

## what is this for

The current repo should ease the process of setting up a djangobaseproject-based django-project

## Quickstart

* Install the latest Cookiecutter if you haven't installed it yet (this requires Cookiecutter 1.7.0 or higher) by running `pip install -U cookiecutter`
* To generate a new djangobaseproject-based django-project project run `cookiecutter https://github.com/mdwRepository/djangobase-cookiecutter` and answer the following questions, see below:

```json
{
    "directory_name": "my-new-project",
    "project_title": "My New Project",
    "project_abbr": "mnp"
} 
```

* change into the new created repo, by default `$ my-new-project`
* create a virtual env
* install requirements `pip install -r requirements.txt`
* *optional* add/modify environment-variables in `env.default`, rename it into e.g. `env.secret`
* *optional* change `set_env_varibales.sh` so it uses your actual env-file

* run `python manage.py migrate`
* start developing