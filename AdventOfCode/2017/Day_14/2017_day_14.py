#!/bin/python
# -*- coding: utf-8 -*-
# http://adventofcode.com/2017/day/14

import KnotHash

###################################################################################################################################################################
#  
#  Solution to day 14 part 1: 8190
#  Solution to day 14 part 2: 1134
#
###################################################################################################################################################################


def getKnotHashes(problemInput):
    memory = []
    for i in xrange(128):
        key = problemInput + "-" + str(i)
        knotHash = KnotHash.computeKnotHash(key)
        memory.append(knotHash)

    return memory
### getKnotHashes


def convertHexStringToBinaryString(hexString):
    t = {
        "0" : "0000",
        "1" : "0001",
        "2" : "0010",
        "3" : "0011",
        "4" : "0100",
        "5" : "0101",
        "6" : "0110",
        "7" : "0111",
        "8" : "1000",
        "9" : "1001",
        "a" : "1010",
        "b" : "1011",
        "c" : "1100",
        "d" : "1101",
        "e" : "1110",
        "f" : "1111"
    }
    binaryString = ""
    for hexChar in hexString:
        binaryString += t[hexChar]
    return binaryString
### convertHexStringToBinaryString


def countOnes(binaryString):
    count = 0
    for binChar in binaryString:
        if binChar == "1":
            count += 1

    return count
### countOnes


def performAlgorith(problemInput):
    hashes = getKnotHashes(problemInput)
    binaryStrings = []

    count = 0
    for h in hashes:
        binaryString = convertHexStringToBinaryString(h)
        binaryStrings.append(binaryString)
        count += countOnes(binaryString)

    return count, binaryStrings
### performAlgorith

###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################


sampleInput = "flqrgnkx"
problemInput = "ffayrhll"

result = 0

print "===== PART 1 ====="

count, binaryStrings = performAlgorith(problemInput)

print ""
print "Solution to day 14 part 1: " + str(count)


###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################

print ""
print "===== PART 2 ====="

IGNORE_MARKINGS = ["0", "_"]


def findNextNonMarkedRegion(matrix, x, y):
    while x < len(matrix) and y < len(matrix[0]) and (matrix[x][y] in IGNORE_MARKINGS):

        y += 1
        if y >= len(matrix[0]):
            y = 0
            x += 1

    if x < len(matrix) and y < len(matrix[0]):
        return True, x,y
    else:
        return False, x,y
### findNextNonMarkedRegion


def markRegion(matrix, x, y):
    marked = 0
    stack = [(x,y)]
    while len(stack) > 0:
        point = stack.pop(0)
        x = point[0]
        y = point[1]

        # check point, if a region mark it
        if matrix[x][y] not in IGNORE_MARKINGS:
            marked += 1
            matrix[x] = matrix[x][:y] + "_" + matrix[x][y+1:]

            # find all neighbors and add to stack
            # look up
            if x - 1 >= 0:
                stack.append((x-1, y))

            # look down
            if x + 1 < len(matrix):
                stack.append((x+1, y))

            # look left
            if y - 1 >= 0:
                stack.append((x, y-1))

            # look right
            if y +1 < len(matrix[0]):
                stack.append((x, y+1))

    return marked
### markRegion


def countRegions(matrix):
    valid, x, y = findNextNonMarkedRegion(matrix, 0, 0)
    count = 0

    while valid:
        marked = markRegion(matrix, x, y)
        if marked > 0:
            count += 1

        valid, x, y = findNextNonMarkedRegion(matrix, x, y)

    return count
### countRegions


count, binaryStrings = performAlgorith(problemInput)
count = countRegions(binaryStrings)

print ""
print "Solution to day 14 part 2: " + str(count)
