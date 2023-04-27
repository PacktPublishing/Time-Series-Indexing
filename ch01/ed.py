#!/usr/bin/env python3

import numpy as np
import sys

# This works because the Euclidean distance is the l2 norm,
# and the default value of the ord parameter
# in numpy.linalg.norm is 2
def euclidean(a, b):
    return np.linalg.norm(a-b)

def main():
    ta = np.array([1, 2, 3])
    tb = np.array([0, 2, 2])

    if len(ta) != len(tb):
        print("Time series should have the same length!")
        print(len(ta), len(tb))
        sys.exit()

    ed = euclidean(ta, tb)
    print("Euclidean distance:", ed)

if __name__ == '__main__':
    main()

