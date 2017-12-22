#!/bin/python
# -*- coding: utf-8 -*-
# http://adventofcode.com/2017/day/19


###################################################################################################################################################################
#  
#  Solution to day 19 part 1: SXWAIBUZY
#  Solution to day 19 part 2: 16676
#
###################################################################################################################################################################
class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    ### __init__

    def applyDirection(self, directionVector):
        return Point(self.x + directionVector[0], self.y + directionVector[1])
    ### applyDirection


    def __str__(self):
        return "P(" + str(self.x) + "," + str(self.y) + ")"

    def __repr__(self):
        return "P(" + str(self.x) + "," + str(self.y) + ")"
###

def loadMap(inputFile):
    matrix = []

    with open(inputFile) as f:
        for line in f:
            row = []
            line = line.strip("\n")
            # print line
            for letter in line:
                row.append(letter)

            matrix.append(row)

    return matrix
### loadMap


def findStartingLocations(matrix):
    points = []
    for i in xrange(len(matrix[0])):
        
        if matrix[0][i] != " ":
            points.append( Point(i, 0) )    

    return points
### findStartingLocations


def traversePath(matrix, startingPoint):
    direction = (0, 1)
    currentLocation = startingPoint
    letters = []
    stepCount = 0

    while True:
        stepCount += 1

        # Look down at the current square. If letter, record it.
        if matrix[currentLocation.y][currentLocation.x] not in [" ", "-", "|", "+"]:
            letters.append( matrix[currentLocation.y][currentLocation.x] )

        print "<<<<< \t L=" + str (currentLocation) + "\t  D=" + str (direction) + " \t S=" + str(stepCount) + " \t L=" + "".join(letters) + "\t >>>>>"

        # If we can still move in the current direction do so.
        nextPoint = currentLocation.applyDirection(direction)
        if not isValidPath(matrix, nextPoint):
            nextDir = findNewDirection(matrix, currentLocation, direction)

            # no where else to go. dead end or completed. simple case of completed for now.
            if nextDir is None:
                print "no valid direction found. completed the maze."
                return letters, stepCount
            else:
                print "turning: " + str(direction) + " -> " + str(nextDir)
                direction = nextDir
        
        nextPoint = currentLocation.applyDirection(direction)
        if isValidPath(matrix, nextPoint):
            currentLocation = nextPoint
        else:
            print "wha wha what?!!?! \t"  + currentLocation + " \t " + direction
### traversePath


def findNewDirection(matrix, currentLocation, currentDirection):
    directionsToTry = {
        (0,1):  [(1,0), (-1,0)],
        (0,-1): [(1,0), (-1,0)],
        (1,0):  [(0,1), (0,-1)],
        (-1,0): [(0,1), (0,-1)]
    }

    testDir = directionsToTry[currentDirection]
    print "findNewDir:  current=" + str(currentDirection) + "\t testDir=" + str(testDir)

    for d in testDir:
        if isValidPath(matrix, currentLocation.applyDirection(d)):
            return d

    return None
### findNewDirection


def isValidPath(matrix, point):
    # if the new point is not contained in the matrix, not a valid location
    if point.y < 0 or point.y >= len(matrix):
        return False

    if point.x < 0 or point.x >= len( matrix[0] ):
        return False

    return matrix[point.y][point.x] != " "
### isValidPath


###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################

inputFile = "input_19.txt"
# inputFile = "input_19_sample.txt"

matrix =  loadMap(inputFile)
points =  findStartingLocations(matrix)
letters, stepCount  = traversePath(matrix, points[0])

print ""
print "Solution to day 19 part 1: " + "".join(letters)


###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################


print ""
print "===== PART 2 ====="


print "Solution to day 19 part 2: " + str(stepCount)
