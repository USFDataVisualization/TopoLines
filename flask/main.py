import json
import mod_filter1d as filter
import mod_measures as measures
import os

from flask import Flask
from flask import request
from flask import render_template
from flask import send_from_directory
from flask import send_file

from operator import itemgetter, attrgetter

import statistics as stats

app = Flask(__name__)


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


@app.route('/data', methods=['GET', 'POST'])
def get_data():
    # print( request.args )

    # dir = ""

    # splits = int(request.args.get('splits'))

    # dataset = []

    with open('../data/climate/avgTemp.json') as json_file:
        dataset = json.load(json_file)

    outdata = []
    dataset['data'].sort(reverse=False, key=itemgetter('timestamp'))

    for i, d in enumerate(dataset['data']):
        # outdata.append( { "id": i, "value": d["value"] } )
        outdata.append(d["value"])
        # print( d )

    filter_level = 0
    if not request.args.get("level") is None:
        filter_level = float(request.args.get("level"))

    filter_data = []
    if request.args.get("filter") == 'lowpass':
        filter_data = filter.lowpass(outdata, len(outdata) - int(filter_level) - 1)
    elif request.args.get("filter") == 'gaussian':
        filter_data = filter.gaussian(outdata, filter_level)
    elif request.args.get("filter") == 'median':
        filter_data = filter.median(outdata, int(filter_level))
    elif request.args.get("filter") == 'rdp':
        filter_data = filter.rdp(outdata, filter_level)
    elif request.args.get("filter") == 'mean':
        filter_data = filter.mean(outdata, int(filter_level))
    elif request.args.get("filter") == 'tda':
        filter_data = filter.tda(outdata, filter_level)
    elif request.args.get("filter") == 'subsample':
        filter_data = filter.subsample(outdata, int(filter_level))
    else:
        filter_data = list(enumerate(outdata))

    d = []
    for X in filter_data:
        d.append(X[1])

    metrics = {}
    print( len(d) )
    print( len(outdata) )
    print( filter_data )

    print()
    metrics["mean"] = measures.mean(outdata)
    metrics["Pop Stdev"] = measures.stdev_population(outdata)
    metrics["Sample Stdev"] = measures.stdev_sample(outdata)
    metrics["Pop Variance"] = measures.variance_population(outdata)
    metrics["Sample Variance"] = measures.variance_sample(outdata)
    metrics["SNR"] = measures.snr(outdata)
    metrics["Covariance"] = measures.covariance(outdata,d)
    metrics["PCC"] = measures.pearson_correlation(outdata,d)
    metrics["L1-norm"] = measures.l1_norm(outdata,d)
    metrics["L2-norm"] = measures.l2_norm(outdata,d)
    metrics["Linf-norm"] = measures.linf_norm(outdata,d)
    metrics["DVol"] = measures.delta_volume(outdata,d)
    metrics["Approx Ent"] = measures.approximate_entropy(outdata,4,1)
    print()
    print()

    # if (Float.isFinite(f.L1Norm())) ret.setFloat( "L1Norm", f.L1Norm() );
    # if (Float.isFinite(f.L2Norm())) ret.setFloat( "L2Norm", f.L2Norm() );
    # if (Float.isFinite(f.LInfNorm())) ret.setFloat("LInfNorm", f.LInfNorm() );
    # if (Float.isFinite(f.frequencyPreservation())) ret.setFloat( "frequencyPreservation", f.frequencyPreservation() );
    # if (Float.isFinite(f.deltaVolume())) ret.setFloat( "deltaVolume", f.deltaVolume() );
    # if (Float.isFinite(f.peakinessBottleneck())) ret.setFloat( "peakinessBottleneck", f.peakinessBottleneck() );
    # if (Float.isFinite(f.peakinessWasserstein())) ret.setFloat( "peakinessWasserstein", f.peakinessWasserstein() );
    # if (Float.isFinite(f.phaseShifted(fPhi))) ret.setFloat( "phaseShift", f.phaseShifted(fPhi) );
    # if (Float.isFinite(f.signalToNoise())) ret.setFloat( "SNR", f.signalToNoise() );
    # if (Double.isFinite(Measures.getSNR(f))) ret.setFloat( "SNRAlt", (float)Measures.getSNR(f) );
    # if (Double.isFinite(Measures.approximateEntropy(f, 2, 0.25
    # f)) ) ret.setFloat( "ent0_25", (float)Measures.approximateEntropy(f, 2, 0.25f) );
    # if (Double.isFinite(Measures.approximateEntropy(f, 2, 0.50
    # f)) ) ret.setFloat( "ent0_50", (float)Measures.approximateEntropy(f, 2, 0.50f) );
    # if (Double.isFinite(Measures.approximateEntropy(f, 2, 1.00
    # f)) ) ret.setFloat( "ent1_00", (float)Measures.approximateEntropy(f, 2, 1.00f) );
    # if (Double.isFinite(Measures.approximateEntropy(f, 2, 2.00
    # f)) ) ret.setFloat( "ent2_00", (float)Measures.approximateEntropy(f, 2, 2.00f) );
    # if (Double.isFinite(Measures.approximateEntropy(f, 2, 4.00
    # f)) ) ret.setFloat( "ent4_00", (float)Measures.approximateEntropy(f, 2, 4.00f) );

    return json.dumps({'original': list(enumerate(outdata)), 'filtered': filter_data, 'metrics':metrics})
