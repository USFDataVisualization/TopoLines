import os

__hera_bottleneck = os.getenv('HERA_BOTTLENECK')
__hera_wasserstein = os.getenv('HERA_WASSERSTEIN')

if __hera_bottleneck is None or __hera_wasserstein is None or \
        (not os.path.exists(__hera_bottleneck)) or (not os.path.exists(__hera_wasserstein)):
    print("Path to Hera Bottleneck and Wasserstein not set correctly.")
    print("   For example: ")
    print("       > export HERA_BOTTLENECK=\"/bin/tda/hera/bottleneck_dist\"")
    print("       > export HERA_WASSERSTEIN=\"/bin/tda/hera/wasserstein_dist\"")
    print()
    print("These functionalities will be disabled.")
    __hera_bottleneck = None
    __hera_wasserstein = None


def save_persistence_diagram(outfile, pd0, pd1=None):
    f = open(outfile, "w")

    for x in pd0:
        f.write(str(x[0]) + " " + str(x[1]) + "\n")

    if pd1 is not None:
        for x in pd1:
            f.write(str(x[0]) + " " + str(x[1]) + "\n")

    f.close()


def wasserstein_distance(pd_file0, pd_file1, rel_error=0.01):
    if __hera_wasserstein is None:
        return 'nan'

    stream = os.popen(__hera_wasserstein + " " + pd_file0 + " " + pd_file1 + " " + str(rel_error))
    output = stream.read()
    stream.close()
    return float(output)


def bottleneck_distance(pd_file0, pd_file1, rel_error=0.01):
    if __hera_bottleneck is None:
        return 'nan'

    stream = os.popen(__hera_bottleneck + " " + pd_file0 + " " + pd_file1 + " " + str(rel_error))
    output = stream.read()
    stream.close()
    return float(output)
