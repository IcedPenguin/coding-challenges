#!/bin/python
# -*- coding: utf-8 -*-
# http://adventofcode.com/2017/day/22

import re


###################################################################################################################################################################
#  
#  Solution to day 22 part 1: 5339
#  Solution to day 22 part 2: 2512380
#
###################################################################################################################################################################
CLEAN = "."
INFECTED = "#"
WEAKENED = "W"
FLAGGED = "F"

direction = {
    # Clean direction selector
    (CLEAN,  0,  1): ( 1,  0),
    (CLEAN,  0, -1): (-1,  0),
    (CLEAN,  1,  0): ( 0, -1),
    (CLEAN, -1,  0): ( 0,  1),

    # Infected direction selector
    (INFECTED,  0,  1): (-1,  0),
    (INFECTED,  0, -1): ( 1,  0),
    (INFECTED,  1,  0): ( 0,  1),
    (INFECTED, -1,  0): ( 0, -1),
}

evolvedDirection = {
    # Clean - turn left
    (CLEAN,  0,  1): ( 1,  0),
    (CLEAN,  0, -1): (-1,  0),
    (CLEAN,  1,  0): ( 0, -1),
    (CLEAN, -1,  0): ( 0,  1),

    # Weakened - stay in same direction
    (WEAKENED,  0,  1): ( 0,  1),
    (WEAKENED,  0, -1): ( 0, -1),
    (WEAKENED,  1,  0): ( 1,  0),
    (WEAKENED, -1,  0): (-1,  0),
    
    # Infected - turn right
    (INFECTED,  0,  1): (-1,  0),
    (INFECTED,  0, -1): ( 1,  0),
    (INFECTED,  1,  0): ( 0,  1),
    (INFECTED, -1,  0): ( 0, -1),

    # Flagged - reverse
    (FLAGGED,  0,  1): ( 0, -1),
    (FLAGGED,  0, -1): ( 0,  1),
    (FLAGGED,  1,  0): (-1,  0),
    (FLAGGED, -1,  0): ( 1,  0),
}



class VirusCarrier(object):
    def __init__(self, grid):
        self.infectionCount = 0
        self.cleanedCount = 0
        self.weakenedCount = 0
        self.flaggedCount = 0

        self.direction = (0, -1)
        self.grid = grid

        self.x = len(grid) / 2
        self.y = len(grid) / 2
    ### __init__


    def burst(self):
        currentNodeState = self.grid[self.y][self.x]
        # print "BURST START: x=%s y=%s node=%s direction=%s" % (self.x, self.y, currentNodeState, self.direction)

        ####################################
        # determine new direction
        ####################################
        self.direction = direction[(currentNodeState, self.direction[0], self.direction[1])]


        ####################################
        # determine new state of current node
        ####################################
        if currentNodeState == CLEAN:
            self.grid[self.y][self.x] = INFECTED
            self.infectionCount += 1
            newState = INFECTED
        else:
            self.grid[self.y][self.x] = CLEAN
            self.cleanedCount += 1
            newState = CLEAN
    
        ####################################
        # move to next node
        ####################################
        self.x += self.direction[0]
        self.y += self.direction[1]

        # print "BURST END:   x=%s y=%s nod∆=%s direction=%s" % (self.x, self.y, newState, self.direction)
    ### burst


    def evolvedBurst(self):
        currentNodeState = self.grid[self.y][self.x]

        ####################################
        # determine new direction
        ####################################
        self.direction = evolvedDirection[(currentNodeState, self.direction[0], self.direction[1])]


        ####################################
        # determine new state of current node
        ####################################
        if currentNodeState == CLEAN:
            # *   Clean nodes become weakened.
            self.grid[self.y][self.x] = WEAKENED
            self.weakenedCount += 1
            newState = WEAKENED
            
        elif currentNodeState == WEAKENED:
            # *   Weakened nodes become infected.
            self.grid[self.y][self.x] = INFECTED
            self.infectionCount += 1
            newState = INFECTED
            
        elif currentNodeState == INFECTED:
            # *   Infected nodes become flagged.
            self.grid[self.y][self.x] = FLAGGED
            self.flaggedCount += 1
            newState = FLAGGED

        elif currentNodeState == FLAGGED:
            # *   Flagged nodes become clean.
            self.grid[self.y][self.x] = CLEAN
            self.cleanedCount += 1
            newState = CLEAN
            
        ####################################
        # move to next node
        ####################################
        self.x += self.direction[0]
        self.y += self.direction[1]
    ### evolvedBurst


    def printMatrix(self):
        s = ""
        sideLength = len(self.grid)
        for i in xrange(sideLength):
            for j in xrange(sideLength):
                s += self.grid[i][j]
                if self.x == j and self.y == i:
                    s += "←"
                else:
                    s += " "

            s += "\n"
        print s
    ### printMatrix

### VirusCarrier


def loadGridContents(gridFile):
    grid = []    

    with open(gridFile) as f:
        for line in f:
            line = line.strip()
            l = list(line)
            grid.append(l)

    return grid
### loadMap


def expandGrid(grid):
    # Assumption, the grid is a square
    width = len(grid[0])
    height = len(grid)

    print "Grid expansion: %s x %s  to  %s x %s" % (width, width, width*3, width*3)

    if width != height:
        raise "Error"

    newWidth = 3 * width
    newHeight = 3 * height

    newGrid = []
    for i in xrange(newHeight):
        row = [CLEAN] * newWidth
        if i >= height and i < height *2:
            row = row[:width] + grid[i-width] + row[width*2:]

        newGrid.append(row)

    return newGrid
### expandGrid


###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################

inputFile = "input_22.txt"

grid = loadGridContents(inputFile)
grid = expandGrid(grid)
grid = expandGrid(grid)
grid = expandGrid(grid)
grid = expandGrid(grid)
grid = expandGrid(grid)
grid = expandGrid(grid)

virus = VirusCarrier(grid)

for i in xrange(10000):
    virus.burst()

print ""
print "Solution to day 22 part 1: " + str( virus.infectionCount )


###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################


print ""
print "===== PART 2 ====="

inputFile = "input_22.txt"

grid = loadGridContents(inputFile)
grid = expandGrid(grid)
grid = expandGrid(grid)
grid = expandGrid(grid)
grid = expandGrid(grid)
grid = expandGrid(grid)
grid = expandGrid(grid)

virus = VirusCarrier(grid)

for i in xrange(10000000):
    
    if i % 500000 == 0:
        print i

    virus.evolvedBurst()


print "Solution to day 22 part 2: " + str( virus.infectionCount )

