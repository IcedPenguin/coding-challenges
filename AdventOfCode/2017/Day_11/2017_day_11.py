#!/bin/python
# -*- coding: utf-8 -*-
# http://adventofcode.com/2017/day/11


###################################################################################################################################################################
#  
#  Solution to day 11 part 1: 812
#  Solution to day 11 part 2: 1603
#
###################################################################################################################################################################


###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################


def performAlgorithmOne(inputValue):
    steps = countSteps(inputValue)
    steps = reduceSteps(steps)
    answer = getDistance(steps)
    return answer
### performAlgorithm


def countSteps(directions):
    steps = {"n": 0, "s": 0, "ne": 0, "nw": 0, "sw": 0, "se": 0}

    directions = directions.split(",")
    for direction in directions:
        steps[direction] += 1

    return steps
### countSteps

def reduceStepCancel(steps, a, b):
    smaller = min(steps[a], steps[b])
    steps[a] -= smaller
    steps[b] -= smaller

    return smaller != 0
### reduceStepCancel


def reduceStepsHorizonalVertical(steps, a, b, c):
    smaller = min(steps[a], steps[b])
    steps[a] -= smaller
    steps[b] -= smaller
    steps[c] += smaller

    return smaller != 0
### reduceStepsHorizonalVertical


def reduceSteps(steps):
    somethingChanged = True
    while somethingChanged:
        somethingChanged = False

        # N cancels with S
        somethingChanged |= reduceStepCancel(steps, "n", "s")

        # SE and SW reduce into S
        somethingChanged |= reduceStepsHorizonalVertical(steps, "se", "sw", "s")

        # NE and NW reduce into N
        somethingChanged |= reduceStepsHorizonalVertical(steps, "ne", "nw", "n")
        
        # SE cancels with NW
        somethingChanged |= reduceStepCancel(steps, "se", "nw")

        # SW cancels with NE
        somethingChanged |= reduceStepCancel(steps, "sw", "ne")
        
        # NE and S reduces to SE
        somethingChanged |= reduceStepsHorizonalVertical(steps, "ne", "s", "se")

        # NW and S reduces to SW
        somethingChanged |= reduceStepsHorizonalVertical(steps, "nw", "s", "sw")

        # SE and N reduces to NE
        somethingChanged |= reduceStepsHorizonalVertical(steps, "se", "n", "ne")

        # SW and N reduces to NW
        somethingChanged |= reduceStepsHorizonalVertical(steps, "sw", "n", "nw")

    return steps
### reduceSteps


def getDistance(steps):
    distance = 0
    for step in steps:
        distance += steps[step]

    return distance
### getDistance


def verifyDistance(ourAnswer, theirAnswer, inputValue):
    ourAnswer = str(ourAnswer)
    theirAnswer = str(theirAnswer)

    if ourAnswer == theirAnswer:
        print "PASS: %s   %s " % (theirAnswer, inputValue)

    else:
        print "FAIL: act=%s   expect=%s    input=%s" % (ourAnswer, theirAnswer, inputValue)
### verifyDistance


directionTestCases = [
    ("ne,ne,ne", 3),
    ("ne,ne,sw,sw", 0),     # (back where you started).
    ("ne,ne,s,s", 2),       # (se,se). 
    ("se,sw,se,sw,sw",3),   # (s,s,sw).
    # ---- my cases ----
    ("ne,nw,ne,nw,ne",3),
    ("sw,n", 1), 
    ("sw,sw,n", 2),
]

print "===== PART 1 ====="
for case in directionTestCases:
    result = performAlgorithmOne(case[0])
    verifyDistance(result, case[1], case[0])


inputFile = "input_11.txt"
with open(inputFile) as f:
    for line in f:
        result = performAlgorithmOne(line)

print ""    
print "Solution to day 11 part 1: " + str(result)

###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################

print ""
print "===== PART 2 ====="

def performAlgorithmTwo(inputValue):
    """
    Gross, a N^2 algorithm. Can't we better? 
    Probably, but that would that time and the input string is only a few thousand items long...
    """
    counter = 0
    distances = []
    for chunk in find_all(inputValue, ","):
        
        counter +=1 
        if counter % 100 == 0:
            print counter

        steps = countSteps(chunk)
        steps = reduceSteps(steps)
        answer = getDistance(steps)

        distances.append(answer)

    return distances
### performAlgorithm


def find_all(inputValue, sub):
    # https://stackoverflow.com/questions/4664850/find-all-occurrences-of-a-substring-in-python
    start = 0
    idx = 0
    fullStringReturned = False

    while True:
        idx = inputValue.find(sub, idx)
        
        if idx == -1 and not fullStringReturned:
            yield inputValue
            return

        yield inputValue[:idx]
        idx += 1
### find_all


totalDistanceTestCases = [
    ("ne,ne,ne",        [1,2,3]),
    ("ne,ne,sw,sw",     [1,2,1,0]),
    ("ne,ne,s,s",       [1,2,2,2]),
    ("se,sw,se,sw,sw",  [1,1,2,2,3]),
    # ---- my cases ----
    ("ne,nw,ne,nw,ne",  [1,1,2,2,3]),
    ("sw,n",            [1,1]), 
    ("sw,sw,n",         [1,2,2])
]


for case in totalDistanceTestCases:
    result = performAlgorithmTwo(case[0])
    verifyDistance(result, case[1], case[0])


inputFile = "input_11.txt"
with open(inputFile) as f:
    for line in f:
        result = performAlgorithmTwo(line)
        result = max(result)


print ""
print "Solution to day 11 part 2: " + str(result)
