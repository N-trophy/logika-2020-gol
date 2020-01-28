#!/bin/bash

virtualenv -p python3 djangoenv
source djangoenv/bin/activate
pip3 install -r requirements.txt
