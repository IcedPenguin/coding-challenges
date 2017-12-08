#!/bin/python
# -*- coding: utf-8 -*-
# http://adventofcode.com/2017/day/5


###################################################################################################################################################################
#  
#  Solution to day 5 part 1: 358309
#  Solution to day 5 part 2: 28178177
#
###################################################################################################################################################################


###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################

def readFileIntoArray(fileName):
    array = []
    with open(fileName) as f:
        for line in f:
            array.append(int(line.strip()))

    return array
### readFileIntoArray    


def jumpAndIncrementAlgorithm1(array, index):
    # Returns boolean (legal jump), int (location we are jumping to)
    if index < 0 or index >= len(array):
        return False, index

    distanceToJump = array[index]
    array[index] += 1
    locationToJumpTo = index + distanceToJump
    return True, locationToJumpTo
### jumpAndIncrement


def jumpAndIncrementAlgorithm2(array, index):
    # Returns boolean (legal jump), int (location we are jumping to)
    if index < 0 or index >= len(array):
        return False, index

    distanceToJump = array[index]
    if distanceToJump >= 3:
        array[index] -= 1
    else:
        array[index] += 1

    locationToJumpTo = index + distanceToJump
    return True, locationToJumpTo
### jumpAndIncrement


# input_file = "input_sample.txt"
input_file = "input_5.txt"

array = readFileIntoArray(input_file)
keepGoing = True
index = 0
count = 0

while keepGoing:
    count += 1
    keepGoing, index = jumpAndIncrementAlgorithm1(array, index)
    
count -= 1

print "Solution to day 5 part 1: " + str(count)


###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################


array = readFileIntoArray(input_file)
keepGoing = True
index = 0
count = 0

while keepGoing:
    count += 1
    keepGoing, index = jumpAndIncrementAlgorithm2(array, index)
    
count -= 1

print "Solution to day 5 part 2: " + str(count)

