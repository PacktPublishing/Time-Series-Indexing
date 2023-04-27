#!/usr/bin/env python3.10

import pandas as pd
import argparse

import numpy as np
import time

def euclidean(a, b):
    aN = normalize(a)
    bN = normalize(b)
    return np.linalg.norm(aN-bN)

def normalize(x):
    eps = 1e-6
    mu = np.mean(x)
    std = np.std(x)
    if std < eps:
        return np.zeros(shape=x.shape)
    else:
        return (x-mu)/std

# Self Join
def mp(ts, window):
    l = len(ts) - window + 1
    dist = [None] * l
    index = [None] * l

    for i1 in range(l):
        t1 = ts[i1:i1+window]
        min = None
        minIndex = 0

        exclusionMin = i1 - window // 4
        if exclusionMin < 0:
            exclusionMin = 0

        exclusionMax = i1 + window // 4
        if exclusionMax > l-1:
            exclusionMax = l-1

        for i2 in range(l):
            # Exclusion zone
            if i2 >= exclusionMin and i2 <= exclusionMax:
                continue

            t2 = ts[i2:i2+window]
            temp = round(euclidean(t1, t2), 3)
            if min == None:
                min = temp
                minIndex = i2
            elif min > temp:
                min = temp
                minIndex = i2

        dist[i1] = min
        index[i1] = minIndex

    return dist, index

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--window", dest = "window", default = "16", help="Sliding Window", type=int)
    parser.add_argument("TS")
    args = parser.parse_args()

    windowSize = args.window
    inputTS = args.TS

    print("TS:", inputTS, "Sliding Window size:", windowSize)

    start_time = time.time()
    ts = pd.read_csv(inputTS, names=['values'], compression='gzip')

    # Convert to NParray
    ts_numpy = ts.to_numpy()
    ta = ts_numpy.reshape(len(ts_numpy))
    dist, index = mp(ta, windowSize)
    print(dist)
    print(index)
    print("--- %.5f seconds ---" % (time.time() - start_time))

if __name__ == '__main__':
	main()
