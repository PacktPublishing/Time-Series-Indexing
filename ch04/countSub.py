#!/usr/bin/env python3

from isax import variables
from isax import isax
from isax import tools
from isax import sax

import sys
import pandas as pd
import numpy as np

import time
import argparse

def main():
    parser = argparse.ArgumentParser()
    # -s #n -c #n -s #n
    parser.add_argument("-s", "--segments", dest = "segments", default = "16", help="Number of Segments", type=int)
    parser.add_argument("-c", "--cardinality", dest = "cardinality", default = "16", help="Cardinality", type=int)
    parser.add_argument("-w", "--windows", dest = "window", default = "16", help="Sliding Window Size", type=int)
    parser.add_argument("-t", "--threshold", dest = "threshold", default = "1000", help="Threshold for split", type=int)
    parser.add_argument("-p", "--promotion", action='store_true', help="Define Promotion Strategy")
    parser.add_argument("TSfile")

    args = parser.parse_args()

    variables.segments = args.segments
    variables.maximumCardinality = args.cardinality
    variables.slidingWindowSize = args.window
    variables.threshold = args.threshold
    variables.defaultPromotion = args.promotion
    file = args.TSfile

    maxCardinality = variables.maximumCardinality
    segments = variables.segments
    windowSize = variables.slidingWindowSize

    if tools.power_of_two(maxCardinality) == -1:
        print("Not a power of 2:", maxCardinality)
        sys.exit()

    if variables.segments > variables.slidingWindowSize:
        print("Segments:", variables.segments, "Sliding window:", variables.slidingWindowSize)
        print("Sliding window size should be bigger than # of segments.")
        sys.exit()

    print("Max Cardinality:", maxCardinality, "Segments:", variables.segments,
        "Sliding Window:", variables.slidingWindowSize,
        "Threshold:", variables.threshold,
        "Default Promotion:", variables.defaultPromotion)

    ts = pd.read_csv(file, names=['values'], compression='gzip')
    ts_numpy = ts.to_numpy()
    length = len(ts_numpy)

    #
    # Initialize iSAX index
    #
    ISAX = isax.iSAX()

    # Split sequence into subsequences
    for i in range(length - windowSize + 1):
        # Get the subsequence
        ts = ts_numpy[i:i+windowSize]
        # Create new TS node based on ts
        ts_node = isax.TS(ts, segments)
        ISAX.insert(ts_node)

    # Visit all entries in Dictionary
    # Count TS in Terminal Nodes
    sum = 0
    for k in ISAX.ht:
        t = ISAX.ht[k]
        if t.terminalNode:
            sum += t.nTimeSeries()

    print(length - windowSize + 1, sum)

if __name__ == '__main__':
	main()
