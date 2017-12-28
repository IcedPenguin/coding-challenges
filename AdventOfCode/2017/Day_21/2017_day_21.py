#!/bin/python
# -*- coding: utf-8 -*-
# http://adventofcode.com/2017/day/21

import re
import TransformMatrix

###################################################################################################################################################################
#  
#  Solution to day 21 part 1: 173
#  Solution to day 21 part 2: 2456178
#
###################################################################################################################################################################
 

def loadRulesMap(ruleFile):
    rulesMap = {}    

    with open(ruleFile) as f:
        for line in f:
            line = line.strip()
            addRuleToRulesMap(rulesMap, line)

    return rulesMap
### loadMap


def addRuleToRulesMap(rulesMap, rule):
    parts = re.compile("(.*)( => )(.*)").split(rule)
    pattern = convertStringToMatrix(parts[1])
    permutations = getAllPermutationOfPattern(pattern)
    for permutation in permutations:
        rulesMap[permutation] = convertStringToMatrix(parts[3], True)
### addRuleToRulesMap


def convertStringToMatrix(s, asTuple=False):
    matrix = []
    parts = s.split("/")
    for row in parts:
        line = []
        for letter in row:
            line.append(letter)
        if asTuple:
            matrix.append(tuple(line))
        else:
            matrix.append(line) 
    
    if asTuple:
        return tuple(matrix)
    else:
        return matrix
### convertStringToMatrix


def convertListMatrixToTupleMatrix(matrix):
    out = []
    for row in matrix:
        out.append( tuple(row))
    return tuple(out)
### convertListMatrixToTupleMatrix


def getAllPermutationOfPattern(pattern):
    pattern_2 = TransformMatrix.rotateMatrix(pattern  )
    pattern_3 = TransformMatrix.rotateMatrix(pattern_2)
    pattern_4 = TransformMatrix.rotateMatrix(pattern_3)
    pattern_5 = TransformMatrix.flipMatrix(  pattern  )
    pattern_6 = TransformMatrix.rotateMatrix(pattern_5)
    pattern_7 = TransformMatrix.rotateMatrix(pattern_6)
    pattern_8 = TransformMatrix.rotateMatrix(pattern_7)

    return (
        convertListMatrixToTupleMatrix(pattern), 
        convertListMatrixToTupleMatrix(pattern_2), 
        convertListMatrixToTupleMatrix(pattern_3), 
        convertListMatrixToTupleMatrix(pattern_4), 
        convertListMatrixToTupleMatrix(pattern_5), 
        convertListMatrixToTupleMatrix(pattern_6), 
        convertListMatrixToTupleMatrix(pattern_7), 
        convertListMatrixToTupleMatrix(pattern_8)
    )
### getAllPermutationOfPattern


def performIterations(matrix, rulesMap, iterationCount):
    for i in xrange(iterationCount):
        if len(matrix) % 2 == 0:
            matrix = enhanceMatrix(matrix, rulesMap, 2)
        elif len(matrix) % 3 == 0:
            matrix = enhanceMatrix(matrix, rulesMap, 3)

    return matrix
### performIterations


def allocateMatrix(size):
    m = []
    for i in xrange(size):
        r = []
        for j in xrange(size):
            r.append("=")
        m.append(r)
    return m
    # return [ ["="] * size ] * size   <-- This does not work. each matrix row is a shallow copy of the others?!
### allocateMatrix


def enhanceMatrix(matrix, rulesMap, size):
    sideLength = len(matrix)
    oldPatternPerSide = sideLength / size
    newMatrix = allocateMatrix(sideLength / size * (size +1))

    print "sideLength=%s" % (sideLength)
    print "oldPatternPerSide=%s" % (oldPatternPerSide)
        
    for i in xrange((sideLength/size) ** 2):
    # extract the NxN pattern from the oldMatrix
        x = i % oldPatternPerSide * size
        y = i / oldPatternPerSide * size
        pattern = extractPattern(matrix, size, x, y)

    # find its transformation
        transformation = rulesMap[pattern]

    # write the (N+1)x(N+1) pattern to newMatrix
        x = i % oldPatternPerSide * (size +1)
        y = i / oldPatternPerSide * (size +1)
        insertPattern(newMatrix, transformation, size+1, x, y)
        
    # printMatrix(newMatrix)
    return newMatrix
### enhanceMatrix


def extractPattern(matrix, size, x, y):
    pattern = []
    for i in xrange(size):
        row = []
        for j in xrange(size):
            row.append(matrix[y+i][x+j])
        pattern.append( tuple(row) )

    
    return tuple(pattern)
### extractPattern


def insertPattern(newMatrix, transformation, size, x, y):
    for i in xrange(size):
        for j in xrange(size):
            newMatrix[y+i][x+j] = transformation[i][j]
### insertPattern


def printMatrix(matrix):
    s = ""
    for row in matrix:
        for col in row:
            s += str(col)
            s += " "
        s += "\n"
    print s
### printMatrix


def countOnPixels(matrix):
    count = 0
    print "--- counting ---"
    for row in matrix:
        for col in row:
            if col == "#":
                count += 1
    return count
### countOnPixels


###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################


inputFile = "input_21.txt"
rulesMap = loadRulesMap(inputFile)
initialMatrix = [[".", "#", "."],[".", ".", "#"],["#", "#", "#"]]
iterationCount = 5

printMatrix(initialMatrix)
matrix = performIterations(initialMatrix, rulesMap, iterationCount)
count = countOnPixels(matrix)

print ""
print "Solution to day 21 part 1: " + str(count)


###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################


print ""
print "===== PART 2 ====="

initialMatrix = [[".", "#", "."],[".", ".", "#"],["#", "#", "#"]]
iterationCount = 18

printMatrix(initialMatrix)
matrix = performIterations(initialMatrix, rulesMap, iterationCount)
count = countOnPixels(matrix)

print "Solution to day 20 part 2: " + str(count)

