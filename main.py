import json
import mod_filter1d as filter
import mod_measures as measures
import os
import os, fnmatch

from flask import Flask
from flask import request
from flask import render_template
from flask import send_from_directory
from flask import send_file

from operator import itemgetter, attrgetter

import statistics as stats

app = Flask(__name__)

data_dir = "../data"
datasets = {}

for dataset in os.listdir(data_dir):
    if os.path.isdir(data_dir + "/" + dataset):
        cur_ds = []
        for data_file in os.listdir(data_dir + "/" + dataset):
            if fnmatch.fnmatch(data_file, "*.json"):
                cur_ds.append(data_file[:-5])
            if fnmatch.fnmatch(data_file, "*.csv"):
                cur_ds.append(data_file[:-4])
        datasets[dataset] = cur_ds


def error(err):
    print(err)


@app.route('/')
def render_index():
    return send_file('pages/main.html')


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


@app.errorhandler(404)
def page_not_found(error):
    print("Error: " + str(error))
    return 'This page does not exist', 404


@app.route('/datasets', methods=['GET', 'POST'])
def get_datasets():
    return json.dumps(datasets)


@app.route('/data', methods=['GET', 'POST'])
def get_data():
    ds = request.args.get("dataset")
    df = request.args.get("datafile")

    input_signal = []

    if ds == 'climate':
        if df in datasets[ds]:
            filename = data_dir + "/" + ds + "/" + df + ".json"

            with open(filename) as json_file:
                cur_dataset = json.load(json_file)
                cur_dataset['data'].sort(reverse=False, key=itemgetter('timestamp'))

                for X in cur_dataset['data']:
                    input_signal.append(X["value"])
    elif ds == 'stock' or ds == 'temperature' or ds == 'radioAstronomy' or ds == 'statistical':
        if df in datasets[ds]:
            filename = data_dir + "/" + ds + "/" + df + ".json"

            with open(filename) as json_file:
                cur_dataset = json.load(json_file)

                for X in cur_dataset['results']:
                    input_signal.append(X["value"])
    elif ds == 'eeg':
        if df in datasets[ds]:
            filename = data_dir + "/" + ds + "/" + df + ".csv"

            with open(filename) as json_file:
                for i in range(0,1000):
                    input_signal.append(float(json_file.readline()))


    else:
        print("unknown dataset: " + request.args.get("dataset"))
        return "{}";

    input_min = min(input_signal)
    input_max = max(input_signal)
    input_range = input_max - input_min

    filter_level = 0
    if not request.args.get("level") is None:
        filter_level = float(request.args.get("level"))

    filter_data = []
    if request.args.get("filter") == 'lowpass':
        level = filter.__linear_map(filter_level, 0, 1, len(input_signal), 2)
        print(level)
        filter_data = filter.lowpass(input_signal, int(level))
    elif request.args.get("filter") == 'subsample':
        level = filter.__linear_map(filter_level, 0, 1, len(input_signal), 2)
        filter_data = filter.subsample(input_signal, int(level))
    elif request.args.get("filter") == 'tda':
        level = filter.__linear_map(filter_level, 0, 1, 0, input_range)
        filter_data = filter.tda(input_signal, level)
    elif request.args.get("filter") == 'rdp':
        level = filter.__linear_map(filter_level, 0, 1, 0, input_range)
        filter_data = filter.rdp(input_signal, level)
    elif request.args.get("filter") == 'gaussian':
        level = filter.__linear_map(filter_level, 0, 1, 0.1, 30)
        filter_data = filter.gaussian(input_signal, level)
    elif request.args.get("filter") == 'median':
        level = filter.__linear_map(filter_level, 0, 1, 1, 30)
        filter_data = filter.median(input_signal, int(level))
    elif request.args.get("filter") == 'mean':
        level = filter.__linear_map(filter_level, 0, 1, 1, 30)
        filter_data = filter.mean(input_signal, int(level))
    else:
        filter_data = list(enumerate(input_signal))

    output_signal = []
    for X in filter_data:
        output_signal.append(X[1])

    stats = {}
    stats["mean"] = measures.mean(output_signal)
    stats["Pop Stdev"] = measures.stdev_population(output_signal)
    stats["Sample Stdev"] = measures.stdev_sample(output_signal)
    stats["Pop Variance"] = measures.variance_population(output_signal)
    stats["Sample Variance"] = measures.variance_sample(output_signal)
    stats["SNR"] = measures.snr(output_signal)

    metrics = {}
    metrics["Covariance"] = measures.covariance(input_signal, output_signal)
    metrics["PCC"] = measures.pearson_correlation(input_signal, output_signal)
    metrics["SRC"] = measures.spearman_correlation(input_signal, output_signal)
    metrics["L1-norm"] = measures.l1_norm(input_signal, output_signal)
    metrics["L2-norm"] = measures.l2_norm(input_signal, output_signal)
    metrics["Linf-norm"] = measures.linf_norm(input_signal, output_signal)
    metrics["DVol"] = measures.delta_volume(input_signal, output_signal)
    metrics["Approx Ent (2,0.25)"] = measures.approximate_entropy(output_signal, 2, 0.25)
    metrics["Approx Ent (2,0.5)"] = measures.approximate_entropy(output_signal, 2, 0.5)
    metrics["Approx Ent (2,1.0)"] = measures.approximate_entropy(output_signal, 2, 1.0)
    metrics["Approx Ent (2,2.0)"] = measures.approximate_entropy(output_signal, 2, 2.0)
    metrics["Approx Ent (2,4.0)"] = measures.approximate_entropy(output_signal, 2, 4.0)
    metrics["Frequency Preservation"] = measures.frequency_preservation(input_signal, output_signal)
    metrics["signal to noise"] = measures.signal_to_noise(input_signal, output_signal)

    # if (Float.isFinite(f.peakinessBottleneck())) ret.setFloat( "peakinessBottleneck", f.peakinessBottleneck() );
    # if (Float.isFinite(f.peakinessWasserstein())) ret.setFloat( "peakinessWasserstein", f.peakinessWasserstein() );
    # if (Float.isFinite(f.phaseShifted(fPhi))) ret.setFloat( "phaseShift", f.phaseShifted(fPhi) );

    return json.dumps(
        {'original': list(enumerate(input_signal)), 'filtered': filter_data, 'statistics': stats, 'metrics': metrics})
