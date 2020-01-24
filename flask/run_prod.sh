#!/bin/bash

. venv/bin/activate

gunicorn -b 0.0.0.0:6500 main:app > run_prod.log 2>&1  
