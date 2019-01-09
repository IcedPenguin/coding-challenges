#!/bin/python
# -*- coding: utf-8 -*-
# http://adventofcode.com/2015/day/2

###################################################################################################################################################################
#  
#  Solution to day 2 part 1: 1588178
#  Solution to day 2 part 2: 3783758
#
###################################################################################################################################################################

def loadPresentSizes(inputFile):
    presents = []

    with open(inputFile) as f:
        content = f.readlines()
        
    for line in content:
        parts = line.strip().split("x")
        presents.append( (int(parts[0]), int(parts[1]), int(parts[2])) )

    return presents
### loadPresentSizes

def processPresents(presents):
    totalPaper = 0
    totalRibbon = 0

    for p in presents:
        totalPaper += calculateWrappingPaperForPresent(p)
        totalRibbon += calculateRibbingForPresent(p)

    return totalPaper, totalRibbon
### getSquareFeetOfWrappingPaperForPresent


def calculateWrappingPaperForPresent(present):
    l = present[0]
    w = present[1]
    h = present[2]

    a = l*w
    b = w*h
    c = h*l

    m = min(a, b, c)
    
    return 2*a + 2*b + 2*c + m
###


def calculateRibbingForPresent(present):
    l = present[0]
    w = present[1]
    h = present[2]

    smallestParemeter = min(
        2*l + 2*w,
        2*w + 2*h,
        2*h + 2*l
    )

    volume = l*w*h

    return smallestParemeter + volume
### calculateRibbingForPresent

###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################


print "===== PART 1 ====="

inputFile = "input_2.txt"



presents = loadPresentSizes(inputFile)
totalPaper, totalRibbon = processPresents(presents)

print ""
print "Solution to day 2 part 1: " + str(totalPaper)


###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################


print ""
print "===== PART 2 ====="
print "Solution to day 2 part 2: " + str(totalRibbon)

