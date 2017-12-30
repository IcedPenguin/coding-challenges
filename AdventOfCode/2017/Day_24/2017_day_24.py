#!/bin/python
# -*- coding: utf-8 -*-
# http://adventofcode.com/2017/day/24

###################################################################################################################################################################
#  
#  Solution to day 24 part 1: 1906
#  Solution to day 24 part 2: 1824
#
###################################################################################################################################################################

class Stats(object):
    def __init__(self):
        # Look for the highest valued bridge
        self.strongestBridge = None
        self.strongestBridgeValue = -1

        # Look for the longest valued bridge
        self.longestBridge = []
        self.longestBridgeValue = -1;
    ### __init__


    def nextPossibleBestBridge(self, bridge):
        score = 0
        for component in bridge:
            score += component.getStrength()

        # First, test for the strongest bridge
        if self.strongestBridgeValue < score:
            self.strongestBridge = bridge
            self.strongestBridgeValue = score


        # Then, test for length
        lengthCurrent = len(self.longestBridge)
        lengthBridge = len(bridge)

        if lengthCurrent < lengthBridge:
            self.longestBridge = bridge
            self.longestBridgeValue = score

        elif lengthCurrent == lengthBridge:
            if self.longestBridgeValue < score:
                self.longestBridge = bridge
                self.longestBridgeValue = score
    ### nextPossibleHighestValueBridge
### Stats


class Component(object):
    def __init__(self, portOne, portTwo):
        self.portOne = portOne
        self.portTwo = portTwo
    ### __init__


    def __repr__(self):
        return "C[" + str(self.portOne) + "/" + str(self.portTwo) + "]"
    ### __repr__


    def getValueOfOppositePort(self, value):
        if self.portOne == value:
            return self.portTwo
        else:
            return self.portOne
    ### getValueOfOppositePort


    def getStrength(self):
        return self.portOne + self.portTwo
    ### getStrength
### Component


# class Bridge(object):
#     pass


def loadComponents(componentFile):
    componentBag = []
    with open(componentFile) as f:
        for line in f:
            parts = line.strip().split("/")
            componentBag.append( Component(int(parts[0]), int(parts[1])) )

    return componentBag
### loadComponents


def getAllComponentsCompatibleWith(componentBag, port):
    compatibleComponents = []
    for componet in componentBag:
        if componet.portOne == port or componet.portTwo == port:
            compatibleComponents.append(componet)

    return compatibleComponents
### getAllComponentsCompatibleWith


def buildLongestBridge(stats, currentBridge, componentBag, port):
    # Get all the remaining components that are compatible with the port.
    nextLinkInBridge = getAllComponentsCompatibleWith(componentBag, port)

    # if there are none, then we have reached the end of this bridge branch.
    # calculate the bridge value. store the value if it is the greatest.
    # return
    if len(nextLinkInBridge) == 0:
        stats.nextPossibleBestBridge(currentBridge)
        return

    # for each component
    for component in nextLinkInBridge:
        nextBridge = currentBridge[:]
        nextBridge.append(component)
        
        nextComponentBag = componentBag[:]
        nextComponentBag.remove(component)
        
        buildLongestBridge(stats, nextBridge, nextComponentBag, component.getValueOfOppositePort(port))
### buildLongestBridge


###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################


inputFile = "input_24.txt"
# inputFile = "input_24_sample.txt"

print "===== PART 1 ====="

componentBag = loadComponents(inputFile)
stats = Stats()
buildLongestBridge(stats, [], componentBag, 0)

print ""
print "Solution to day 24 part 1: " + str(stats.strongestBridgeValue)


###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################

print ""
print "===== PART 2 ====="

# All additional work is tracked in the stats object.

print "Solution to day 24 part 2: " + str(stats.longestBridgeValue)

