#!/bin/python
# -*- coding: utf-8 -*-
# http://adventofcode.com/2017/day/2


###################################################################################################################################################################
#  
#  Solution to day 2 part 1: 37923
#  Solution to day 2 part 2: 263
#
###################################################################################################################################################################


###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################

# input_file = "part_1_sample_input.txt"
input_file = "part_1.txt"

checksum = 0

def getLineChecksum(line):
    numbers = line.strip().split(" ")
    numbers = map(int, numbers)
    numbers.sort()
    return int(numbers[-1]) - int(numbers[0])

with open(input_file) as f:
    for line in f:
        checksum += getLineChecksum(line)

print "Solution to day 2 part 1: " + str(checksum)


###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################

# input_file = "part_2_sample_input.txt"

checksum = 0

def findEvenlyDivisibleNumbers(line):
    numbers = line.strip().split(" ")
    numbers = map(int, numbers)
    numbers.sort(reverse=True)
    
    for idx in xrange(len(numbers)):
        for n in xrange(idx+1, len(numbers)):

            resultFloat = (numbers[idx] * 1.0) / (numbers[n] * 1.0)
            resultInt = numbers[idx] / numbers[n]

            if resultFloat == resultInt:
                return resultInt
    return 0

with open(input_file) as f:
    for line in f:
        checksum += findEvenlyDivisibleNumbers(line)

print "Solution to day 2 part 2: " + str(checksum)


