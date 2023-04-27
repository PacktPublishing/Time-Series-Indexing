# https://github.com/msaffarm/pySAX/blob/master/util/sax.py

import numpy as np
from scipy.stats import norm

from sax import tools

import sys
sys.path.insert(0,'..')

def normalize(x):
    eps = 1e-6
    mu = np.mean(x)
    std = np.std(x)
    if std < eps:
        return np.zeros(shape=x.shape)
    else:
        return (x-mu)/std

def createPAA(ts, cardinality, segments):
    SAXword = ""
    ts_norm = normalize(ts)
    segment_size = len(ts_norm) // segments
    mValue = 0
    for i in range(segments):
        ts_segment = ts_norm[segment_size * i :(i+1) * segment_size]
        mValue = meanValue(ts_segment)
        index = getIndex(mValue, cardinality)
        SAXword += str(index) + "_"

    return SAXword

def meanValue(ts_segment):
    sum = 0
    for i in range(len(ts_segment)):
        sum += ts_segment[i]
    mean_value = sum / len(ts_segment)
    return mean_value

def getIndex(mValue, cardinality):
    index = 0
    # With cardinality we get cardinality + 1
    # So we need cardinality - 1 to get
    # exactly cardinality number of ranges
    bPoints = tools.breakpoints(cardinality-1)

    while mValue < float(bPoints[index]):
        if index == len(bPoints) - 1:
            # This means that index should be advanced
            # before breaking out of the while loop
            index += 1
            break
        else:
            index += 1

    digits = tools.power_of_two(cardinality)
    binary_index = f'{index:0{digits}b}'

    # Inverse the result
    inverse_s = ""
    for i in binary_index:
       if i == '0':
           inverse_s += '1'
       else:
           inverse_s += '0'

    return inverse_s

