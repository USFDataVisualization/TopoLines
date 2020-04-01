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
pip install numpy sklearn python-dotenv watchdog simplejson

# Install entropy package
git clone https://github.com/raphaelvallat/entropy.git entropy/
cd entropy/
pip install -r requirements.txt
python setup.py develop
cd ..

# Deactivate virtual environment
deactivate

# Clone hera
git clone https://bitbucket.org/grey_narn/hera.git

# Patching for macport error
patch hera/bottleneck/CMakeLists.txt hera_macport.patch

# Build Hera Bottleneck
mkdir hera/bottleneck/bin
cd hera/bottleneck/bin
cmake ..
make
cd ../../../

# Build Hera Wasserstein
mkdir hera/wasserstein/bin
cd hera/wasserstein/bin
cmake ..
make
cd ../../../



