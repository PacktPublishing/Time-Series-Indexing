#!/usr/bin/env python3

import sys

def main():
    if len(sys.argv) != 2:
        print("TS")
        sys.exit()

    TS = sys.argv[1]
    file = open(TS, 'r')
    Lines = file.readlines()

    count = 0
    for line in Lines:
        # Strips the newline character
        t = line.strip()
        try:
            _ = float(t)
        except:
            count = count + 1

    print("Number of errors:", count)

if __name__ == '__main__':
	main()
