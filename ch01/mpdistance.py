#!/usr/bin/env python3

import stumpy
import stumpy.mpdist
import numpy as np

import time
import sys
import pandas as pd

if len(sys.argv) != 4:
    print("TS1 + TS2 + Window size")
    sys.exit()

# Time series files
TS1 = sys.argv[1]
TS2 = sys.argv[2]
windowSize = int(sys.argv[3])

print("TS1:", TS1, "TS2:", TS2, "Window Size:", windowSize)

# Read Sequence as Pandas
ts1Temp = pd.read_csv(TS1, compression='gzip', header = None).astype(np.float64)
# Convert to NParray
ta = ts1Temp.to_numpy()
ta = ta.reshape(len(ta))

# Read Sequence as Pandas
ts2Temp = pd.read_csv(TS2, compression='gzip', header = None).astype(np.float64)
# Convert to NParray
tb = ts2Temp.to_numpy()
tb = tb.reshape(len(tb))

print(len(ta), len(tb))

start_time = time.time()
mpdist = stumpy.mpdist(ta, tb, m=windowSize)
print("--- %.5f seconds ---" % (time.time() - start_time))
print("MPdist: %.4f " % mpdist)

