#!/bin/python
# -*- coding: utf-8 -*-
# https://adventofcode.com/2020/day/10


###################################################################################################################################################################
#  
#  Solution to day 10 part 1: 2380
#
#  Solution to day 10 part 2: 48358655787008   (48 trillion)
#
###################################################################################################################################################################


###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################
#   
#   --- Day 10: Adapter Array ---
#   Patched into the aircraft's data port, you discover weather forecasts of a massive tropical 
#   storm. Before you can figure out whether it will impact your vacation plans, however, your 
#   device suddenly turns off!
#   
#   Its battery is dead.
#   
#   You'll need to plug it in. There's only one problem: the charging outlet near your seat 
#   produces the wrong number of jolts. Always prepared, you make a list of all of the joltage 
#   adapters in your bag.
#   
#   Each of your joltage adapters is rated for a specific output joltage (your puzzle input). 
#   Any given adapter can take an input 1, 2, or 3 jolts lower than its rating and still produce 
#   its rated output joltage.
#   
#   In addition, your device has a built-in joltage adapter rated for 3 jolts higher than the highest-rated 
#   adapter in your bag. (If your adapter list were 3, 9, and 6, your device's built-in adapter would 
#       be rated for 12 jolts.)
#   
#   Treat the charging outlet near your seat as having an effective joltage rating of 0.
#   
#   Since you have some time to kill, you might as well test all of your adapters. Wouldn't want to get to 
#   your resort and realize you can't even charge your device!
#   
#   If you use every adapter in your bag at once, what is the distribution of joltage differences between the 
#   charging outlet, the adapters, and your device?
#   
#   For example, suppose that in your bag, you have adapters with the following joltage ratings:
#   
#       16
#       10
#       15
#       5
#       1
#       11
#       7
#       19
#       6
#       12
#       4
#   
#   With these adapters, your device's built-in joltage adapter would be rated for 19 + 3 = 22 
#   jolts, 3 higher than the highest-rated adapter.
#   
#   Because adapters can only connect to a source 1-3 jolts lower than its rating, in order to use 
#   every adapter, you'd need to choose them like this:
#   
#   *   The charging outlet has an effective rating of 0 jolts, so the only adapters that could 
#       connect to it directly would need to have a joltage rating of 1, 2, or 3 jolts. Of these, 
#       only one you have is an adapter rated 1 jolt (difference of 1).
#   *   From your 1-jolt rated adapter, the only choice is your 4-jolt rated adapter (difference of 3).
#   *   From the 4-jolt rated adapter, the adapters rated 5, 6, or 7 are valid choices. However, in 
#       order to not skip any adapters, you have to pick the adapter rated 5 jolts (difference of 1).
#   *   Similarly, the next choices would need to be the adapter rated 6 and then the adapter rated 7 
#       (with difference of 1 and 1).
#   *   The only adapter that works with the 7-jolt rated adapter is the one rated 10 jolts (difference of 3).
#   *   From 10, the choices are 11 or 12; choose 11 (difference of 1) and then 12 (difference of 1).
#   *   After 12, only valid adapter has a rating of 15 (difference of 3), then 16 (difference of 1), 
#       then 19 (difference of 3).
#   *   Finally, your device's built-in adapter is always 3 higher than the highest adapter, so its rating 
#       is 22 jolts (always a difference of 3).
#   
#   In this example, when using every adapter, there are 7 differences of 1 jolt and 5 differences of 3 jolts.
#   
#   Here is a larger example:
#   
#       28
#       33
#       18
#       42
#       31
#       14
#       46
#       20
#       48
#       47
#       24
#       23
#       49
#       45
#       19
#       38
#       39
#       11
#       1
#       32
#       25
#       35
#       8
#       17
#       7
#       9
#       4
#       2
#       34
#       10
#       3
#   
#   In this larger example, in a chain that uses all of the adapters, there are 22 differences 
#   of 1 jolt and 10 differences of 3 jolts.
#   
#   Find a chain that uses all of your adapters to connect the charging outlet to your device's 
#   built-in adapter and count the joltage differences between the charging outlet, the adapters, 
#   and your device. What is the number of 1-jolt differences multiplied by the number of 3-jolt differences?
#   

def test_equal(actual, expected, message):
    if actual != expected:
        print("FAIL: Found={0}  Expected={1}    {2}".format(actual, expected, message))


sample_input_file   = "2020_10_sample.txt"
sample_input_file_2 = "2020_10_sample_2.txt"
input_file          = "2020_10_input.txt"



def get_joltage_adaptors(file_name, sort_output=False):
    joltage_adaptors = []

    with open(file_name) as f:
        for line in f:
            joltage_adaptors.append(int(line.strip()))
                
    if sort_output:
        joltage_adaptors = sorted(joltage_adaptors)

    return joltage_adaptors
### get_joltage_adaptors



def get_count_of_differences(joltage_adaptors, starting_joltage):
    count_of_1 = 0
    count_of_2 = 0
    count_of_3 = 0

    current_joltage = starting_joltage
    for adaptor in joltage_adaptors:
        diff = adaptor - current_joltage

        if diff == 1:
            count_of_1 += 1
        elif diff == 2:
            count_of_2 += 1
        elif diff == 3:
            count_of_3 += 1

        current_joltage = adaptor

    return count_of_1, count_of_2, count_of_3
### get_count_of_differences




print("--- P1 sample input ---")

joltage_adaptors = get_joltage_adaptors(sample_input_file, True)
count_of_1, count_of_2, count_of_3 = get_count_of_differences(joltage_adaptors, 0)
count_of_3 += 1 # for the built in adaptor

test_equal(count_of_1, 7, "P1A count of 1 wrong")
test_equal(count_of_3, 5, "P1A count of 3 wrong")


joltage_adaptors = get_joltage_adaptors(sample_input_file_2, True)
count_of_1, count_of_2, count_of_3 = get_count_of_differences(joltage_adaptors, 0)
count_of_3 += 1 # for the built in adaptor

test_equal(count_of_1, 22, "P1B count of 1 wrong")
test_equal(count_of_3, 10, "P1B count of 3 wrong")


print("-------------------------")


joltage_adaptors = get_joltage_adaptors(input_file, True)
count_of_1, count_of_2, count_of_3 = get_count_of_differences(joltage_adaptors, 0)
count_of_3 += 1 # for the built in adaptor



print("Solution to day 10 part 1: {0}".format(count_of_1 * count_of_3))


###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################
# 
# --- Part Two ---
# To completely determine whether you have enough adapters, you'll need to figure out how 
# many different ways they can be arranged. Every arrangement needs to connect the charging 
# outlet to your device. The previous rules about when adapters can successfully connect still apply.
# 
# The first example above (the one that starts with 16, 10, 15) supports the following arrangements:
# 
#     (0), 1, 4, 5, 6, 7, 10, 11, 12, 15, 16, 19, (22)
#     (0), 1, 4, 5, 6, 7, 10, 12, 15, 16, 19, (22)
#     (0), 1, 4, 5, 7, 10, 11, 12, 15, 16, 19, (22)
#     (0), 1, 4, 5, 7, 10, 12, 15, 16, 19, (22)
#     (0), 1, 4, 6, 7, 10, 11, 12, 15, 16, 19, (22)
#     (0), 1, 4, 6, 7, 10, 12, 15, 16, 19, (22)
#     (0), 1, 4, 7, 10, 11, 12, 15, 16, 19, (22)
#     (0), 1, 4, 7, 10, 12, 15, 16, 19, (22)
# 
# (The charging outlet and your device's built-in adapter are shown in parentheses.) Given the 
# adapters from the first example, the total number of arrangements that connect the charging 
# outlet to your device is 8.
# 
# The second example above (the one that starts with 28, 33, 18) has many arrangements. Here are a few:
# 
#     (0), 1, 2, 3, 4, 7, 8, 9, 10, 11, 14, 17, 18, 19, 20, 23, 24, 25, 28, 31, 32, 33, 34, 35, 38, 39, 42, 45, 46, 47, 48, 49, (52)
# 
#     (0), 1, 2, 3, 4, 7, 8, 9, 10, 11, 14, 17, 18, 19, 20, 23, 24, 25, 28, 31, 32, 33, 34, 35, 38, 39, 42, 45, 46, 47, 49, (52)
# 
#     (0), 1, 2, 3, 4, 7, 8, 9, 10, 11, 14, 17, 18, 19, 20, 23, 24, 25, 28, 31, 32, 33, 34, 35, 38, 39, 42, 45, 46, 48, 49, (52)
# 
#     (0), 1, 2, 3, 4, 7, 8, 9, 10, 11, 14, 17, 18, 19, 20, 23, 24, 25, 28, 31, 32, 33, 34, 35, 38, 39, 42, 45, 46, 49, (52)
# 
#     (0), 1, 2, 3, 4, 7, 8, 9, 10, 11, 14, 17, 18, 19, 20, 23, 24, 25, 28, 31, 32, 33, 34, 35, 38, 39, 42, 45, 47, 48, 49, (52)
# 
#     (0), 3, 4, 7, 10, 11, 14, 17, 20, 23, 25, 28, 31, 34, 35, 38, 39, 42, 45, 46, 48, 49, (52)
# 
#     (0), 3, 4, 7, 10, 11, 14, 17, 20, 23, 25, 28, 31, 34, 35, 38, 39, 42, 45, 46, 49, (52)
# 
#     (0), 3, 4, 7, 10, 11, 14, 17, 20, 23, 25, 28, 31, 34, 35, 38, 39, 42, 45, 47, 48, 49, (52)
# 
#     (0), 3, 4, 7, 10, 11, 14, 17, 20, 23, 25, 28, 31, 34, 35, 38, 39, 42, 45, 47, 49, (52)
# 
#     (0), 3, 4, 7, 10, 11, 14, 17, 20, 23, 25, 28, 31, 34, 35, 38, 39, 42, 45, 48, 49, (52)
# 
# In total, this set of adapters can connect the charging outlet to your device in 
# 19208 distinct arrangements.
# 
# You glance back down at your bag and try to remember why you brought so many adapters; 
# there must be more than a trillion valid ways to arrange them! Surely, there must be 
# an efficient way to count the arrangements.
# 
# What is the total number of distinct ways you can arrange the adapters to connect the 
# charging outlet to your device?
# 

def count_number_of_possible_arrangements(joltage_adaptors):
    
    # if 0 not in joltage_adaptors:
    #     joltage_adaptors.append(0)                      # add the initial node

    joltage_sorted = sorted(joltage_adaptors)
    joltage_sorted.append(joltage_sorted[-1] +3)        # add the final node, the devices charging cord.
    joltage_map = { i : None for i in joltage_sorted }
    joltage_map[0] = 1
    
    # node_weight = 1
    for adapter in joltage_sorted:

        ancestor_minus_1_weight = joltage_map.get(adapter -1, 0)
        ancestor_minus_2_weight = joltage_map.get(adapter -2, 0)
        ancestor_minus_3_weight = joltage_map.get(adapter -3, 0)

        node_weight = ancestor_minus_1_weight + ancestor_minus_2_weight + ancestor_minus_3_weight
        joltage_map[adapter] = node_weight

        # print("node: {0} \t-1→{1} \t-2→{2} \t-3→{3}  node_weight={4}".format(adapter, ancestor_minus_1_weight, ancestor_minus_2_weight, ancestor_minus_3_weight, node_weight))

    # print("result. {0} -> {1}".format(joltage_sorted[-1], joltage_map[ joltage_sorted[-1] ]))
    return joltage_map[ joltage_sorted[-1] ]

### count_number_of_possible_arrangements



print("--- P2 sample input ---")

joltage_adaptors = get_joltage_adaptors(sample_input_file, True)
test_equal(count_number_of_possible_arrangements(joltage_adaptors), 8, "P2A count of sample 1 is wrong")

joltage_adaptors = get_joltage_adaptors(sample_input_file_2, True)
test_equal(count_number_of_possible_arrangements(joltage_adaptors), 19208, "P2B count of sample 1 is wrong")

print("-------------------------")


joltage_adaptors = get_joltage_adaptors(input_file, True)
count_of_paths = count_number_of_possible_arrangements(joltage_adaptors)

print("Solution to day 10 part 2: {0}".format(count_of_paths))

 