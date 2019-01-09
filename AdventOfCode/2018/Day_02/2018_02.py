#!/bin/python
# -*- coding: utf-8 -*-
# https://adventofcode.com/2018/day/2


###################################################################################################################################################################
#  
#  Solution to day 2 part 1: 5928
#  Solution to day 2 part 2: bqlporuexkwzyabnmgjqctvfs
#
###################################################################################################################################################################


###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################

# input_file = "2018_02_1_sample_1.txt"
input_file = "2018_02_input.txt"

idsWithLetterAppearsExactlyTwoTimesCount = 0
idsWithLetterAppearsExactlyThreeTimesCount = 0


def processId(input):
    global idsWithLetterAppearsExactlyTwoTimesCount
    global idsWithLetterAppearsExactlyThreeTimesCount

    letters = {}

    for letter in input:
        if letter in letters:
            letters[letter] += 1

        else:
            letters[letter] = 1

    # look for 
    doubleFound = False
    tripleFound = False

    for key in letters:
        if letters[key] == 2 and not doubleFound:
            doubleFound = True
            idsWithLetterAppearsExactlyTwoTimesCount += 1

        if letters[key] == 3 and not tripleFound:
            tripleFound = True
            idsWithLetterAppearsExactlyThreeTimesCount += 1
### processId


with open(input_file) as f:
    
    for line in f:
        processId(line.strip())

print "Solution to day 2 part 1: " + str( idsWithLetterAppearsExactlyTwoTimesCount * idsWithLetterAppearsExactlyThreeTimesCount)



###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################


# input_file = "2018_02_2_sample_1.txt"
input_file = "2018_02_input.txt"

def processListOfIds(ids):
    length = len(ids)
    solution = None

    for i in xrange(0, length):
        for j in xrange(0, length):
            if i != j:
                if 1 == countLetterDifferences(ids[i], ids[j]):
                    return dropDiferentLetters(ids[i], ids[j])
                    
    return None
### processListOfIds


def countLetterDifferences(one, two):
    diff = 0

    for i in xrange(0, len(one)):
        if one[i] != two[i]:
            diff += 1

    return diff
### countLetterDifferences


def dropDiferentLetters(one, two):
    for i in xrange(0, len(one)):
        if one[i] != two[i]:
            one = one[:i] + one[i+1:]
            return one

    return None
### dropDiferentLetters


ids = []

with open(input_file) as f:    
    for line in f:
        ids.append( line.strip() )

solution = processListOfIds(ids)

print "Solution to day 2 part 2: " + str(solution)
