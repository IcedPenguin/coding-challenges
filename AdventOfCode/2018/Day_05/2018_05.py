#!/bin/python
# -*- coding: utf-8 -*-
# https://adventofcode.com/2018/day/5


###################################################################################################################################################################
#  
#  Solution to day 5 part 1: 11118
#  Solution to day 5 part 2: 6948
#
###################################################################################################################################################################

import string
import sys

###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################

# input_file = "2018_05_1_sample_1.txt"
input_file = "2018_05_input.txt"

def reducePolymer(polymer):
    # print "-------"
    # print "Initial Length: %s" % (len(polymer))
    # if len(polymer) < 20:
    #     print polymer
    

    reducedPolymer = polymer
    reductionOccurred = True
    while reductionOccurred:
        reductionOccurred, reducedPolymer = reductionPass(reducedPolymer)

    # print "Final Length: %s" % (len(reducedPolymer))
    # print reducedPolymer
 
    return reducedPolymer
### reducePolymer


def reductionPass(polymer):
    reductionOccurred = False
    i = 0

    while len(polymer) >= 2 and i < len(polymer) -1: 
        a = polymer[i]
        b = polymer[i+1]

        if a != b and a.lower() == b.lower():
            # print " >reduction<"
            polymer = polymer[:i] + polymer[i+2:]
            reductionOccurred = True
        else:   
            i += 1

    return reductionOccurred, polymer
### reductionPass


suitPolymer = "dabAcCaCBAcCcaDA"
with open(input_file) as f:
    for line in f:
        suitPolymer = line



reducedPolymer = reducePolymer(suitPolymer)



print "Solution to day 5 part 1: " + str( len(reducedPolymer) )


###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################



def findUnitToRemoveAndThenReduce(polymer):
    letterToRemove = ""
    bestPolymer = ""
    bestLength = sys.maxint
    # all of the polymers are letters...
    for letter in string.ascii_lowercase:
        print "Testing: %s" % (letter)

        testPolymer = polymer
        testPolymer = testPolymer.replace(letter, "")
        testPolymer = testPolymer.replace(letter.upper(), "")

        reducedPolymer = reducePolymer(testPolymer)

        if len(reducedPolymer) < bestLength:
            letterToRemove = letter
            bestPolymer = reducedPolymer
            bestLength = len(reducedPolymer)

    return bestPolymer
### findUnitToRemoveAndThenReduce

reducedPolymer = findUnitToRemoveAndThenReduce(suitPolymer)

print "Solution to day 5 part 2: " + str( len(reducedPolymer) )
