#!/bin/python
# -*- coding: utf-8 -*-
# https://adventofcode.com/2021/day/5


###################################################################################################################################################################
#  
#  Solution to day 5 part 1: 6311
#
#  Solution to day 5 part 2: 19929
#
###################################################################################################################################################################

import unittest
import re

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

###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################
#
#  --- Day 5: Hydrothermal Venture ---
#  You come across a field of hydrothermal vents on the ocean floor! These vents constantly produce large, opaque clouds, 
#  so it would be best to avoid them if possible.
#  
#  They tend to form in lines; the submarine helpfully produces a list of nearby lines of vents (your puzzle input) for 
#  you to review. For example:
#  
#      0,9 -> 5,9
#      8,0 -> 0,8
#      9,4 -> 3,4
#      2,2 -> 2,1
#      7,0 -> 7,4
#      6,4 -> 2,0
#      0,9 -> 2,9
#      3,4 -> 1,4
#      0,0 -> 8,8
#      5,5 -> 8,2
#  
#  Each line of vents is given as a line segment in the format x1,y1 -> x2,y2 where x1,y1 are the coordinates of one end 
#  the line segment and x2,y2 are the coordinates of the other end. These line segments include the points at both ends. 
#  In other words:
#  
#      An entry like 1,1 -> 1,3 covers points 1,1, 1,2, and 1,3.
#      An entry like 9,7 -> 7,7 covers points 9,7, 8,7, and 7,7.
#  
#  For now, only consider horizontal and vertical lines: lines where either x1 = x2 or y1 = y2.
#  
#  So, the horizontal and vertical lines from the above list would produce the following diagram:
#  
#      .......1..
#      ..1....1..
#      ..1....1..
#      .......1..
#      .112111211
#      ..........
#      ..........
#      ..........
#      ..........
#      222111....
#  
#  In this diagram, the top left corner is 0,0 and the bottom right corner is 9,9. Each position is shown as the number of 
#  lines which cover that point or . if no line covers that point. The top-left pair of 1s, for example, comes from 2,2 -> 2,1; 
#  the very bottom row is formed by the overlapping lines 0,9 -> 5,9 and 0,9 -> 2,9.
#  
#  To avoid the most dangerous areas, you need to determine the number of points where at least two lines overlap. In the 
#  above example, this is anywhere in the diagram with a 2 or larger - a total of 5 points.
#  
#  Consider only horizontal and vertical lines. At how many points do at least two lines overlap?
#  
#  


def parse_line_segments(input_data):
    lines = []
    for line_segment in input_data:
        line_parts = re.split(",| -> ", line_segment)
        line = {"x1": int(line_parts[0]), "y1": int(line_parts[1]), "x2": int(line_parts[2]), "y2": int(line_parts[3])}
        lines.append(line)

    return lines
### parse_line_segments


def increase_vent_count(vents, x, y):
    k = (x,y)
    # print("\t\tstoring point: {0}".format(k))
    if k in vents:
        vents[k] += 1
    else:
        vents[k] = 1
### increase_vent_count

def handle_line_direction(p1, p2, pp1=None, pp2=None):
    if p1 < p2:
        return p1, p2, pp1, pp2
    else:
        return p2, p1, pp2, pp1

def count_intersections(lines, include_diagonals, debug=False):
    thermal_vent_locations = {}
    intersection_count = 0

    # fill in the points
    for line in lines:
        # print("loading line: {0}".format(line))

        # single point
        if line["x1"] == line["x2"] and line["y1"] == line["y2"]:
            increase_vent_count(thermal_vent_locations, line["x1"], line["y1"])


        # horizontal
        elif line["x1"] == line["x2"]:
            y1 = line["y1"]
            y2 = line["y2"]
            y1, y2, _, _ = handle_line_direction(y1, y2)

            for i in range(y2 - y1 + 1):
                increase_vent_count(thermal_vent_locations, line["x1"], y1 + i)


        # vertical
        elif line["y1"] == line["y2"]:
            x1 = line["x1"]
            x2 = line["x2"]
            x1, x2, _, _ = handle_line_direction(x1, x2)
            for i in range(x2 - x1 + 1):
                increase_vent_count(thermal_vent_locations, x1 + i, line["y1"])

        # diagonal
        elif include_diagonals:
            #  1) start on left end, go towards right
            x1 = line["x1"]
            x2 = line["x2"]
            y1 = line["y1"]
            y2 = line["y2"]
            x1, x2, y1, y2 = handle_line_direction(x1, x2, y1, y2)

            #  2) going up or down
            # result = <value_if_true> if <condition> else <value_if_false>
            step = 1 if y1 < y2 else -1

            #  3) fill in the points
            for i in range(x2 - x1 + 1):
                increase_vent_count(thermal_vent_locations, x1 + i, y1)
                y1 += step


    if debug:
        print("--- vents")
        print(thermal_vent_locations)
        print("^^^ vents")

    # count the intersections
    for point in thermal_vent_locations:
        if thermal_vent_locations[point] > 1:
            intersection_count += 1

    return intersection_count
### count_intersections


class Day5PartOneTests(unittest.TestCase):

    def test__part_1__no_interestions(self):
        raw_segements = ["5,5 -> 8,2"]
        line_segments = parse_line_segments(raw_segements)
        intersections = count_intersections(line_segments, False)
        self.assertEqual(intersections, 0)

    def test__part_1__horizontal_interestion(self):
        raw_segements = ["0,9 -> 5,9", "0,9 -> 2,9"]
        line_segments = parse_line_segments(raw_segements)
        intersections = count_intersections(line_segments, False)
        self.assertEqual(intersections, 3)

    def test__part_1__vertical_interestion(self):
        raw_segements = ["9,0 -> 9,5", "9,0 -> 9,4"]
        line_segments = parse_line_segments(raw_segements)
        intersections = count_intersections(line_segments, False)
        self.assertEqual(intersections, 5)

    def test__part_1__vert_and_hor_interestions(self):
        raw_segements = ["0,2 -> 4,2", "3,0 -> 3,4"]
        line_segments = parse_line_segments(raw_segements)
        intersections = count_intersections(line_segments, False)
        self.assertEqual(intersections, 1)

    def test__part_1__single_point_interestion(self):
        raw_segements = ["9,0 -> 9,5", "9,2 -> 9,2"]
        line_segments = parse_line_segments(raw_segements)
        intersections = count_intersections(line_segments, False)
        self.assertEqual(intersections, 1)

    

    def test__part_1__sample_input(self):
        print("")
        raw_segements = read_file_into_array(sample_input_file_1, False)
        line_segments = parse_line_segments(raw_segements)
        intersections = count_intersections(line_segments, False, False)
        self.assertEqual(intersections, 5)


    def test__part_1__challenge_input(self):
        print("")
        raw_segements = read_file_into_array(input_file, False)
        line_segments = parse_line_segments(raw_segements)
        intersections = count_intersections(line_segments, False, False)
        print("Solution to day 5 part 1: {0}".format(intersections))

        


###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################
#  
#  --- Part Two ---
#  Unfortunately, considering only horizontal and vertical lines doesn't give you the full picture; you 
#  need to also consider diagonal lines.
#  
#  Because of the limits of the hydrothermal vent mapping system, the lines in your list will only ever 
#  be horizontal, vertical, or a diagonal line at exactly 45 degrees. In other words:
#  
#      An entry like 1,1 -> 3,3 covers points 1,1, 2,2, and 3,3.
#      An entry like 9,7 -> 7,9 covers points 9,7, 8,8, and 7,9.
#  
#  Considering all lines from the above example would now produce the following diagram:
#  
#      1.1....11.
#      .111...2..
#      ..2.1.111.
#      ...1.2.2..
#      .112313211
#      ...1.2....
#      ..1...1...
#      .1.....1..
#      1.......1.
#      222111....
#  
#  You still need to determine the number of points where at least two lines overlap. In the above example, 
#  this is still anywhere in the diagram with a 2 or larger - now a total of 12 points.
#  
#  Consider all of the lines. At how many points do at least two lines overlap?
#  


class Day5PartTwoTests(unittest.TestCase):


    def test__part_2__two_diagonal_interestion(self):
        raw_segements = ["0,0 -> 4,4", "0,4 -> 4,0"]
        line_segments = parse_line_segments(raw_segements)
        intersections = count_intersections(line_segments, True)
        self.assertEqual(intersections, 1)


    def test__part_2__two_diagonal_interestion_reversed(self):
        raw_segements = ["4,4 -> 0,0", "4,0 -> 0,4"]
        line_segments = parse_line_segments(raw_segements)
        intersections = count_intersections(line_segments, True)
        self.assertEqual(intersections, 1)


    def test__part_2__sample_input(self):
        print("")
        raw_segements = read_file_into_array(sample_input_file_1, False)
        line_segments = parse_line_segments(raw_segements)
        intersections = count_intersections(line_segments, True, False)
        self.assertEqual(intersections, 12)

    def test__part_2__challenge_input(self):
        print("")
        raw_segements = read_file_into_array(input_file, False)
        line_segments = parse_line_segments(raw_segements)
        intersections = count_intersections(line_segments, True, False)
        print("Solution to day 5 part 1: {0}".format(intersections))        
 

 
###################################################################################################################################################################
########################################################################## RUN THE TESTS ##########################################################################


# run then unit tests "last"
if __name__ == '__main__':
    unittest.main()
 

