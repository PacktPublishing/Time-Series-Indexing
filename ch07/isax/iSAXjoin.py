from isax import variables
from isax import tools

def Join(iSAX1, iSAX2):
    # Begin with the children of the root node. That it, the
    # nodes with SAX words with Cardinality of 1.
    for t1 in iSAX1.children:
        k1 = iSAX1.children[t1]
        if k1 == None:
            continue
        for t2 in iSAX2.children:
            k2 = iSAX2.children[t2]
            if k2 == None:
                continue
            # J_AB
            _Join(k1, k2)
            # J_BA
            _Join(k2, k1)
    return

def _Join(t1, t2):
    if t1.word != t2.word:
        return
    # Inner + Inner
    if t1.terminalNode == False and t2.terminalNode == False:
        _Join(t1.left, t2.left)
        _Join(t1.right, t2.left)
        _Join(t1.left, t2.right)
        _Join(t1.right, t2.right)
    # Terminal + Inner
    elif t1.terminalNode == True and t2.terminalNode == False:
        _Join(t1, t2.left)
        _Join(t1, t2.right)
    # Inner + Terminal
    elif t1.terminalNode == False and t2.terminalNode == True:
        _Join(t1.left, t2)
        _Join(t1.right, t2)
    # Terminal + Terminal
    # As both are terminal nodes, calculate
    # Euclidean Distances between Time Series pairs
    elif t1.terminalNode == True and t2.terminalNode == True:
        for i in range(t1.nTimeSeries()):
            minDistance = None
            for j in range(t2.nTimeSeries()):
                distance = round(tools.euclidean(t1.children[i].ts, t2.children[j].ts), variables.precision)
                # Keeping the smallest Euclidean Distance for each node
                # of the t1 Terminal node
                if minDistance == None:
                    minDistance = distance
                elif minDistance > distance:
                    minDistance = distance
            # Insert distance to PQ
            if minDistance != None:
                variables.ED.append(minDistance)
    else:
        print("This cannot happen!")
