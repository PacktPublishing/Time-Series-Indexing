#!/usr/bin/env python3

import random
import sys

precision = 5

if len(sys.argv) != 4:
    print("N MIN MAX")
    sys.exit()

# Number of values
N = int(sys.argv[1])
# Minimum value
MIN = int(sys.argv[2])
# Maximum value
MAX = int(sys.argv[3])

x = random.uniform(MIN, MAX)
# Random float number
for i in range(N):
    print(round(random.uniform(MIN, MAX), precision))
