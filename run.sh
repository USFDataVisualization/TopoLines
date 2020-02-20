#!/bin/bash

. venv/bin/activate

export HERA_BOTTLENECK="/Users/prosen/tda/hera/bottleneck_dist"
export HERA_WASSERSTEIN="/Users/prosen/tda/hera/wasserstein_dist"

export FLASK_APP=flask_main.py

flask run --host 0.0.0.0 --port 5050

#gunicorn -b 0.0.0.0:5050 flask_main:app > run_server_prod.log 2>&1


deactivate
