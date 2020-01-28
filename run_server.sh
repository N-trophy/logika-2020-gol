#!/bin/bash

source djangoenv/bin/activate
./manage.py runserver --settings=gol.settings.development
