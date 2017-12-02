#!/bin/python
# -*- coding: utf-8 -*-
# http://adventofcode.com/2016/day/3

###################################################################################################################################################################
#  
#  Solution to day 3 part 1: 862
#  Solution to day 3 part 2: 1577
#
###################################################################################################################################################################


###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################

def isValidTriangle(a,b,c):
    return (a + b > c) and (b + c > a) and (a + c > b)



################################################################################################################################################################
########################################################################### PART 1 #############################################################################


valid = []
invalid = []


with open("part_1.data") as f:
    for line in f:
        parts = line.strip().split(" ")

        a = int(parts[0].strip())
        b = int(parts[1].strip())
        c = int(parts[2].strip())

        if isValidTriangle(a,b,c):
            valid.append(parts)
        else:
            invalid.append(parts)


print "Solution to day 3 part 1: " + str(len(valid))


################################################################################################################################################################
########################################################################### PART 2 #############################################################################


valid = []
invalid = []


with open("part_1.data") as f:
    try:
        while True:
            line1, line2, line3 = next(f), next(f), next(f)

            parts = line1.strip().split(" ")
            a1 = int(parts[0].strip())
            b1 = int(parts[1].strip())
            c1 = int(parts[2].strip())

            parts = line2.strip().split(" ")
            a2 = int(parts[0].strip())
            b2 = int(parts[1].strip())
            c2 = int(parts[2].strip())

            parts = line3.strip().split(" ")
            a3 = int(parts[0].strip())
            b3 = int(parts[1].strip())
            c3 = int(parts[2].strip())3

            if isValidTriangle(a1, a2, a3):
                valid.append(parts)
            else:
                invalid.append(parts)


            if isValidTriangle(b1, b2, b3):
                valid.append(parts)
            else:
                invalid.append(parts)

            if isValidTriangle(c1, c2, c3):
                valid.append(parts)
            else:
                invalid.append(parts)

    except:
        pass


print "Solution to day 3 part 2: " + str(len(valid))
