#!/bin/python
# -*- coding: utf-8 -*-
# https://adventofcode.com/2021/day/3


###################################################################################################################################################################
#  
#  Solution to day 3 part 1: 2724524
#
#  Solution to day 3 part 2: 2775870
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
#  --- Day 3: Binary Diagnostic ---
#  The submarine has been making some odd creaking noises, so you ask it to produce a diagnostic report just in case.
#  
#  The diagnostic report (your puzzle input) consists of a list of binary numbers which, when decoded properly, can tell 
#  you many useful things about the conditions of the submarine. The first parameter to check is the power consumption.
#  
#  You need to use the binary numbers in the diagnostic report to generate two new binary numbers (called the gamma rate 
#  and the epsilon rate). The power consumption can then be found by multiplying the gamma rate by the epsilon rate.
#  
#  Each bit in the gamma rate can be determined by finding the most common bit in the corresponding position of all numbers 
#  in the diagnostic report. For example, given the following diagnostic report:
#  
#          00100
#          11110
#          10110
#          10111
#          10101
#          01111
#          00111
#          11100
#          10000
#          11001
#          00010
#          01010
#  
#  Considering only the first bit of each number, there are five 0 bits and seven 1 bits. Since the most common bit is 1, 
#  the first bit of the gamma rate is 1.
#  
#  The most common second bit of the numbers in the diagnostic report is 0, so the second bit of the gamma rate is 0.
#  
#  The most common value of the third, fourth, and fifth bits are 1, 1, and 0, respectively, and so the final three bits 
#  of the gamma rate are 110.
#  
#  So, the gamma rate is the binary number 10110, or 22 in decimal.
#  
#  The epsilon rate is calculated in a similar way; rather than use the most common bit, the least common bit from each 
#  position is used. So, the epsilon rate is 01001, or 9 in decimal. Multiplying the gamma rate (22) by the epsilon 
#  rate (9) produces the power consumption, 198.
#  
#  Use the binary numbers in your diagnostic report to calculate the gamma rate and epsilon rate, then multiply them 
#  together. What is the power consumption of the submarine? (Be sure to represent your answer in decimal, not binary.)
#  
#  




def most_and_least_common_bit_in_each_column(binary_numbers):
    l = len(binary_numbers[0])
    bit_zero_counts = [0] * l
    bit_one_counts = [0] * l
    
    # count the number "1" in each column
    for number in binary_numbers:
        for i in range(len(number)):
            if number[i] == "1":
                bit_one_counts[i] += 1
            else: 
                bit_zero_counts[i] += 1


    most_common_bit = []
    least_common_bit = []
    for i in range(len(bit_zero_counts)):
        if bit_zero_counts[i] > bit_one_counts[i]:
            most_common_bit.append(0)
            least_common_bit.append(1)
        else:
            most_common_bit.append(1)
            least_common_bit.append(0)
        
    return most_common_bit, least_common_bit
### most_and_least_common_bit_in_each_column


def calculate_rate(common_bit):
    bit_string = "".join(str(x) for x in common_bit)
    return int(bit_string, 2)
### calculate_rate




class DayXXPartOneTests(unittest.TestCase):


    def test__part_1__sample_input(self):
        binary_numbers = read_file_into_array(sample_input_file_1, False)
        most_common_bit, least_common_bit = most_and_least_common_bit_in_each_column(binary_numbers)
        gamma = calculate_rate(most_common_bit)
        epsilon = calculate_rate(least_common_bit)

        self.assertEqual(gamma, 22)
        self.assertEqual(epsilon, 9)


    def test__part_1__challenge_input(self):
        print("")

        binary_numbers = read_file_into_array(input_file, False)
        most_common_bit, least_common_bit = most_and_least_common_bit_in_each_column(binary_numbers)
        gamma = calculate_rate(most_common_bit)
        epsilon = calculate_rate(least_common_bit)

        print("Solution to day 3 part 1: {0}".format(gamma * epsilon))
        


# print("Solution to day 3 part 1: {0}".format(-1))


###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################
#  
#  --- Part Two ---
#  Next, you should verify the life support rating, which can be determined by multiplying the oxygen generator rating 
#  by the CO2 scrubber rating.
#  
#  Both the oxygen generator rating and the CO2 scrubber rating are values that can be found in your diagnostic report - 
#  finding them is the tricky part. Both values are located using a similar process that involves filtering out values 
#  until only one remains. Before searching for either rating value, start with the full list of binary numbers from your 
#  diagnostic report and consider just the first bit of those numbers. Then:
#  
#    - Keep only numbers selected by the bit criteria for the type of rating value for which you are searching. Discard numbers 
#      which do not match the bit criteria.
#    - If you only have one number left, stop; this is the rating value for which you are searching.
#      Otherwise, repeat the process, considering the next bit to the right.
#  
#  The bit criteria depends on which type of rating value you want to find:
#  
#    - To find oxygen generator rating, determine the most common value (0 or 1) in the current bit position, and keep only 
#      numbers with that bit in that position. If 0 and 1 are equally common, keep values with a 1 in the position being considered.
#  
#    - To find CO2 scrubber rating, determine the least common value (0 or 1) in the current bit position, and keep only 
#      numbers with that bit in that position. If 0 and 1 are equally common, keep values with a 0 in the position being considered.
#  
#  For example, to determine the oxygen generator rating value using the same example diagnostic report from above:
#  
#    - Start with all 12 numbers and consider only the first bit of each number. There are more 1 bits (7) than 0 bits (5), 
#      so keep only the 7 numbers with a 1 in the first position: 11110, 10110, 10111, 10101, 11100, 10000, and 11001.
#    - Then, consider the second bit of the 7 remaining numbers: there are more 0 bits (4) than 1 bits (3), so keep only 
#      the 4 numbers with a 0 in the second position: 10110, 10111, 10101, and 10000.
#    - In the third position, three of the four numbers have a 1, so keep those three: 10110, 10111, and 10101.
#    - In the fourth position, two of the three numbers have a 1, so keep those two: 10110 and 10111.
#    - In the fifth position, there are an equal number of 0 bits and 1 bits (one each). So, to find the oxygen generator 
#      rating, keep the number with a 1 in that position: 10111.
#    - As there is only one number left, stop; the oxygen generator rating is 10111, or 23 in decimal.
#  
#  Then, to determine the CO2 scrubber rating value from the same example above:
#  
#    - Start again with all 12 numbers and consider only the first bit of each number. There are fewer 0 bits (5) than 1 bits (7), 
#      so keep only the 5 numbers with a 0 in the first position: 00100, 01111, 00111, 00010, and 01010.
#    - Then, consider the second bit of the 5 remaining numbers: there are fewer 1 bits (2) than 0 bits (3), so keep only the 2 numbers 
#      with a 1 in the second position: 01111 and 01010.
#    - In the third position, there are an equal number of 0 bits and 1 bits (one each). So, to find the CO2 scrubber rating, keep 
#      the number with a 0 in that position: 01010.
#    - As there is only one number left, stop; the CO2 scrubber rating is 01010, or 10 in decimal.
#  
#  Finally, to find the life support rating, multiply the oxygen generator rating (23) by the CO2 scrubber rating (10) to get 230.
#  
#  Use the binary numbers in your diagnostic report to calculate the oxygen generator rating and CO2 scrubber rating, then 
#  multiply them together. What is the life support rating of the submarine? (Be sure to represent your answer in decimal, not binary.)
#  


def calculate_oxygen_generator_rating(binary_numbers):
    return calculate_rate_part_2(binary_numbers, oxygen_generator_comparator)
### calculate_oxygen_generator_rating


def oxygen_generator_comparator(zero_list, one_list):
    # which list to keep
    if len(zero_list) > len(one_list):
        return zero_list
    elif len(zero_list) < len(one_list):
        return one_list
    else:
        return one_list
### oxygen_generator_comparator


def calculate_co2_scrubber_rating(binary_numbers):
    return calculate_rate_part_2(binary_numbers, co2_scrubber_comparator)
### calculate_oxygen_generator_rating

def co2_scrubber_comparator(zero_list, one_list):
    # which list to keep
    if len(zero_list) > len(one_list):
        return one_list
    elif len(zero_list) < len(one_list):
        return zero_list
    else:
        return zero_list
### co2_scrubber_comparator


def calculate_rate_part_2(binary_numbers, comparator):
    tmp_list = binary_numbers[:]        # clone the list, so I can mutate it.

    idx = -1     # which bit to consider

    while len(tmp_list) > 1:
        # move onto the next bit
        idx += 1

        # determine which bit is most significate in thie column
        zero_list = []
        one_list = []
        for num in tmp_list:
            if num[idx] == "0":
                zero_list.append(num)
            else:
                one_list.append(num)

        # which list to keep
        tmp_list = comparator(zero_list, one_list)


    # we have found the number
    return int(tmp_list[0], 2)
### calculate_rate_part_2


class DayXXPartTwoTests(unittest.TestCase):

    
    def test__part_2__sample_input(self):
        print("")
        binary_numbers = read_file_into_array(sample_input_file_1, False)
        oxygen_generator_rating = calculate_oxygen_generator_rating(binary_numbers)
        co2_scrubber_rating = calculate_co2_scrubber_rating(binary_numbers)

        self.assertEqual(oxygen_generator_rating, 23)
        self.assertEqual(co2_scrubber_rating, 10)


    def test__part_2__challenge_input(self):
        print("")

        binary_numbers = read_file_into_array(input_file, False)
        oxygen_generator_rating = calculate_oxygen_generator_rating(binary_numbers)
        co2_scrubber_rating = calculate_co2_scrubber_rating(binary_numbers)

        print("Solution to day 3 part 2: {0}".format(oxygen_generator_rating * co2_scrubber_rating))
        


# print("Solution to day 3 part 2: {0}".format(-1))
 

 
###################################################################################################################################################################
########################################################################## RUN THE TESTS ##########################################################################


# run then unit tests "last"
if __name__ == '__main__':
    unittest.main()
 

