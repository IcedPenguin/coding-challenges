#!/bin/python
# -*- coding: utf-8 -*-
# http://adventofcode.com/2016/day/1

import re
import math

###################################################################################################################################################################
#  
#  Solution to day 1 part 2: 115
#  Solution to day 1 part 1: 273
#  
###################################################################################################################################################################

###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################

directions = "L5, R1, R3, L4, R3, R1, L3, L2, R3, L5, L1, L2, R5, L1, R5, R1, L4, R1, R3, L4, L1, R2, R5, R3, R1, R1, L1, R1, L1,   " \
             "L2, L1, R2, L5, L188, L4, R1, R4, L3, R47, R1, L1, R77, R5, L2, R1, L2, R4, L5, L1, R3, R187, L4, L3, L3, R2, L3, L5, " \
             "L4, L4, R1, R5, L4, L3, L3, L3, L2, L5, R1, L2, R5, L3, L4, R4, L5, R3, R4, L2, L1, L4, R1, L3, R1, R3, L2, R1, R4,   " \
             "R5, L3, R5, R3, L3, R4, L2, L5, L1, L1, R3, R1, L4, R3, R3, L2, R5, R4, R1, R3, L4, R3, R3, L2, L4, L5, R1, L4, L5,   " \
             "R4, L2, L1, L3, L3, L5, R3, L4, L3, R5, R4, R2, L4, R2, R3, L3, R4, L1, L3, R2, R1, R5, L4, L5, L5, R4, L5, L2, L4,   " \
             " R4, R4, R1, L3, L2, L4, R3"

compase = ["N", "E", "S", "W"]

traveled = { "N" : 0,
             "E" : 0, 
             "S" : 0,
             "W" : 0
            }

locations = []
part_2_solved = False

def massageDirecitons(directions):
    directions = re.sub(r"\s+", "", directions)
    steps = directions.split(",")
    return steps
### massageDirecitons


def splitDirection(step):
    return step[0], int(step[1:])
### splitDirection


def getHeading(heading, turn):
    idx = compase.index(heading)
    if turn == "L":
        idx -=1
    else:
        idx += 1

    return compase[idx % len(compase)]
### getHeading


def applyDistance(heading, distance):
    if distance >= 0:  # positive
        for i in xrange(distance):
            traveled[heading] += 1
            haveIBeenHereBefore( *getShortestDistance(False) )
    else: # negative
        for i in xrange(distance):
            traveled[heading] -= 1
            haveIBeenHereBefore( *getShortestDistance(False) )
### applyDistance


def getShortestDistance(absoluteValue):
    if absoluteValue:
        east_west = (int)(math.fabs(traveled["E"] - traveled["W"]))
        north_south = (int)(math.fabs(traveled["N"] - traveled["S"]))
    else:
        east_west = traveled["E"] - traveled["W"]
        north_south = traveled["N"] - traveled["S"]

    return east_west, north_south
### getShortestDistance


def haveIBeenHereBefore(east_west, north_south):
    global part_2_solved

    if not part_2_solved:
        point = (east_west, north_south)
        if point in locations:
            print "Solution to day 1 part 2: " + str(east_west + north_south)
            part_2_solved = True
        else:
            locations.append(point)
### haveIBeenHereBefore

def main():
    heading = "N"
    steps = massageDirecitons(directions)
    haveIBeenHereBefore(0, 0)


    for step in steps: 
        turn, distance = splitDirection(step)
        heading = getHeading(heading, turn)
        applyDistance(heading, distance)

    print "Solution to day 1 part 1: " + str(sum(getShortestDistance(True)))
### main


if __name__ == "__main__":
    main()
