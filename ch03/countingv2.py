#!/usr/bin/env python3

import sys
import pandas as pd
from sax import sax

def calculate(ts_numpy, sliding, segments, cardinality):
    KEYS = {}

    length = len(ts_numpy)
    for i in range(length - sliding + 1):
        t1_temp = ts_numpy[i:i+sliding]
        tempSAXword = sax.createPAA(t1_temp, cardinality, segments)
        tempSAXword = tempSAXword[:-1]

        if KEYS.get(tempSAXword) == None:
            KEYS[tempSAXword] = 1
        else:
            KEYS[tempSAXword] = KEYS[tempSAXword] + 1

    return KEYS

def main():
    if len(sys.argv) != 6:
        print("TS1 sliding_window cardinality segments threshold")
        sys.exit()

    file = sys.argv[1]
    sliding = int(sys.argv[2])
    cardinality = int(sys.argv[3])
    segments = int(sys.argv[4])
    threshold = int(sys.argv[5])

    if sliding % segments != 0:
        print("sliding MODULO segments != 0...")
        sys.exit()

    if sliding <= 0:
        print("Sliding value is not allowed:", sliding)
        sys.exit()

    if cardinality <= 0:
        print("Cardinality Value is not allowed:", cardinality)
        sys.exit()

    ts = pd.read_csv(file, names=['values'], compression='gzip')
    ts_numpy = ts.to_numpy()

    # See if it fits
    overflow = False
    KEYS = calculate(ts_numpy, sliding, segments, cardinality)
    maxVal = max(KEYS.values())
    if maxVal > threshold:
        overflow = True

    # See if we can make it fit or reduce the parameters
    if overflow:
        i = 2
        while overflow:
            # We cannot have more segments than the sliding window
            if segments * i > sliding:
                break
            print("Increasing segments to", i * segments)
            overflow = False
            KEYS = calculate(ts_numpy, sliding, segments * i, cardinality)
            maxVal = max(KEYS.values())
            if maxVal > threshold:
                overflow = True
                print("Overflow")
                i = 2 * i
            if overflow == False:
                print("New segments:", i * segments)
    else:
        print("Threshold can be", max(KEYS.values()))
        print("Reducing cardinality to", cardinality//2)
        overflow = False
        KEYS = calculate(ts_numpy, sliding, segments, cardinality//2)
        maxVal = max(KEYS.values())
        if maxVal > threshold:
            print("Cannot reduce cardinality")
        elif overflow == False:
            print("New cardinality:", cardinality//2)

    # Now let us see whether the iSAX index is going to be
    # balanced or not using a cardinality value of 2
    KEYS = calculate(ts_numpy, sliding, segments, 2)
    minVal = min(KEYS.values())
    maxVal = max(KEYS.values())
    print("Min:", minVal, "Max:", maxVal)
    for k in KEYS.keys():
        print(k, ":", KEYS[k])


if __name__ == '__main__':
	main()
