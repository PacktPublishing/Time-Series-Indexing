import os
import numpy as np
from isax import variables

breakpointsFile = variables.breakpointsFile
maxCard = variables.maximumCardinality

def power_of_two(n):
    power = 1
    while n/2 != 1:
        # Not a power of 2
        if n % 2 == 1:
            return -1

        n = n / 2
        power += 1

    return power

def load_sax_alphabet():
    path = os.path.dirname(__file__)

    file_variable = open(path + "/" + breakpointsFile)
    variables.elements = file_variable.readlines()

def breakpoints(cardinality):
    if variables.elements == "":
        load_sax_alphabet()

    myLine = variables.elements[cardinality - 1].rstrip()
    elements = myLine.split(',')
    elements.reverse()
    return elements

#
# As we have the maximum cardinality precalculated
# promoting is just a matter of string operations
# to the desired segment of a SAX word
#
def promote(node, segments):
    new_sax_word = ""
    max_array = node.maxCard.split("_")[0:variables.segments]

    # segments is an array
    #
    for i in range(variables.segments):
        t = len(segments[i])
        new_sax_word = new_sax_word + "_" + max_array[i][0:t]

    # Remove _ from the beginning of the new_sax_word
    new_sax_word = new_sax_word[1:len(new_sax_word)]
    return new_sax_word


def lowerCardinality(segs, ts_node):
    # Get Maximum Cardinality
    max = ts_node.maxCard
    lowerCardinality = [""] * variables.segments

    # Because max is a string, we need to split.
    # The max string has an underscore character at the end.
    max_array = max.split("_")[0:variables.segments]

    for i in range(variables.segments):
        t = segs[i]
        lowerCardinality[i] = max_array[i][0:t]

    return lowerCardinality

def shorter_first_promotion(nSegs):
    length = len(nSegs)
    pos = 0
    min = len(nSegs[pos])
    for i in range(1,length):
        if min > len(nSegs[i]):
            min = len(nSegs[i])
            pos = i

    # print(pos, min, len(nSegs[pos]), nSegs[pos], nSegs)
    variables.promote = pos

def round_robin_promotion(nSegs):
    # Check if there is a promotion overflow
    n = power_of_two(variables.maximumCardinality)
    t = 0

    while len(nSegs[variables.promote]) == n:
        # Go to the next SAX word and promote it
        variables.promote = (variables.promote + 1) % variables.segments
        t += 1
        if t == variables.segments:
            if variables.overflow == 0:
                print("Non recoverable Promotion overflow!")
            return
