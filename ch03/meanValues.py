#!/usr/bin/env python3

# Date: Monday 19 December 2022
#
# This utility outputs the mean value of all
# (NORMALIZED) subsequences of a time series

import sys
import numpy as np
import pandas as pd

sys.path.insert(0,'..')

def normalize(x):
    eps = 1e-6
    mu = np.mean(x)
    std = np.std(x)
    if std < eps:
        return np.zeros(shape=x.shape)
    else:
        return (x-mu)/std

def main():
    if len(sys.argv) != 4:
        print("Usage: TS1 sliding_window segments")
        print("For the sliding window, we prefer values which are a power of 2.")
        sys.exit()

    file = sys.argv[1]
    # We prefer values which are powers of 2
    sliding = int(sys.argv[2])
    segments = int(sys.argv[3])

    if sliding <= 0:
        print("Sliding value is not allowed:", sliding)
        sys.exit()

    ts = pd.read_csv(file, names=['values'], compression='gzip')
    ts_numpy = ts.to_numpy()
    length = len(ts_numpy)

    splits = sliding // segments
    # Split time series into subsequences
    for i in range(length - sliding + 1):
        t1_temp = ts_numpy[i:i+sliding]
        normalized = normalize(t1_temp)

        for s in range(segments):
            temp = normalized[splits*s:splits*(s+1)]
            mValue = np.mean(temp)
            print(round(mValue,5))


if __name__ == '__main__':
	main()
