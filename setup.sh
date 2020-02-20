#!/bin/bash

# Remove old files
./clean.sh

# Create Virtual Environment
python3 -m venv venv

# Activate the environment
. venv/bin/activate

# Upgrade pip to latest
pip install --upgrade pip

# Install Flask and other dependancies within virtual environment
pip install wheel Flask numpy sklearn python-dotenv watchdog simplejson blinker gunicorn

# Install entropy package
git clone https://github.com/raphaelvallat/entropy.git entropy/
cd entropy/
pip install -r requirements.txt
python setup.py develop
cd ..

# Deactivate virtual environment
deactivate


