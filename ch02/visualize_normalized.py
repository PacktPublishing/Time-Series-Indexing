#!/usr/bin/env python3

import sys
import pandas as pd
import matplotlib.pyplot as plt
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

    # Find its normalized version
    taNorm = normalize(ta)

    plt.plot(ta, label="Regular", linestyle='-', markevery=10, marker='o')
    plt.plot(taNorm, label="Normalized", linestyle='-.', markevery=10, marker='o')
    plt.xlabel('Time Series', fontsize=14)
    plt.ylabel('Values', fontsize=14)
    plt.legend()

    plt.grid()
    plt.savefig("CH02_01.png", dpi=300, format='png', bbox_inches='tight')

if __name__ == '__main__':
	main()
