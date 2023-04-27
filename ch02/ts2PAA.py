#!/usr/bin/env python3

import sys
import numpy as np
import pandas as pd

from sax import sax

def main():
    if len(sys.argv) != 5:
        print("TS1 sliding_window cardinality segments")
        print("For the sliding window, we prefer values which are a power of 2.")
        print("The cardinality value SHOULD be a power of 2.")
        sys.exit()

    file = sys.argv[1]
    # We prefer values which are powers of 2
    sliding = int(sys.argv[2])
    cardinality = int(sys.argv[3])
    segments = int(sys.argv[4])

    if sliding % segments != 0:
        print("sliding MODULO segments != 0...")
        sys.exit()

    if sliding <= 0:
        print("Sliding value is not allowed:", sliding)
        sys.exit()

    if cardinality <= 0:
        print("Cardinality Value is not allowed:", cardinality)
        sys.exit()

    # Read Sequence as Pandas
    ts = pd.read_csv(file, names=['values'], compression='gzip')

    # Convert to NParray
    ts_numpy = ts.to_numpy()
    length = len(ts_numpy)

    PAA_representations = []
    # Split sequence into subsequences
    for i in range(length - sliding + 1):
        t1_temp = ts_numpy[i:i+sliding]
        # Generate SAX for each subsequence
        tempSAXword = sax.createPAA(t1_temp, cardinality, segments)
        SAXword = tempSAXword.split("_")[:-1]
        print(SAXword, end = ' ')
        PAA_representations.append(SAXword)

        print("[", end = ' ')
        for i in t1_temp.tolist():
            for k in i:
                print("%.2f" % k, end = ' ')
        print("]", end = ' ')

        print("[", end = ' ')
        for i in sax.normalize(t1_temp).tolist():
            for k in i:
                print("%.2f" % k, end = ' ')
        print("]")


if __name__ == '__main__':
	main()
