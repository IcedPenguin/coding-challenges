#!/bin/python
# -*- coding: utf-8 -*-
# https://adventofcode.com/2022/day/4


###################################################################################################################################################################
#  
#  Solution to part 1: 487
#
#  Solution to part 2: 849
#
###################################################################################################################################################################

import unittest
import re

###################################################################################################################################################################
#   --- Day 4: Camp Cleanup ---
#   
#   Space needs to be cleared before the last supplies can be unloaded from the ships, and so several Elves have been assigned the 
#   job of cleaning up sections of the camp. Every section has a unique ID number, and each Elf is assigned a range of section IDs.
#   
#   However, as some of the Elves compare their section assignments with each other, they've noticed that many of the assignments 
#   overlap. To try to quickly find overlaps and reduce duplicated effort, the Elves pair up and make a big list of the section 
#   assignments for each pair (your puzzle input).
#   
#   For example, consider the following list of section assignment pairs:
#   
#       2-4,6-8
#       2-3,4-5
#       5-7,7-9
#       2-8,3-7
#       6-6,4-6
#       2-6,4-8
#   
#   For the first few pairs, this list means:
#   
#       Within the first pair of Elves, the first Elf was assigned sections 2-4 (sections 2, 3, and 4), while the second Elf was 
#       assigned sections 6-8 (sections 6, 7, 8).
#       The Elves in the second pair were each assigned two sections.
#       The Elves in the third pair were each assigned three sections: one got sections 5, 6, and 7, while the other also got 7, plus 8 and 9.
#   
#   This example list uses single-digit section IDs to make it easier to draw; your actual list might contain larger numbers. 
#   Visually, these pairs of section assignments look like this:
#   
#       .234.....  2-4
#       .....678.  6-8
#   
#       .23......  2-3
#       ...45....  4-5
#   
#       ....567..  5-7
#       ......789  7-9
#   
#       .2345678.  2-8
#       ..34567..  3-7
#   
#       .....6...  6-6
#       ...456...  4-6
#   
#       .23456...  2-6
#       ...45678.  4-8
#   
#   Some of the pairs have noticed that one of their assignments fully contains the other. For example, 2-8 fully contains 3-7, 
#   and 6-6 is fully contained by 4-6. In pairs where one assignment fully contains the other, one Elf in the pair would be 
#   exclusively cleaning sections their partner will already be cleaning, so these seem like the most in need of reconsideration. 
#   In this example, there are 2 such pairs.
#   
#   In how many assignment pairs does one range fully contain the other?
#   
############################################################################ PROBLEM 1 ############################################################################


puzzle_day          = 4
sample_input_file_1 = "2022_{0:02d}_sample_1.txt".format(puzzle_day)
input_file          = "2022_{0:02d}_input.txt".format(puzzle_day)


def load_file(file_path):
    file_ptr = open(file_path, "r")
    data = file_ptr.read()
    file_ptr.close()
    return data

def load_elf_ranges(raw_elves):
    raw_elves = raw_elves.strip()
    raw_elves = raw_elves.split("\n")
    pairs_of_elves = []

    for row in raw_elves:
        elves = re.split(",|-", row)
        elf_1 = get_elf_seats(int(elves[0]), int(elves[1]))
        elf_2 = get_elf_seats(int(elves[2]), int(elves[3]))

        pairs_of_elves.append([elf_1, elf_2])

    return pairs_of_elves


# Why make this a function? In case the ranges get more complicated in part 2.
def get_elf_seats(elf_range_start, elf_range_stop):
    return  [v for v in range(elf_range_start,elf_range_stop +1)]


def check_for_fully_overlapped_seats(elf_one_seats, elf_two_seats):
    elf_1 = set(elf_one_seats)
    elf_2 = set(elf_two_seats)

    over_lap = elf_1.intersection(elf_2)

    return len(elf_1) == len(over_lap) or len(elf_2) == len(over_lap)



def find_elves_with_overlapping_seats(elf_pairs, over_lap_method=check_for_fully_overlapped_seats):
    counter = 0 # number of overlapping ranges
    for pair in elf_pairs:
        if over_lap_method(pair[0], pair[1]):
            counter += 1

    return counter


class Day4PartOneTests(unittest.TestCase):


    def test__p1__elf_range(self):
        self.assertEqual(get_elf_seats(2,4), [2,3,4])
        self.assertEqual(get_elf_seats(4,6), [4,5,6])


    def test__p1__check_overlap(self):
        self.assertEqual(check_for_fully_overlapped_seats([1,2], [3,4,5]), False)
        self.assertEqual(check_for_fully_overlapped_seats([1],[1]), True)
        self.assertEqual(check_for_fully_overlapped_seats([1,2,3],[3]), True)
        self.assertEqual(check_for_fully_overlapped_seats([4],[2,4,7]), True)



    def test__p1__sample1(self):
        raw_elves = load_file(sample_input_file_1)
        elves= load_elf_ranges(raw_elves)
        count = find_elves_with_overlapping_seats(elves)
        self.assertEqual(count, 2)


    
    def test__part_1__challenge_input(self):
        print("")
        raw_elves = load_file(input_file)
        elves= load_elf_ranges(raw_elves)
        count = find_elves_with_overlapping_seats(elves)
        print("Solution to day {0} part 1: {1}".format(puzzle_day, count))
        


###################################################################################################################################################################
#  --- Part Two ---
#  
#  It seems like there is still quite a bit of duplicate work planned. Instead, the Elves would like to know the number 
#  of pairs that overlap at all.
#  
#  In the above example, the first two pairs (2-4,6-8 and 2-3,4-5) don't overlap, while the remaining four 
#  pairs (5-7,7-9, 2-8,3-7, 6-6,4-6, and 2-6,4-8) do overlap:
#  
#      5-7,7-9 overlaps in a single section, 7.
#      2-8,3-7 overlaps all of the sections 3 through 7.
#      6-6,4-6 overlaps in a single section, 6.
#      2-6,4-8 overlaps in sections 4, 5, and 6.
#  
#  So, in this example, the number of overlapping assignment pairs is 4.
#  
#  In how many assignment pairs do the ranges overlap?
#  
############################################################################ PROBLEM 2 ############################################################################

def check_for_parially_overlapped_seats(elf_one_seats, elf_two_seats):
    elf_1 = set(elf_one_seats)
    elf_2 = set(elf_two_seats)

    over_lap = elf_1.intersection(elf_2)

    return len(over_lap) > 0


class Day4PartTwoTests(unittest.TestCase):
    
    def test__p2__sample1(self):
        raw_elves = load_file(sample_input_file_1)
        elves= load_elf_ranges(raw_elves)
        count = find_elves_with_overlapping_seats(elves, check_for_parially_overlapped_seats)
        self.assertEqual(count, 4)

        

    def test__part_2__challenge_input(self):
        print("")
        raw_elves = load_file(input_file)
        elves= load_elf_ranges(raw_elves)
        count = find_elves_with_overlapping_seats(elves, check_for_parially_overlapped_seats)
        print("Solution to day {0} part 2: {1}".format(puzzle_day, count))


 
###################################################################################################################################################################
########################################################################## RUN THE TESTS ##########################################################################


# run then unit tests "last"
if __name__ == '__main__':
    unittest.main()
 

