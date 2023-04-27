#!/usr/bin/env python3.10

import pandas as pd
import argparse

import numpy as np
import time

def euclidean(a, b):
    a = normalize(a)
    b = normalize(b)
    return np.linalg.norm(a-b)

def normalize(x):
    eps = 1e-6
    mu = np.mean(x)
    std = np.std(x)
    if std < eps:
        return np.zeros(shape=x.shape)
    else:
        return (x-mu)/std

def mpdist(ts1, ts2, window):
    L_AB = JOIN(ts1, ts2, window)
    L_BA = JOIN(ts2, ts1, window)

    JABBA = L_AB + L_BA
    JABBA.sort()

    index = int(0.05 * (len(JABBA) + 2 * window)) + 1
    return JABBA[index]

def JOIN(ts1, ts2, window):
    LIST = []

    l1 = len(ts1) - window + 1
    l2 = len(ts2) - window + 1

    for i1 in range(l1):
        t1 = ts1[i1:i1+window]
        min = round(euclidean(t1, ts2[0:window]), 4)
        for i2 in range(1, l2):
            t2 = ts2[i2:i2+window]
            temp = round(euclidean(t1, t2), 4)
            if min > temp:
                min = temp

        LIST.append(min)

    return LIST

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--window", dest = "window", default = "16", help="Sliding Window", type=int)
    parser.add_argument("TS1")
    parser.add_argument("TS2")
    args = parser.parse_args()

    windowSize = args.window
    inputTS1 = args.TS1
    inputTS2 = args.TS2

    start_time = time.time()

    ts1 = pd.read_csv(inputTS1, names=['values'], compression='gzip')
    ts_numpy1 = ts1.to_numpy()
    ta1 = ts_numpy1.reshape(len(ts_numpy1))
    ts2 = pd.read_csv(inputTS2, names=['values'], compression='gzip')
    ts_numpy2 = ts2.to_numpy()
    ta2 = ts_numpy2.reshape(len(ts_numpy2))

    distance = mpdist(ta1, ta2, windowSize)
    print("--- %.5f seconds ---" % (time.time() - start_time))

    print("MPdist:", distance)

if __name__ == '__main__':
	main()
