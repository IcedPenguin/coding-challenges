#!/bin/python
# -*- coding: utf-8 -*-
# http://adventofcode.com/2016/day/5


###################################################################################################################################################################
#  
#  Solution to day 5 part 1: 801b56a7
#  Solution to day 5 part 2: 424a0197
#
###################################################################################################################################################################

import hashlib

################################################################################################################################################################
########################################################################### PART 1 #############################################################################

def findNextHashWithLeadingZeros(door, index, zeroCount):
    leadingZeros = "0" * zeroCount

    while True:
        # So we can see progress is being made.
        if index % 1000000 == 0:
            print "idx: " + str(index)

        m = hashlib.md5()
        m.update(door + str(index))
        digest = m.hexdigest()

        if digest.startswith(leadingZeros):
            return index, digest
        else:
            index += 1
### findNextHashWithLeadingZeros


def buildPasswordPart1(partialPassword, digest, leadingZeros):
    partialPassword += digest[leadingZeros]
    return partialPassword
### buildPasswordPart1    


key = "abbhdwsy"
index = 0
password = ""
leadingZeros = 5
sizeOfPassword = 8

for x in xrange(sizeOfPassword):
    index, digest = findNextHashWithLeadingZeros(key, index, leadingZeros)
    password = buildPasswordPart1(password, digest, leadingZeros)
    index += 1

print "Solution to day 5 part 1: " + password


################################################################################################################################################################
########################################################################### PART 2 #############################################################################

key = "abbhdwsy"
index = 0
validIndices = "01234567"
passwordTwo = "?" * sizeOfPassword


def buildPasswordPart2(partialPassword, digest, leadingZeros):
    index = digest[leadingZeros]
    value = digest[leadingZeros +1]

    if index not in validIndices:
        return partialPassword, True

    index = int(index)

    # print "hash: " + digest + "\tindex: " + str(index) + "\tvalue:" + str(value)
    if partialPassword[index] == "?":
        partialPassword = partialPassword[:index] + value + partialPassword[index +1:]
        print partialPassword
    else:
        print "ignoring repeat position: " + str(index)

    return partialPassword, "?" in partialPassword
### buildPasswordPart1    


running = True
while running:
    index, digest = findNextHashWithLeadingZeros(key, index, leadingZeros)
    passwordTwo, running = buildPasswordPart2(passwordTwo, digest, leadingZeros)
    index += 1

print "Solution to day 5 part 2: " + passwordTwo

