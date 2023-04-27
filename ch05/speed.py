#!/usr/bin/env python3

from isax import variables
from isax import isax
from isax import tools

import sys
import pandas as pd
import numpy as np
import argparse

totalQueries = 0

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


# ISAX: An iSAX object
# q: a NumPy array
#
# Return values: Found, Accesses
def query(ISAX, q):
    global totalQueries
    totalQueries = totalQueries + 1
    Accesses = 0

    # Create TS Node
    qTS = isax.TS(q, variables.segments)

    segs = [1] * variables.segments
    # If the relevant child of root is not there, we have a miss
    lower_cardinality = tools.lowerCardinality(segs, qTS)

    lower_cardinality_str = ""
    for i in lower_cardinality:
        lower_cardinality_str = lower_cardinality_str + "_" + i

    # Remove _ at the beginning
    lower_cardinality_str = lower_cardinality_str[1:len(lower_cardinality_str)]
    if ISAX.ht.get(lower_cardinality_str) == None:
        return False, 0

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
    for i in range(0, variables.threshold):
        Accesses = Accesses + 1
        child = n.children[i]
        if type(child) == isax.TS:
            # print("Shapes:", child.ts.shape, qTS.ts.shape)
            if np.allclose(child.ts, qTS.ts):
                return True, Accesses
        else:
            return False, Accesses

    return False, Accesses


def main():
    global totalQueries

    parser = argparse.ArgumentParser()
    # -s #n -c #n -s #n
    parser.add_argument("-s", "--segments", dest = "segments", default = "16", help="Number of Segments", type=int)
    parser.add_argument("-c", "--cardinality", dest = "cardinality", default = "16", help="Cardinality", type=int)
    parser.add_argument("-w", "--window", dest = "window", default = "16", help="Sliding Window Size", type=int)
    parser.add_argument("-t", "--threshold", dest = "threshold", default = "1000", help="Threshold for split", type=int)
    parser.add_argument("-p", "--promotion", action='store_true', help="Define Promotion Strategy")
    parser.add_argument("TS1")
    parser.add_argument("TS2")

    args = parser.parse_args()

    variables.segments = args.segments
    variables.maximumCardinality = args.cardinality
    variables.slidingWindowSize = args.window
    variables.threshold = args.threshold
    variables.defaultPromotion = args.promotion
    f1 = args.TS1
    f2 = args.TS2

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

    totalAccesses = 0
    totalSplits = 0

    totalQueries = 0
    variables.nSplits = 0
    totalSplits = 0
    variables.nSubsequences = 0
    totalAccesses = 0

    # Build iSAX for TS1
    i1, ts1 = createISAX(f1, windowSize, segments)
    totalSplits = totalSplits + variables.nSplits
    totalAccesses = totalAccesses + variables.nSubsequences

    # Build iSAX for TS2
    variables.nSubsequences = 0
    variables.nSplits = 0
    i2, ts2 = createISAX(f2, windowSize, segments)
    totalSplits = totalSplits + variables.nSplits
    totalAccesses = totalAccesses + variables.nSubsequences

    # Query iSAX for TS1
    for idx in range(0, len(ts1)-windowSize+1):
        currentQuery = ts1[idx:idx+windowSize]
        found, ac = query(i1, currentQuery)
        if found == False:
            print("This cannot be happening!")
            return
        totalAccesses = totalAccesses + ac

    # Query iSAX for TS1
    for idx in range(0, len(ts2)-windowSize+1):
        currentQuery = ts2[idx:idx+windowSize]
        found, ac = query(i1, currentQuery)
        totalAccesses = totalAccesses + ac

    # Query iSAX for TS2
    for idx in range(0, len(ts2)-windowSize+1):
        currentQuery = ts2[idx:idx+windowSize]
        found, ac = query(i2, currentQuery)
        if found == False:
            print("This cannot be happening!")
            return
        totalAccesses = totalAccesses + ac

    # Query iSAX for TS2
    for idx in range(0, len(ts1)-windowSize+1):
        currentQuery = ts1[idx:idx+windowSize]
        found, ac = query(i2, currentQuery)
        totalAccesses = totalAccesses + ac

    print("Total subsequence accesses:", totalAccesses)
    print("Total splits:", totalSplits)
    print("Total queries:", totalQueries)

if __name__ == '__main__':
	main()
