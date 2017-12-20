#!/bin/python
# -*- coding: utf-8 -*-
# http://adventofcode.com/2017/day/17


###################################################################################################################################################################
#  
#  Solution to day 17 part 1: 136
#  Solution to day 17 part 2: 1080289
#
###################################################################################################################################################################

class SpinLock(object):
    def __init__(self, stepSize):
        self.stepSize = stepSize
        self.indexOfHead = 0
        self.circularBuffer = [0]
    ### __init__


    def printBuffer(self):
        buff = ""
        for i in xrange(len(self.circularBuffer)):
            if i == self.indexOfHead:
                buff += " (" + str(self.circularBuffer[i]) + ")"
            else:
                buff += " " + str(self.circularBuffer[i])
        print buff
    ### printBuff


    def step(self):
        size = len(self.circularBuffer)
        self.indexOfHead = (self.indexOfHead + self.stepSize) % size + 1
        
        newBuffer = []
        offset = 0
        for i in xrange(size + 1):
            if i == self.indexOfHead:
                newBuffer.append(size)
                offset = -1
            else:
                newBuffer.append( self.circularBuffer[i + offset] )

        self.circularBuffer = newBuffer

        return self.circularBuffer[(self.indexOfHead + 1) % len(self.circularBuffer)]
    ### step

### SpinLock

###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################

print "===== PART 1 ====="

spinLock = SpinLock(363)
for i in xrange(2017):
    result = spinLock.step()

print ""
print "Solution to day 17 part 1: " + str(result)


###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################


print ""
print "===== PART 2 ====="

def getValueAfterZeroForIteration(stepSize, iterations):
    indexOfHead = 0
    valueAfterZero = 0
    indexAtEndOfStepping = 0

    # walk through all 50 Million values
    for x in xrange(iterations):
        if x == 0:
            continue

        inserted = False

        # get the index of the head at the end of this iteration
        indexAtEndOfStepping = (indexOfHead + stepSize) % x 

        # save the value we are going to insert, if we landed at the front of the list
        if indexAtEndOfStepping == 0: 
            valueAfterZero = x
            # print "x=%s \t valueAfterZero=%s" % (x, valueAfterZero)
            inserted = True

        # get the new head index
        indexOfHead = indexAtEndOfStepping + 1

        # print "x=%s \t indexStep=%s \t newHead=%s \t headValue=%s \t saved=%s \t curValueAfterZero=%s" % (x, indexAtEndOfStepping, indexOfHead, x+1, inserted, valueAfterZero)
    return valueAfterZero
### getValueAfterZeroForIteration


# print """
# (0)
#  0 (1)
#  0 (2) 1
#  0  2 (3) 1
#  0  2 (4) 3  1
#  0 (5) 2  4  3  1
#  0  5  2  4  3 (6) 1
#  0  5 (7) 2  4  3  6  1
#  0  5  7  2  4  3 (8) 6  1 
#  0 (9) 5  7  2  4  3  8  6  1
# """ 
# result = getValueAfterZeroForIteration(3, 10)

result = getValueAfterZeroForIteration(363, 50000000)

print "Solution to day 17 part 2: " + str(result)
