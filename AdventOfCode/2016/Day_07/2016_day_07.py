#!/bin/python
# -*- coding: utf-8 -*-
# http://adventofcode.com/2016/day/7


###################################################################################################################################################################
#  
#  Solution to day 7 part 1: 105
#  Solution to day 7 part 2: 258
#
###################################################################################################################################################################

def supportsTls(address):
    supported = False
    i = 0
    insideSquareBracket = False
    while i <= len(address) -4:
        # look for start of hypernet
        if address[i] == "[":
            insideSquareBracket = True

        # look for end of hypernet
        elif insideSquareBracket:
            if address[i] == "]":
                insideSquareBracket = False

            # Autonomous Bridge Bypass Annotation inside of hypernet, not supported
            elif address[i] == address[i+3] and address[i+1] == address [i+2] and address[i] != address[i+1]:
                return False

        # Autonomous Bridge Bypass Annotation outside of hypernet, allowed.
        elif address[i] == address[i+3] and address[i+1] == address [i+2] and address[i] != address[i+1]:
            supported = True

        i += 1

    return supported
### supportsTls


def supportsSsl(address):
    supported = False
    i = 0
    insideSquareBracket = False

    areaBroadcastAccessor = []
    byteAllocationBlock = []

    while i <= len(address) -3:
        if insideSquareBracket == False:
            # detect the start of a hypernet region, and skip to the inside.
            if address[i] == "[":
                insideSquareBracket = True

            elif address[i+1] == "[":
                insideSquareBracket = True
                i += 1                

            elif address[i+2] == "[":
                insideSquareBracket = True
                i += 2

            # not starting a hypernet. do processing.
            elif address[i] == address[i+2] and address[i] != address[i+1]:
                areaBroadcastAccessor.append(address[i:i+2]) # save the first 2 letters

        elif insideSquareBracket == True:
            # detect the end of a hypernet region, and skip to the outside
            if address[i] == "]":
                insideSquareBracket = False

            elif address[i+1] == "]":
                insideSquareBracket = False
                i += 1                

            elif address[i+2] == "]":
                insideSquareBracket = False
                i += 2

            # not leaving a hypernet. do processing.
            elif address[i] == address[i+2] and address[i] != address[i+1]:
                byteAllocationBlock.append(address[i+1:i+3]) # save the last two letters

        i += 1

    return len(set(areaBroadcastAccessor).intersection(byteAllocationBlock)) > 0
### supportsSsl

###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################

tlsSupportTestCases = [
    ("", False),
    ("abba", True),
    ("abcd", False),
    ("abba[mnop]qrst", True),
    ("abcd[bddb]xyyx", False),
    ("aaaa[qwer]tyui", False),
    ("ioxxoj[asdfgh]zxcvbn", True),
    ("abba[abba]abba", False),
]

sslSupportTestCases = [
    ("aba[bab]xyz", True), 
    ("xyx[xyx]xyx", False),
    ("aaa[kek]eke", True),
    ("zazbz[bzb]cdb", True),
]

print "===== Test TLS Support ====="
for testCase in tlsSupportTestCases:
    address = testCase[0]
    supported = supportsTls(address)
    print "expected: " + str(testCase[1]) + "\tactual: " + str(supported)


print "===== Test SSL Support ====="
for testCase in sslSupportTestCases:
    address = testCase[0]
    supported = supportsSsl(address)
    print "expected: " + str(testCase[1]) + "\tactual: " + str(supported)



input_file = "input_7.txt"

tlsSupportedCount = 0
sslSupportedCount = 0
with open(input_file) as f:
    for line in f:
        result = supportsTls(line)
        if result:
            tlsSupportedCount += 1

        result = supportsSsl(line)
        if result:
            sslSupportedCount += 1

print ""    
print "===== Solution ====="
print "Solution to day 7 part 1: " + str(tlsSupportedCount)

###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################

print "Solution to day 7 part 2: " + str(sslSupportedCount)

