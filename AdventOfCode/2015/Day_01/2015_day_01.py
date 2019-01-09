#!/bin/python
# -*- coding: utf-8 -*-
# http://adventofcode.com/2015/day/1  

###################################################################################################################################################################
#  
#  Solution to day 1 part 1: 74
#  Solution to day 1 part 2: 1795
#
###################################################################################################################################################################



def processFloorTraversal(path):
    currentFloor = 0
    indexOfBasement = None

    for i in xrange(len(path)):
        step = path[i]
        if step == "(":
            currentFloor += 1
        elif step == ")":
            currentFloor -= 1

        if currentFloor == -1 and indexOfBasement is None:
            indexOfBasement = i +1

    return currentFloor, indexOfBasement
### processFloorTraversal


###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################


print "===== PART 1 ====="

inputFile = "input_1.txt"

testCases = [
    ("(())", 0),
    ("()()", 0),
    ("(((", 3),
    ("(()(()(", 3),
    ("))(((((", 3),
    ("())", -1),
    ("))(", -1),
    (")))", -3),
    (")())())", -3)
]

for testCase in testCases:
    if testCase[1] == processFloorTraversal(testCase[0])[0]:
        print "PASS"
    else:
        print "FAIL: " + testCase[0]

with open(inputFile) as f:
    content = f.readlines()


floor, indexOfBasement = processFloorTraversal(content[0])

print ""
print "Solution to day 1 part 1: " + str(floor)


###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################

testCases = [
    (")", 1),
    ("()())", 5)
]

for testCase in testCases:
    if testCase[1] == processFloorTraversal(testCase[0])[1]:
        print "PASS"
    else:
        print "FAIL: " + testCase[0]
        print processFloorTraversal(testCase[0])[1]


print ""
print "===== PART 2 ====="
print "Solution to day 1 part 2: " + str(indexOfBasement)

