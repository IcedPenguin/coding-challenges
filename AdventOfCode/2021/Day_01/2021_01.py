#!/bin/python
# -*- coding: utf-8 -*-
# https://adventofcode.com/2021/day/1


###################################################################################################################################################################
#  
#  Solution to day XX part 1: 1266
#
#  Solution to day XX part 2: 1217
#
###################################################################################################################################################################

import unittest


###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################
#   
#   --- Day 1: Sonar Sweep ---
#   You're minding your own business on a ship at sea when the overboard alarm goes off! You rush to see if you can help. Apparently, 
#   one of the Elves tripped and accidentally sent the sleigh keys flying into the ocean!
#   
#   Before you know it, you're inside a submarine the Elves keep ready for situations like this. It's covered in Christmas lights 
#   (because of course it is), and it even has an experimental antenna that should be able to track the keys if you can boost its signal 
#   strength high enough; there's a little meter that indicates the antenna's signal strength by displaying 0-50 stars.
#   
#   Your instincts tell you that in order to save Christmas, you'll need to get all fifty stars by December 25th.
#   
#   Collect stars by solving puzzles. Two puzzles will be made available on each day in the Advent calendar; the second puzzle is unlocked 
#   when you complete the first. Each puzzle grants one star. Good luck!
#   
#   As the submarine drops below the surface of the ocean, it automatically performs a sonar sweep of the nearby sea floor. On a small 
#   screen, the sonar sweep report (your puzzle input) appears: each line is a measurement of the sea floor depth as the sweep looks 
#   further and further away from the submarine.
#   
#   For example, suppose you had the following report:
#   
#           199
#           200
#           208
#           210
#           200
#           207
#           240
#           269
#           260
#           263
#
#   This report indicates that, scanning outward from the submarine, the sonar sweep found depths of 199, 200, 208, 210, and so on.
#   
#   The first order of business is to figure out how quickly the depth increases, just so you know what you're dealing with - you 
#   never know if the keys will get carried into deeper water by an ocean current or a fish or something.
#   
#   To do this, count the number of times a depth measurement increases from the previous measurement. (There is no measurement 
#   before the first measurement.) In the example above, the changes are as follows:
#   
#       199 (N/A - no previous measurement)
#       200 (increased)
#       208 (increased)
#       210 (increased)
#       200 (decreased)
#       207 (increased)
#       240 (increased)
#       269 (increased)
#       260 (decreased)
#       263 (increased)
#
#   In this example, there are 7 measurements that are larger than the previous measurement.
#   
#   How many measurements are larger than the previous measurement?



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



def count_depth_increases(depth_array):
    count = 0
    for i in range(len(depth_array) -1):
        if depth_array[i] < depth_array[i+1]:
            count += 1

    return count
### count_depth_increases


class Day01PartOneTests(unittest.TestCase):

    def test__part_1__sample_input(self):
        depth_array = read_file_into_array(sample_input_file_1, True)
        depth_increases = count_depth_increases(depth_array)
        self.assertEqual(7, depth_increases)



depth_array = read_file_into_array(input_file, True)
depth_increases = count_depth_increases(depth_array)
print("Solution to day 1 part 1: {0}".format(depth_increases))


###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################
#  
#  --- Part Two ---
#  Considering every single measurement isn't as useful as you expected: there's just too much noise in the data.
#  
#  Instead, consider sums of a three-measurement sliding window. Again considering the above example:
#  
#          199  A      
#          200  A B    
#          208  A B C  
#          210    B C D
#          200  E   C D
#          207  E F   D
#          240  E F G  
#          269    F G H
#          260      G H
#          263        H
#  
#  Start by comparing the first and second three-measurement windows. The measurements in the first window are marked A (199, 200, 208); 
#  their sum is 199 + 200 + 208 = 607. The second window is marked B (200, 208, 210); its sum is 618. The sum of measurements in the second 
#  window is larger than the sum of the first, so this first comparison increased.
#  
#  Your goal now is to count the number of times the sum of measurements in this sliding window increases from the previous sum. So, 
#  compare A with B, then compare B with C, then C with D, and so on. Stop when there aren't enough measurements left to create a new 
#  three-measurement sum.
#  
#  In the above example, the sum of each three-measurement window is as follows:
#  
#          A: 607 (N/A - no previous sum)
#          B: 618 (increased)
#          C: 618 (no change)
#          D: 617 (decreased)
#          E: 647 (increased)
#          F: 716 (increased)
#          G: 769 (increased)
#          H: 792 (increased)
#
#  In this example, there are 5 sums that are larger than the previous sum.
#  
#  Consider sums of a three-measurement sliding window. How many sums are larger than the previous sum?


def build_sliding_deltas(depth_array, window_size):
    windowed_depth_array = []
    for n in range(len(depth_array) - window_size +1):
        s = 0
        for i in range(window_size):
            s += depth_array[n + i]
        windowed_depth_array.append(s)

    return windowed_depth_array



class Day01PartTwoTests(unittest.TestCase):


    def test__part_2__sample_input(self):
        depth_array = read_file_into_array(sample_input_file_1, True)
        windowed_depth_array = build_sliding_deltas(depth_array, 3)
        depth_increases = count_depth_increases(windowed_depth_array)
        self.assertEqual(5, depth_increases)



#     def test__part_2__challenge_input(self):
#         print("")
#         print("Solution to day 1 part 2: {0}".format(-1))
        

depth_array = read_file_into_array(input_file, True)
windowed_depth_array = build_sliding_deltas(depth_array, 3)
depth_increases = count_depth_increases(windowed_depth_array)
print("Solution to day 1 part 2: {0}".format(depth_increases))


 

 
###################################################################################################################################################################
########################################################################## RUN THE TESTS ##########################################################################


# print ('Number of arguments:', len(sys.argv), 'arguments.')
# print ('Argument List:', str(sys.argv))

# run then unit tests "last"
if __name__ == '__main__':
    unittest.main()
 

