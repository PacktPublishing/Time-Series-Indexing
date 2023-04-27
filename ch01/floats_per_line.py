#!/usr/bin/env python3

import sys

def main():
    if len(sys.argv) != 2:
        print("TS")
        sys.exit()

    TS = sys.argv[1]
    file = open(TS, 'r')
    Lines = file.readlines()

    first = True
    wordsPerLine = 0
    for line in Lines:
        t = line.strip()
        words = t.split()
        for word in words:
            try:
                _ = float(word)
            except:
                print("Error:", word)

        if first:
            wordsPerLine = len(words)
            first = False
        elif wordsPerLine != len(words):
            print("Expected", wordsPerLine, "found", len(words))
            continue

if __name__ == '__main__':
	main()
