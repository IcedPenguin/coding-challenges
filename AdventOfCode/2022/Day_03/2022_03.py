#!/bin/python
# -*- coding: utf-8 -*-
# https://adventofcode.com/2022/day/3


###################################################################################################################################################################
#  
#  Solution to part 1: 7742
#
#  Solution to part 2: 2276
#
###################################################################################################################################################################

import unittest
import itertools

###################################################################################################################################################################
#   --- Day 3: Rucksack Reorganization ---
#   
#   One Elf has the important job of loading all of the rucksacks with supplies for the jungle journey. Unfortunately, 
#   that Elf didn't quite follow the packing instructions, and so a few items now need to be rearranged.
#   
#   Each rucksack has two large compartments. All items of a given type are meant to go into exactly one of the two compartments. 
#   The Elf that did the packing failed to follow this rule for exactly one item type per rucksack.
#   
#   The Elves have made a list of all of the items currently in each rucksack (your puzzle input), but they need your help 
#   finding the errors. Every item type is identified by a single lowercase or uppercase letter (that is, a and A refer to 
#       different types of items).
#   
#   The list of items for each rucksack is given as characters all on a single line. A given rucksack always has the same number 
#   of items in each of its two compartments, so the first half of the characters represent items in the first compartment, while 
#   the second half of the characters represent items in the second compartment.
#   
#   For example, suppose you have the following list of contents from six rucksacks:
#   
#       vJrwpWtwJgWrhcsFMMfFFhFp
#       jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
#       PmmdzqPrVvPwwTWBwg
#       wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
#       ttgJtRGJQctTZtZT
#       CrZsJsPPZsGzwwsLwLmpwMDw
#   
#       The first rucksack contains the items vJrwpWtwJgWrhcsFMMfFFhFp, which means its first compartment contains 
#       the items vJrwpWtwJgWr, while the second compartment contains the items hcsFMMfFFhFp. The only item type 
#       that appears in both compartments is lowercase p.
#   
#       The second rucksack's compartments contain jqHRNqRjqzjGDLGL and rsFMfFZSrLrFZsSL. The only item type that 
#       appears in both compartments is uppercase L.
#       
#       The third rucksack's compartments contain PmmdzqPrV and vPwwTWBwg; the only common item type is uppercase P.
#       
#       The fourth rucksack's compartments only share item type v.
#       
#       The fifth rucksack's compartments only share item type t.
#       
#       The sixth rucksack's compartments only share item type s.
#   
#   To help prioritize item rearrangement, every item type can be converted to a priority:
#   
#       Lowercase item types a through z have priorities 1 through 26.
#       Uppercase item types A through Z have priorities 27 through 52.
#   
#   In the above example, the priority of the item type that appears in both compartments of each rucksack is 16 (p), 38 (L), 42 (P), 22 (v), 20 (t), and 19 (s); the sum of these is 157.
#   
#   Find the item type that appears in both compartments of each rucksack. What is the sum of the priorities of those item types?
#   
############################################################################ PROBLEM 1 ############################################################################


puzzle_day          = 3
sample_input_file_1 = "2022_{0:02d}_sample_1.txt".format(puzzle_day)
input_file          = "2022_{0:02d}_input.txt".format(puzzle_day)


def load_file(file_path):
    file_ptr = open(file_path, "r")
    data = file_ptr.read()
    file_ptr.close()
    return data


def find_common_item(rucksack):
    # split the string in half
    compartment_1 = rucksack[:len(rucksack)//2]
    compartment_2 = rucksack[len(rucksack)//2:]

    # create a set holding elements from each side
    items_1 = set()
    for item in compartment_1:
        items_1.add(item)

    items_2 = set()
    for item in compartment_2:
        items_2.add(item)

    # intersect the set
    return items_1.intersection(items_2).pop()



def get_item_priority(item):
    return "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ".index(item) +1


def get_prioirity_of_mixed_item_in_compartments(compartments):
    priority_sum = 0
    for compartment in compartments:
        item = find_common_item(compartment)
        priority_sum += get_item_priority(item)

    return priority_sum



class Day3PartOneTests(unittest.TestCase):

    def test__p1__common_item(self):
        find_common_item
        self.assertEqual(find_common_item("vJrwpWtwJgWrhcsFMMfFFhFp"), 'p')
        self.assertEqual(find_common_item("jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL"), 'L')
        self.assertEqual(find_common_item("PmmdzqPrVvPwwTWBwg"), 'P')
        self.assertEqual(find_common_item("wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn"), 'v')
        self.assertEqual(find_common_item("ttgJtRGJQctTZtZT"), 't')
        self.assertEqual(find_common_item("CrZsJsPPZsGzwwsLwLmpwMDw"), 's')



    def test__p1__sample1(self):
        compartments = load_file(sample_input_file_1).split("\n")
        total_priority = get_prioirity_of_mixed_item_in_compartments(compartments)
        self.assertEqual(total_priority, 157)
        


    def test__p1__sample2(self):
        pass

    
    def test__part_1__challenge_input(self):
        print("")
        compartments = load_file(input_file).split("\n")
        total_priority = get_prioirity_of_mixed_item_in_compartments(compartments)
        print("Solution to day {0} part 1: {1}".format(puzzle_day, total_priority))
        


###################################################################################################################################################################
#  --- Part Two ---
#  
#  As you finish identifying the misplaced items, the Elves come to you with another issue.
#  
#  For safety, the Elves are divided into groups of three. Every Elf carries a badge that identifies their group. 
#  For efficiency, within each group of three Elves, the badge is the only item type carried by all three Elves. 
#  That is, if a group's badge is item type B, then all three Elves will have item type B somewhere in their rucksack, 
#  and at most two of the Elves will be carrying any other item type.
#  
#  The problem is that someone forgot to put this year's updated authenticity sticker on the badges. All of the 
#  badges need to be pulled out of the rucksacks so the new authenticity stickers can be attached.
#  
#  Additionally, nobody wrote down which item type corresponds to each group's badges. The only way to tell which 
#  item type is the right one is by finding the one item type that is common between all three Elves in each group.
#  
#  Every set of three lines in your list corresponds to a single group, but each group can have a different badge item 
#  type. So, in the above example, the first group's rucksacks are the first three lines:
#  
#      vJrwpWtwJgWrhcsFMMfFFhFp
#      jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
#      PmmdzqPrVvPwwTWBwg
#  
#  And the second group's rucksacks are the next three lines:
#  
#      wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
#      ttgJtRGJQctTZtZT
#      CrZsJsPPZsGzwwsLwLmpwMDw
#  
#  In the first group, the only item type that appears in all three rucksacks is lowercase r; this must be their badges. 
#  In the second group, their badge item type must be Z.
#  
#  Priorities for these items must still be found to organize the sticker attachment efforts: here, they are 18 (r) for 
#  the first group and 52 (Z) for the second group. The sum of these is 70.
#  
#  Find the item type that corresponds to the badges of each three-Elf group. What is the sum of the priorities of those 
#  item types?
#  
############################################################################ PROBLEM 2 ############################################################################


def find_badge_for_elf_group(compartments):
    compartment_contents = []
    
    for compartment in compartments:
        items = set()
        for item in compartment:
            items.add(item)
        compartment_contents.append(items)
 

    common_items = compartment_contents.pop(0)
    while(len(compartment_contents) > 0):
        common_items = common_items.intersection(compartment_contents.pop(0))

    return common_items.pop()



# https://stackoverflow.com/questions/1624883/alternative-way-to-split-a-list-into-groups-of-n
def mygrouper(n, iterable):
    args = [iter(iterable)] * n
    return ([e for e in t if e != None] for t in itertools.zip_longest(*args))


def get_prioirity_of_badges_compartments(compartments):
    priority_sum = 0

    for compartment_group in mygrouper(3, compartments):
        badge = find_badge_for_elf_group(compartment_group)
        priority_sum += get_item_priority(badge)

    return priority_sum




class Day3PartTwoTests(unittest.TestCase):
    
    def test__p2__find_badges(self):
        contents = ["vJrwpWtwJgWrhcsFMMfFFhFp", "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL", "PmmdzqPrVvPwwTWBwg"]
        badge = find_badge_for_elf_group(contents)
        self.assertEqual(badge, 'r')

        contents = ["wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn", "ttgJtRGJQctTZtZT"," CrZsJsPPZsGzwwsLwLmpwMDw"]
        badge = find_badge_for_elf_group(contents)
        self.assertEqual(badge, 'Z')
        

    def test__part_2__challenge_input(self):
        print("")
        compartments = load_file(input_file).split("\n")
        priority = get_prioirity_of_badges_compartments(compartments)
        print("Solution to day {0} part 2: {1}".format(puzzle_day, priority))


 
###################################################################################################################################################################
########################################################################## RUN THE TESTS ##########################################################################


# run then unit tests "last"
if __name__ == '__main__':
    unittest.main()
 

