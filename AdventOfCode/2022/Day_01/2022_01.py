#!/bin/python
# -*- coding: utf-8 -*-
# https://adventofcode.com/2022/day/1


###################################################################################################################################################################
#  
#  Solution to part 1: 75501
#
#  Solution to part 2: 215594
#
###################################################################################################################################################################

import unittest

###################################################################################################################################################################
# --- Day 1: Calorie Counting ---
# 
# Santa's reindeer typically eat regular reindeer food, but they need a lot of magical energy to deliver presents on 
# Christmas. For that, their favorite snack is a special type of star fruit that only grows deep in the jungle. The 
# Elves have brought you on their annual expedition to the grove where the fruit grows.
# 
# To supply enough magical energy, the expedition needs to retrieve a minimum of fifty stars by December 25th. Although 
# the Elves assure you that the grove has plenty of fruit, you decide to grab any fruit you see along the way, just in case.
# 
# Collect stars by solving puzzles. Two puzzles will be made available on each day in the Advent calendar; the second 
# puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!
# 
# The jungle must be too overgrown and difficult to navigate in vehicles or access from the air; the Elves' expedition 
# traditionally goes on foot. As your boats approach land, the Elves begin taking inventory of their supplies. One 
# important consideration is food - in particular, the number of Calories each Elf is carrying (your puzzle input).
# 
# The Elves take turns writing down the number of Calories contained by the various meals, snacks, rations, etc. that 
# they've brought with them, one item per line. Each Elf separates their own inventory from the previous Elf's inventory 
# (if any) by a blank line.
# 
# For example, suppose the Elves finish writing their items' Calories and end up with the following list:
# 
#     1000
#     2000
#     3000
# 
#     4000
# 
#     5000
#     6000
# 
#     7000
#     8000
#     9000
# 
#     10000
# 
# This list represents the Calories of the food carried by five Elves:
# 
#     The first Elf is carrying food with 1000, 2000, and 3000 Calories, a total of 6000 Calories.
#     The second Elf is carrying one food item with 4000 Calories.
#     The third Elf is carrying food with 5000 and 6000 Calories, a total of 11000 Calories.
#     The fourth Elf is carrying food with 7000, 8000, and 9000 Calories, a total of 24000 Calories.
#     The fifth Elf is carrying one food item with 10000 Calories.
# 
# In case the Elves get hungry and need extra snacks, they need to know which Elf to ask: they'd like to know how many 
# Calories are being carried by the Elf carrying the most Calories. In the example above, this is 24000 (carried by the 
# fourth Elf).
# 
# Find the Elf carrying the most Calories. How many total Calories is that Elf carrying?
# 
############################################################################ PROBLEM 1 ############################################################################


puzzle_day          = 1
sample_input_file_1 = "2022_{0:02d}_sample_1.txt".format(puzzle_day)
input_file          = "2022_{0:02d}_input.txt".format(puzzle_day)


def load_file(file_path):
    file_ptr = open(file_path, "r")
    data = file_ptr.read()
    file_ptr.close()
    return data


def calories_per_elf(calorie_list):
    calorie_list = calorie_list.split("\n")
    elves = [0]
    count = 0
    for calorie in calorie_list:
        if calorie == "":
            elves.append(0)
        else:
            elves[-1] += int(calorie.strip())

    return elves



class Day01PartOneTests(unittest.TestCase):

    def test__p1__sample1(self):
        test_input = "1000\n2000\n3000"
        self.assertEqual( calories_per_elf(test_input), [6000])

        test_input = "1000\n2000\n3000\n\n2000"
        self.assertEqual( calories_per_elf(test_input), [6000, 2000])


    def test__p1__sample2(self):
        test_input = load_file(sample_input_file_1)
        elves = calories_per_elf(test_input)
        self.assertEqual( max(elves), 24000)

    
    def test__part_1__challenge_input(self):
        challenge_input = load_file(input_file)
        elves = calories_per_elf(challenge_input)
        print("")
        result = max(elves)
        print("Solution to day {0} part 1: {1}".format(puzzle_day, result))
        


###################################################################################################################################################################
#  --- Part Two ---
#  
#  By the time you calculate the answer to the Elves' question, they've already realized that the Elf carrying the 
#  most Calories of food might eventually run out of snacks.
#  
#  To avoid this unacceptable situation, the Elves would instead like to know the total Calories carried by the top 
#  three Elves carrying the most Calories. That way, even if one of those Elves runs out of snacks, they still have 
#  two backups.
#  
#  In the example above, the top three Elves are the fourth Elf (with 24000 Calories), then the third Elf 
#  (with 11000 Calories), then the fifth Elf (with 10000 Calories). The sum of the Calories carried by these 
#  three elves is 45000.
#  
#  Find the top three Elves carrying the most Calories. How many Calories are those Elves carrying in total?
#  
############################################################################ PROBLEM 2 ############################################################################


def get_max_3_elves(elves):
    sorted_elves = sorted(elves, reverse=True)
    return sorted_elves[0] + sorted_elves[1] + sorted_elves[2]


class Day01PartTwoTests(unittest.TestCase):
    
    def test__p2__sample1(self):
        test_input = load_file(sample_input_file_1)
        elves = calories_per_elf(test_input)
        top_3 = get_max_3_elves(elves)
        self.assertEqual( top_3, 45000)


    def test__part_2__challenge_input(self):
        challenge_input = load_file(input_file)
        elves = calories_per_elf(challenge_input)
        print("")
        print("Solution to day {0} part 2: {1}".format(puzzle_day, get_max_3_elves(elves)))

 
###################################################################################################################################################################
########################################################################## RUN THE TESTS ##########################################################################


# run then unit tests "last"
if __name__ == '__main__':
    unittest.main()
 

