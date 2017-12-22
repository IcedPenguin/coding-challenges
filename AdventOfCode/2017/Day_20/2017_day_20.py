#!/bin/python
# -*- coding: utf-8 -*-
# http://adventofcode.com/2017/day/20

import re

###################################################################################################################################################################
#  
#  Solution to day 20 part 1: 170
#  Solution to day 20 part 2: 571
#
###################################################################################################################################################################
 
# For each time interval, we can get the distance to the origin for each particle
#   distance_i = math.abs( (1/2)(accel_i)(time ^ 2) + (velocity_i)(time) + (initialPosition_i) )
#   calculate for all three axies, sum, that is the manhatten distance to the origin.


def loadFile(fileName):
    counter = 0
    particles = []
    with open(fileName) as f:
        for line in f:
            p = Particle(counter, line)
            particles.append(p)
            counter += 1

    return particles
### loadFile


class Particle(object):
    def __init__(self, name, line):
        parts = re.compile("(p=<)(.*)(>, v=<)(.*)(>, a=<)(.*)(>)").split(line.strip())
        
        self.name = name
        self.position = self.extractValues(parts[2])
        self.velocity = self.extractValues(parts[4])
        self.acceleration = self.extractValues(parts[6])
    ### __init__


    def extractValues(self, compacted):
        a = compacted.split(",")
        return (int(a[0]), int(a[1]), int(a[2]))
    ### extractValues


    def __repr__(self):
        s = "P[name="
        s += str(self.name)
        s += ", p="
        s += str(self.position)
        s += ", v="
        s += str(self.velocity)
        s += ", a="
        s += str(self.acceleration)
        s += ", ∆A="
        s += str( self.getMinimumedAccleration())
        s += "]"
        return s
    ### __resp__


    def getMinimumedAccleration(self):
        return abs(self.acceleration[0]) + abs(self.acceleration[1]) + abs(self.acceleration[2])
    ### getMinimumedAccleration


    def getMinimumedVelocity(self):
        return abs(self.velocity[0]) + abs(self.velocity[1]) + abs(self.velocity[2])
    ### getMinimumedAccleration


    def getMinimumedPosition(self):
        return abs(self.position[0]) + abs(self.position[1]) + abs(self.position[2])
    ### getMinimumedAccleration


    def isColliding(self, other):
        return self.position == other.position
    ### isColliding

    def stepForward(self):
        self.velocity = (self.velocity[0] + self.acceleration[0], self.velocity[1] + self.acceleration[1], self.velocity[2] + self.acceleration[2])
        self.position = (self.position[0] + self.velocity[0],     self.position[1] + self.velocity[1],     self.position[2] + self.velocity[2])
    ### stepForward
### Particle

###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################

def sortParticlesByAcceleration(particles):
    particles.sort(key=lambda x: x.getMinimumedPosition(), reverse=False)
    particles.sort(key=lambda x: x.getMinimumedVelocity(), reverse=False)
    particles.sort(key=lambda x: x.getMinimumedAccleration(), reverse=False)
### sortParticlesByAcceleration


def printFirstNItems(items, count):
    for i in xrange( min(len(items), count)):
        print items[i]
### printFirstNItems

inputFile = "input_20.txt"
# inputFile = "input_20_sample.txt"
# inputFile = "input_20_sample_2.txt"

particles = []

particles = loadFile(inputFile)


sortParticlesByAcceleration(particles)
printFirstNItems(particles, 5)


print ""
print "Solution to day 20 part 1: " + str( particles[0].name )


###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################

def checkForCollisions(particles):
    
    indiciesToRemove = []
    for i in xrange(len(particles)):
        p = particles[i]
        for j in xrange(i +1, len(particles)):
            if p.isColliding(particles[j]):
                indiciesToRemove.append(i)
                indiciesToRemove.append(j)
                print "--Collision Found--\t" + str(particles[i].name) + "\t" + str(particles[j].name)

    if len(indiciesToRemove) == 0:
        return False

    # collapse to set
    indiciesToRemoveSet = set(indiciesToRemove)

    # convert back to list
    indiciesToRemove = list(indiciesToRemoveSet)

    # sort
    indiciesToRemove.sort(reverse=True)

    # remove from highest index to lowest index
    for i in indiciesToRemove:
        particles.pop(i)

    return True

def stepAllParticles(particles):
    for p in particles:
        p.stepForward()
### stepAllParticles


def iterateThroughCollisions(particles):
    # There is probably a nice mathy way to solve this. 
    step = 0

    # walk forward 100 iterations. If a collision is detected, rest counter to 0.
    counter = 0
    while counter < 100:

        print "checking for collisions: " + str(step)
        if checkForCollisions(particles):
            counter = 0

        # step every partical forward.
        stepAllParticles(particles)

        counter += 1
        step += 1
### iterateThroughCollisions


print ""
print "===== PART 2 ====="
iterateThroughCollisions(particles)
print ""

print "Solution to day 20 part 2: " + str( len( particles ) )
