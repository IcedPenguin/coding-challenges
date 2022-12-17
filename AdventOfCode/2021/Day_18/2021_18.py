#!/bin/python
# -*- coding: utf-8 -*-
# https://adventofcode.com/2021/day/18


###################################################################################################################################################################
#  
#  Solution to part 1: 4173
#
#  Solution to part 2: 4706
#
###################################################################################################################################################################

import unittest
import math

####################################################################################################################################################################
#  --- Day 18: Snailfish ---
#  
#  You descend into the ocean trench and encounter some snailfish. They say they saw the sleigh keys! They'll 
#  even tell you which direction the keys went if you help one of the smaller snailfish with his math homework.
#  
#  Snailfish numbers aren't like regular numbers. Instead, every snailfish number is a pair - an ordered list of 
#  two elements. Each element of the pair can be either a regular number or another pair.
#  
#  Pairs are written as [x,y], where x and y are the elements within the pair. Here are some example snailfish 
#  numbers, one snailfish number per line:
#  
#      [1,2]
#      [[1,2],3]
#      [9,[8,7]]
#      [[1,9],[8,5]]
#      [[[[1,2],[3,4]],[[5,6],[7,8]]],9]
#      [[[9,[3,8]],[[0,9],6]],[[[3,7],[4,9]],3]]
#      [[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]]
#  
#  This snailfish homework is about addition. To add two snailfish numbers, form a pair from the left and right 
#  parameters of the addition operator. For example, [1,2] + [[3,4],5] becomes [[1,2],[[3,4],5]].
#  
#  There's only one problem: snailfish numbers must always be reduced, and the process of adding two snailfish 
#  numbers can result in snailfish numbers that need to be reduced.
#  
#  To reduce a snailfish number, you must repeatedly do the first action in this list that applies to the 
#  snailfish number:
#  
#      If any pair is nested inside four pairs, the leftmost such pair explodes.
#      If any regular number is 10 or greater, the leftmost such regular number splits.
#  
#  Once no action in the above list applies, the snailfish number is reduced.
#  
#  During reduction, at most one action applies, after which the process returns to the top of the list of actions. 
#  For example, if split produces a pair that meets the explode criteria, that pair explodes before other splits occur.
#  
#  To explode a pair, the pair's left value is added to the first regular number to the left of the exploding pair 
#  (if any), and the pair's right value is added to the first regular number to the right of the exploding pair 
#  (if any). Exploding pairs will always consist of two regular numbers. Then, the entire exploding pair is replaced 
#  with the regular number 0.
#  
#  Here are some examples of a single explode action:
#  
#      [[[[[9,8],1],2],3],4] becomes [[[[0,9],2],3],4] (the 9 has no regular number to its left, so it is not added to any regular number).
#      [7,[6,[5,[4,[3,2]]]]] becomes [7,[6,[5,[7,0]]]] (the 2 has no regular number to its right, and so it is not added to any regular number).
#      [[6,[5,[4,[3,2]]]],1] becomes [[6,[5,[7,0]]],3].
#      [[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]] becomes [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]] (the pair [3,2] is unaffected because the pair [7,3] is further to the left; [3,2] would explode on the next action).
#      [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]] becomes [[3,[2,[8,0]]],[9,[5,[7,0]]]].
#  
#  To split a regular number, replace it with a pair; the left element of the pair should be the regular number 
#  divided by two and rounded down, while the right element of the pair should be the regular number divided by 
#  two and rounded up. For example, 10 becomes [5,5], 11 becomes [5,6], 12 becomes [6,6], and so on.
#  
#  Here is the process of finding the reduced result of [[[[4,3],4],4],[7,[[8,4],9]]] + [1,1]:
#  
#   after addition: [[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]
#   after explode:  [[[[0,7],4],[7,[[8,4],9]]],[1,1]]
#   after explode:  [[[[0,7],4],[15,[0,13]]],[1,1]]
#   after split:    [[[[0,7],4],[[7,8],[0,13]]],[1,1]]
#   after split:    [[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]
#   after explode:  [[[[0,7],4],[[7,8],[6,0]]],[8,1]]
#  
#  Once no reduce actions apply, the snailfish number that remains is the actual result of the addition 
#  operation: [[[[0,7],4],[[7,8],[6,0]]],[8,1]].
#  
#  The homework assignment involves adding up a list of snailfish numbers (your puzzle input). The snailfish numbers 
#  are each listed on a separate line. Add the first snailfish number and the second, then add that result and the 
#  third, then add that result and the fourth, and so on until all numbers in the list have been used once.
#  
#  For example, the final sum of this list is [[[[1,1],[2,2]],[3,3]],[4,4]]:
#  
#      [1,1]
#      [2,2]
#      [3,3]
#      [4,4]
#  
#  The final sum of this list is [[[[3,0],[5,3]],[4,4]],[5,5]]:
#  
#      [1,1]
#      [2,2]
#      [3,3]
#      [4,4]
#      [5,5]
#  
#  The final sum of this list is [[[[5,0],[7,4]],[5,5]],[6,6]]:
#  
#      [1,1]
#      [2,2]
#      [3,3]
#      [4,4]
#      [5,5]
#      [6,6]
#  
#  Here's a slightly larger example:
#  
#      [[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
#      [7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
#      [[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
#      [[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
#      [7,[5,[[3,8],[1,4]]]]
#      [[2,[2,2]],[8,[8,1]]]
#      [2,9]
#      [1,[[[9,3],9],[[9,0],[0,7]]]]
#      [[[5,[7,4]],7],1]
#      [[[[4,2],2],6],[8,7]]
#  
#  The final sum [[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]] is found after adding up the above snailfish numbers:
#  
#        [[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
#      + [7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
#      = [[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]
#  
#        [[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]
#      + [[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
#      = [[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]
#  
#        [[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]
#      + [[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
#      = [[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]
#  
#        [[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]
#      + [7,[5,[[3,8],[1,4]]]]
#      = [[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]]
#  
#        [[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]]
#      + [[2,[2,2]],[8,[8,1]]]
#      = [[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]]
#  
#        [[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]]
#      + [2,9]
#      = [[[[6,6],[7,7]],[[0,7],[7,7]]],[[[5,5],[5,6]],9]]
#  
#        [[[[6,6],[7,7]],[[0,7],[7,7]]],[[[5,5],[5,6]],9]]
#      + [1,[[[9,3],9],[[9,0],[0,7]]]]
#      = [[[[7,8],[6,7]],[[6,8],[0,8]]],[[[7,7],[5,0]],[[5,5],[5,6]]]]
#  
#        [[[[7,8],[6,7]],[[6,8],[0,8]]],[[[7,7],[5,0]],[[5,5],[5,6]]]]
#      + [[[5,[7,4]],7],1]
#      = [[[[7,7],[7,7]],[[8,7],[8,7]]],[[[7,0],[7,7]],9]]
#  
#        [[[[7,7],[7,7]],[[8,7],[8,7]]],[[[7,0],[7,7]],9]]
#      + [[[[4,2],2],6],[8,7]]
#      = [[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]
#  
#  To check whether it's the right answer, the snailfish teacher only checks the magnitude of the final sum. 
#  The magnitude of a pair is 3 times the magnitude of its left element plus 2 times the magnitude of its right 
#  element. The magnitude of a regular number is just that number.
#  
#  For example, the magnitude of [9,1] is 3*9 + 2*1 = 29; the magnitude of [1,9] is 3*1 + 2*9 = 21. Magnitude 
#  calculations are recursive: the magnitude of [[9,1],[1,9]] is 3*29 + 2*21 = 129.
#  
#  Here are a few more magnitude examples:
#  
#      [[1,2],[[3,4],5]] becomes 143.
#      [[[[0,7],4],[[7,8],[6,0]]],[8,1]] becomes 1384.
#      [[[[1,1],[2,2]],[3,3]],[4,4]] becomes 445.
#      [[[[3,0],[5,3]],[4,4]],[5,5]] becomes 791.
#      [[[[5,0],[7,4]],[5,5]],[6,6]] becomes 1137.
#      [[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]] becomes 3488.
#  
#  So, given this example homework assignment:
#  
#      [[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
#      [[[5,[2,8]],4],[5,[[9,9],0]]]
#      [6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
#      [[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
#      [[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
#      [[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
#      [[[[5,4],[7,7]],8],[[8,3],8]]
#      [[9,3],[[9,9],[6,[4,9]]]]
#      [[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
#      [[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
#  
#  The final sum is:
#  
#      [[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]
#  
#  The magnitude of this final sum is 4140.
#  
#  Add up all of the snailfish numbers from the homework assignment in the order they appear. What is the magnitude of the final sum?
#  
############################################################################# PROBLEM 1 ############################################################################


puzzle_day          = 18
sample_input_file_1 = "2021_{0:02d}_sample_1.txt".format(puzzle_day)
input_file          = "2021_{0:02d}_input.txt".format(puzzle_day)



def load_file(file_path):
    file_ptr = open(file_path, "r")
    data = file_ptr.read()
    file_ptr.close()
    return data


class SnailFishNode:

    def __init__(self, string_rep=None, parent=None, left=None, right=None, side=None):
        self.parent = parent
        self.left = left
        self.right = right
        self.side = side

        if string_rep is not None:
            self.parse_node(string_rep)


    def __repr__(self):
        return "[" + str(self.left) + "," + str(self.right) + "]"


    def parse_node(self, number_string):
        # print(number_string)
        # find the "middle" of the number.
        number_string = number_string[1:len(number_string)-1]

        v = 0
        i = 0
        while i < len(number_string):
            if number_string[i] == '[':
                v += 1
            elif number_string[i] == ']':
                v -= 1
            elif number_string[i] == ',' and v == 0: # middle condition
                left = number_string[:i]
                right = number_string[i+1:]
                break
            i += 1

        # we have the middle. build out the two sides of the node
        if left.isnumeric():
            self.left = int(left)
        else:
            self.left = SnailFishNode(string_rep=left, parent=self, side="L")

        if right.isnumeric():
            self.right = int(right)
        else:
            self.right = SnailFishNode(string_rep=right, parent=self, side="R")


    def addition(self, other_number):
        new_root = SnailFishNode()
        new_root.left = self 
        new_root.right = other_number

        self.parent = new_root
        self.side = "L"
        other_number.parent = new_root
        other_number.side = "R"

        return new_root


    # The magnitude of a pair is 3 times the magnitude of its left element plus 2 times the magnitude of its right element. 
    # The magnitude of a regular number is just that number.
    def magnitude(self):
        left_mag  = self.left  if type(self.left)  is int else self.left.magnitude()
        right_mag = self.right if type(self.right) is int else self.right.magnitude()
        return 3*left_mag + 2*right_mag


    def reduce(self):
        step = 0
        op = ""
        something_happened = True

        while(something_happened):
            step += 1
            # print("reduce: {0} \t{1}\t -> {2}".format(step, op, self))
            op = " "

            something_happened = False

            something_happened = self.find_node_to_explode()
            if something_happened:
                # print("explode found")
                # print(self)
                op = "explode"
                continue

            something_happened = self.find_and_split_node()
            if something_happened:
                op = "split  "


        step += 1
        # print("reduce: {0} \t{1}\t -> {2}".format(step, op, self))


    def find_node_to_explode(self, depth=0):
        # print("ep: d=" + str(depth) + "\t" + str(self))

        if depth >= 4:
            # print("explode!! \t" + str(self))      
            # print(self.side)      
            # print(self.left)
            # print(self.right)
            explode_left(self.parent, self.side, "up", self.left)
            explode_right(self.parent, self.side, "up", self.right)
            
            # replace this node with 0
            if self.side == "L":
                self.parent.left = 0
            else:
                self.parent.right = 0

            return True # an explosion happened
            # return self  # should this be returnung an "explode happened" like i do for split

        r = False
        if type(self.left) is SnailFishNode:
            r = self.left.find_node_to_explode(depth +1)

        if not r and type(self.right) is SnailFishNode:
            r = self.right.find_node_to_explode(depth +1)

        return r


    def find_and_split_node(self):
        # print("split: n=" + str(self))

        split_happened = False

        if type(self.left) is int:
            if self.left > 9:
                # split this
                child = SnailFishNode()
                child.left = math.floor(self.left / 2) 
                child.right = math.ceil(self.left / 2)
                child.parent = self
                child.side = "L"
                # print("splitting left value: " + str(self.left) + "\t" + str(child))
                self.left = child
                return True
            # else:
            #     return False

        else: # left item is a child node
            split_happened = self.left.find_and_split_node()

        if split_happened:
            return True

        if type(self.right) is int:
            if self.right > 9:
                # split this
                child = SnailFishNode()
                child.left = math.floor(self.right / 2) 
                child.right = math.ceil(self.right / 2)
                child.parent = self
                child.side = "R"
                # print("splitting right value: " + str(self.left) + "\t" + str(child))
                self.right = child
                return True
            else:
                return False

        # else:
        #     split_happened = self.right.find_and_split_node()

        # return split_happened
        return self.right.find_and_split_node()




def explode_left(node, side, direction, value):
    # print("Explode Left: n={0}, s={1}, d={2}, v={3}".format(node, side, direction, value))
    if direction == "up":
        if side == "L":
            if node.parent is not None:
                explode_left(node.parent, node.side, "up", value)

        else: # right
            if type(node.left) is int:
                node.left += value

            else:
                return explode_left(node.left, "R", "down", value)

    else: # down
        if side == "L":
            print("!!!!! this should be unreachable !! left")

        else: # right
            if type(node.right) is int:
                node.right += value

            else:
                explode_left(node.right, "R", "down", value)
### explode_left



def explode_right(node, side, direction, value):
    # print("Explode Right: n={0}, s={1}, d={2}, v={3}".format(node, side, direction, value))
    if direction == "up":
        if side == "R":
            if node.parent is not None:
                explode_right(node.parent, node.side, "up", value)

        else: # left
            if type(node.right) is int:
                node.right += value

            else:
                return explode_right(node.right, "L", "down", value)

    else: # down
        if side == "R":
            print("!!!!! this should be unreachable !! right")

        else: # left
            if type(node.left) is int:
                node.left += value

            else:
                explode_right(node.left, "L", "down", value)


def add_series_of_numbers(number_list):
    sn = SnailFishNode(number_list.pop(0))

    for number in number_list:
        sn_2 = SnailFishNode(number)
        sn = sn.addition(sn_2)
        sn.reduce()

    return sn


class Day18PartOneTests(unittest.TestCase):

    def test__p1__addition(self):
        self.assertEqual(
            str(SnailFishNode("[1,1]").addition(SnailFishNode("[2,2]"))), 
            "[[1,1],[2,2]]"
        )
        self.assertEqual(
            str(SnailFishNode("[[[[4,3],4],4],[7,[[8,4],9]]]").addition(SnailFishNode("[1,1]"))), 
            "[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]"
        )
        self.assertEqual(
            str(SnailFishNode("[1,2]").addition(SnailFishNode("[[3,4],5]"))), 
            "[[1,2],[[3,4],5]]"
        )


    def test__p1__magnitude(self):
        self.assertEqual(SnailFishNode("[9,1]").magnitude(), 29)
        self.assertEqual(SnailFishNode("[1,9]").magnitude(), 21)
        self.assertEqual(SnailFishNode("[[9,1],[1,9]]").magnitude(), 129)
        self.assertEqual(SnailFishNode("[[1,2],[[3,4],5]]").magnitude(), 143)
        self.assertEqual(SnailFishNode("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]").magnitude(), 1384)
        self.assertEqual(SnailFishNode("[[[[1,1],[2,2]],[3,3]],[4,4]]").magnitude(), 445)
        self.assertEqual(SnailFishNode("[[[[3,0],[5,3]],[4,4]],[5,5]]").magnitude(), 791)
        self.assertEqual(SnailFishNode("[[[[5,0],[7,4]],[5,5]],[6,6]]").magnitude(), 1137)
        self.assertEqual(SnailFishNode("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]").magnitude(), 3488)


    def test__p1__explode(self):
        # no explosion
        sn = SnailFishNode("[9,1]")
        sn.find_node_to_explode()
        self.assertEqual(str(sn), "[9,1]")

        # left most fall outside list.
        sn = SnailFishNode("[[[[[9,8],1],2],3],4]")
        sn.find_node_to_explode()
        self.assertEqual(str(sn), "[[[[0,9],2],3],4]")

        # right most falls outside list
        sn = SnailFishNode("[4,[3,[2,[1,[8,9]]]]]")
        sn.find_node_to_explode()
        self.assertEqual(str(sn), "[4,[3,[2,[9,0]]]]")

        # both sides end up in list
        sn = SnailFishNode("[4,[3,[2,[1,[8,9]]]]]")
        sn.find_node_to_explode()
        self.assertEqual(str(sn), "[4,[3,[2,[9,0]]]]")

        # test cases from the website
        sn = SnailFishNode("[[6,[5,[4,[3,2]]]],1]")
        sn.find_node_to_explode()
        self.assertEqual(str(sn), "[[6,[5,[7,0]]],3]")

        sn = SnailFishNode("[7,[6,[5,[4,[3,2]]]]]")
        sn.find_node_to_explode()
        self.assertEqual(str(sn), "[7,[6,[5,[7,0]]]]")

        sn = SnailFishNode("[[6,[5,[4,[3,2]]]],1]")
        sn.find_node_to_explode()
        self.assertEqual(str(sn), "[[6,[5,[7,0]]],3]")

        sn = SnailFishNode("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]")
        sn.find_node_to_explode()
        self.assertEqual(str(sn), "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]")

        sn = SnailFishNode("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]")
        sn.find_node_to_explode()
        self.assertEqual(str(sn), "[[3,[2,[8,0]]],[9,[5,[7,0]]]]")

        sn = SnailFishNode("[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]")
        sn.find_node_to_explode()
        self.assertEqual(str(sn), "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]")
        

    def test__p1__split(self):
        sn = SnailFishNode("[10,2]")
        sn.find_and_split_node()
        self.assertEqual(str(sn), "[[5,5],2]")

        sn = SnailFishNode("[1,[3,11]]")
        sn.find_and_split_node()
        self.assertEqual(str(sn), "[1,[3,[5,6]]]")

        sn = SnailFishNode("[[[[0,7],4],[[7,8],[0,13]]],[1,1]]")
        sn.find_and_split_node()
        self.assertEqual(str(sn), "[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]")


    def test__p1__reduce(self):
        sn = SnailFishNode("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]")
        sn.reduce()
        self.assertEqual(str(sn), "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]")
        

    def test__p1__sum_numbers(self):
        n_l = ["[1,1]", "[2,2]", "[3,3]", "[4,4]"]
        sn = add_series_of_numbers(n_l)
        self.assertEqual(str(sn), "[[[[1,1],[2,2]],[3,3]],[4,4]]")


        n_l = ["[1,1]","[2,2]","[3,3]","[4,4]","[5,5]"]
        sn = add_series_of_numbers(n_l)
        self.assertEqual(str(sn), "[[[[3,0],[5,3]],[4,4]],[5,5]]")


        n_l = ["[1,1]","[2,2]","[3,3]","[4,4]","[5,5]","[6,6]"]
        sn = add_series_of_numbers(n_l)
        self.assertEqual(str(sn), "[[[[5,0],[7,4]],[5,5]],[6,6]]")


        n_l = [
            "[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]", 
            "[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]", 
            "[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]", 
            "[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]", 
            "[7,[5,[[3,8],[1,4]]]]", 
            "[[2,[2,2]],[8,[8,1]]]", 
            "[2,9]", 
            "[1,[[[9,3],9],[[9,0],[0,7]]]]", 
            "[[[5,[7,4]],7],1]", 
            "[[[[4,2],2],6],[8,7]]"
        ]
        sn = add_series_of_numbers(n_l)
        self.assertEqual(str(sn), "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]")



    def test__p1__sample1(self):
        n_l = load_file(sample_input_file_1).split("\n")
        sn = add_series_of_numbers(n_l)
        self.assertEqual(str(sn), "[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]")
        self.assertEqual(sn.magnitude(), 4140)


    def test__part_1__challenge_input(self):
        print("")
        n_l = load_file(input_file).split("\n")
        sn = add_series_of_numbers(n_l)

        print("Solution to day {0} part 1: {1}".format(puzzle_day, sn.magnitude()))
        

###################################################################################################################################################################

############################################################################ PROBLEM 2 ############################################################################


def find_max_magnitude_of_two_numbers(number_list):
    max_magnitude_found = -1

    for i in range(len(number_list)):
        for j in range(len(number_list)):
            if i != j:
                sn_1 = SnailFishNode(number_list[i])
                sn_2 = SnailFishNode(number_list[j])

                sn = sn_1.addition(sn_2)
                sn.reduce()
                current_magnitude = sn.magnitude()

                if current_magnitude > max_magnitude_found:
                    max_magnitude_found = current_magnitude

    return max_magnitude_found




class Day18PartTwoTests(unittest.TestCase):
    
    def test__p1__sum_numbers(self):
        n_l = ["[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]","[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]"]
        magnitude = find_max_magnitude_of_two_numbers(n_l)
        self.assertEqual(magnitude, 3993)

    def test__p2__sample1(self):
        n_l = load_file(sample_input_file_1).split("\n")
        magnitude = find_max_magnitude_of_two_numbers(n_l)
        self.assertEqual(magnitude, 3993)
        

    def test__part_2__challenge_input(self):
        print("")
        n_l = load_file(input_file).split("\n")
        magnitude = find_max_magnitude_of_two_numbers(n_l)
        print("Solution to day {0} part 2: {1}".format(puzzle_day, magnitude))


 
###################################################################################################################################################################
########################################################################## RUN THE TESTS ##########################################################################


# run then unit tests "last"
if __name__ == '__main__':
    unittest.main()
 

