#!/bin/bash

export PYTHONPATH=/usr/local/bin/python
export DJANGO_SETTINGS_MODULE=reception.settings
python /code/manage.py cron
