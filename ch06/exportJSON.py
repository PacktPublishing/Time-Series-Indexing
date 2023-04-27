#!/usr/bin/env python3.10

from isax import variables
from isax import isax
from isax import tools

import sys
import pandas as pd
import numpy as np

import time
import argparse

import json

JSON_message = {
 "name": None,
 "size": None,
 "children": []
}

def createJSON(subtree):
    if subtree == None:
        return None

    t = {}
    t['name'] = subtree.word
    t['children'] = []

    # First, check if this is a Terminal node
    if subtree.terminalNode == True:
        t['size'] = subtree.nTimeSeries()
        return t
    # This is still a Terminal node
    # Just in case!
    elif subtree.left == None and subtree.right == None:
        print("This should not happen!")
        return t
    else:
        ch1 = createJSON(subtree.left)
        ch2 = createJSON(subtree.right)
        t['children'].append(ch1)
        t['children'].append(ch2)

    return t

def main():
    parser = argparse.ArgumentParser()
    # -s #n -c #n -s #n
    parser.add_argument("-s", "--segments", dest = "segments", default = "16", help="Number of Segments", type=int)
    parser.add_argument("-c", "--cardinality", dest = "cardinality", default = "16", help="Cardinality", type=int)
    parser.add_argument("-w", "--windows", dest = "window", default = "16", help="Sliding Window Size", type=int)
    parser.add_argument("-t", "--threshold", dest = "threshold", default = "1000", help="Threshold for split", type=int)
    parser.add_argument("-p", "--promotion", action='store_true', help="Define Promotion Strategy")
    parser.add_argument("TSfile")

    args = parser.parse_args()

    variables.segments = args.segments
    variables.maximumCardinality = args.cardinality
    variables.slidingWindowSize = args.window
    variables.threshold = args.threshold
    variables.defaultPromotion = args.promotion
    file = args.TSfile

    maxCardinality = variables.maximumCardinality
    segments = variables.segments
    windowSize = variables.slidingWindowSize

    if tools.power_of_two(maxCardinality) == -1:
        print("Not a power of 2:", maxCardinality)
        sys.exit()

    if variables.segments > variables.slidingWindowSize:
        print("Segments:", variables.segments, "Sliding window:", variables.slidingWindowSize)
        print("Sliding window size should be bigger than # of segments.")
        sys.exit()

    # Read Sequence as Pandas
    ts = pd.read_csv(file, names=['values'], compression='gzip')

    # Convert to NParray
    ts_numpy = ts.to_numpy()
    length = len(ts_numpy)

    #
    # Initialize iSAX index
    #
    ISAX = isax.iSAX()

    # Split sequence into subsequences
    for i in range(length - windowSize + 1):
        # Get the subsequence
        ts = ts_numpy[i:i+windowSize]
        # Create new TS node based on ts
        ts_node = isax.TS(ts, segments)
        ISAX.insert(ts_node)

    # The JSON data to return
    data = {}
    data['name'] = "0"
    data['children'] = []

    # Create JSON output
    for subTree in ISAX.children:
        if ISAX.ht[subTree] == None:
            continue

        subTreeData = createJSON(ISAX.ht[subTree])
        data['children'].append(subTreeData)


    print(json.dumps(data))


if __name__ == '__main__':
	main()

