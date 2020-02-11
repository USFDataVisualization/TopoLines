import json
import lcsmooth.filter1d as filter1d
import lcsmooth.measures as measures
import os
import os, fnmatch

from flask import Flask
from flask import request
from flask import render_template
from flask import send_from_directory
from flask import send_file

from operator import itemgetter, attrgetter

import common
import generate

app = Flask(__name__)

data_dir = "data/"
datasets = common.get_datasets(data_dir)


def error(err):
    print(err)


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
    filter_name = request.args.get("filter")

    input_signal = common.load_dataset(data_dir, datasets, ds, df )

    if input_signal is None:
        print("unknown dataset: " + ds + " or data file: " + df )
        return "{}";

    if filter_name == 'all':
        ret = []
        for f_name in common.filter_list:
            f = generate.generate_metric_data(input_signal, f_name, data_dir, ds, df)
            with open(f) as json_file:
                ret += json.load(json_file)
        return json.dumps(ret)
    else:
        return send_file(generate.generate_metric_data(input_signal, filter_name, data_dir, ds, df))


@app.route('/data', methods=['GET', 'POST'])
def get_data():
    ds = request.args.get("dataset")
    df = request.args.get("datafile")

    input_signal = common.load_dataset(data_dir, datasets, ds, df )

    if input_signal is None:
        print("unknown dataset: " + ds + " or data file: " + df )
        return "{}";

    res = common.process_smoothing(input_signal,request.args.get("filter"), float(request.args.get("level")) )

    return json.dumps(res)
