import json

from flask import Flask
from flask import request
from flask import send_file
from flask import send_from_directory

import experiments
import webbrowser
import os

app = Flask(__name__)

datasets = experiments.get_datasets()
with open("docs/json/datasets.json", 'w') as outfile:
    json.dump(datasets, outfile)

for _ds in datasets:
    for _df in datasets[_ds]:
        metric_data = experiments.generate_metric_data(_ds, _df)
        metric_reg = [experiments.metric_regression(metric_data, 'approx entropy', 'L1 norm'),
                      experiments.metric_regression(metric_data, 'approx entropy', 'L_inf norm'),
                      experiments.metric_regression(metric_data, 'approx entropy', 'peak wasserstein'),
                      experiments.metric_regression(metric_data, 'approx entropy', 'peak bottleneck')]
        with open("docs/json/metric/" + _ds + '_' + _df + ".json", 'w') as outfile:
            json.dump({'metric': metric_data, 'rank': metric_reg}, outfile)

with open("docs/json/all_ranks.json", 'w') as outfile:
    json.dump( experiments.metric_ranks(datasets), outfile )


webbrowser.open_new_tab("http://localhost:5050")


@app.route('/')
@app.route('/index.html')
def render_index():
    return send_file('pages/index.html')


@app.route('/figures.html')
def render_figures():
    return send_file('pages/figures.html')


@app.route('/ranks.html')
def render_ranks():
    return send_file('pages/ranks.html')


@app.route('/performance.html')
def render_performance():
    return send_file('pages/performance.html')


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

    if not experiments.valid_dataset(datasets, ds, df):
        print("unknown dataset: " + ds + " or data file: " + df)
        return "{}"

    metric_data = experiments.generate_metric_data(ds, df)
    metric_reg = [experiments.metric_regression(metric_data, 'approx entropy', 'L1 norm'),
                  experiments.metric_regression(metric_data, 'approx entropy', 'L_inf norm'),
                  experiments.metric_regression(metric_data, 'approx entropy', 'peak wasserstein'),
                  experiments.metric_regression(metric_data, 'approx entropy', 'peak bottleneck')]

    return json.dumps({'metric': metric_data, 'rank': metric_reg})


@app.route('/all_ranks', methods=['GET', 'POST'])
def get_all_rank_data():
    return json.dumps( experiments.metric_ranks(datasets) )


@app.route('/data', methods=['GET', 'POST'])
def get_data():
    ds = request.args.get("dataset")
    df = request.args.get("datafile")

    if not experiments.valid_dataset(datasets, ds, df):
        print("unknown dataset: " + ds + " or data file: " + df)
        return "{}"

    input_signal = experiments.load_dataset(ds, df)
    res = experiments.process_smoothing(input_signal, request.args.get("filter"), float(request.args.get("level")))

    return json.dumps(res)
