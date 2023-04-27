from isax import variables
from isax import isax
from isax.sax import normalize
from isax.iSAXjoin import Join
import pandas as pd
import numpy as np

segments = 8
cardinality = 32
threshold = 500
slidingWindow = 1024
TS = "./500k.gz"

splits = 5983

# Helper function that is not a test function
def createISAX(file, w, s):
    ts = pd.read_csv(file, names=['values'], compression='gzip').astype(np.float64)

    ts_numpy = ts.to_numpy()
    length = len(ts_numpy)
    ISAX = isax.iSAX()
    ISAX.length = length

    # Split sequence into subsequences
    for i in range(length - w + 1):
        ts = ts_numpy[i:i+w]
        ts_node = isax.TS(normalize(ts), s)
        ISAX.insert(ts_node)

    return ISAX, ts_numpy

def test_count_subsequences():
    variables.nSplits = 0
    variables.segments = segments
    variables.maximumCardinality = cardinality
    variables.slidingWindowSize = slidingWindow
    variables.threshold = threshold
    i, ts = createISAX(TS, slidingWindow, segments)

    sum = 0
    for k in i.ht:
        t = i.ht[k]
        if t.terminalNode:
            sum += t.nTimeSeries()

    assert sum == len(ts) - slidingWindow + 1


def test_count_splits():
    variables.nSplits = 0
    variables.segments = segments
    variables.maximumCardinality = cardinality
    variables.slidingWindowSize = slidingWindow
    variables.threshold = threshold
    variables.defaultPromotion = False
    i, ts = createISAX(TS, slidingWindow, segments)

    assert variables.nSplits == splits


def test_join_same():
    variables.nSplits = 0
    variables.segments = segments
    variables.maximumCardinality = cardinality
    variables.slidingWindowSize = slidingWindow
    variables.threshold = threshold
    i, _ = createISAX(TS, slidingWindow, segments)
    Join(i, i)

    assert np.allclose(variables.ED, np.zeros(len(variables.ED))) == True
