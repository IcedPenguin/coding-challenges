#!/bin/python
# -*- coding: utf-8 -*-
# https://adventofcode.com/2021/day/6


###################################################################################################################################################################
#  
#  Solution to day 6 part 1: 395627
#
#  Solution to day 6 part 2: 1767323539209
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

###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################
#  
#  --- Day 6: Lanternfish ---
#  The sea floor is getting steeper. Maybe the sleigh keys got carried this way?
#  
#  A massive school of glowing lanternfish swims past. They must spawn quickly to reach such large numbers - maybe 
#  exponentially quickly? You should model their growth rate to be sure.
#  
#  Although you know nothing about this specific species of lanternfish, you make some guesses about their attributes. 
#  Surely, each lanternfish creates a new lanternfish once every 7 days.
#  
#  However, this process isn't necessarily synchronized between every lanternfish - one lanternfish might have 2 days 
#  left until it creates another lanternfish, while another might have 4. So, you can model each fish as a single number 
#  that represents the number of days until it creates a new lanternfish.
#  
#  Furthermore, you reason, a new lanternfish would surely need slightly longer before it's capable of producing more 
#  lanternfish: two more days for its first cycle.
#  
#  So, suppose you have a lanternfish with an internal timer value of 3:
#  
#      After one day, its internal timer would become 2.
#      After another day, its internal timer would become 1.
#      After another day, its internal timer would become 0.
#      After another day, its internal timer would reset to 6, and it would create a new lanternfish with an internal timer of 8.
#      After another day, the first lanternfish would have an internal timer of 5, and the second lanternfish would have an internal timer of 7.
#  
#  A lanternfish that creates a new fish resets its timer to 6, not 7 (because 0 is included as a valid timer value). 
#  The new lanternfish starts with an internal timer of 8 and does not start counting down until the next day.
#  
#  Realizing what you're trying to do, the submarine automatically produces a list of the ages of several hundred nearby 
#  lanternfish (your puzzle input). For example, suppose you were given the following list:
#  
#      3,4,3,1,2
#  
#  This list means that the first fish has an internal timer of 3, the second fish has an internal timer of 4, and so on 
#  until the fifth fish, which has an internal timer of 2. Simulating these fish over several days would proceed as follows:
#  
#      Initial state: 3,4,3,1,2
#      After  1 day:  2,3,2,0,1
#      After  2 days: 1,2,1,6,0,8
#      After  3 days: 0,1,0,5,6,7,8
#      After  4 days: 6,0,6,4,5,6,7,8,8
#      After  5 days: 5,6,5,3,4,5,6,7,7,8
#      After  6 days: 4,5,4,2,3,4,5,6,6,7
#      After  7 days: 3,4,3,1,2,3,4,5,5,6
#      After  8 days: 2,3,2,0,1,2,3,4,4,5
#      After  9 days: 1,2,1,6,0,1,2,3,3,4,8
#      After 10 days: 0,1,0,5,6,0,1,2,2,3,7,8
#      After 11 days: 6,0,6,4,5,6,0,1,1,2,6,7,8,8,8
#      After 12 days: 5,6,5,3,4,5,6,0,0,1,5,6,7,7,7,8,8
#      After 13 days: 4,5,4,2,3,4,5,6,6,0,4,5,6,6,6,7,7,8,8
#      After 14 days: 3,4,3,1,2,3,4,5,5,6,3,4,5,5,5,6,6,7,7,8
#      After 15 days: 2,3,2,0,1,2,3,4,4,5,2,3,4,4,4,5,5,6,6,7
#      After 16 days: 1,2,1,6,0,1,2,3,3,4,1,2,3,3,3,4,4,5,5,6,8
#      After 17 days: 0,1,0,5,6,0,1,2,2,3,0,1,2,2,2,3,3,4,4,5,7,8
#      After 18 days: 6,0,6,4,5,6,0,1,1,2,6,0,1,1,1,2,2,3,3,4,6,7,8,8,8,8
#  
#  Each day, a 0 becomes a 6 and adds a new 8 to the end of the list, while each other number decreases by 1 if it was present at the start of the day.
#  
#  In this example, after 18 days, there are a total of 26 fish. After 80 days, there would be a total of 5934.
#  
#  Find a way to simulate lanternfish. How many lanternfish would there be after 80 days?
#  
#  


######
# Thoughts
#  * exponential growth makes tracking each fish infeasible.
#  * instead track number of fish at each point in the cycle. 


class LanterFishTracker:
    def __init__(self, reset_value, new_fish_value):
        self.reset_value = reset_value
        self.new_fish_value = new_fish_value
        self.fish_internal_counter_map = {k: 0 for k in range(self.new_fish_value +1)}

    def load_school(self, school):
        lantern_fish_school = school.split(",")
        for lantern_fish in lantern_fish_school:
            self.load_fish(lantern_fish)

    def load_fish(self, fish_internal_counter):
        self.fish_internal_counter_map[int(fish_internal_counter)] += 1

    def increment_day(self):
        yesterdays_fish = self.fish_internal_counter_map
        todays_fish = {k: 0 for k in range(self.new_fish_value +1)}

        todays_fish[8] = yesterdays_fish[0]     # brand new fish
        todays_fish[0] = yesterdays_fish[1]
        todays_fish[1] = yesterdays_fish[2]
        todays_fish[2] = yesterdays_fish[3]
        todays_fish[3] = yesterdays_fish[4]
        todays_fish[4] = yesterdays_fish[5]
        todays_fish[5] = yesterdays_fish[6]
        todays_fish[6] = yesterdays_fish[7]
        todays_fish[6] += yesterdays_fish[0]    # reset count for those that just made a new fish
        todays_fish[7] = yesterdays_fish[8]
        
        self.fish_internal_counter_map = todays_fish

    def get_fish_count(self):
        count = 0
        for k in self.fish_internal_counter_map:
            count += self.fish_internal_counter_map[k]
        return count



class Day6PartOneTests(unittest.TestCase):

    
    def test__part_1__sample_input(self):
        print("")
        raw_fish = read_file_into_array(sample_input_file_1, False)
        tracker = LanterFishTracker(6, 8)
        tracker.load_school(raw_fish[0])
        self.assertEqual(5, tracker.get_fish_count())

        for i in range(18): 
            tracker.increment_day()
        self.assertEqual(26, tracker.get_fish_count())

        for i in range(80 - 18): 
            tracker.increment_day()
        self.assertEqual(5934, tracker.get_fish_count())


    def test__part_1__challenge_input(self):
        print("")

        raw_fish = read_file_into_array(input_file, False)
        tracker = LanterFishTracker(6, 8)
        tracker.load_school(raw_fish[0])

        for i in range(80): 
            tracker.increment_day()

        print("Solution to day 6 part 1: {0}".format(tracker.get_fish_count()))
        


###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################
#  
#  --- Part Two ---
#  Suppose the lanternfish live forever and have unlimited food and space. Would they take over the entire ocean?
#  
#  After 256 days in the example above, there would be a total of  lanternfish!
#  
#  How many lanternfish would there be after 256 days?
#  


class Day6PartTwoTests(unittest.TestCase):

    
    def test__part_2__sample_input(self):
        print("")
        raw_fish = read_file_into_array(sample_input_file_1, False)
        tracker = LanterFishTracker(6, 8)
        tracker.load_school(raw_fish[0])
        self.assertEqual(5, tracker.get_fish_count())

        for i in range(256): 
            tracker.increment_day()
        self.assertEqual(26984457539, tracker.get_fish_count())



    def test__part_2__challenge_input(self):
        print("")
        raw_fish = read_file_into_array(input_file, False)
        tracker = LanterFishTracker(6, 8)
        tracker.load_school(raw_fish[0])

        for i in range(256): 
            tracker.increment_day()

        print("Solution to day 6 part 2: {0}".format(tracker.get_fish_count()))

 

 
###################################################################################################################################################################
########################################################################## RUN THE TESTS ##########################################################################


# run then unit tests "last"
if __name__ == '__main__':
    unittest.main()
 

