#!/usr/bin/env python3

from isax import variables
from isax import isax
import numpy as np

# The promote() function mimics the digits of the segments
# of an existing SAX representation, which is based
# on the SAX representation of existing nodes
# and decreases the MAXIMUM SAX representation of a subsequence
# to match the given SAX representation

# The variables.promote variable defines the SAX word
# that is going to get promoted
#
# This depends on the promotion strategy

# Based on the value of variables.promote, we create the
# SAX representation of the two nodes of a split
#
# Each time we have a split, variables.promote is updated

variablesPromote = 0
maximumCardinality = 8
segments = 4

def promote(node, s):
    global segments

    new_sax_word = ""
    max_array = node.maxCard.split("_")[0:segments]

    for i in range(segments):
        t = len(s[i])
        new_sax_word = new_sax_word + "_" + max_array[i][0:t]

    new_sax_word = new_sax_word[1:len(new_sax_word)]
    return new_sax_word

def main():
    global variablesPromote
    global maximumCardinality
    global segments

    # Used by isax.TS()
    variables.maximumCardinality = maximumCardinality

    ts = np.array([1, 2, 3, 4])
    t = isax.TS(ts, segments)

    SAX_WORD = "0_0_1_1_"
    Segs = SAX_WORD.split('_')

    print("Max cardinality:", t.maxCard)

    SAX_WORD = "00_0_1_1_"
    Segs = SAX_WORD.split('_')
    print("P1:", promote(t, Segs))

    SAX_WORD = "000_0_1_1_"
    Segs = SAX_WORD.split('_')
    print("P2:", promote(t, Segs))

    SAX_WORD = "000_01_1_1_"
    Segs = SAX_WORD.split('_')
    print("P3:", promote(t, Segs))

    SAX_WORD = "000_011_1_100_"
    Segs = SAX_WORD.split('_')
    print("P4:", promote(t, Segs))

if __name__ == '__main__':
	main()
