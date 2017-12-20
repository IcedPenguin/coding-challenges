#!/bin/python
# -*- coding: utf-8 -*-
# http://adventofcode.com/2017/day/18

import re
import logging

logging.getLogger().addHandler(logging.StreamHandler())
logger = logging.getLogger('duet')
logger.setLevel(logging.INFO)


###################################################################################################################################################################
#  
#  Solution to day 18 part 1: 2951
#  Solution to day 18 part 2: 7366
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
            elif command == "add":
                self.add(register, value)
            elif command == "mul":
                self.mul(register, value)
            elif command == "mod":
                self.mod(register, value)
            elif command == "jgz":
                self.jgz(register, value)
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


    # snd X       plays a sound with a frequency equal to the value of X.
    def snd(self, X):
        self.lastSoundPlayed = self.valueOf(X)
    ### 


    def add(self, X, Y):
        self.registerBank[X] = self.valueOf(X) + self.valueOf(Y)
    ### add


    def mul(self, X, Y):
        self.registerBank[X] = self.valueOf(X) * self.valueOf(Y)
    ### mul
    

    def mod(self, X, Y):
        self.registerBank[X] = self.valueOf(X) % self.valueOf(Y)
    ### mod
    

    def rcv(self, X):
        if self.valueOf(X) != 0:
            self.previousRecoveredValue = self.lastSoundPlayed
    ### rcv
    

    def jgz(self, X, Y):
        if self.valueOf(X) > 0:
            Y = self.valueOf(Y)
            self.instructionPointer += (Y -1) # -1 to cancel with the standard step forward upon return
    ### jgz    

### Processor




###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################

# inputFile = "input_18_sample.txt"
inputFile = "input_18.txt"

count = 0

def exitConditionPartOne(self):
    if self.previousRecoveredValue != None:
        print self.previousRecoveredValue
        self.solution = self.previousRecoveredValue
        return True

    return False
### exitConditionPartOne

print "===== PART 1 ====="
proc = Processor(inputFile, exitConditionPartOne)
proc.executeInstructions()


print ""
print "Solution to day 18 part 1: " + str(proc.solution)


###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################

print ""
print "===== PART 2 ====="


class ProcessorDuet(Processor):
    def __init__(self, name, instructionFile, exitCondition):
        Processor.__init__(self, instructionFile, exitCondition)
        self.name = name
        self.companionProcess = None
        self.queue = []
        self.sendCounter = 0

        self.registerBank["p"] = self.name
    ### __init__


    def __str__(self):
        s = "Proc["
        s += str(self.name)
        s += ", cnt="
        s += str(self.sendCounter)
        s += ", ptr="
        s += str(self.instructionPointer)
        s += ", q_l="
        s += str(len(self.queue))
        if len(self.queue) > 0:
            s += ", q_h=" 
            s += str(self.queue[0])
        s += ", registers="
        s += str(self.registerBank)
        s += "]"
        return s
    ### __str___


    def setCompanionProcess(self, process):
        self.companionProcess = process
    ###


    def addToQueue(self, value):
        self.queue.append(value)
    ### addToQueue


    # send X
    def snd(self, X):
        v = self.valueOf(X)
        self.sendCounter += 1
        self.companionProcess.addToQueue(v)
    ### 


    # receive X
    # Return True if we could not get a value
    def rcv(self, X):
        if len(self.queue) > 0:
            self.registerBank[X] = self.queue.pop(0)
            return False
        
        return True
    ### rcv

    def getNextInstruction(self):
        # if there are instructions left to read, return them
        if self.instructionPointer < len(self.instructions):
            instruction = self.instructions[self.instructionPointer]
            return instruction

        else:
            return None
    ### getNextInstruction


    def executeNextInstruction(self, instruction):
        logger.debug("%s -- excuting instruction: %s -> %s" % (self.name, self.instructionPointer, instruction))

        # we have run out of instructions. execution is effectively "blocked", return True.
        if instruction is None:
            return False

        parts = self.regex.split(instruction.strip())
        command = parts[1].strip()
        register = parts[2].strip()

        blocked = False

        # handle all commands with only one operand first
        if command == "snd":
            self.snd(register)
        elif command == "rcv":
            blocked = self.rcv(register)
        
        # then handle all commands with two operands
        else:
            value = parts[3].strip()
            if command == "set":
                self.set(register, value)
            elif command == "add":
                self.add(register, value)
            elif command == "mul":
                self.mul(register, value)
            elif command == "mod":
                self.mod(register, value)
            elif command == "jgz":
                self.jgz(register, value)

        if not blocked:
            self.instructionPointer += 1

        return blocked
    ### executeNextInstruction

### ProcessorDuet




class DuetConductor(object):
    def __init__(self, instructionFile, exitCondition):
        self.blockedA = False
        self.previousInstructionA = None
        self.procA = ProcessorDuet(0, instructionFile, exitCondition)

        self.blockedB = False
        self.previousInstructionB = None
        self.procB = ProcessorDuet(1, instructionFile, exitCondition)

        self.exitCondition = exitCondition

        self.procA.setCompanionProcess(self.procB)
        self.procB.setCompanionProcess(self.procA)
    ### __init__


    def performTheDuet(self):
        counter = 0
        running = True

        while running:
            counter += 1

            if counter % 5000 == 0:
                logger.info( "c=%s    pA=%s <> %s     pB=%s <> %s" % (counter, self.procA.sendCounter, len(self.procA.queue), self.procB.sendCounter, len(self.procB.queue)))

            
            logger.debug("-------------------------------")
            logger.debug("DUET:: A=%s    B=%s" % (self.blockedA, self.blockedB) )

            # perform processor A's logic
            if not self.blockedA:
                self.previousInstructionA = self.procA.getNextInstruction()

            self.blockedA = self.procA.executeNextInstruction(self.previousInstructionA)
            logger.debug( str(self.procA) )

            # perform processor B's logic
            if not self.blockedB:
                self.previousInstructionB = self.procB.getNextInstruction()

            self.blockedB = self.procB.executeNextInstruction(self.previousInstructionB)
            logger.debug( str(self.procB) )

            # test for exit condition
            running = self.exitCondition(self)
    ### performTheDuet

### DuetConductor



def exitConditionPartTwo(self):
    # both processors blocked
    if self.blockedA and self.blockedB:
        print "EXIT CONDITION:: %s   %s" % (self.blockedA, self.blockedB)
        return False

    # keep going
    else:
        return True
### exitConditionPartTwo

# inputFile = "input_18_sample_2.txt"

duet = DuetConductor(inputFile, exitConditionPartTwo)
duet.performTheDuet()

print ""

print duet.procA
print duet.procB
print ""
print "Solution to day 18 part 2: " + str(duet.procB.sendCounter)

