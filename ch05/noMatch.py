#!/usr/bin/env python3

from isax import variables
from isax import isax
from isax import tools
from isax.sax import normalize

import sys
import pandas as pd
import argparse

def buildISAX(file, windowSize):
    variables.overflow = 0

    # Read Sequence as Pandas
    ts = pd.read_csv(file, names=['values'], compression='gzip', header = None)

    # Convert to NParray
    ts_numpy = ts.to_numpy()
    length = len(ts_numpy)

    # Initialize iSAX index
    ISAX = isax.iSAX()
    ISAX.length = length

    # Split sequence into subsequences
    for i in range(length - windowSize + 1):
        # Get the subsequence
        ts = ts_numpy[i:i+windowSize]
        # Create new TS node based on ts
        ts_node = isax.TS(normalize(ts), variables.segments)
        ISAX.insert(ts_node)

    if variables.overflow != 0:
        print("Number of overflows:", variables.overflow)

    return ISAX

def main():
    parser = argparse.ArgumentParser()
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

	# Visit all entries in Dictionary
    sum = 0
    for k in i1.ht:
        t = i1.ht[k]
        if t.terminalNode:
            saxWord = t.word
            # Look for a match in the other iSAX
            if saxWord in i2.ht.keys():
                i2Node = i2.ht[saxWord]
                # But we still need that to be a terminal node
                if i2Node.terminalNode == False:
                    sum = sum + 1
                    print(saxWord, end=' ')

    print()
	# Look at the other iSAX
    for k in i2.ht:
        t = i2.ht[k]
        if t.terminalNode:
            saxWord = t.word
            # Look for a match in the other iSAX
            if saxWord in i1.ht.keys():
                i1Node = i1.ht[saxWord]
                # But we still need that to be a terminal node
                if i1Node.terminalNode == False:
                    sum = sum + 1
                    print(saxWord, end=' ')

    print()
    print("Total number of iSAX nodes without a match:", sum)

if __name__ == '__main__':
        main()
