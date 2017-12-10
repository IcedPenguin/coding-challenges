#!/bin/python
# -*- coding: utf-8 -*-
# http://adventofcode.com/2017/day/10


###################################################################################################################################################################
#  
#  Solution to day 10 part 1: 23715
#  Solution to day 10 part 2: 541dc3180fd4b72881e39cf925a50253
#
###################################################################################################################################################################


def getFreshRope(length):
    rope = []
    for i in xrange(arraySize):
        rope.append(i)
    return rope
### getFreshRope


def reversePortionOfRope(rope, position, length):
    ropeLen = len(rope)
    double = rope + rope
    section = double[position:position + length]
    section = section[::-1]

    for i in xrange(len(section)):
        rope[(position + i) % ropeLen] = section[i]

    return rope
### reversePortionOfRope


def getNextPosition(arraySize, currentPosition, length, skipSize):
    nextIndex = currentPosition + length + skipSize
    nextIndex %= arraySize
    skipSize += 1
    return nextIndex, skipSize
### getNextPosition


def convertSparseHashToDenseHash(rope):
    output = []
    for b in xrange(16):
        h = 0
        for i in xrange(16):
            h ^= rope[b*16 + i]

        output.append( format(h, '#04x')[2:] )
    output = "".join(output)
    return output
### convertSparseHashToDenseHash


def performKnotHasing(rope, rounds, inputLengths):
    length = 0
    position = 0
    skipSize = 0

    # perform the rounds
    for i in xrange(rounds):
        for part in inputLengths:
            if type(part) == str:
                length = int(part.strip())
            else:
                length = part
            rope = reversePortionOfRope(rope, position, length)
            position, skipSize = getNextPosition(arraySize, position, length, skipSize)

    # encode the output hash
    return convertSparseHashToDenseHash(rope)
### performKnotHasing


###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################

# arraySize = 5
# inputFile = "input_10_sample.txt"

arraySize = 256
inputFile = "input_10.txt"

position = 0
skipSize = 0
rope = getFreshRope(arraySize)

with open(inputFile) as f:
    for line in f:
        parts = line.split(",")
        performKnotHasing(rope, 1, parts)

print ""    
print "===== Solution ====="
print "Solution to day 10 part 1: " + str(rope[0] * rope[1])

###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################


def convertAsciiToLengths(inputAscii):
    lengths = []

    for character in inputAscii:
        lengths.append(ord(character))

    # append standard post-fix
    lengths += [17, 31, 73, 47, 23]

    return lengths
### convertAsciiToLengths


asciiTestCases = [
    ("",            "a2582a3a0e66e6e86e3812dcb672a272"),
    ("AoC 2017",    "33efeb34ea91902bb2f59c9920caa6cd"),
    ("1,2,3",       "3efbe78a8d82f29979031a4aa0b16a9d"),
    ("1,2,4",       "63960835bcdc130f0b66d7ff4f6a5a8e")
]


for testCase in asciiTestCases:
    case = testCase[0]
    expected = testCase[1]
    rope = getFreshRope(arraySize)

    inputLengths = convertAsciiToLengths(case)
    knotHash = performKnotHasing(rope, 64, inputLengths)
    
    if knotHash == expected:
        print "PASS: %s" % (case)
    else:
        print "FAIL FAIL FAIL: \nexected: %s   \n actual: %s" % (expected, knotHash)


rope = getFreshRope(arraySize)
with open(inputFile) as f:
    for line in f:
        inputLengths = convertAsciiToLengths(line)
        knotHash = performKnotHasing(rope, 64, inputLengths)

print "Solution to day 10 part 2: " + knotHash
