#!/bin/python
# -*- coding: utf-8 -*-
# https://adventofcode.com/2021/day/9


###################################################################################################################################################################
#  
#  Solution to day 9 part 1: 462
#
#  Solution to day 9 part 2: 1397760
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
#  --- Day 9: Smoke Basin ---
#  These caves seem to be lava tubes. Parts are even still volcanically active; small hydrothermal 
#  vents release smoke into the caves that slowly settles like rain.
#  
#  If you can model how the smoke flows through the caves, you might be able to avoid it and be that 
#  much safer. The submarine generates a heightmap of the floor of the nearby caves for you (your puzzle input).
#  
#  Smoke flows to the lowest point of the area it's in. For example, consider the following heightmap:
#  
#      2199943210
#      3987894921
#      9856789892
#      8767896789
#      9899965678
#  
#  Each number corresponds to the height of a particular location, where 9 is the highest and 0 is the 
#  lowest a location can be.
#  
#  Your first goal is to find the low points - the locations that are lower than any of its adjacent 
#  locations. Most locations have four adjacent locations (up, down, left, and right); locations on the 
#  edge or corner of the map have three or two adjacent locations, respectively. (Diagonal locations do 
#      not count as adjacent.)
#  
#  In the above example, there are four low points, all highlighted: two are in the first row (a 1 and a 0), 
#  one is in the third row (a 5), and one is in the bottom row (also a 5). All other locations on the 
#  heightmap have some lower adjacent location, and so are not low points.
#  
#  The risk level of a low point is 1 plus its height. In the above example, the risk levels of the low 
#  points are 2, 1, 6, and 6. The sum of the risk levels of all low points in the heightmap is therefore 15.
#  
#  Find all of the low points on your heightmap. What is the sum of the risk levels of all low points on your heightmap?
#  


def create_map(input_map):
    height = len(input_map)
    height_map = {}

    width = len(input_map[0])
    height = len(input_map)

    for w in range(width):
        for h in range(height):
            height_map[(w,h)] = input_map[h][w]

    return height_map, width, height
### create_map


def find_low_points(height_map, width, height):
    low_points = []

    for h in range(height):
        for w in range(width):
            if is_low_point(height_map, w, h):
                low_points.append( (w, h, height_map[(w,h)] ) )

    return low_points
### find_low_points


def is_low_point(height_map, w, h):
    
    point = height_map.get((w  ,h  ))

    above = height_map.get((w  ,h-1))
    below = height_map.get((w  ,h+1))
    left  = height_map.get((w-1,h  ))
    right = height_map.get((w+1,h  ))


    if above is not None and point >= above:
        return False

    if below is not None and point >= below:
        return False

    if left is not None and point >= left:
        return False

    if right is not None and point >= right:
        return False

    # print("low point found: {1} : {0} -> {2} {3} {4} {5}".format(point, (w,h), above, below, left,right))

    return True
### is_low_point


def print_map(height_map):
    for m in height_map:
        print(m)


def calculate_risk_score(low_points):
    risk_score = 0
    for point in low_points:
        risk_score += int(point[2]) + 1

    return risk_score


class Day9PartOneTests(unittest.TestCase):

    
    def test__part_1__sample_input(self):
        print("")
        height_map, width, height = create_map(read_file_into_array(sample_input_file_1, False))
        low_points = find_low_points(height_map, width, height)
        risk_score = calculate_risk_score(low_points)
        
        self.assertEqual(15, risk_score)
        
        

    def test__part_1__challenge_input(self):
        print("")
        height_map, width, height = create_map(read_file_into_array(input_file, False))
        low_points = find_low_points(height_map, width, height)
        risk_score = calculate_risk_score(low_points)
        print("Solution to day  9 part 1: {0}".format(risk_score))
        


###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################
#  
#  
#  --- Part Two ---
#  Next, you need to find the largest basins so you know what areas are most important to avoid.
#  
#  A basin is all locations that eventually flow downward to a single low point. Therefore, every 
#  low point has a basin, although some basins are very small. Locations of height 9 do not count 
#  as being in any basin, and all other locations will always be part of exactly one basin.
#  
#  The size of a basin is the number of locations within the basin, including the low point. The 
#  example above has four basins.
#  
#  The top-left basin, size 3:
#  
#      2199943210
#      3987894921
#      9856789892
#      8767896789
#      9899965678
#  
#  The top-right basin, size 9:
#  
#      2199943210
#      3987894921
#      9856789892
#      8767896789
#      9899965678
#  
#  The middle basin, size 14:
#  
#      2199943210
#      3987894921
#      9856789892
#      8767896789
#      9899965678
#  
#  The bottom-right basin, size 9:
#  
#      2199943210
#      3987894921
#      9856789892
#      8767896789
#      9899965678
#  
#  Find the three largest basins and multiply their sizes together. 
#  In the above example, this is 9 * 14 * 9 = 1134.
#  
#  What do you get if you multiply together the sizes of the three largest basins?
#  

def get_basin_sizes(height_map, low_points):
    sizes = []
    for point in low_points:
        sizes.append( get_basin_size(height_map, point) )

    return sorted(sizes, reverse=True)


def get_basin_size(height_map, low_point):
    POINT_VISITED = "_"

    basin_size = 0
    points_left_to_visit = [low_point]

    while len(points_left_to_visit) > 0:
        test_point = points_left_to_visit.pop()

        x = test_point[0]
        y = test_point[1]
        

        # avoid double counting
        if height_map[(x, y)] == POINT_VISITED:
            continue
        
        # print("point: x={0} y={1}   v={2}".format(x, y, height_map[(x, y)]))
        # mark the current spot as visited
        height_map[(x, y)] = POINT_VISITED
        basin_size += 1

        # look at neighbors
        above = height_map.get((x, y-1))
        if above is not None and above != POINT_VISITED and above != "9":
            points_left_to_visit.append(( x, y-1, above))

        below = height_map.get((x  ,y+1))
        if below is not None and below != POINT_VISITED and below != "9":
            points_left_to_visit.append(( x, y+1, below))

        left  = height_map.get((x-1,y  ))
        if left is not None and left != POINT_VISITED and left != "9":
            points_left_to_visit.append(( x-1, y, left))

        right = height_map.get((x+1,y  ))
        if right is not None and right != POINT_VISITED and right != "9":
            points_left_to_visit.append((x+1, y, right))

    return basin_size


class Day9PartTwoTests(unittest.TestCase):

    
    def test__part_2__sample_input(self):
        print("")
        height_map, width, height = create_map(read_file_into_array(sample_input_file_1, False))
        low_points = find_low_points(height_map, width, height)
        
        top_left_basin = get_basin_size(height_map, (0,0,1))
        self.assertEqual(3, top_left_basin)

        top_left_basin = get_basin_size(height_map, (9,0,1))
        self.assertEqual(9, top_left_basin)

        top_left_basin = get_basin_size(height_map, (3,3,1))
        self.assertEqual(14, top_left_basin)

        top_left_basin = get_basin_size(height_map, (6,4,1))
        self.assertEqual(9, top_left_basin)


    def test__part_2__sample_input_b(self):
        print("")
        height_map, width, height = create_map(read_file_into_array(sample_input_file_1, False))
        low_points = find_low_points(height_map, width, height)
        basin_sizes_sorted = get_basin_sizes(height_map, low_points)
        self.assertEqual(1134, basin_sizes_sorted[0] * basin_sizes_sorted[1] * basin_sizes_sorted[2])


    def test__part_2__challenge_input(self):
        print("")
        height_map, width, height = create_map(read_file_into_array(input_file, False))
        low_points = find_low_points(height_map, width, height)
        basin_sizes_sorted = get_basin_sizes(height_map, low_points)
        print("Solution to day  9 part 2: {0}".format(basin_sizes_sorted[0] * basin_sizes_sorted[1] * basin_sizes_sorted[2]))
        

 
###################################################################################################################################################################
########################################################################## RUN THE TESTS ##########################################################################


# run then unit tests "last"
if __name__ == '__main__':
    unittest.main()
 

