#!/usr/bin/env python3.10

from isax import variables
from isax import isax
from isax import tools
from isax.sax import normalize
from isax.iSAXjoin import Join

import sys
import pandas as pd
import time
import argparse

def buildISAX(file, windowSize):
    variables.overflow = 0

    # Read Sequence as Pandas
    ts = pd.read_csv(file, names=['values'], compression='gzip', header = None)

    ts_numpy = ts.to_numpy()
    length = len(ts_numpy)

    ISAX = isax.iSAX()
    ISAX.length = length

    for i in range(length - windowSize + 1):
        ts = ts_numpy[i:i+windowSize]
        # Create new TS node based on ts
        # Store the normalized version of the subsequence
        ts_node = isax.TS(normalize(ts), variables.segments)
        ISAX.insert(ts_node)

    if variables.overflow != 0:
        print("Number of overflows:", variables.overflow)

    return ISAX

def main():
    parser = argparse.ArgumentParser()
    # -s #n -c #n -s #n -t #n -p
    parser.add_argument("-s", "--segments", dest = "segments", default = "16", help="Number of Segments", type=int)
    parser.add_argument("-c", "--cardinality", dest = "cardinality", default = "256", help="Cardinality", type=int)
    parser.add_argument("-w", "--window", dest = "window", default = "16", help="Sliding Window Size", type=int)
    parser.add_argument("-t", "--threshold", dest = "threshold", default = "50", help="Threshold for split", type=int)
    parser.add_argument("-p", "--promotion", action='store_true', help="Define Promotion Strategy")
    parser.add_argument("TS1")
    parser.add_argument("TS2")

    args = parser.parse_args()

    variables.segments = args.segments
    variables.maximumCardinality = args.cardinality
    variables.slidingWindowSize = args.window
    variables.threshold = args.threshold
    variables.defaultPromotion = args.promotion

    windowSize = variables.slidingWindowSize
    maxCardinality = variables.maximumCardinality
    f1 = args.TS1
    f2 = args.TS2

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

    # Build iSAX for TS1
    i1 = buildISAX(f1, windowSize)

    # Build iSAX for TS2
    i2 = buildISAX(f2, windowSize)

    start_time = time.time()
    # Join the two iSAX indexes
    Join(i1, i2)
    variables.ED.sort()
    print("MPdist: %.2f seconds" % (time.time() - start_time))

    print("variables.ED length:", len(variables.ED))

    # Index
    idx = int(0.05 * ( len(variables.ED) + 2 * windowSize)) + 1
    print("Approximate MPdist:", variables.ED[idx])


if __name__ == '__main__':
        main()
