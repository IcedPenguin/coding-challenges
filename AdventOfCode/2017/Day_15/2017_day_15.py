#!/bin/python
# -*- coding: utf-8 -*-
# http://adventofcode.com/2017/day/15

###################################################################################################################################################################
#  
#  Solution to day 15 part 1: 600
#  Solution to day 15 part 2: 313
#
###################################################################################################################################################################

class Judge(object):
    def __init__(self, name):
        self.name = name
        self.count = 0
    ### __init__


    def compareValues(self, valueOne, valueTwo):
        one = self.getLower16BitsInHex(valueOne)
        two = self.getLower16BitsInHex(valueTwo)
        if one == two:
            self.count += 1
    ### compareValues


    def getLower16BitsInHex(self, value):
        return value & 0xFFFF
    ### getLower16BitsInHex


    def getCount(self):
        return self.count
    ### getCount
### Judge


class Generator(object):
    def __init__(self, name, factor, multiple, seed):
        self.name = name
        self.factor = factor
        self.multiple = multiple
        self.previousValue = seed
    ### __init__


    def __str__(self):
        return "Generator [%s, %s, %s, %s]" % (self.name, self.factor, self.multiple, self.previousValue)
    ### __str__


    def nextValue(self):
        remainder = 1
        while remainder != 0:
            self.previousValue = (self.previousValue * self.factor) % 2147483647
            remainder = self.previousValue % self.multiple
            # print "%s -> %s  [%s]" % (self.name, self.previousValue, remainder)

        return self.previousValue
    ### nextValue
### Generator


def compareValue(expected, actual):
    if expected != actual:
        print "FAIL: %s %s" % (expected, actual)
    else:
        print "PASS: %s" % (actual)
### compareValue


###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################



count = 0

print "===== PART 1 ====="

genA = Generator("A", 16807, 1, 65)
genB = Generator("B", 48271, 1, 8921)

compareValue(   1092455, genA.nextValue())
compareValue(1181022009, genA.nextValue())
compareValue( 245556042, genA.nextValue())
compareValue(1744312007, genA.nextValue())
compareValue(1352636452, genA.nextValue())

compareValue( 430625591, genB.nextValue())
compareValue(1233683848, genB.nextValue())
compareValue(1431495498, genB.nextValue())
compareValue( 137874439, genB.nextValue())
compareValue( 285222916, genB.nextValue())




def partOne():
    genA = Generator("A", 16807, 1, 699)
    genB = Generator("B", 48271, 1, 124)
    judge = Judge("Dred")

    for i in xrange(40000000):
        # if i % 50000 == 0:
            # print i
        judge.compareValues( genA.nextValue(), genB.nextValue() )

    return judge.getCount()
## partOne

count = partOne()

print ""
print "Solution to day 15 part 1: " + str(count)


###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################

print ""
print "===== PART 2 ====="


genA = Generator("A", 16807, 4, 65)
genB = Generator("B", 48271, 8, 8921)

compareValue(1352636452, genA.nextValue())
compareValue(1992081072, genA.nextValue())
compareValue( 530830436, genA.nextValue())
compareValue(1980017072, genA.nextValue())
compareValue( 740335192, genA.nextValue())

compareValue(1233683848, genB.nextValue())
compareValue( 862516352, genB.nextValue())
compareValue(1159784568, genB.nextValue())
compareValue(1616057672, genB.nextValue())
compareValue( 412269392, genB.nextValue())


  
def partTwo():
    genA = Generator("A", 16807, 4, 699)
    genB = Generator("B", 48271, 8, 124)
    judge = Judge("Dred")

    for i in xrange(5000000):
        # if i % 50000 == 0:
            # print i
        judge.compareValues( genA.nextValue(), genB.nextValue() )

    return judge.getCount()
### partTwo
   

count = partTwo()


print ""
print "Solution to day 15 part 2: " + str(count)
