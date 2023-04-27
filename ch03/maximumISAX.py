#!/usr/bin/env python3

import sys

def main():
    if len(sys.argv) != 4:
        print("cardinality segments threshold")
        print("The cardinality SHOULD be a power of 2.")
        sys.exit()

    cardinality = int(sys.argv[1])
    segments = int(sys.argv[2])
    threshold = int(sys.argv[3])

    terminalNodes = pow(cardinality, segments)
    print("Nodes:", terminalNodes)

    subsequences = terminalNodes * threshold
    print("Maximum number of subsequences:", subsequences)

if __name__ == '__main__':
	main()
