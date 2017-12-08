#!/bin/python
# -*- coding: utf-8 -*-
# http://adventofcode.com/2017/day/7

import re

###################################################################################################################################################################
#  
#  Solution to day 7 part 1: veboyvy
#  Solution to day 7 part 2: 749
#
###################################################################################################################################################################

class Node:
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight
        self.parent = None
        self.children = []

    def addChild(self, child):
        self.children.append(child)

    # two way link. why not.
    def setParent(self, parent):
        self.parent = parent

    def hasParent(self):
        return self.parent is None

    def hasChildren(self):
        return len(self.children) != 0

    def getWeightOfChildren(self):
        weights = {}
        weightsWithMoreThanOne = []
        for child in children:
            childWeight = child.getWeightOfTree()
            if childWeight in weights:
                weights[childWeight].append(child)
            else:
                weights[childWeight] = [child]

        return weights

    def getWeightOfTree(self):
        weight = self.weight
        for child in self.children:
            weight += child.getWeightOfTree()

        return weight

    def __str__(self):
        if self.parent is None:
            return "Node[%s, %s, %s, %s, %s, %s]" % (self.name, self.weight, None, self.hasParent(), len(self.children), self.hasChildren())
        else:
            return "Node[%s, %s, %s, %s, %s, %s]" % (self.name, self.weight, self.parent.name, self.hasParent(), len(self.children), self.hasChildren())

    def __repr__(self):
        return self.__str__()


###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################

nodeRegEx = "([a-z]+)( \()([0-9]+)(\))(.*)"

def readFileIntoTree(fileName):
    nodes = []
    tree = {}
    nodesHoldingDiscs = []

    with open(fileName) as f:
        for line in f:
            # create the base node
            parts = re.compile(nodeRegEx).split(line.strip())
            node = Node(parts[1], int(parts[3]))
            tree[parts[1]] = node
            nodes.append(node)

            if len(parts[5]) > 0:
                nodesHoldingDiscs.append(line)

    # now process the disks, all of the needed nodes should exist
    for item in nodesHoldingDiscs:
        parts = re.compile(nodeRegEx).split(item.strip())
        parent = tree[parts[1]]
        children = [x.strip() for x in parts[5][3:].split(',')]

        for child in children:
            parent.addChild(tree[child])
            tree[child].setParent(parent)

    return tree, nodes
### readFileIntoTree    


def findTreeRoots(tree):
    roots = []
    for node in tree:
        n = tree[node]
        if n.hasParent():
            roots.append(n)
    
    return roots
### findTreeRoots


# input_file = "input_sample.txt"
input_file = "input_7.txt"

tree, nodes = readFileIntoTree(input_file)
roots = findTreeRoots(tree)

print "Solution to day 7 part 1: " + str(roots[0].name)


###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################


def getChildWeights(node):
    children = node.children
    childWeights = {}
    for child in children:
        w = child.getWeightOfTree()
        if w in childWeights:
            childWeights[w].append(child)
        else:
            childWeights[w] = [child]
    return childWeights
### getChildWeights


def separateWeights(childWeights):
    targetWeight = 0
    differentWeight = None

    for i in childWeights:
        if len(childWeights[i]) > 1:
            targetWeight = i
        else:
            differentWeight = i

    return targetWeight, differentWeight
### separateWeights


def performSearch(root):
    childWeights = getChildWeights(root)
    targetWeight, differentWeight = separateWeights(childWeights)
    return fixWeights(targetWeight, childWeights[differentWeight][0])
### performSearch


def fixWeights(targetWeight, node):
    if not node.hasChildren():
        # print "AAA: leaf node needed patching: %s %s" % (node.name, targetWeight)
        return targetWeight

    # determine if a child is unbalanced.
    childWeights = getChildWeights(node)

    # all the children weigh the same, fix the parent weight
    if len(childWeights) == 1:
        w = childWeights.keys()[0]
        targetWeight -= len(childWeights[w]) * w
        # print "BBB: parent node needed patching: %s %s" % (node.name, targetWeight)
        return targetWeight

    # one of the children is different, recurse into that child.
    else:
        newTargetWeight, differentWeight = separateWeights(childWeights)
        # print "CCC: hunting child tree. %s %s" % (newTargetWeight, childWeights[differentWeight][0].name)
        return fixWeights(newTargetWeight, childWeights[differentWeight][0])
### fixWeights




newWeight = performSearch(roots[0])


print "Solution to day 7 part 2: " + str(newWeight)

