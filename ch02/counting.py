#!/usr/bin/env python3

import sys
import pandas as pd
from sax import sax

def main():
    if len(sys.argv) != 5:
        print("TS1 sliding_window cardinality segments")
        print("Suggestion: The window be a power of 2.")
        print("The cardinality SHOULD be a power of 2.")
        sys.exit()

    file = sys.argv[1]
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

    ts = pd.read_csv(file, names=['values'], compression='gzip')
    ts_numpy = ts.to_numpy()
    length = len(ts_numpy)

    KEYS = {}
    for i in range(length - sliding + 1):
        t1_temp = ts_numpy[i:i+sliding]
        # Generate SAX for each subsequence
        tempSAXword = sax.createPAA(t1_temp, cardinality, segments)
        tempSAXword = tempSAXword[:-1]

        if KEYS.get(tempSAXword) == None:
            KEYS[tempSAXword] = 1
        else:
            KEYS[tempSAXword] = KEYS[tempSAXword] + 1

    for k in KEYS.keys():
        print(k, ":", KEYS[k])


if __name__ == '__main__':
	main()
