#!/bin/python
# -*- coding: utf-8 -*-
# https://adventofcode.com/2021/day/7


###################################################################################################################################################################
#  
#  Solution to day 7 part 1: 345035
#
#  Solution to day 7 part 2: 97038163
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

    if asInt:
        parts = [int(i) for i in parts]

    return parts
### read_and_parse_single_line_input

###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################
#  
#  --- Day 7: The Treachery of Whales ---
#  A giant whale has decided your submarine is its next meal, and it's much faster than you are. There's nowhere to run!
#  
#  Suddenly, a swarm of crabs (each in its own tiny submarine - it's too deep for them otherwise) zooms in to rescue you! 
#      They seem to be preparing to blast a hole in the ocean floor; sensors indicate a massive underground cave system 
#      just beyond where they're aiming!
#  
#  The crab submarines all need to be aligned before they'll have enough power to blast a large enough hole for your 
#  submarine to get through. However, it doesn't look like they'll be aligned before the whale catches you! Maybe you can help?
#  
#  There's one major catch - crab submarines can only move horizontally.
#  
#  You quickly make a list of the horizontal position of each crab (your puzzle input). Crab submarines have limited 
#  fuel, so you need to find a way to make all of their horizontal positions match while requiring them to spend as 
#  little fuel as possible.
#  
#  For example, consider the following horizontal positions:
#  
#  16,1,2,0,4,2,7,1,2,14
#  
#  This means there's a crab with horizontal position 16, a crab with horizontal position 1, and so on.
#  
#  Each change of 1 step in horizontal position of a single crab costs 1 fuel. You could choose any horizontal 
#  position to align them all on, but the one that costs the least fuel is horizontal position 2:
#  
#      Move from 16 to 2: 14 fuel
#      Move from 1 to 2: 1 fuel
#      Move from 2 to 2: 0 fuel
#      Move from 0 to 2: 2 fuel
#      Move from 4 to 2: 2 fuel
#      Move from 2 to 2: 0 fuel
#      Move from 7 to 2: 5 fuel
#      Move from 1 to 2: 1 fuel
#      Move from 2 to 2: 0 fuel
#      Move from 14 to 2: 12 fuel
#  
#  This costs a total of 37 fuel. This is the cheapest possible outcome; more expensive outcomes include aligning at 
#  position 1 (41 fuel), position 3 (39 fuel), or position 10 (71 fuel).
#  
#  Determine the horizontal position that the crabs can align to using the least fuel possible. 
#  How much fuel must they spend to align to that position?
#  


def get_index_range(crabs):
    return min(crabs), max(crabs)



def cost_to_move_crabs_to_index(crabs, index):
    cost = 0

    for crab in crabs:
        cost += abs(crab - index)
    
    return cost


def minimum_crab_moves(crabs, min_index, max_index, cost_function):
    min_cost_found = float('inf')
    min_idx_found = -1
    for idx in range(min_index, max_index +1, 1):
        cost_at_index = cost_function(crabs, idx)
        # print("testing idx={0}\tcost={1}".format(idx, cost_at_index))

        if cost_at_index < min_cost_found:
            min_cost_found  = cost_at_index
            min_idx_found = idx

    return min_idx_found, min_cost_found
### minimum_crab_moves

class Day7PartOneTests(unittest.TestCase):

    
    def test__part_1__sample_input(self):
        print("")
        crabs = read_and_parse_single_line_input(sample_input_file_1, ",", True)
        left_index, right_index = get_index_range(crabs)
        idx, cost = minimum_crab_moves(crabs, left_index, right_index, cost_to_move_crabs_to_index)

        self.assertEqual(cost, 37)
        self.assertEqual(idx, 2)


    def test__part_1__challenge_input(self):
        print("")
        crabs = read_and_parse_single_line_input(input_file, ",", True)
        left_index, right_index = get_index_range(crabs)
        idx, cost = minimum_crab_moves(crabs, left_index, right_index, cost_to_move_crabs_to_index)

        print("Solution to day 7 part 1: {0}".format(cost))
        


###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################
#  
#  --- Part Two ---
#  The crabs don't seem interested in your proposed solution. Perhaps you misunderstand crab engineering?
#  
#  As it turns out, crab submarine engines don't burn fuel at a constant rate. Instead, each change of 1 step 
#  in horizontal position costs 1 more unit of fuel than the last: the first step costs 1, the second step 
#  costs 2, the third step costs 3, and so on.
#  
#  As each crab moves, moving further becomes more expensive. This changes the best horizontal position to 
#  align them all on; in the example above, this becomes 5:
#  
#      Move from 16 to 5: 66 fuel
#      Move from 1 to 5: 10 fuel
#      Move from 2 to 5: 6 fuel
#      Move from 0 to 5: 15 fuel
#      Move from 4 to 5: 1 fuel
#      Move from 2 to 5: 6 fuel
#      Move from 7 to 5: 3 fuel
#      Move from 1 to 5: 10 fuel
#      Move from 2 to 5: 6 fuel
#      Move from 14 to 5: 45 fuel
#  
#  This costs a total of 168 fuel. This is the new cheapest possible outcome; the old alignment position (2) 
#  now costs 206 fuel instead.
#  
#  Determine the horizontal position that the crabs can align to using the least fuel possible so they can make 
#  you an escape route! How much fuel must they spend to align to that position?
#  


def cost_to_move_crabs_to_index_2(crabs, index):
    cost = 0

    for crab in crabs:
        delta = abs(crab - index)
        cost += ((delta-0)+1) * (0 + delta) / 2;
    return cost


class Day7PartTwoTests(unittest.TestCase):

    
    def test__part_2__sample_input(self):
        print("")
        crabs = read_and_parse_single_line_input(sample_input_file_1, ",", True)
        left_index, right_index = get_index_range(crabs)
        idx, cost = minimum_crab_moves(crabs, left_index, right_index, cost_to_move_crabs_to_index_2)

        self.assertEqual(cost, 168)
        self.assertEqual(idx, 5)


    def test__part_2__challenge_input(self):
        print("")
        crabs = read_and_parse_single_line_input(input_file, ",", True)
        left_index, right_index = get_index_range(crabs)
        idx, cost = minimum_crab_moves(crabs, left_index, right_index, cost_to_move_crabs_to_index_2)

        print("Solution to day 7 part 2: {0}".format(int(cost)))
 

 
###################################################################################################################################################################
########################################################################## RUN THE TESTS ##########################################################################


# run then unit tests "last"
if __name__ == '__main__':
    unittest.main()
 

