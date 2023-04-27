#!/usr/bin/env python3

import argparse
import stumpy
import numpy as np
import pandas as pd
import sys

class TS:
    def __init__(self, ts, index):
        self.ts = ts
        self.index = index

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--window", dest = "window", default = "16", help="Sliding Window Size", type=int)
    parser.add_argument("TS")

    args = parser.parse_args()
    windowSize = args.window
    file = args.TS

    ts = pd.read_csv(file, names=['values'], compression='gzip', header = None)
    ts_numpy = ts.to_numpy()
    length = len(ts_numpy)

    # Split time series into subsequences
    for i in range(length - windowSize + 1):
        # Get the subsequence
        ts = ts_numpy[i:i+windowSize]
        # Create new TS node based on ts
        ts_node = TS(ts, i)


if __name__ == '__main__':
	main()
