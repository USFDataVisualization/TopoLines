import json

from flask import Flask
from flask import request
from flask import send_file
from flask import send_from_directory

import common

app = Flask(__name__)

datasets = common.get_datasets()

for _ds in datasets:
    for _df in datasets[_ds]:
        common.generate_metric_data(_ds, _df)


@app.route('/')
def render_index():
    return send_file('pages/main.html')


@app.route('/public/<path:path>')
def send_static(path):
    return send_from_directory('pages/public', path)


@app.errorhandler(404)
def page_not_found(error_msg):
    print("Error: " + str(error_msg))
    return 'This page does not exist', 404


@app.route('/datasets', methods=['GET', 'POST'])
def get_datasets():
    return json.dumps(datasets)


@app.route('/metric', methods=['GET', 'POST'])
def get_metric_data():
    ds = request.args.get("dataset")
    df = request.args.get("datafile")

    if not common.valid_dataset(datasets, ds, df):
        print("unknown dataset: " + ds + " or data file: " + df)
        return "{}"

    metric_data = common.generate_metric_data(ds, df)
    metric_reg = [common.metric_regression(metric_data, 'approx entropy', 'L1 norm'),
                  common.metric_regression(metric_data, 'approx entropy', 'L_inf norm'),
                  common.metric_regression(metric_data, 'approx entropy', 'peak wasserstein'),
                  common.metric_regression(metric_data, 'approx entropy', 'peak bottleneck')]

    return json.dumps({'metric': metric_data, 'rank': metric_reg})


@app.route('/data', methods=['GET', 'POST'])
def get_data():
    ds = request.args.get("dataset")
    df = request.args.get("datafile")

    if not common.valid_dataset(datasets, ds, df):
        print("unknown dataset: " + ds + " or data file: " + df)
        return "{}"

    input_signal = common.load_dataset(ds, df)
    res = common.process_smoothing(input_signal, request.args.get("filter"), float(request.args.get("level")))

    return json.dumps(res)
