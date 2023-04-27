#!/usr/bin/env python3

import argparse
from isax import variables

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--segments", dest = "segments", default = "4", help="Number of Segments", type=int)
    parser.add_argument("-c", "--cardinality", dest = "cardinality", default = "32", help="Cardinality", type=int)
    parser.add_argument("-w", "--window", dest = "window", default = "16", help="Sliding Window Size", type=int)
    parser.add_argument("TS1")

    args = parser.parse_args()

    variables.segments = args.segments
    variables.maximumCardinality = args.cardinality
    variables.slidingWindowSize = args.window

    windowSize = variables.slidingWindowSize
    maxCardinality = variables.maximumCardinality
    f1 = args.TS1
    print("Time Series:", f1, "Window Size:", windowSize)
    print("Maximum Cardinality:", maxCardinality, "Segments:", variables.segments)

if __name__ == '__main__':
	main()
