import os
import sys

rel_error = 0.01

hera_bottleneck = os.getenv('HERA_BOTTLENECK')
hera_wasserstein = os.getenv('HERA_WASSERSTEIN')

print("Hera Bottleneck:  " + hera_bottleneck)
print("Hera Wasserstein: " + hera_wasserstein)

if (not os.path.exists(hera_bottleneck)) or (not os.path.exists(hera_wasserstein)):
    print("Path to Hera Bottleneck and Wasserstein not set correctly.")
    print("   For example: ")
    print("       > export HERA_BOTTLENECK=\"/Users/prosen/tda/hera/bottleneck_dist\"")
    print("       > export HERA_WASSERSTEIN=\"/Users/prosen/tda/hera/wasserstein_dist\"")
    sys.exit()


def save_persistence_diagram(outfile, pd0, pd1=None):
    f = open(outfile, "w")

    for x in pd0:
        f.write(str(x[0]) + " " + str(x[1]) + "\n")

    if pd1 is not None:
        for x in pd1:
            f.write(str(x[0]) + " " + str(x[1]) + "\n")

    f.close()


def wasserstein_distance(pd_file0, pd_file1):
    stream = os.popen(hera_wasserstein + " " + pd_file0 + " " + pd_file1 + " " + str(rel_error))
    output = stream.read()
    stream.close()
    return float(output)


def bottleneck_distance(pd_file0, pd_file1):
    stream = os.popen(hera_bottleneck + " " + pi + " " + pj + " " + str(rel_error))
    output = stream.read()
    stream.close()
    return float(output)
