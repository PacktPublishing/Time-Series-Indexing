#!/usr/bin/env python3

from isax import variables
from isax import tools
from isax import isax
import numpy as np

# For lowering the cardinality in all segments
#
# Mainly used for getting the children of root

def main():
    global maximumCardinality
    global segments

    # Used by isax.TS()
    variables.maximumCardinality = 8
    variables.segments = 4

    ts = np.array([1, 2, 3, 4])
    t = isax.TS(ts, variables.segments)

    Segs = [1] * variables.segments
    print(tools.lowerCardinality(Segs, t))

    Segs = [2] * variables.segments
    print(tools.lowerCardinality(Segs, t))

    Segs = [3] * variables.segments
    print(tools.lowerCardinality(Segs, t))

    return

if __name__ == '__main__':
	main()
