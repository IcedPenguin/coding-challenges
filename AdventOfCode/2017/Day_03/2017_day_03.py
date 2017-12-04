#!/bin/python
# -*- coding: utf-8 -*-
# http://adventofcode.com/2017/day/3

import math

###################################################################################################################################################################
#  
# Solution to day 3 part 1 approach 1: 419
# Solution to day 3 part 1 approach 2: 419
# Solution to day 3 part 2 approach 2: 295229
#
###################################################################################################################################################################


###################################################################################################################################################################
###################################################################################################################################################################
############################################################################ Aproach 1 ############################################################################
#
# Approach 1 thoughts. 
#
# I initially considered the naïve approach of simply creating a large matrix, filling it square 
# by square, and testing for the completion condition as each individual matrix cell was filled.
# I knew this would work. However, I was wondering if there was a more analytical method that 
# wasn’t pure brute force.
#
# The approach I took started by noticing the value in the lower right corner of each concentric 
# square were the odd numbered perfect cubes. I reasoned, if I could find the concentric square 
# that held the target value, I could walk backward from the known perfect cube value to the target 
# to derive the coordinate of the target.
# 
# This approach worked great, and took almost zero memory to compute.
#

def findFirstPerfectSquareLargerThanTarget(target):
    i = 1
    while True:
        square = i**2
        if square >= target:
            return i
        else:
            i += 2
### findFirstPerfectSquareLargerThanTarget


def findPointForValue(value, matrixSize):
    valueSquare = findFirstPerfectSquareLargerThanTarget(value)

    ##### search the bottom row.
    testValue = valueSquare**2
    counter = valueSquare -1
    while counter >= 0:
        if testValue == value:
            # print "%d Found botom row. (%d, %d)" % (testValue, counter, matrixSize-1)
            return counter, matrixSize-1

        testValue -= 1
        counter -= 1

    ##### search the left row
    counter = valueSquare -2
    while counter >= 0:
        if testValue == value:
            # print "%d Found left column. (%d, %d)" % (testValue, 0, counter)
            return 0, counter

        testValue -= 1
        counter -= 1

    ##### search the top row
    counter = 1
    while counter < valueSquare :
        if testValue == value:
            # print "%d Found top row. (%d, %d)" % (testValue, counter, 0)
            return counter, 0

        testValue -= 1
        counter += 1

    ##### search the right column
    counter = 1
    while counter < valueSquare :
        if testValue == value:
            # print "%d Found right column. (%d, %d)" % (testValue, matrixSize-1, counter)
            return matrixSize-1, counter

        testValue -= 1
        counter += 1

    return -1, -1 # error, not found.
### findPointForValue


def getDistanceToMiddleOfMatrix(matrixSize, x, y):
    middleX = matrixSize / 2 
    middleY = matrixSize / 2

    return int(math.fabs(middleX - x) + math.fabs(middleY - y))
### getDistanceToMiddleOfMatrix


###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################
targetValue = 289326

perfectSquare = findFirstPerfectSquareLargerThanTarget(targetValue)
x,y = findPointForValue(targetValue, perfectSquare)
distance = getDistanceToMiddleOfMatrix(perfectSquare, x, y)

# print "target: %d" % (targetValue)
# print "square: %d" % (perfectSquare)
# print "x: %d" % (x)
# print "y: %d" % (y)
# print "distance: %d" % (distance)
print "Solution to day 3 part 1 approach 1: %d" % (distance)


###################################################################################################################################################################
###################################################################################################################################################################
############################################################################ Aproach 2 ############################################################################
# 
# Why did I need an approach two? Simple, part 2 of the problem required having additional 
# knowledge that was not derivable using approach 1. After just a few seconds of thought, 
# it became clear that using the brute force, fill the matrix approach would work wonders 
# here. I simply would change out the algorithm to calculate the value and then part two 
# would be solved.  I went ahead and proved to myself the next cell location search and fill 
# worked as expected by resolving part 1 and verifying the answers matched.
# 



up = (-1, 0)
down = (1, 0)
left = (0, -1)
right = (0, 1)

directionTransitions = {
    up: left,
    left: down,
    down: right,
    right: up
}

def createZeroFilledMatrix(side):
    matrix = []
    for y in xrange(side):
        row = []
        for x in xrange(side):
            row.append(0)
        matrix.append(row)
    return matrix
### createZeroFilledMatrix


def applyDirection(x, y, direction):
    x += direction[0]
    y += direction[1]
    return x, y
### applyDirection


def findNextLocationToFill(matrix, x, y, previousDirection, counter):
    if counter == 2:
        x, y = applyDirection(x, y, right)
        return x, y, right

    # determine if we should turn of keep going.
    xTest, yTest = applyDirection(x, y, directionTransitions[previousDirection])

    # If we turn and are facing an empty square, then we should move into that empty square
    if matrix[xTest][yTest] == 0: 
        return xTest, yTest, directionTransitions[previousDirection]

    # If we turn and the square is occupied, then should stay in the previous direction
    else: 
        x, y = applyDirection(x, y, previousDirection)
        return x, y, previousDirection
### findNextLocationToFill


def fillNextLocation(algorithm, matrix, x, y, counter):
    if algorithm == 1:
        matrix[x][y] = counter
        return counter

    elif algorithm == 2:
        total = 0
        weCanGoUp       = x - 1 >= 0
        weCanGoDown     = x + 1 <  len(matrix)
        weCanGoLeft     = y - 1 >= 0
        weCanGoRight    = y + 1 <  len(matrix)

        if weCanGoUp and weCanGoLeft:
            total += matrix[x-1][y-1]

        if weCanGoUp:
            total += matrix[x-1][y]

        if weCanGoUp and weCanGoRight:
            total += matrix[x-1][y+1]

        if weCanGoLeft:
            total += matrix[x][y-1]

        if weCanGoRight:
            total += matrix[x][y+1]

        if weCanGoDown and weCanGoLeft:
            total += matrix[x+1][y-1]

        if weCanGoDown:
            total += matrix[x+1][y]

        if weCanGoDown and weCanGoRight:
            total += matrix[x+1][y+1]

        matrix[x][y] = total
        return total
### fillNextLocation


def workwork(algorithm, targetValue):
    counter = 2
    currentDirection = right
    filledValue = -1
    side = findFirstPerfectSquareLargerThanTarget(targetValue)
    x = side / 2
    y = side / 2

    matrix = createZeroFilledMatrix(side)
    matrix[x][y] = 1
    direction = None

    while filledValue < targetValue:
        x, y, direction = findNextLocationToFill(matrix, x, y, direction, counter)
        filledValue = fillNextLocation(algorithm, matrix, x, y, counter)
        # print "Completed step: %d (%d, %d) ← %d" % (counter, x, y, filledValue)
        counter += 1

    return (side / 2, side / 2), (x, y), filledValue
### workwork

###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################


targetValue = 289326
initialPoint, finalPoint, filledValue = workwork(1, targetValue)
print "Solution to day 3 part 1 approach 2: %d" % (int(math.fabs(initialPoint[0] - finalPoint[0]) + math.fabs(initialPoint[1] - finalPoint[1])))


###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################


targetValue = 289326
initialPoint, finalPoint, filledValue = workwork(2, targetValue)
print "Solution to day 3 part 2 approach 2: %d" % (filledValue)


