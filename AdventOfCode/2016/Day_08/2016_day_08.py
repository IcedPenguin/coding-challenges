#!/bin/python
# -*- coding: utf-8 -*-
# http://adventofcode.com/2016/day/8


###################################################################################################################################################################
#  
#  Solution to day 8 part 1: 108
#  Solution to day 8 part 2: ZJHRKCPLYJ
#
###################################################################################################################################################################

def createScreen(width, height):
    screen = []
    for y in xrange(height):
        row = []
        for x in xrange(width):
            row.append(0)
        screen.append(row)

    return screen
### createScreen


def fillRectangle(screen, width, height):
    print "fill -> w: %s   h: %s" % (width, height)
    for y in xrange(height):
        for x in xrange(width):
            screen[y][x] = 1
### fillRectangle


def rotateColumn(screen, column, amount):
    print "rotate Col  ->  c: %s   a: %s" % (column, amount)
    rows = len(screen)

    for a in xrange(amount):
        tempValue = screen[rows -1][column]
        for i in xrange(rows -1, 0, -1):
            screen[i][column] = screen[i-1][column] 
        screen[0][column] = tempValue
### rotateColumn


def rotateRow(screen, row, amount):
    print "rotate Row  ->  r: %s   a: %s" % (row, amount)
    screenRow = screen[row]
    screenWidth = len(screenRow)
    rowTail =  screenRow[len(screenRow) - amount:]
    extendedRow = rowTail + screenRow
    
    screen[row] = extendedRow[:screenWidth]
### rotateRow


def execCommand(screen, line):
    print line.strip()
    parts = line.strip().split()

    if parts[0] == "rect":
        coords = parts[1].split("x")
        fillRectangle(screen, int(coords[0]), int(coords[1]))

    elif parts[1] == "column":
        colId = parts[2].split("=")[1]
        rotateColumn(screen, int(colId), int(parts[4]))

    elif parts[1] == "row":
        rowId = parts[2].split("=")[1]
        rotateRow(screen, int(rowId), int(parts[4]))

    else:
        print "unknown command: " + line
### execCommand


def countLitPixels(screen):
    count = 0
    for y in xrange(len(screen)):
        for x in xrange(len(screen[0])):
            if screen[y][x] == 1:
                count += 1
    return count
### countLitPixels


def printLetters(screen):
    for y in xrange(len(screen)):
        line = ""
        for x in xrange(len(screen[0])):
            if screen[y][x] == 1:
                line += "█"
            else:
                line += " "
        print line
### printLetters


def printScreen(screen):
    print "----------"
    for i in screen:
        print i
    print "----------"
### printScreen

###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################

# width = 7
# height = 3
# input_file = "input_8_sample.txt"

width = 50
height = 6
input_file = "input_8.txt"

screen = createScreen(width,height)
print countLitPixels(screen)

with open(input_file) as f:
    for line in f:
        execCommand(screen, line)

print ""    
print "===== Solution ====="
print "Solution to day 8 part 1: " + str(countLitPixels(screen))

###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################

printScreen(screen)


print "Solution to day 8 part 2: "
printLetters(screen)
