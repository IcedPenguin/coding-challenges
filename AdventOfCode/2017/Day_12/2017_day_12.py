#!/bin/python
# -*- coding: utf-8 -*-
# http://adventofcode.com/2017/day/12

import re

###################################################################################################################################################################
#  
#  Solution to day 12 part 1: 378
#  Solution to day 12 part 2: 204
#
###################################################################################################################################################################


def parseProgramPipes(pipes, relationship):
    parts = re.compile("([0-9]+)( <-> )(.*)").split(relationship.strip())

    programId = parts[1]
    values = parts[3].split(",")
    connection = []

    for v in values:
        connection.append(v.strip())
    
    pipes[programId] = connection
### parseProgramPipes


def getAllProgramsChainedToSource(pipes, sourceId):
    if sourceId not in pipes:
        return []

    waitingToBeSearched = pipes[sourceId][:]
    alreadySearched = [sourceId]        # by definition

    while len(waitingToBeSearched) > 0:
        nextProgramId = waitingToBeSearched.pop(0)
        if nextProgramId in alreadySearched:
            continue

        connections = pipes[nextProgramId]
        for connection in connections:
            if connection not in alreadySearched:
                waitingToBeSearched.append(connection)

        alreadySearched.append(nextProgramId)

    return list(set(alreadySearched))
### 


def countGroups(pipes):
    count = 0
    while len(pipes) > 0:
        count += 1
        sourceProgram = pipes.keys()[0]

        linked = getAllProgramsChainedToSource(pipes, sourceProgram)
        for item in linked:
            pipes.pop(item)

    return count
# countGroups


###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################


print "===== PART 1 ====="

# inputFile = "input_12_sample.txt"
inputFile = "input_12.txt"

pipes = {}
with open(inputFile) as f:
    for line in f:
        parseProgramPipes(pipes, line)

result = getAllProgramsChainedToSource(pipes, "0")

print ""    
print "Solution to day 11 part 1: " + str(len(result))


###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################


print ""
print "===== PART 2 ====="

result = countGroups(pipes)

print ""
print "Solution to day 11 part 2: " + str(result)
