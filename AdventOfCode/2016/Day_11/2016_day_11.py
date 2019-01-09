#!/bin/python
# -*- coding: utf-8 -*-
# http://adventofcode.com/2016/day/11


###################################################################################################################################################################
#  
#  Solution to day 11 part 1: 
#  Solution to day 11 part 2: 
#
###################################################################################################################################################################


# Sam's solution: https://github.com/samlindsaylevine/advent/blob/master/src/main/java/advent/year2016/day11/RadioisotopeTestingFacility.java

class Generator:
    def __init__(self, _element):
        self.element = _element

    def isCompatibleWithGenerator(self, generator):
        return generator.element == self.element

    def __str__(self):
        return "Generator[%s]" % (self.element)


class Microchip:
    def __init__(self, _element):
        self.element = _element

    def isCompatibleWithMicrochip(self, microchip):
        return microchip.element == self.element

    def __str__(self):
        return "Microchip[%s]" % (self.element)


class Floor:
    def __init__(self, floor):
        self.floor = _floor
        self.microchips = []
        self.generators = []

    def addMicrochip(self, chip):
        self.microchips.append(chip)

    def removeMicrochip(self, chip):
        self.microchips.remove(chip)

    def addGenerators(self, chip):
        self.generators.append(chip)

    def removeGenerators(self, chip):
        self.generators.remove(chip)

    def isValidState(self):
        pass

class Building:
    def __init__(self):
        self.floors = []

    def addFloor(self, floor):
        # Assumption, floors added bottom to top. ground floor == index 0.
        self.floors.append(floor)

class Transition:
    def __init__(self, source, destination, contents):
        self.sourceFloor = source
        self.destinationFloor = destination
        self.contents = contents
    ###

    def applyTransition(self):
        pass

    def reverseTransition(self):
        pass


class Solver:
    pass


###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################
