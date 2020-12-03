#!/bin/python
# -*- coding: utf-8 -*-
# https://adventofcode.com/2020/day/2


###################################################################################################################################################################
#  
#  Solution to day 2 part 1: 622
#       valid_password_count =  622
#       invalid_password_count =  378
#
#  Solution to day 2 part 2: 263
#
###################################################################################################################################################################


###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################

# --- Day 2: Password Philosophy ---
#
# Your flight departs in a few days from the coastal airport; the easiest way down to the coast from here 
# is via toboggan.
#
# The shopkeeper at the North Pole Toboggan Rental Shop is having a bad day. "Something's wrong with our 
# computers; we can't log in!" You ask if you can take a look.
#
# Their password database seems to be a little corrupted: some of the passwords wouldn't have been allowed 
# by the Official Toboggan Corporate Policy that was in effect when they were chosen.
#
# To try to debug the problem, they have created a list (your puzzle input) of passwords (according to the 
# corrupted database) and the corporate policy when that password was set.
#
# For example, suppose you have the following list:
#
#       1-3 a: abcde
#       1-3 b: cdefg
#       2-9 c: ccccccccc
#
# Each line gives the password policy and then the password. The password policy indicates the lowest and 
# highest number of times a given letter must appear for the password to be valid. For example, 1-3 a means 
# that the password must contain a at least 1 time and at most 3 times.
#
# In the above example, 2 passwords are valid. The middle password, cdefg, is not; it contains no instances 
# of b, but needs at least 1. The first and third passwords are valid: they contain one a or nine c, both 
# within the limits of their respective policies.
#
# How many passwords are valid according to their policies?
#  
import re


input_file = "2020_02_sample.txt"
input_file = "2020_02_input.txt"
file_lines = []


with open(input_file) as f:
    drift = 0
    for line in f:
        file_lines.append(line)
        

def parse_password_rule(raw_rule):
    # Sample input: 1-3 a
    # output:
    #   min: int
    #   max: int
    #  char: char
    plain = raw_rule.strip()
    parts = plain.replace("-", " ").split(" ")

    min_count = int(parts[0])
    max_count = int(parts[1])
    target_char = parts[2]
    return min_count, max_count, target_char

valid_password_count = 0
invalid_password_count = 0

for a in file_lines:
    p = a.split(":")
    s, l, c = parse_password_rule(p[0])
    # print(s)
    # print(l)
    # print(c)
    # print(s, "\t", l, "\t", c)

    target_letter_count = 0
    for letter in p[1]:
        if letter == c:
            target_letter_count += 1

    if s <= target_letter_count and target_letter_count <= l:
        valid_password_count += 1
        # print(a.strip(), "\t valid")
    else:
        invalid_password_count += 1
        # print(a.strip(), "\t invalid")

print("valid_password_count = ", valid_password_count)
print("invalid_password_count = ", invalid_password_count)

print( "Solution to day 2 part 1: ", valid_password_count)



###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################
# 
# --- Part Two ---
# 
# While it appears you validated the passwords correctly, they don't seem to be what the Official Toboggan Corporate 
# Authentication System is expecting.
# 
# The shopkeeper suddenly realizes that he just accidentally explained the password policy rules from his old job 
# at the sled rental place down the street! The Official Toboggan Corporate Policy actually works a little differently.
# 
# Each policy actually describes two positions in the password, where 1 means the first character, 2 means the second 
# character, and so on. (Be careful; Toboggan Corporate Policies have no concept of "index zero"!) Exactly one of 
# these positions must contain the given letter. Other occurrences of the letter are irrelevant for the purposes of 
# policy enforcement.
# 
# Given the same example list from above:
# 
#     1-3 a: abcde is valid: position 1 contains a and position 3 does not.
#     1-3 b: cdefg is invalid: neither position 1 nor position 3 contains b.
#     2-9 c: ccccccccc is invalid: both position 2 and position 9 contain c.
# 
# How many passwords are valid according to the new interpretation of the policies?
# 
# 

valid_password_count = 0
invalid_password_count = 0

def check_position_for_match(string, position, target):
    if len(string) <= position or position < 0:
        return False
    return string[position] == target
### check_position_for_match

for a in file_lines:
    p = a.split(":")
    s, l, c = parse_password_rule(p[0])


    # determine the indices to look at. work with their "we index from 1" non-sense. 
    index_one = s -1
    index_two = l -1
    password = p[1]

    
    position_one_matches = check_position_for_match(password, s, c)
    position_two_matches = check_position_for_match(password, l, c) 

    result = bool(position_one_matches) ^ bool(position_two_matches) # xor


    if result:
        valid_password_count += 1
    else:
        invalid_password_count += 1

print( "Solution to day 2 part 2: ", valid_password_count)

