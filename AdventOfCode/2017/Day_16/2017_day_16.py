#!/bin/python
# -*- coding: utf-8 -*-
# http://adventofcode.com/2017/day/16

import re

###################################################################################################################################################################
#  
#  Solution to day 16 part 1: kbednhopmfcjilag
#  Solution to day 16 part 2: fbmcgdnjakpioelh
#
###################################################################################################################################################################


# Spin, written sX, makes X programs move from the end to the front, but maintain their 
# order otherwise. (For example, s3 on abcde produces cdeab).
def spin(danceLine, X):
    X = len(danceLine) - X
    danceLine = danceLine[X:] + danceLine[:X]
    return danceLine
### spin


# Exchange, written xA/B, makes the programs at positions A and B swap places.
def exchange(danceLine, A, B):
    tmp = danceLine[A]
    danceLine[A] = danceLine[B]
    danceLine[B] = tmp

    return danceLine
### exchange

# Partner, written pA/B, makes the programs named A and B swap places.
def partner(danceLine, A, B):
    idxA = danceLine.index(A)
    idxB = danceLine.index(B)

    return exchange(danceLine, idxA, idxB)
### partner


def performDance(danceInstructionFile, danceLine):
    originalDanceLine = list(danceLine)

    regex = re.compile("([a-z])([0-9a-z]+)(/)([0-9a-z]+)")
    danceLine = list(danceLine)

    with open(danceInstructionFile) as f:
        for line in f:
            if line[0] == "s":
                danceLine = spin(danceLine, int(line[1:]))
                continue

            parts = regex.split(line.strip())
            move = parts[1]
            A = parts[2]
            B = parts[4]

            if move == "x":
                danceLine = exchange(danceLine, int(A), int(B))

            elif move == "p":
                danceLine = partner(danceLine, A, B)

    return danceLine
### performDance


def findCycle(danceInstructionFile, danceLine):
    permutations = [list(danceLine)]

    while True:
        danceLine = performDance(danceInstructionFile, danceLine)
        if danceLine in permutations:
            return permutations
        else:
            permutations.append(danceLine)

    return permutations
### findCycle


def findPaternAfterIteration(cycles, iterations):
    idx = iterations % len(cycles)
    return cycles[idx]
### findPaternAfterIteration


###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################

inputFile = "input_16.txt"
danceLine = "abcdefghijklmnop"

# inputFile = "input_16_sample.txt"
# danceLine = "abcde"

danceLine = performDance(inputFile, danceLine)

print ""
print "Solution to day 16 part 1: " + "".join(danceLine)


###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################
#
# Thoughts on part 2
# 1) We already have an algorith for completing a dance. Simply brute-force the 1 billion dances to get the
#    final state. That's probably going to take forever... yep. Looks like a run time of several hours. I 
#    can do better. 
#
# 2) Create a mapping of starting and ending positions for each dancer for a single round. Brute force the
#    solution, only skip perform the steps one-by-one and simply move the dancers to their final position.
#    Hmm, run time is down to a little less than an hour (guestimating). I can do better.
#
# 3) Test for cylces in dance positions. If we see the same position twice, then we can mod out the vast
#    majority of the dance steps. Is there a cycle... yes! Run time, seconds. ^_^
#

print ""
print "===== PART 2 ====="

danceLine = "abcdefghijklmnop"
permutations = findCycle(inputFile, danceLine)
danceLine = findPaternAfterIteration(permutations, 1000000000)

print "Solution to day 16 part 2: " + "".join(danceLine)
