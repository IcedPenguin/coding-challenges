#!/bin/python
# -*- coding: utf-8 -*-
# https://adventofcode.com/2018/day/3


###################################################################################################################################################################
#  
#  Solution to day 3 part 1: 113576
#  Solution to day 3 part 2: 825
#
###################################################################################################################################################################


###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################

# input_file = "2018_03_1_sample_1.txt"
input_file = "2018_03_input.txt"


class FabricClaim:
    def __init__(self, line):
        for ch in ['#','@',',','x',':']:
            if ch in line:
                line = line.replace(ch," ")
        
        parts = line.split()


        self.id = parts[0]
        self.fromLeft = int(parts[1])
        self.fromTop = int(parts[2])
        self.width = int(parts[3])
        self.height = int(parts[4])

        self.intersectsWithOther = False

        self.intersectionPoints = None
    ### __init__

    def __repr__(self):
        return self.id
    ### __repr__

    def getClaimPoints(self):
        if self.intersectionPoints is not None:
            return self.intersectionPoints

        pointsSelf = set()
        for x in xrange(self.fromLeft, self.fromLeft + self.width):
            for y in xrange(self.fromTop, self.fromTop + self.height):
                pointsSelf.add( (x,y) )

        self.intersectionPoints = pointsSelf
        return self.intersectionPoints
    ### getClaimPoints

    def getIntersectionPoints(self, other):        
        pointsSelf = self.getClaimPoints()
        pointsOther = other.getClaimPoints()

        intersections = pointsSelf & pointsOther # set intersection
        
        if len(intersections) > 0:
            self.intersectsWithOther = True
            other.intersectsWithOther = True

        return intersections
    ### getIntersections







claims = []

with open(input_file) as f:
    for line in f:
        claim = FabricClaim(line)
        claims.append(claim)


overlappingPoints = set()

for i in xrange(0, len(claims)):
    for j in xrange(i+1, len(claims)):
        print str(i) + "\t" + str(j)
        claimOne = claims[i]
        claimTwo = claims[j]
        ii = claimOne.getIntersectionPoints(claimTwo)
        print ii
        overlappingPoints.update(ii)

claimId = -1
for claim in claims:
    if not claim.intersectsWithOther:
        print "claims to have no intersections: " + str(claim)
        claimId = claim.id




print "Solution to day 3 part 1: " + str(len(overlappingPoints))



###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################


print "Solution to day 3 part 2: " + str(claimId)
