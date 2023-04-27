#!/usr/bin/env python3

import sys
import pandas as pd
import numpy as np

def main():
    if len(sys.argv) != 2:
        print("TS")
        sys.exit()

    F = sys.argv[1]
    ts = pd.read_csv(F, compression='gzip')
    ta = ts.to_numpy()
    ta = ta.reshape(len(ta))

    per01 = round(np.quantile(ta, .01), 5)
    per25 = round(np.quantile(ta, .25), 5)
    per75 = round(np.quantile(ta, .75), 5)

    print("Percentile 1%:", per01, "Percentile 25%:", per25, "Percentile 75%:", per75)

if __name__ == '__main__':
	main()
