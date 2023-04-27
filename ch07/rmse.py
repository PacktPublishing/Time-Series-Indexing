#!/usr/bin/env python3.10

from isax import variables
from isax import isax
from isax import tools
from isax import sax

import sys
import pandas as pd
import numpy as np
import stumpy

import math
import argparse

def approximateMP(ts_numpy):
    #
    # Initialize iSAX index
    #
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

    nSubsequences = length - windowSize + 1
    vDist = [None] * nSubsequences
    vIndex = [None] * nSubsequences

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

# Root Mean Square Error (RMSE)
def RMSE(realV, approximateV):
    # Pass the above actual and predicted lists as the arguments to the np.subtract()
    # function to get the difference between the predicted and the actual values.
    # store it in another variable.
    diffrnce = np.subtract(realV, approximateV)
    # Square the above obtained difference using the np.square() function
    # store it in another variable.
    sqre_err = np.square(diffrnce)
    # Apply mean() function to the above obtained squared value to
    # get the mean of the squared value(MSE).
    # store it in another variable.
    rslt_meansqre_err = sqre_err.mean()
    # Pass the above obtained mean square error as an argument to the math.sqrt()
    # function to get the Root mean square error
    # store it in another variable.
    error = math.sqrt(rslt_meansqre_err)

    return error

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
    # segments = variables.segments
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

    # Real Matrix Profile
    TSreshape = ts_numpy.reshape(len(ts_numpy))
    realMP = stumpy.stump(TSreshape, windowSize)
    realDistances = realMP[:,0]

    # Approximate Matrix Profile
    _, vDist = approximateMP(ts_numpy)

    rmseError = RMSE(realDistances, vDist)
    print("Error =", rmseError)

if __name__ == '__main__':
	main()
