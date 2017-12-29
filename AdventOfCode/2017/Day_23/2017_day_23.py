#!/bin/python
# -*- coding: utf-8 -*-
# http://adventofcode.com/2017/day/23

import re
import logging

logging.getLogger().addHandler(logging.StreamHandler())
logger = logging.getLogger('duet')
logger.setLevel(logging.INFO)


###################################################################################################################################################################
#  
#  Solution to day 23 part 1: 5929
#  Solution to day 23 part 2: 907
#
###################################################################################################################################################################


class Processor(object):
    def __init__(self, instructionFile, exitCondition):
        self.registerBank = {}
        self.regex = re.compile("([a-z]+ )([0-9a-z]+)(.*)")
        self.instructions = []
        self.instructionPointer = 0
        self.exitCondition = exitCondition
        self.solution = None
        self.mulCount = 0

        self.lastSoundPlayed = None
        self.previousRecoveredValue = None

        self.loadInstructionFile(instructionFile)
    ### __init__


    def loadInstructionFile(self, fileName):
        with open(fileName) as f:
            for line in f:
                self.instructions.append(line.strip())
    ### loadInstructionFile


    def executeInstructions(self):
        while True:
            instruction = self.instructions[self.instructionPointer]
            result = self.executeNextInstruction(instruction)

            self.instructionPointer += 1

            if self.exitCondition(self):
                print "Exit condition is true."
                return

            # We have run out of instructions, exit
            if self.instructionPointer >= len(self.instructions):
                print "All instructions have been executed. Exiting..."
                return
    ### executeInstructions


    def executeNextInstruction(self, instruction):
        logger.debug( "excuting instruction: %s -> %s" % (self.instructionPointer, instruction) )

        parts = self.regex.split(instruction.strip())
        command = parts[1].strip()
        register = parts[2].strip()

        # handle all commands with only one operand first
        if command == "snd":
            self.snd(register)
        elif command == "rcv":
            self.rcv(register)
        
        # then handle all commands with two operands
        else:
            value = parts[3].strip()
            if command == "set":
                self.set(register, value)
            elif command == "sub":
                self.sub(register, value)
            elif command == "mul":
                self.mul(register, value)
            elif command == "jnz":
                self.jnz(register, value)
    ### executeNextInstruction


    def valueOf(self, Y):
        try: 
            return int(Y)            
        except ValueError:

            if Y in self.registerBank:
                return self.registerBank[Y]
            else:
                self.set(Y, 0)
                return 0
    ### valueOf


    def set(self, X, Y):
        self.registerBank[X] = self.valueOf(Y)
    ### set


    def sub(self, X, Y):
        self.registerBank[X] = self.valueOf(X) - self.valueOf(Y)
    ### add


    def mul(self, X, Y):
        self.registerBank[X] = self.valueOf(X) * self.valueOf(Y)
        self.mulCount += 1
    ### mul    

    def jnz(self, X, Y):
        if self.valueOf(X) != 0:
            Y = self.valueOf(Y)
            self.instructionPointer += (Y -1) # -1 to cancel with the standard step forward upon return
    ### jgz    

### Processor




###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################


inputFile = "input_23.txt"

count = 0

def exitConditionPartOne(self):
    # This time, the exit condition is we point at an instruction that does not exist.
    return self.instructionPointer >= len(self.instructions)
### exitConditionPartOne

print "===== PART 1 ====="
proc = Processor(inputFile, exitConditionPartOne)
proc.executeInstructions()


print ""
print "Solution to day 23 part 1: " + str( proc.mulCount )


###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################

# inputFile = "input_23_optimized.txt"
print ""
print "===== PART 2 ====="

# https://stackoverflow.com/questions/4114167/checking-if-a-number-is-a-prime-number-in-python
from math import sqrt; from itertools import count, islice
def isPrime(n):
    return n > 1 and all(n%i for i in islice(count(2), int(sqrt(n)-1)))


compositeCount = 0
for i in xrange(107900, 124900+1, 17):
    if not isPrime(i):
        compositeCount += 1

print "Solution to day 23 part 2: " + str(compositeCount)

