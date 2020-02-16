import argparse
import fnmatch

import simplejson as json
import os
import csv

def load_dataset(datasets, ds, df):
    if ds == 'climate' and df in datasets[ds]:
        filename = ds + "/" + df + ".json"

        with open(filename) as json_file:
            cur_dataset = json.load(json_file)
            cur_dataset['data'].sort(reverse=False, key=itemgetter('timestamp'))
            return list(map(lambda X: float(X['value']), cur_dataset['data']))

    elif (ds == 'stock' or ds == 'temperature' or ds == 'radioAstronomy' or ds == 'statistical') and df in datasets[ds]:
        filename = ds + "/" + df + ".json"

        with open(filename) as json_file:
            cur_dataset = json.load(json_file)
            return list(map(lambda X: float(X['value']), cur_dataset['results']))

    elif ds == 'eeg' and df in datasets[ds]:
        filename = ds + "/" + df + ".csv"
        with open(filename) as csv_file:
            data = [next(csv_file) for x in range(2500)]
            return list(map(lambda X: float(X), data))

    elif ds == 'stock2' and df in datasets[ds]:
        filename = ds + "/" + df + ".csv"
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            return list(map(lambda X: float(X['Close']), reader))

    return None


def get_datasets( ):
    ret = {}
    for dataset in os.listdir("."):
        if os.path.isdir(dataset):
            cur_ds = []
            for data_file in os.listdir(dataset):
                if fnmatch.fnmatch(data_file, "*.json"):
                    cur_ds.append(data_file[:-5])
                if fnmatch.fnmatch(data_file, "*.csv"):
                    cur_ds.append(data_file[:-4])
            ret[dataset] = cur_ds
    return ret


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Time-varying Graph Subdivder.')
    parser.add_argument('-ds', '--dataset', metavar='[SET]', nargs=1, required=True, help='dataset name')
    parser.add_argument('-df', '--datafile', metavar='[FILE]', nargs=1, required=True, help='data file name')

    args = parser.parse_args()

    ds = args.dataset[0]
    df = args.datafile[0]

    datasets = get_datasets()

    input_signal = load_dataset(datasets, ds, df)

    if input_signal is not None:
        print(json.dumps(input_signal))
    else:
        print("unknown dataset: " + ds)
