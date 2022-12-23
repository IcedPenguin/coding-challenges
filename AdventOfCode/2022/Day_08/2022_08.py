#!/bin/python
# -*- coding: utf-8 -*-
# https://adventofcode.com/2022/day/8


###################################################################################################################################################################
#  
#  Solution to part 1: 1849
#
#  Solution to part 2: 201600
#
###################################################################################################################################################################

import unittest
from colorama import init
from termcolor import colored

init() # colorama

###################################################################################################################################################################
#   --- Day 8: Treetop Tree House ---
#   
#   The expedition comes across a peculiar patch of tall trees all planted carefully in a grid. The Elves explain that 
#   a previous expedition planted these trees as a reforestation effort. Now, they're curious if this would be a good 
#   location for a tree house.
#   
#   First, determine whether there is enough tree cover here to keep a tree house hidden. To do this, you need to count 
#   the number of trees that are visible from outside the grid when looking directly along a row or column.
#   
#   The Elves have already launched a quadcopter to generate a map with the height of each tree (your puzzle input). For example:
#   
#       30373
#       25512
#       65332
#       33549
#       35390
#   
#   Each tree is represented as a single digit whose value is its height, where 0 is the shortest and 9 is the tallest.
#   
#   A tree is visible if all of the other trees between it and an edge of the grid are shorter than it. Only consider 
#   trees in the same row or column; that is, only look up, down, left, or right from any given tree.
#   
#   All of the trees around the edge of the grid are visible - since they are already on the edge, there are no trees 
#   to block the view. In this example, that only leaves the interior nine trees to consider:
#   
#       The top-left 5 is visible from the left and top. (It isn't visible from the right or bottom since other trees 
#           of height 5 are in the way.)
#       The top-middle 5 is visible from the top and right.
#       The top-right 1 is not visible from any direction; for it to be visible, there would need to only be trees of 
#           height 0 between it and an edge.
#       The left-middle 5 is visible, but only from the right.
#       The center 3 is not visible from any direction; for it to be visible, there would need to be only trees of at 
#           most height 2 between it and an edge.
#       The right-middle 3 is visible from the right.
#       In the bottom row, the middle 5 is visible, but the 3 and 4 are not.
#   
#   With 16 trees visible on the edge and another 5 visible in the interior, a total of 21 trees are visible in this arrangement.
#   
#   Consider your map; how many trees are visible from outside the grid?
#   
############################################################################ PROBLEM 1 ############################################################################


puzzle_day          = 8
sample_input_file_1 = "2022_{0:02d}_sample_1.txt".format(puzzle_day)
input_file          = "2022_{0:02d}_input.txt".format(puzzle_day)


def load_file(file_path):
    file_ptr = open(file_path, "r")
    data = file_ptr.read()
    file_ptr.close()
    return data



def parse_forest(tree_lines):
    forest = {}

    for y in range(len(tree_lines)):
        for x in range(len(tree_lines[y])):
            forest[(x,y)] = (int(tree_lines[y][x]), False, None, -1) # value, visited, is_visible, scenic_score

    forest["size"] = (len(tree_lines[y]), len(tree_lines))

    return forest


def print_forest(forest):
    size = forest["size"]

    print()
    for y in range(size[1]):
        line = ""

        for x in range(size[0]):
            tree = forest[(x,y)]

            if tree[2] is None:
                line += colored(tree[0], 'cyan')
            elif tree[2] is True:
                line += colored(tree[0], 'red') #, 'on_black')
            else:
                line += colored(tree[0], 'green') #, 'on_black')

        print(line)


def walk_trees(forest):
    size = forest["size"]
    width = size[0]
    height = size[1]

    for y in range(height):
        for x in range(width):
            tree = forest[(x, y)]

            trees_in_line_up = get_all_trees_in_line(forest, x, y, width, height, "up")
            trees_in_line_left = get_all_trees_in_line(forest, x, y, width, height, "left")
            trees_in_line_down = get_all_trees_in_line(forest, x, y, width, height, "down")
            trees_in_line_right = get_all_trees_in_line(forest, x, y, width, height, "right")

            visible = is_visible_tree(tree[0], trees_in_line_up) or is_visible_tree(tree[0], trees_in_line_left) or is_visible_tree(tree[0], trees_in_line_down) or is_visible_tree(tree[0], trees_in_line_right)

            forest[(x, y)] = (tree[0], True, visible, tree[3])


def is_visible_tree(tree_height, other_trees):
    if len(other_trees) == 0:
        return True

    not_visible = False
    # if there exists at least one tree taller than target, then hidden
    for tree in other_trees:
        if tree >= tree_height:
            return False

    return True


def get_all_trees_in_line(forest, x, y, width, height, direction):
    trees = []

    if direction == "up":
        for i in range(0, y):
           trees.append(forest[(x, i)][0]) 

    elif direction == "down":
        for i in range(y+1, height):
           trees.append(forest[(x, i)][0]) 

    elif direction == "left":
        for i in range(0, x):
            trees.append(forest[(i, y)][0])

    else: #elif direction == "right":
        for i in range(x+1, width):
            trees.append(forest[(i, y)][0])

    return trees


def find_interior_trees(input_file):
    tree_lines = load_file(input_file)
    tree_lines = tree_lines.split("\n")
    forest = parse_forest(tree_lines)
    walk_trees(forest)
    print_forest(forest)
    return forest


def count_visible_trees(forest):
    count = 0
    for key in forest:
        if key != "size":
            if forest[key][2]:
                count += 1

    return count


class Day8PartOneTests(unittest.TestCase):


    
    def test__p1__is_visible_tree(self):
        self.assertEqual(is_visible_tree(3, []), True)
        self.assertEqual(is_visible_tree(3, [1]), True)
        self.assertEqual(is_visible_tree(3, [3]), False)
        self.assertEqual(is_visible_tree(3, [4]), False)
        self.assertEqual(is_visible_tree(3, [1,2,3]), False)
        

    #  30373
    #  25512
    #  65332
    #  33549
    #  35390
    def test__p1__get_all_trees_in_line(self):
        forest = parse_forest(["30373","25512","65332","33549","35390"])
        self.assertEqual(get_all_trees_in_line(forest, 0, 0, 5, 5, "up"), [])
        self.assertEqual(get_all_trees_in_line(forest, 0, 0, 5, 5, "down"), [2,6,3,3])

        self.assertEqual(get_all_trees_in_line(forest, 1, 2, 5, 5, "up"), [0,5])
        self.assertEqual(get_all_trees_in_line(forest, 1, 2, 5, 5, "down"), [3,5])
        self.assertEqual(get_all_trees_in_line(forest, 1, 2, 5, 5, "left"), [6])
        self.assertEqual(get_all_trees_in_line(forest, 1, 2, 5, 5, "right"), [3,3,2])


    def test__p1__sample1(self):
        print()
        forest = find_interior_trees(sample_input_file_1)
        count = count_visible_trees(forest)
        self.assertEqual(count, 21)


    def test__part_1__challenge_input(self):
        print("")
        forest = find_interior_trees(input_file)
        count = count_visible_trees(forest)        
        print("Solution to day {0} part 1: {1}".format(puzzle_day, count))
        


###################################################################################################################################################################
#   --- Part Two ---
#   
#   Content with the amount of tree cover available, the Elves just need to know the best spot to build their tree house: 
#   they would like to be able to see a lot of trees.
#   
#   To measure the viewing distance from a given tree, look up, down, left, and right from that tree; stop if you reach an 
#   edge or at the first tree that is the same height or taller than the tree under consideration. (If a tree is right on 
#       the edge, at least one of its viewing distances will be zero.)
#   
#   The Elves don't care about distant trees taller than those found by the rules above; the proposed tree house has large 
#   eaves to keep it dry, so they wouldn't be able to see higher than the tree house anyway.
#   
#   In the example above, consider the middle 5 in the second row:
#   
#       30373
#       25512
#       65332
#       33549
#       35390
#   
#       Looking up, its view is not blocked; it can see 1 tree (of height 3).
#       Looking left, its view is blocked immediately; it can see only 1 tree (of height 5, right next to it).
#       Looking right, its view is not blocked; it can see 2 trees.
#       Looking down, its view is blocked eventually; it can see 2 trees (one of height 3, then the tree of height 5 that 
#           blocks its view).
#   
#   A tree's scenic score is found by multiplying together its viewing distance in each of the four directions. For this 
#   tree, this is 4 (found by multiplying 1 * 1 * 2 * 2).
#   
#   However, you can do even better: consider the tree of height 5 in the middle of the fourth row:
#   
#       30373
#       25512
#       65332
#       33549
#       35390
#   
#       Looking up, its view is blocked at 2 trees (by another tree with a height of 5).
#       Looking left, its view is not blocked; it can see 2 trees.
#       Looking down, its view is also not blocked; it can see 1 tree.
#       Looking right, its view is blocked at 2 trees (by a massive tree of height 9).
#   
#   This tree's scenic score is 8 (2 * 2 * 1 * 2); this is the ideal spot for the tree house.
#   
#   Consider each tree on your map. What is the highest scenic score possible for any tree?
#   
############################################################################ PROBLEM 2 ############################################################################

def calculate_scenic_scores(forest):
    max_score = -1

    size = forest["size"]
    width = size[0]
    height = size[1]

    for y in range(height):
        for x in range(width):
            tree = forest[(x, y)]

            trees  = get_all_trees_in_line(forest, x, y, width, height, "up")
            trees.reverse()
            score_u = scenic_score(tree[0], trees)

            trees  = get_all_trees_in_line(forest, x, y, width, height, "left")
            trees.reverse()
            score_l = scenic_score(tree[0], trees)

            score_d = scenic_score(tree[0], get_all_trees_in_line(forest, x, y, width, height, "down"))
            score_r = scenic_score(tree[0], get_all_trees_in_line(forest, x, y, width, height, "right"))

            score = score_u * score_l * score_d * score_r

            forest[(x, y)] = (tree[0], tree[1], tree[2], score)

            if score > max_score:
                max_score = score

    return max_score

# in one direction. assiming index 0 is closest to the tree.
def scenic_score(tree_height, line_of_sight_trees):
    score = 0
    for i in range(len(line_of_sight_trees)):
        if tree_height > line_of_sight_trees[i]:
            score += 1 
        else:
            score += 1 
            break

    return score



class Day8PartTwoTests(unittest.TestCase):
    
    def test__p2__sample1(self):
        print()
        forest = find_interior_trees(sample_input_file_1)
        score = calculate_scenic_scores(forest)
        self.assertEqual(score, 8)
        

    def test__part_2__challenge_input(self):
        print("")
        forest = find_interior_trees(input_file)
        score = calculate_scenic_scores(forest)
        print("Solution to day {0} part 2: {1}".format(puzzle_day, score))


 
###################################################################################################################################################################
########################################################################## RUN THE TESTS ##########################################################################


# run then unit tests "last"
if __name__ == '__main__':
    unittest.main()
 

