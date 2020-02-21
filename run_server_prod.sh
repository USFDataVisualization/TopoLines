#!/bin/bash

. venv/bin/activate

export HERA_BOTTLENECK="/tda/hera/bottleneck_dist"
export HERA_WASSERSTEIN="/tda/hera/wasserstein_dist"

HN=`hostname`

gunicorn -b 0.0.0.0:5050 flask_main:app > run_server_prod_$HN.log 2>&1
