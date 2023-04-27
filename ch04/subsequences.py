#!/usr/bin/env python3

import argparse
import numpy as np
import pandas as pd
from isax import sax
from isax import variables

class TS:
    def __init__(self, ts, index):
        self.ts = ts
        self.sax = sax.createPAA(ts, variables.maximumCardinality, variables.segments)
        self.index = index

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--window", dest = "window", default = "16", help="Sliding Window Size", type=int)
    parser.add_argument("-s", "--segments", dest = "segments", default = "4", help="Number of Segments", type=int)
    parser.add_argument("-c", "--cardinality", dest = "cardinality", default = "32", help="Cardinality", type=int)
    parser.add_argument("TS")

    args = parser.parse_args()
    windowSize = args.window
    variables.segments = args.segments
    variables.maximumCardinality = args.cardinality
    file = args.TS

    ts = pd.read_csv(file, names=['values'], compression='gzip', header = None)
    ts_numpy = ts.to_numpy()
    length = len(ts_numpy)

    # Split sequence into subsequences
    n = 0
    for i in range(length - windowSize + 1):
        # Get the actual subsequence
        ts = ts_numpy[i:i+windowSize]
        # Create new TS node based on ts
        ts_node = TS(sax.normalize(ts), i)
        n = n + 1
    
    print("Created", n, "TS() nodes")


if __name__ == '__main__':
	main()

