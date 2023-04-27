#!/usr/bin/env python3.10

from isax import variables
from isax import isax
from isax import tools
from isax import sax

import sys
import pandas as pd
import numpy as np

import argparse

def approximateMP(ts_numpy):
    ISAX = isax.iSAX()

    length = len(ts_numpy)
    windowSize = variables.slidingWindowSize
    segments = variables.segments

    # Split sequence into subsequences
    for i in range(length - windowSize + 1):
        # Get the subsequence
        ts = ts_numpy[i:i+windowSize]
        # Create new TS node based on ts
        ts_node = isax.TS(ts, segments)
        ts_node.index = i
        ISAX.insert(ts_node)

    vDist = [None] * (length - windowSize + 1)
    vIndex = [None] * (length - windowSize + 1)
    nSubsequences = length - windowSize + 1

    for k in ISAX.ht:
        t = ISAX.ht[k]
        if t.terminalNode == False:
            continue

        # i is the index of the subsequence in the terminal node
        for i in range(t.nTimeSeries()):
            # This is the REAL index of the subsequence
            # in the time series
            idx = t.children[i].index
            # This is the subsequence that we are examining
            currentTS = t.children[i].ts

            exclusionMin = idx - windowSize // 4
            if exclusionMin < 0:
                exclusionMin = 0

            exclusionMax = idx + windowSize // 4
            if exclusionMax > nSubsequences-1:
                exclusionMax = nSubsequences-1

            min = None
            minIndex = 0
            for sub in range(t.nTimeSeries()):
                # This is the REAL index of the subsequence
                # we are examining in the time series
                currentIdx = t.children[sub].index
                if currentIdx >= exclusionMin and currentIdx <= exclusionMax:
                    continue

                temp = round(tools.euclidean(currentTS, t.children[sub].ts), 3)
                if min == None:
                    min = temp
                    minIndex = currentIdx
                elif min > temp:
                    min = temp
                    minIndex = currentIdx

            # Pick left limit first, then the right limit
            if min == None:
                if exclusionMin-1 > 0:
                    randomSub = ts_numpy[exclusionMin-1:exclusionMin+windowSize-1]
                    vDist[idx] = round(tools.euclidean(currentTS, randomSub), 3)
                    vIndex[idx] = exclusionMin - 1
                else:
                    randomSub = ts_numpy[exclusionMax+1:exclusionMax+windowSize+1]
                    vDist[idx] = round(tools.euclidean(currentTS, randomSub), 3)
                    vIndex[idx] = exclusionMax + 1
            else:
                vDist[idx] = min
                vIndex[idx] = minIndex

    return vIndex, vDist

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

    vIndex, vDist = approximateMP(ts_numpy)
    # Printing a small part of the output
    print("Indexes:", vIndex[:25])
    print("Distances:", vDist[:25])

if __name__ == '__main__':
	main()
