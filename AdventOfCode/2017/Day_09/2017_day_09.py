#!/bin/python
# -*- coding: utf-8 -*-
# http://adventofcode.com/2017/day/9

import re

###################################################################################################################################################################
#  
#  Solution to day 9 part 1: 8337
#  Solution to day 9 part 2: 4330
#
###################################################################################################################################################################

def filterOutGarbage(stream):
    i = 0
    garbageCount = 0
    startOfGarbage = -1
    garbageRemovedCount = 0
    while i < len(stream):
        # we are searching for the starting location of a garbage patch
        if startOfGarbage == -1:
            if stream[i] == "<":
                startOfGarbage = i

        # we are currently inside garbage... looking for the end
        else:
            # if we hid an escaped character, jump ahead one
            if stream[i] == "!":
                i += 1

            # we have found the closing character
            elif stream[i] == ">":
                garbageCount += 1
                stream = stream[:startOfGarbage] + stream[i+1:]
                i = max(0, startOfGarbage -1)
                startOfGarbage = -1
                continue

            else: 
                garbageRemovedCount += 1

        # move on to the next character
        i += 1

    return stream, garbageRemovedCount
### filterOutGarbage


def scoreGroups(depth, groups):
    if len(groups) == 0:
        return depth

    if groups[0] != "{" or groups[-1] != "}":
        print "invalid start or stop character"
        print groups[0]
        print groups[-1]
        return -1

    children = getChildrenOfGroup(groups[1:-1])

    score = depth
    for child in children:
        score += scoreGroups(depth +1, child)

    return score
### scoreGroups


def getChildrenOfGroup(group):
    childrenFound = []
    i = 0

    startIndex = -1
    curlyBracketsToIgnore = 0
    while i < len(group):
        # look for start of group
        if group[i] == "{" and startIndex == -1:
            startIndex = i 

        # count sub-opens
        elif group[i] == "{":
            curlyBracketsToIgnore += 1

        # count sub-closes
        elif group[i] == "}" and curlyBracketsToIgnore > 0:
            curlyBracketsToIgnore -= 1

        # look for real close
        elif group[i] == "}":
            childrenFound.append(group[startIndex:i+1])
            startIndex = -1

        i += 1

    return childrenFound
### getChildrenOfGroup


###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################

gargabeTestCases = [
    ("<>", ""),
    ("<random characters>", ""),
    ("<<<<>", ""),
    ("<{!>}>", ""),
    ("<!!>", ""),
    ("<!!!>>", ""),
    ("<<<<> <!!!>> <{!>}>", "  ")
]

groupsTestCases = [
    ("{}", 1),
    ("{{}}", 3),
    ("{{{}}}", 6), 
    ("{{},{}}", 5), 
    ("{{{},{},{{}}}}", 16), 
    ("{<a>,<a>,<a>,<a>}", 1), 
    ("{{<ab>},{<ab>},{<ab>},{<ab>}}", 9),
    ("{{<!!>},{<!!>},{<!!>},{<!!>}}", 9),
    ("{{<a!>},{<a!>},{<a!>},{<ab>}}", 3)
]

garbageCountTestCases = [
    ("<>", 0),
    ("<random characters>", 17),
    ("<<<<>", 3),
    ("<{!>}>", 2),
    ("<!!>", 0), 
    ("<!!!>>", 0),
    ("<{o\"i!a,<{i<a>", 10)
]


print "===== Test Garbage Removal ====="
for g in gargabeTestCases:
    line = g[0]
    line, garbageRemoved =  filterOutGarbage(line)
    print "expected: " + str(len(g[1])) + "\tactual: " + str(len(line))


print "===== Test Group Identification and Scoring ====="
for g in groupsTestCases:
    line = g[0]
    line, garbageRemoved = filterOutGarbage(line)
    score = scoreGroups(1, line)
    print "expected: " + str(g[1]) + "\tactual: " + str(score)


print "===== Test Garbage Character Counting ====="
for g in garbageCountTestCases:
    line = g[0]
    line, garbageRemoved = filterOutGarbage(line)
    score = scoreGroups(1, line)
    print "expected: " + str(g[1]) + "\tactual: " + str(garbageRemoved)


input_file = "input_9.txt"
score = 0
garbageRemoved = 0
with open(input_file) as f:
    for line in f:
        line, garbageRemoved = filterOutGarbage(line)
        score = scoreGroups(1, line)


print "Solution to day 9 part 1: " + str(score)

###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################

print "Solution to day 9 part 2: " + str(garbageRemoved)

