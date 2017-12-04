#!/bin/python
# -*- coding: utf-8 -*-
# http://adventofcode.com/2017/day/4


###################################################################################################################################################################
#  
#  Solution to day 4 part 1: 451
#  Solution to day 4 part 2: 223
#
###################################################################################################################################################################


###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################

def isPasswordPhraseValid(phrase):
    unique = {}
    anagrams = {}
    parts = phrase.split()
    for p in parts:
        unique[p] = 1

        p = ''.join(sorted(p))
        anagrams[p] = 1


    noRepeats = len(unique) == len(parts)
    noAnagrams = len(anagrams) == len(parts)
    return noRepeats, noAnagrams
###

input_file = "input.txt"

validCount = 0
nonAnagramCount = 0
with open(input_file) as f:
    for line in f:
        noRepeats, noAnagrams = isPasswordPhraseValid(line)
        if noRepeats:
            validCount += 1

        if noAnagrams:
            nonAnagramCount += 1

print "Solution to day 4 part 1: " + str(validCount)


###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################


print "Solution to day 4 part 2: " + str(nonAnagramCount)

