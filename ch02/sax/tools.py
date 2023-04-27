import os
import numpy as np
import sys
from sax import variables

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


