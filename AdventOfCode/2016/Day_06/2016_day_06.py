#!/bin/python
# -*- coding: utf-8 -*-
# http://adventofcode.com/2016/day/6


###################################################################################################################################################################
#  
#  Solution to day 6 part 1: qtbjqiuq
#  Solution to day 6 part 2: akothqli
#
###################################################################################################################################################################

import hashlib
import operator

################################################################################################################################################################
########################################################################### PART 1 #############################################################################

def processLine(frequencyDict, line):
    line = line.strip()
    for idx in xrange(len(line)):
        letter = line[idx]
        positionDict = None

        # ensure there is a 
        if idx not in frequencyDict:
            positionDict = {}
            frequencyDict[idx] = positionDict
        else:
            positionDict = frequencyDict[idx]

        # update the letter count in the dictionary
        if letter in positionDict:
            positionDict[letter] = positionDict[letter] + 1
        else:
            positionDict[letter] = 1
### processLine


def extractPassword(algorithm, frequencyDict):
    password = ""
    for idx in xrange(len(frequencyDict)):
        # print frequencyDict[idx]
        if algorithm ==1:
            value = max(frequencyDict[idx].iteritems(), key=operator.itemgetter(1))[0]
        elif algorithm ==2:
            value = min(frequencyDict[idx].iteritems(), key=operator.itemgetter(1))[0]
        # print value
        password += value

    return password
### extractPassword


inputFile = "part_1_sample.txt"
inputFile = "part_1.txt"
freq = {}


with open(inputFile) as f:
    for line in f:
        processLine(freq, line)
        
password = extractPassword(1, freq)
print "Solution to day 6 part 1: " + password


################################################################################################################################################################
########################################################################### PART 2 #############################################################################


password = extractPassword(2, freq)
print "Solution to day 6 part 2: " + password

