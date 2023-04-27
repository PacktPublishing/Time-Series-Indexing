#!/usr/bin/env python3.10

import pandas as pd
import argparse
import time
import stumpy
import numpy as np

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

    ts_numpy = ts.to_numpy()
    ta = ts_numpy.reshape(len(ts_numpy))
    realMP = stumpy.stump(ta, windowSize)

    realDistances = realMP[:,0]
    realIndexes = realMP[:,1]
    print("--- %.5f seconds ---" % (time.time() - start_time))

    print(realDistances)
    print(realIndexes)

if __name__ == '__main__':
	main()
