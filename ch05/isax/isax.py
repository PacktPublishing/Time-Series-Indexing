from isax import variables
from isax import tools
from isax import sax

class TS:
    def __init__(self, ts, segments):
        self.index = 0
        self.ts = ts
        self.maxCard = sax.createPAA(ts, variables.maximumCardinality, segments)

class Node:
    def __init__(self, sax_word):
        self.left = None
        self.right = None
        self.terminalNode = False
        self.word = sax_word
        self.children = [TS] * variables.threshold

    # Follow algorithm from iSAX paper
    def insert(self, ts, ISAX):
        # Accessing a subsequence
        variables.nSubsequences += 1
        if self.terminalNode:
            if self.nTimeSeries() == variables.threshold:
                variables.nSplits += 1

                # Going to duplicate self Node
                temp = Node(self.word)
                temp.children = self.children
                temp.terminalNode = True

                # The current Terminal node becomes an inner node
                self.terminalNode = False
                self.children = None

                # Create TWO new Terminal nodes
                new1 = Node(temp.word)
                new1.terminalNode = True
                new2 = Node(temp.word)
                new2.terminalNode = True

                n1Segs = new1.word.split('_')
                n2Segs = new2.word.split('_')

                # This is where the promotion strategy is selected
                if variables.defaultPromotion:
                    tools.round_robin_promotion(n1Segs)
                else:
                    tools.shorter_first_promotion(n1Segs)

                # New SAX_WORD 1
                n1Segs[variables.promote] = n1Segs[variables.promote] + "0"
                # CONVERT it to string
                new1.word = "_".join(n1Segs)

                # New SAX_WORD 2
                n2Segs[variables.promote] = n2Segs[variables.promote] + "1"
                # CONVERT it to string
                new2.word = "_".join(n2Segs)

                # The inner node has the same SAX word but this is
                # not true for the two NEW Terminal nodes, which should
                # be added to the Hash Table
                ISAX.ht[new1.word] = new1
                ISAX.ht[new2.word] = new2

                # Associate the 2 new Nodes with the Node that is being splitted
                self.left = new1
                self.right = new2

                # Check all TS in original node and put them
                # in one of the two children
                #
                # This is where the actual SPLITTING takes place
                #
                # print(temp.nTimeSeries(), variables.threshold)
                for i in range(variables.threshold):
                    # Accessing a subsequence
                    variables.nSubsequences += 1

                    # Decrease TS.maxCard to current Cardinality
                    tempCard = tools.promote(temp.children[i], n1Segs)

                    if tempCard == new1.word:
                        new1.insert(temp.children[i], ISAX)
                    elif tempCard == new2.word:
                        new2.insert(temp.children[i], ISAX)
                    else:
                        if variables.overflow == 0:
                            print("OVERFLOW:", tempCard)
                        variables.overflow = variables.overflow + 1

                # Now insert the INITIAL TS node!
                # self is now an INNER node
                self.insert(ts, ISAX)

                if variables.defaultPromotion:
                    # Next time, promote the next segment
                    variables.promote = (variables.promote + 1) % variables.segments

            else:
                # TS is added if we have a Terminal node
                self.children[self.nTimeSeries()] = ts
        else:
            # Otherwise, we are dealing with an INNER node
            # and we should add it to the INNER node by trying
            # to find an existing terminal node or create a new one
            # See whether it is going to be included in the left
            # or the right child
            left = self.left
            right = self.right

            leftSegs = left.word.split('_')
            # Promote
            tempCard = tools.promote(ts, leftSegs)

            if tempCard == left.word:
                left.insert(ts, ISAX)
            elif tempCard == right.word:
                right.insert(ts, ISAX)
            else:
                if variables.overflow == 0:
                    print("OVERFLOW:", tempCard, left.word, right.word)
                variables.overflow = variables.overflow + 1

        return

    def nTimeSeries(self):
        if self.terminalNode == False:
            print("Not a terminal node!")
            return

        n = 0
        for i in range(0, variables.threshold):
            if type(self.children[n]) == TS:
                n = n + 1

        return n


class iSAX:
    def __init__(self):
        # This is now a hash table
        self.children = {}
        # HashTable for storing Nodes
        self.ht = {}
        self.length = 0

    def insert(self, ts_node):
        # Array with number of segments
        # For cardinality 1
        segs = [1] * variables.segments

        # Get cardinality 1 from ts_node
        # in order to find its main subtree
        lower_cardinality = tools.lowerCardinality(segs, ts_node)

        lower_cardinality_str = ""
        for i in lower_cardinality:
            lower_cardinality_str = lower_cardinality_str + "_" + i

        # Remove _ at the beginning
        lower_cardinality_str = lower_cardinality_str[1:len(lower_cardinality_str)]

        # Check whether the SAX word with CARDINALITY 1 
        # exists in the Hash Table.
        # If not, create it and update Hash Table
        if self.ht.get(lower_cardinality_str) == None:
            n = Node(lower_cardinality_str)
            n.terminalNode = True
            # Add it to the hash table
            self.children[lower_cardinality_str] = n
            self.ht[lower_cardinality_str] = n
            n.insert(ts_node, self)
        else:
            n = self.ht.get(lower_cardinality_str)
            n.insert(ts_node, self)

        return
