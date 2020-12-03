#!/bin/python
# -*- coding: utf-8 -*-
# https://adventofcode.com/2020/day/3


###################################################################################################################################################################
#  
#  Solution to day 3 part 1: 209
#
#  Solution to day 3 part 2: 1574890240
#
###################################################################################################################################################################


###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################
#  
#  
#  --- Day 3: Toboggan Trajectory ---
#  
#  With the toboggan login problems resolved, you set off toward the airport. While travel 
#  by toboggan might be easy, it's certainly not safe: there's very minimal steering and 
#  the area is covered in trees. You'll need to see which angles will take you near the 
#  fewest trees.
#  
#  Due to the local geology, trees in this area only grow on exact integer coordinates in 
#  a grid. You make a map (your puzzle input) of the open squares (.) and trees (#) you 
#  can see. For example:
#       
#       ..##.......
#       #...#...#..
#       .#....#..#.
#       ..#.#...#.#
#       .#...##..#.
#       ..#.##.....
#       .#.#.#....#
#       .#........#
#       #.##...#...
#       #...##....#
#       .#..#...#.#
#       
#  These aren't the only trees, though; due to something you read about once involving arboreal 
#  genetics and biome stability, the same pattern repeats to the right many times:
#  
#       ..##.........##.........##.........##.........##.........##.......  --->
#       #...#...#..#...#...#..#...#...#..#...#...#..#...#...#..#...#...#..
#       .#....#..#..#....#..#..#....#..#..#....#..#..#....#..#..#....#..#.
#       ..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#
#       .#...##..#..#...##..#..#...##..#..#...##..#..#...##..#..#...##..#.
#       ..#.##.......#.##.......#.##.......#.##.......#.##.......#.##.....  --->
#       .#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#
#       .#........#.#........#.#........#.#........#.#........#.#........#
#       #.##...#...#.##...#...#.##...#...#.##...#...#.##...#...#.##...#...
#       #...##....##...##....##...##....##...##....##...##....##...##....#
#       .#..#...#.#.#..#...#.#.#..#...#.#.#..#...#.#.#..#...#.#.#..#...#.#  --->
#  
#  You start on the open square (.) in the top-left corner and need to reach the bottom 
#  (below the bottom-most row on your map).
#  
#  The toboggan can only follow a few specific slopes (you opted for a cheaper model that prefers 
#  rational numbers); start by counting all the trees you would encounter for the slope right 3, down 1:
#  
#  From your starting position at the top-left, check the position that is right 3 and down 1. 
#  Then, check the position that is right 3 and down 1 from there, and so on until you go past 
#  the bottom of the map.
#  
#  The locations you'd check in the above example are marked here with O where there was an open 
#  square and X where there was a tree:
#  
#       ..##.........##.........##.........##.........##.........##.......  --->
#       #..O#...#..#...#...#..#...#...#..#...#...#..#...#...#..#...#...#..
#       .#....X..#..#....#..#..#....#..#..#....#..#..#....#..#..#....#..#.
#       ..#.#...#O#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#
#       .#...##..#..X...##..#..#...##..#..#...##..#..#...##..#..#...##..#.
#       ..#.##.......#.X#.......#.##.......#.##.......#.##.......#.##.....  --->
#       .#.#.#....#.#.#.#.O..#.#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#
#       .#........#.#........X.#........#.#........#.#........#.#........#
#       #.##...#...#.##...#...#.X#...#...#.##...#...#.##...#...#.##...#...
#       #...##....##...##....##...#X....##...##....##...##....##...##....#
#       .#..#...#.#.#..#...#.#.#..#...X.#.#..#...#.#.#..#...#.#.#..#...#.#  --->
#  
#  In this example, traversing the map using this slope would cause you to encounter 7 trees.
#  
#  Starting at the top-left corner of your map and following a slope of right 3 and down 1, 
#  how many trees would you encounter?
#  


SLOPE_TREE  = "#"
SLOPE_CLEAR = "."

input_file = "2020_03_sample.txt"
input_file = "2020_03_input.txt"

hill_lines = []
with open(input_file) as f:
    drift = 0
    for line in f:
        hill_lines.append(line)
        

def process_next_slope(slope, position, slide_distance):
    # input: 
    #   slope - next line in the file, showing where the trees are
    #   position - where in the line did we start? we will then move
    #   slide_distance - how far will we move to the right?
    # output:
    #   num_trees_hit - did we hit a tree? 0 or 1
    #   updated_position - where did we stop?

    length_of_slope = len(slope)
    updated_position = position + slide_distance
    modulo_position = updated_position % length_of_slope

    # debug lines
    # print("---------")
    # print(" pos_org: ", position)
    # print(" pos_new: ", updated_position)
    # print(" pos_mod: ", modulo_position)
    # print("   slope: ", slope)
    # print("    stop: ", slope[modulo_position])

    if slope[modulo_position] == SLOPE_TREE:
        return 1, updated_position
    else:
        return 0, updated_position
### process_next_slope

SLIDE_DISTANCE_RIGHT = 3
position = -SLIDE_DISTANCE_RIGHT
tree_collision_count = 0

for slope in hill_lines:
    num_trees_hit, position = process_next_slope(slope.strip(), position, SLIDE_DISTANCE_RIGHT)
    tree_collision_count += num_trees_hit
    


print( "Solution to day 3 part 1: ", tree_collision_count)



###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################
# 
# 
# --- Part Two ---
# 
# Time to check the rest of the slopes - you need to minimize the probability of a sudden 
# arboreal stop, after all.
# 
# Determine the number of trees you would encounter if, for each of the following slopes, 
# you start at the top-left corner and traverse the map all the way to the bottom:
# 
#     Right 1, down 1.
#     Right 3, down 1. (This is the slope you already checked.)
#     Right 5, down 1.
#     Right 7, down 1.
#     Right 1, down 2.
# 
# In the above example, these slopes would find 2, 7, 3, 4, and 2 tree(s) respectively; 
# multiplied together, these produce the answer 336.
# 
# What do you get if you multiply together the number of trees encountered on each of the listed slopes?
# 
# 

def process_slope(slopes, right, down):
    # input: 
    #   slopes - listing of all the slopes that make up the hill
    #   right - distance to travel right with each step
    #   down - distance to travel down with each step
    # output:
    #   num_trees_hit
    slope_count = -1
    position = -right
    tree_collision_count = 0


    for slope in hill_lines:
        slope_count += 1

        # handle going down first
        if slope_count % down != 0:
            continue

        # then handle going right.
        num_trees_hit, position = process_next_slope(slope.strip(), position, right)
        tree_collision_count += num_trees_hit


    print("process_slope: right=", right, "\tdown=", down, "\tcollisions=", tree_collision_count)

    return tree_collision_count
### process_slope

a = process_slope(hill_lines, 1, 1)
b = process_slope(hill_lines, 3, 1)
c = process_slope(hill_lines, 5, 1)
d = process_slope(hill_lines, 7, 1)
e = process_slope(hill_lines, 1, 2)


 

print( "Solution to day 3 part 2: ", a*b*c*d*e)



