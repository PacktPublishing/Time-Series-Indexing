#!/usr/bin/env python3

import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
import os

if len(sys.argv) != 2:
    print("TS1")
    sys.exit()

# Time series files
TS1 = sys.argv[1]

# Read Sequence as Pandas
ts1Temp = pd.read_csv(TS1, compression='gzip')
# Convert to NParray
ta = ts1Temp.to_numpy()
ta = ta.reshape(len(ta))

min = np.min(ta)
max = np.max(ta)

plt.style.use('Solarize_Light2')
bins = np.linspace(min, max, 2 * abs(math.floor(max) + 1))

plt.hist([ta], bins, label=[os.path.basename(TS1)])
plt.legend(loc='upper right')
plt.show()
