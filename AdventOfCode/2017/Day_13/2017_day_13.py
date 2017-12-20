#!/bin/python
# -*- coding: utf-8 -*-
# http://adventofcode.com/2017/day/13

import re

###################################################################################################################################################################
#  
#  Solution to day 13 part 1: 648
#  Solution to day 13 part 2: 3933124
#
###################################################################################################################################################################


class Packet:
    def __init__(self, packetNumber):
        self.packetNumber = packetNumber
        self.found = []

    def __str__(self):
        r = " Packet["
        r += str(self.packetNumber)
        r += "] "
        return r
    ### __str__


    def markFound(self, layer):
        self.found.append((layer.depth, layer.size))
    ### markFound


    def getTripSeverity(self):
        severity = 0
        for f in self.found:
            severity += f[0] * f[1]
        return severity
    ### getTripSeverity


    def wasFound(self):
        return len(self.found) > 0
    ### wasFound
### Packet


class Layer:
    def __init__(self, depth, size, hasScanner):
        self.size = size
        self.depth = depth
        self.size = size
        self.scannerIdx = 0 if hasScanner else -10
        self.scannerDirection = 1
        self.packet = None
    ### __init__


    def __str__(self):
        r = " Layer["
        r += " D:" + str(self.depth)
        r += " R:" + str(self.size)
        r += "] "
        return r
    ### __str__


    def moveScanner(self):
        # If the layer has no scanner, we don't have to do anything
        if self.scannerIdx == -10:
            return

        # If we are at the end of the list, where if we moved one further in the current direction we would
        # fall off the list, then we should change our direction
        if self.scannerIdx == 0 and self.scannerDirection == -1:
            self.scannerDirection = 1

        elif self.scannerIdx +1 == self.size and self.scannerDirection == 1:
            self.scannerDirection = -1

        self.scannerIdx += self.scannerDirection
    ### moveScanner
        

    def packetEnter(self, packet):
        self.packet = packet
        if self.scannerIdx == 0 and self.packet is not None:
            self.packet.markFound(self)
    ### packetEnter


    def packetLeave(self):
        packet = self.packet
        self.packet = None
        return packet
    ### packetLeave
### Layer


class Firewall:
    def __init__(self):
        self.layers = []
    ### __init__

    def __str__(self):
        r = " Firewall["
        for l in self.layers:
            r += str(l)
        r += "] "
        return r
    ### __str__

    def addLayer(self, depth, size):
        while len(self.layers) < depth + 1:
            self.layers.append(Layer(len(self.layers), 0, False))

        self.layers[depth] = Layer(depth, size, True)
    ### addLayer


    def advancePackets(self, newPacket):
        # print "---"
        oldPacket = newPacket
        for l in self.layers:
            oldPacket = l.packetLeave()
            l.packetEnter(newPacket)
            newPacket = oldPacket

        return oldPacket
    ### advancePackets


    def advanceScanners(self):
        for l in self.layers:
            l.moveScanner()
    ### advanceScanners

### Firewall


def initFireWall(inputFile):
    firewall = Firewall()
    regex = re.compile("([0-9]+)(: )([0-9]+)")

    with open(inputFile) as f:
        for line in f:
            parts = regex.split(line.strip())
            firewall.addLayer(int(parts[1].strip()), int(parts[3].strip()))

    return firewall            
### initFirewall


def throwPacketsAtFirewall(firewall, exitConditionFunction, solutionFunction):
    counter = 0
    packetExitingFirewall = None
    while not exitConditionFunction(firewall, packetExitingFirewall):
        if counter % 10000 == 0:    # visual indicator the program is progressing...
            print counter

        # make the next packet to put into the firewall
        newPacket = Packet(counter)
        counter += 1

        # move the packets
        packetExitingFirewall = firewall.advancePackets(newPacket)

        # move the scanners
        firewall.advanceScanners()

    return solutionFunction(firewall, packetExitingFirewall)

### throwPacketsAtFirewall

###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################

# inputFile = "input_13_sample.txt"
inputFile = "input_13.txt"

print "===== PART 1 ====="


def exitConditionPart1(firewall, packetExitingFirewall):
    if packetExitingFirewall is None:
        return False

    return True
### exitCondition


def solutionPart1(firewall, packetExitingFirewall):
    return packetExitingFirewall.getTripSeverity()
### solutionPart1


firewall = initFireWall(inputFile)
result = throwPacketsAtFirewall(firewall, exitConditionPart1, solutionPart1)
print ""    
print "Solution to day 13 part 1: " + str(result)


###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################

print ""
print "===== PART 2 ====="


def exitConditionPart2(firewall, packetExitingFirewall):
    if packetExitingFirewall is None:
        return False
    return not packetExitingFirewall.wasFound()
### exitCondition


def solutionPart2(firewall, packetExitingFirewall):
    return packetExitingFirewall.packetNumber
### solutionPart1


firewall = initFireWall(inputFile)
result = throwPacketsAtFirewall(firewall, exitConditionPart2, solutionPart2)
print ""
print "Solution to day 13 part 2: " + str(result)
