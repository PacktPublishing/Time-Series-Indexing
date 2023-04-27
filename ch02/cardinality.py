#!/usr/bin/env python3

import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

breakpointsFile = "./sax/SAXalphabet"

def main():
    if len(sys.argv) != 3:
        print("cardinality output")
        sys.exit()

    # Cardinality 8 requires 7 lines
    # Cardinality 32 requires 31 lines
    n = int(sys.argv[1]) - 1
    output = sys.argv[2]

    path = os.path.dirname(__file__)
    file_variable = open(path + "/" + breakpointsFile)
    alphabet = file_variable.readlines()
    myLine = alphabet[n - 1].rstrip()
    elements = myLine.split(',')

    lines = [eval(i) for i in elements]

    minValue = min(lines) - 1
    maxValue = max(lines) + 1

    fig, ax = plt.subplots()

    for i in lines:
        # Plot a horizontal line using axhline() in pyplot
        plt.axhline(y=i, color='r', linestyle='-.', linewidth=2)

    xLabel = "Cardinality " + str(n)

    ax.set_ylim(minValue, maxValue)
    ax.set_xlabel(xLabel, fontsize=14)
    ax.set_ylabel('Breakpoints', fontsize=14)

    ax.grid()
    fig.savefig(output, dpi=300, format='png', bbox_inches='tight')

if __name__ == '__main__':
	main()
