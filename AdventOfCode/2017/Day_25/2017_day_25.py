#!/bin/python
# -*- coding: utf-8 -*-
# http://adventofcode.com/2017/day/25

###################################################################################################################################################################
#  
#  Solution to day 25 part 1: 3732
#  Solution to day 25 part 2: n/a
#
###################################################################################################################################################################
#
#   Parse the input file
#
def loadInputFile(stateFile):
    with open(stateFile) as f:
        content = f.readlines()

    startingStateName = content[0].split()[3][0]
    content.pop(0)

    checksumStepCount = int(content[0].split()[5])
    content.pop(0)

    # Read all the states
    states = {}

    while len(content) > 0:
        line = content.pop(0)
        if line.startswith("In state"):
            name, state = parseState(line, content)
            states[name] = state

    return startingStateName, checksumStepCount, states
### loadInputFile

def parseState(line, content):
    name = line.strip().split()[2][:-1]

    zeroMap = {}
    oneMap = {}

    # grab all the rules for this state
    line_1 = content.pop(0)     # this always refers to value of "0". ignoring
    line_2 = content.pop(0)     # --
    line_3 = content.pop(0)
    line_4 = content.pop(0)     # --
    line_5 = content.pop(0)     # this always refers to value of "1". ignoring
    line_6 = content.pop(0)     # --
    line_7 = content.pop(0)
    line_8 = content.pop(0)     # --

    # extract the bits that we need.
    zeroMap["writeValue"] = int(line_2.strip().split()[4][0])
    zeroMap["direction"] = line_3.strip().split()[6][:-1]
    zeroMap["distance"] = 1 # input shows this is always one. no need to parse.
    zeroMap["nextState"] = line_4.strip().split()[4][0]
    
    oneMap["writeValue"] = int(line_6.strip().split()[4][0])
    oneMap["direction"] = line_7.strip().split()[6][:-1]
    oneMap["distance"] = 1 # input shows this is always one. no need to parse.
    oneMap["nextState"] = line_8.strip().split()[4][0]

    state = State(name, zeroMap, oneMap)
    return name, state
### parseState


###################################################################################################################################################################

class Tape(object):
    def __init__(self):
        self.tape = {}
        self.pointer = 0
    ### __init__


    def getCurrentValue(self):
        if self.pointer not in self.tape:
            self.tape[self.pointer] = 0

        return self.tape[self.pointer]
    ### getCurrentValue


    def writeValue(self, value):
        self.tape[self.pointer] = value
    ### writeValue


    def updatePointer(self, offset):
        self.pointer += offset
    ### updatePointer


    def getChecksum(self):
        checksum = 0
        for key in self.tape:
            if self.tape[key] == 1:
                checksum += 1

        return checksum
##### Tape


class State(object):
    def __init__(self, name, zeroMap, oneMap):
        self.name = name
        
        # zero entries
        self.zero_writeValue = zeroMap["writeValue"]
        if zeroMap["direction"] == "left":
            direction = -1
        else:
            direction = 1
        self.zero_distance   = zeroMap["distance"] * direction
        self.zero_nextState  = zeroMap["nextState"]

        # one entries
        self.one_writeValue  = oneMap["writeValue"]
        if oneMap["direction"] == "left":
            direction = -1
        else:
            direction = 1
        self.one_distance    = oneMap["distance"] * direction
        self.one_nextState   = oneMap["nextState"]
    ### __init__


    def __repr__(self):
        s = "S["
        s += self.name
        s += ", 0→("
        s += str(self.zero_writeValue)
        s += ", "
        s += str(self.zero_distance)
        s += ", "
        s += str(self.zero_nextState)
        s += "), 1→("
        s += str(self.one_writeValue)
        s += ", "
        s += str(self.one_distance)
        s += ", "
        s += str(self.one_nextState)
        s += ")]"
        return s
    ### __repr__


    def execute(self, tape):
        currentTapeValue = tape.getCurrentValue()

        if currentTapeValue == 0:
            tape.writeValue(self.zero_writeValue)
            tape.updatePointer(self.zero_distance)
            return self.zero_nextState

        else: # == 1
            tape.writeValue(self.one_writeValue)
            tape.updatePointer(self.one_distance)
            return self.one_nextState
    ### execute
##### State


###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################

def algorithmOne(tape, states, startingStateName, checksumStepCount):
    nextStateName = startingStateName

    count = 0

    while count < checksumStepCount:
        state = states[nextStateName]

        if count % 50000 == 0:
            print "--step %s-- %s" % (count, state)

        nextStateName = state.execute(tape)
        count += 1
### algorithmOne

inputFile = "input_25.txt"
# inputFile = "input_25_sample.txt"

print "===== PART 1 ====="

tape = Tape()
startingStateName, checksumStepCount, states = loadInputFile(inputFile)

algorithmOne(tape, states, startingStateName, checksumStepCount)


print ""
print "Solution to day 25 part 1: " + str( tape.getChecksum() )


###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################

print ""
print "===== PART 2 ====="
print "There was no puzzle 25 part 2."

