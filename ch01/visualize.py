#!/usr/bin/env python3

import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math

def main():
    if len(sys.argv) != 2:
        print("TS")
        sys.exit()

    F = sys.argv[1]

    # Read Sequence as Pandas
    ts = pd.read_csv(F, compression='gzip', header = None)
    # Convert to NParray
    ta = ts.to_numpy()
    ta = ta.reshape(len(ta))

    plt.plot(ta, label=F, linestyle='-', markevery=100, marker='o')
    plt.xlabel('Time Series', fontsize=14)
    plt.ylabel('Values', fontsize=14)

    plt.grid()
    plt.savefig("CH01_03.png", dpi=300, format='png', bbox_inches='tight')

if __name__ == '__main__':
	main()

