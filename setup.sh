#!/bin/bash

# delete old directories
rm -rf __pycahce__
rm -rf venv

# Create Virtual Environment
python3 -m venv venv

# Activate the environment
. venv/bin/activate

pip install --upgrade pip

#Within the activated environment, use the following command to install Flask and dependancies:
pip install wheel Flask numpy sklearn python-dotenv watchdog simplejson blinker gunicorn

deactivate

