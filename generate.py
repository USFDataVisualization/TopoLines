import argparse
import simplejson as json
import common
import os


def generate_metric_data(_input_signal, _filter_name, _data_dir, _dataset, _datafile, quiet=False):
    out_dir = _data_dir + _dataset + '/' + _datafile + '/'
    if not os.path.exists(out_dir):
        if not quiet:
            print( "Creating: " + out_dir )
        os.mkdir(out_dir)

    out_filename = out_dir + _filter_name + '.json'

    if os.path.exists(out_filename):
        if not quiet:
            print("File already exists: " + out_filename)
        return out_filename
    else:
        results = []
        # warm up
        common.process_smoothing(_input_signal, _filter_name, 0 )
        for i in range(100):
            res = common.process_smoothing(_input_signal, _filter_name, float(i + 1) / 100)
            res.pop('original')
            res.pop('filtered')
            results.append(res)

        if not quiet:
            print("Saving: " + out_filename)
        with open(out_filename, 'w') as outfile:
            json.dump(results, outfile, indent=4, separators=(',', ': '))
        return out_filename


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Time-varying Graph Subdivder.')
    parser.add_argument('-ds', '--dataset', metavar='[SET]', nargs=1, required=True, help='dataset name')
    parser.add_argument('-df', '--datafile', metavar='[FILE]', nargs=1, required=True, help='data file name')

    args = parser.parse_args()

    ds = args.dataset[0]
    df = args.datafile[0]

    data_dir = "data/"
    datasets = common.get_datasets(data_dir)

    input_signal = common.load_dataset(data_dir, datasets, ds, df)

    if input_signal is not None:
        for filter_name in common.filter_list:
            generate_metric_data(input_signal, filter_name, data_dir, ds, df)
    else:
        print("unknown dataset: " + ds)

