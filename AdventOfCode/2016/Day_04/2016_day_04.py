#!/bin/python
# -*- coding: utf-8 -*-
# http://adventofcode.com/2016/day/4
# https://pythex.org/

###################################################################################################################################################################
#  
#  Solution to day 4 part 1: 361724
#  Solution to day 4 part 2: 482
#
###################################################################################################################################################################

import re
import operator

###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################

def extractRoomNameComponets(room):
    room = re.sub(r"\s+", "", room)
    # room = re.sub("-", "", room)
    parts = re.compile("([a-z\-]+)([0-9]+)(\[)([a-z]+)(\])").split(room.strip())
    return parts[1], parts[2], parts[4]
### extractRoomNameComponets


def getChecksumFromLetters(letters):
    # count number of letters
    letterFreq = {}
    for letter in letters:
        if letter == "-":
            pass
        elif letter in letterFreq:
            letterFreq[letter] = letterFreq[letter] +1
        else:
            letterFreq[letter] = 1
    
    # build structure to hold count and letter
    # sort structure
    sorted_x = sorted(sorted(letterFreq.items(), key = lambda x : x[0]), key = lambda x : x[1], reverse = True)

    # build the checksum
    checksum = ""
    for idx in xrange(5):
        checksum += sorted_x[idx][0]

    return checksum
### getChecksumFromLetters


def decryptName(name, sectorId):
    shift = int(sectorId) % 26

    decrypted = ""
    for letter in name:
        if letter == "-":
            decrypted += " "
        else:
            num = ord(letter)
            num += shift
            if num > ord('z'):
                num -= 26

            decrypted += chr(num)
    return decrypted
### decryptedName


################################################################################################################################################################
########################################################################### PART 1 #############################################################################


# input_file = "part_1_sample.txt"
input_file = "part_1.txt"

sectorSum = 0

with open(input_file) as f:
    for line in f:
        letters, sectorId, checksumExpected = extractRoomNameComponets(line)
        checksumActual = getChecksumFromLetters(letters)

        if checksumActual == checksumExpected:
            sectorSum += int(sectorId)

print "Solution to day 4 part 1: " + str(sectorSum)


################################################################################################################################################################
########################################################################### PART 2 #############################################################################


# input_file = "part_2_sample.txt"
input_file = "part_1.txt"

with open(input_file) as f:
    for line in f:
        letters, sectorId, checksumExpected = extractRoomNameComponets(line)

        name = decryptName(letters, sectorId)

        if "north" in name:
            print "Solution to day 4 part 1: " + str(sectorId)

