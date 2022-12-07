#!/bin/python
# -*- coding: utf-8 -*-
# https://adventofcode.com/2021/day/13


###################################################################################################################################################################
#  
#  Solution to day 13 part 1: 802
#
#  Solution to day 13 part 2: 
#           ###  #  # #  # #### ####  ##  #  # ### 
#           #  # # #  #  # #       # #  # #  # #  #
#           #  # ##   #### ###    #  #    #  # ### 
#           ###  # #  #  # #     #   # ## #  # #  #
#           # #  # #  #  # #    #    #  # #  # #  #
#           #  # #  # #  # #    ####  ###  ##  ### 
#
###################################################################################################################################################################

import unittest

###################################################################################################################################################################
############################################################################# Common ##############################################################################


sample_input_file_1 = "2021_sample_1.txt"
sample_input_file_2 = "2021_sample_2.txt"
input_file          = "2021_input.txt"


def read_file_into_array(filename, asInt):
    lines = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if asInt:
                lines.append(int(line))
            else:
                lines.append(line)

    return lines
### read_file_into_array

def read_and_parse_single_line_input(filename, delimeter, asInt):
    array = read_file_into_array(filename, False)
    parts = array[0].split(delimeter)
    return parts
### read_and_parse_single_line_input


###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################
#  
#  
#  --- Day 13: Transparent Origami ---
#  You reach another volcanically active part of the cave. It would be nice if you could do some kind of thermal 
#  imaging so you could tell ahead of time which caves are too hot to safely enter.
#  
#  Fortunately, the submarine seems to be equipped with a thermal camera! When you activate it, you are greeted with:
#  
#      Congratulations on your purchase! To activate this infrared thermal imaging
#      camera system, please enter the code found on page 1 of the manual.
#  
#  Apparently, the Elves have never used this feature. To your surprise, you manage to find the manual; as 
#  you go to open it, page 1 falls out. It's a large sheet of transparent paper! The transparent paper is 
#  marked with random dots and includes instructions on how to fold it up (your puzzle input). For example:
#  
#      6,10
#      0,14
#      9,10
#      0,3
#      10,4
#      4,11
#      6,0
#      6,12
#      4,1
#      0,13
#      10,12
#      3,4
#      3,0
#      8,4
#      1,10
#      2,14
#      8,10
#      9,0
#  
#      fold along y=7
#      fold along x=5
#  
#  The first section is a list of dots on the transparent paper. 0,0 represents the top-left coordinate. 
#  The first value, x, increases to the right. The second value, y, increases downward. So, the coordinate 3,0 is 
#  to the right of 0,0, and the coordinate 0,7 is below 0,0. The coordinates in this example form the following 
#  pattern, where # is a dot on the paper and . is an empty, unmarked position:
#  
#      ...#..#..#.
#      ....#......
#      ...........
#      #..........
#      ...#....#.#
#      ...........
#      ...........
#      ...........
#      ...........
#      ...........
#      .#....#.##.
#      ....#......
#      ......#...#
#      #..........
#      #.#........
#  
#  Then, there is a list of fold instructions. Each instruction indicates a line on the transparent paper 
#  and wants you to fold the paper up (for horizontal y=... lines) or left (for vertical x=... lines).
#  In this example, the first fold instruction is fold along y=7, which designates the line formed by all 
#  of the positions where y is 7 (marked here with -):
#  
#      ...#..#..#.
#      ....#......
#      ...........
#      #..........
#      ...#....#.#
#      ...........
#      ...........
#      -----------
#      ...........
#      ...........
#      .#....#.##.
#      ....#......
#      ......#...#
#      #..........
#      #.#........
#  
#  Because this is a horizontal line, fold the bottom half up. Some of the dots might end up overlapping 
#  after the fold is complete, but dots will never appear exactly on a fold line. The result of doing 
#  this fold looks like this:
#  
#      #.##..#..#.
#      #...#......
#      ......#...#
#      #...#......
#      .#.#..#.###
#      ...........
#      ...........
#  
#  Now, only 17 dots are visible.
#  
#  Notice, for example, the two dots in the bottom left corner before the transparent paper is folded; 
#  after the fold is complete, those dots appear in the top left corner (at 0,0 and 0,1). Because the 
#  paper is transparent, the dot just below them in the result (at 0,3) remains visible, as it can be 
#  seen through the transparent paper.
#  
#  Also notice that some dots can end up overlapping; in this case, the dots merge together and become a single dot.
#  
#  The second fold instruction is fold along x=5, which indicates this line:
#  
#      #.##.|#..#.
#      #...#|.....
#      .....|#...#
#      #...#|.....
#      .#.#.|#.###
#      .....|.....
#      .....|.....
#  
#  Because this is a vertical line, fold left:
#  
#      #####
#      #...#
#      #...#
#      #...#
#      #####
#      .....
#      .....
#  
#  The instructions made a square!
#  
#  The transparent paper is pretty big, so for now, focus on just completing the first fold. After the 
#  first fold in the example above, 17 dots are visible - dots that end up overlapping after the fold 
#  is completed count as a single dot.
#  
#  How many dots are visible after completing just the first fold instruction on your transparent paper?
#  
#  


# read into map
def read_transparency(filename):
    lines = read_file_into_array(filename, False)
    # print(lines)
    transparency = {}
    fold_instructions = []

    on_dots = True
    for line in lines:
        if line == "":
            on_dots = False
            continue

        if on_dots:
            parts = line.split(",")
            transparency[(int(parts[0]), int(parts[1]))] = "#"

        else:
            fold_instructions.append(line)

    return transparency, fold_instructions


def fold(transparency, instruction):
    parts = instruction.split("=")
    if parts[0] == "fold along y":
        return fold_up(transparency, int(parts[1]))
    else:
        return fold_left(transparency, int(parts[1]))
### fold


def fold_up(transparency, fold):
    folded_transparency = {}

    for k in transparency:
        x = k[0]
        y = transform_axis_point(k[1], fold)

        folded_transparency[(x,y)] = "#"
    return folded_transparency



def fold_left(transparency, fold):
    folded_transparency = {}

    for k in transparency:
        x = transform_axis_point(k[0], fold)
        y = k[1]

        folded_transparency[(x,y)] = "#"
    return folded_transparency


def transform_axis_point(point, fold):
    if point == fold:
        raise Error()
    elif point < fold:
        return point
    else:
        return fold - (point - fold)


# function - get dot count
def count_dots(transparency):
    return len(transparency)



class Day13PartOneTests(unittest.TestCase):

    
    def test__part_1__sample_input(self):
        print("")
        transparency, fold_instructions = read_transparency(sample_input_file_1)
        
        dot_count = count_dots(transparency)
        self.assertEqual(18, dot_count)

        folded_transparency = fold(transparency, fold_instructions[0])
        dot_count = count_dots(folded_transparency)
        self.assertEqual(17, dot_count)



    def test__part_1__challenge_input(self):
        print("")
        transparency, fold_instructions = read_transparency(input_file)
        folded_transparency = fold(transparency, fold_instructions[0])
        dot_count = count_dots(folded_transparency)
        print("Solution to day 13 part 1: {0}".format(dot_count))
        



###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################


def print_transparency_as_grid(transparency):
    # determine size
    max_x = -1
    max_y = -1
    for k in transparency:
        if k[0] > max_x:
            max_x = k[0]

        if k[1] > max_y:
            max_y = k[1]


    # print(max_x)
    # print(max_y)
    # fill in the array
    grid = []
    for _ in range(max_y +1):
        grid.append([" " for i in range(max_x+1)])

    for k in transparency:
        # print("({0}, {1})".format(k[0], k[1]))
        grid[k[1]][k[0]] = "#"


    # print it
    for line in grid:
        print("".join(line))


class Day13PartTwoTests(unittest.TestCase):

    

    def test__part_2__challenge_input(self):
        print("")
        transparency, fold_instructions = read_transparency(input_file)

        for instruction in fold_instructions:
            transparency =  fold(transparency, instruction)

        
        print("Solution to day 13 part 2:")
        print_transparency_as_grid(transparency)
        
        
    pass

# print("Solution to day 13 part 2: {0}".format(-1))
 

 
###################################################################################################################################################################
########################################################################## RUN THE TESTS ##########################################################################


# run then unit tests "last"
if __name__ == '__main__':
    unittest.main()
 

