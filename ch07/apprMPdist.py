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
import numpy as np

def createISAX(file, w, s):
    # Read Sequence as Pandas
    ts = pd.read_csv(file, names=['values'], compression='gzip').astype(np.float64)

    # Convert to NParray
    ts_numpy = ts.to_numpy()
    length = len(ts_numpy)

    ISAX = isax.iSAX()
    ISAX.length = length

    # Split sequence into subsequences
    for i in range(length - w + 1):
        # Get the subsequence
        ts = ts_numpy[i:i+w]
        # Create new TS node based on ts
        ts_node = isax.TS(ts, s)
        ISAX.insert(ts_node)

    return ISAX, ts_numpy

def NN(ISAX, q):
    ED = None
    segments = variables.segments
    threshold = variables.threshold

    # Create TS Node
    qTS = isax.TS(q, segments)

    segs = [1] * segments
    # If the relevant child of root is not there, we have a miss
    lower_cardinality = tools.lowerCardinality(segs, qTS)

    lower_cardinality_str = ""
    for i in lower_cardinality:
        lower_cardinality_str = lower_cardinality_str + "_" + i

    # Remove _ at the beginning
    lower_cardinality_str = lower_cardinality_str[1:len(lower_cardinality_str)]
    if ISAX.ht.get(lower_cardinality_str) == None:
        return None

    # Otherwise, we have a hit
    n = ISAX.ht.get(lower_cardinality_str)
    while n.terminalNode == False:
        left = n.left
        right = n.right

        leftSegs = left.word.split('_')
        # Promote
        tempCard = tools.promote(qTS, leftSegs)

        if tempCard == left.word:
            n = left
        elif tempCard == right.word:
            n = right

    # Iterate over the subsequences of the terminal node
    for i in range(0, threshold):
        child = n.children[i]
        if type(child) == isax.TS:
            distance = tools.euclidean(normalize(child.ts), normalize(qTS.ts))
            if ED == None:
                ED = distance
            if ED > distance:
                ED = distance
        else:
            break

    return ED

def main():
    parser = argparse.ArgumentParser()
    # -s #n -c #n -s #n -t #n -p
    parser.add_argument("-s", "--segments", dest = "segments", default = "16", help="Number of Segments", type=int)
    parser.add_argument("-c", "--cardinality", dest = "cardinality", default = "32", help="Cardinality", type=int)
    parser.add_argument("-w", "--window", dest = "window", default = "16", help="Sliding Window Size", type=int)
    parser.add_argument("-t", "--threshold", dest = "threshold", default = "100", help="Threshold for split", type=int)
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

    ED = []

    # Build iSAX for TS1
    i1, ts1 = createISAX(f1, windowSize, variables.segments)
    # Build iSAX for TS2
    i2, ts2 = createISAX(f2, windowSize, variables.segments)

    start_time = time.time()
    # We search iSAX2 for the NN of the
    # subsequences from TS1
    for idx in range(0, len(ts1)-windowSize+1):
        currentQuery = ts1[idx:idx+windowSize]
        t = NN(i2, currentQuery)
        if t != None:
            ED.append(t)

    # We search iSAX1 for the NN of the
    # subsequences from TS2
    for idx in range(0, len(ts2)-windowSize+1):
        currentQuery = ts2[idx:idx+windowSize]
        t = NN(i1, currentQuery)
        if t != None:
            ED.append(t)

    print("MPdist: %.2f seconds" % (time.time() - start_time))

    ED.sort()
    idx = int(0.05 * ( len(ED) + 2 * windowSize)) + 1
    print("Approximate MPdist:", round(ED[idx], 3))


if __name__ == '__main__':
        main()
