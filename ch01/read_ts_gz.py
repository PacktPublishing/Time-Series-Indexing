#!/usr/bin/env python3

import pandas as pd
import numpy as np
import sys

def main():
	filename = sys.argv[1]

	ts1Temp = pd.read_csv(filename, compression='gzip', header = None).astype(np.float64)
	# Convert to NParray
	ta = ts1Temp.to_numpy()
	ta = ta.reshape(len(ta))

	print("Length:", len(ta))

if __name__ == '__main__':
	main()
