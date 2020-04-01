#!/bin/bash

. venv/bin/activate

export HERA_BOTTLENECK="/tda/hera/bottleneck_dist"
export HERA_WASSERSTEIN="/tda/hera/wasserstein_dist"

python experiments.py

deactivate
