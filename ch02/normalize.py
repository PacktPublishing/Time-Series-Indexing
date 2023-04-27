#!/usr/bin/env python3

import sys
import pandas as pd
import numpy as np

def normalize(x):
    eps = 1e-6
    mu = np.mean(x)
    std = np.std(x)
    if std < eps:
        return np.zeros(shape=x.shape)
    else:
        return (x-mu)/std

def main():
    if len(sys.argv) != 2:
        print("TS")
        sys.exit()

    F = sys.argv[1]

    ts = pd.read_csv(F, compression='gzip', header = None)
    ta = ts.to_numpy()
    ta = ta.reshape(len(ta))

    taNorm = normalize(ta)

    print("[", end = ' ')
    for i in taNorm.tolist():
        print("%.4f" % i, end = ' ')
    print("]")

if __name__ == '__main__':
	main()
