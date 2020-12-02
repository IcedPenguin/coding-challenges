#!/bin/python
# -*- coding: utf-8 -*-
# https://adventofcode.com/2020/day/1


###################################################################################################################################################################
#  
#  Solution to day 1 part 1: 
#     entry_one: 1721
#     entry_two: 299
#     Solution to day 1 part 1: 514579
#
#  Solution to day 1 part 2: 
#     entry_one:   945
#     entry_two:   657
#     entry_three: 418
#     Solution to day 1 part 2: 259521570
#
###################################################################################################################################################################


###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################

# --- Day 1: Report Repair ---
#
# After saving Christmas five years in a row, you've decided to take a vacation at a nice resort on a tropical 
# island. Surely, Christmas will go on without you.
#
# The tropical island has its own currency and is entirely cash-only. The gold coins used there have a little 
# picture of a starfish; the locals just call them stars. None of the currency exchanges seem to have heard of 
# them, but somehow, you'll need to find fifty of these coins by the time you arrive so you can pay the deposit 
# on your room.
#
# To save your vacation, you need to get all fifty stars by December 25th.
#
# Collect stars by solving puzzles. Two puzzles will be made available on each day in the Advent calendar; the 
# second puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!
#
# Before you leave, the Elves in accounting just need you to fix your expense report (your puzzle input); 
# apparently, something isn't quite adding up.
#
# Specifically, they need you to find the two entries that sum to 2020 and then multiply those two numbers together.
#
# For example, suppose your expense report contained the following:
#       1721
#       979
#       366
#       299
#       675
#       1456
#
# In this list, the two entries that sum to 2020 are 1721 and 299. Multiplying them together 
# produces 1721 * 299 = 514579, so the correct answer is 514579.
#
# Of course, your expense report is much larger. Find the two entries that sum to 2020; what do 
# you get if you multiply them together?
#
# Your puzzle answer was 987339.


input_file = "2020_01_p1_sample.txt"
input_file = "2020_01_input.txt"
list_of_inputs = []

complement_list = []
entry_one = 0
entry_two = 0
target_sum = 2020

with open(input_file) as f:
    drift = 0
    for line in f:
        list_of_inputs.append(int(line))
        

for current_value in list_of_inputs:
    # print(current_value)
    # print( complement_list)
    complement = target_sum - current_value
    if current_value in complement_list:
        entry_two = current_value
        entry_one = complement
    else:
        complement_list.append(complement)
        
solution = entry_one * entry_two
        
print( "entry_one: " + str(entry_one) )
print( "entry_two: " + str(entry_two) )
print( "Solution to day 1 part 1: " + str(solution) )



###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################


# --- Part Two ---
#
# The Elves in accounting are thankful for your help; one of them even offers you a starfish coin they had left over 
# from a past vacation. They offer you a second one if you can find three numbers in your expense report that meet the same criteria.
#
# Using the above example again, the three entries that sum to 2020 are 979, 366, and 675. Multiplying them together 
# produces the answer, 241861950.
#
# In your expense report, what is the product of the three entries that sum to 2020?


complement_list = []
entry_three = 0

# build up the complement list
for current_value in list_of_inputs:
    complement_list.append(target_sum - current_value)



count = len(list_of_inputs)
for i in range(count):
    for j in range(i+1,count):
        # print("i=",i,"j=",j)

        intermediate_sum = list_of_inputs[i] + list_of_inputs[j]
        complement = target_sum - intermediate_sum
        if intermediate_sum in complement_list:
            entry_one   = complement
            entry_two   = list_of_inputs[i]
            entry_three = list_of_inputs[j]

solution = entry_one * entry_two * entry_three
        
print( "entry_one:   " + str(entry_one) )
print( "entry_two:   " + str(entry_two) )
print( "entry_three: " + str(entry_three) )
print( "Solution to day 1 part 2: " + str(solution) )

