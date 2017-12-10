#!/bin/python
# -*- coding: utf-8 -*-
# http://adventofcode.com/2017/day/8

import re

###################################################################################################################################################################
#  
#  Solution to day 8 part 1: 4448
#  Solution to day 8 part 2: 6582
#
###################################################################################################################################################################

TARGET_REGISTER = 0
COMMAND = 1
VALUE = 2
TEST_REGISTER = 3
TEST_OPERATION = 4
TEST_VALUE = 5


def parseInstructionLine(instructionLine):
    parts = instructionLine.strip().split()
    # targetRegister, inc/dec, amount, testRegister, testType, testValue)
    return (parts[0], parts[1], int(parts[2]), parts[4], parts[5], int(parts[6]))
### parseInstructionLine


def getValueAtRegister(bank, register):
    if register not in bank:
        bank[register] = 0

    return bank[register]
### getValueAtRegister


def setValueAtRegister(bank, register, value):
    currentValue = getValueAtRegister(bank, register)
    newValue = currentValue + value
    bank[register] = newValue
### setValueAtRegister


def getLargestValueInRegisters(bank):
    values = registerBank.values()[:]
    list.sort(values)
    return values[len(values) -1]
### getLargestValueInRegisters


def executeInstruction(bank, instruction):
    testRegisterValue = getValueAtRegister(bank, instruction[TEST_REGISTER])
    testOperation = instruction[TEST_OPERATION]
    testValue = instruction[TEST_VALUE]

    proceed = False

    # Check if the test condition says we should or shouldn't proceed
    if testOperation == "==":
        proceed = testRegisterValue == testValue

    elif testOperation == "!=":
        proceed = testRegisterValue != testValue

    elif testOperation == "<":
        proceed = testRegisterValue < testValue

    elif testOperation == "<=":
        proceed = testRegisterValue <= testValue

    elif testOperation == ">":
        proceed = testRegisterValue > testValue

    elif testOperation == ">=":
        proceed = testRegisterValue >= testValue

    else:
        print "----------- UNKNOWN OPERATION: %s" % (testOperation)

    # Apply the command if the test condition passes
    if proceed:
        register = instruction[TARGET_REGISTER]
        command = instruction[COMMAND]
        value = instruction[VALUE]
        if command == "dec":
            value *= -1

        elif command == "inc":
            pass

        else:
            print "----------- UNKNOWN COMMAND: %s" % (command)
    
        setValueAtRegister(bank, register, value)
### executeInstruction



###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################


# input_file = "input_8_sample.txt"
input_file = "input_8.txt"
largestValueSeen = 0

registerBank = {}
with open(input_file) as f:
    for line in f:
        instruction = parseInstructionLine(line)
        executeInstruction(registerBank, instruction)
        currentLargest = getLargestValueInRegisters(registerBank)

        if currentLargest > largestValueSeen:
            largestValueSeen = currentLargest


# values = registerBank.values()[:]
# list.sort(values)

print "Solution to day 8 part 1: " + str(getLargestValueInRegisters(registerBank))


###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################


print "Solution to day 8 part 2: " + str(largestValueSeen)

