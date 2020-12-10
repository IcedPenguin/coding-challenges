#!/bin/python
# -*- coding: utf-8 -*-
# https://adventofcode.com/2020/day/5


###################################################################################################################################################################
#  
#  Solution to day 5 part 1:  987
#
#  Solution to day 5 part 2:  603
#
###################################################################################################################################################################


###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################
#
# --- Day 5: Binary Boarding ---
# You board your plane only to discover a new problem: you dropped your boarding pass! You aren't sure 
# which seat is yours, and all of the flight attendants are busy with the flood of people that suddenly 
# made it through passport control.
# 
# You write a quick program to use your phone's camera to scan all of the nearby boarding passes (your 
# puzzle input); perhaps you can find your seat through process of elimination.
# 
# Instead of zones or groups, this airline uses binary space partitioning to seat people. A seat might 
# be specified like FBFBBFFRLR, where F means "front", B means "back", L means "left", and R means "right".
# 
# The first 7 characters will either be F or B; these specify exactly one of the 128 rows on the plane 
# (numbered 0 through 127). Each letter tells you which half of a region the given seat is in. Start 
# with the whole list of rows; the first letter indicates whether the seat is in the front (0 through 63) 
# or the back (64 through 127). The next letter indicates which half of that region the seat is in, and 
# so on until you're left with exactly one row.
# 
# For example, consider just the first seven characters of FBFBBFFRLR:
# 
#     Start by considering the whole range, rows 0 through 127.
#     F means to take the lower half, keeping rows 0 through 63.
#     B means to take the upper half, keeping rows 32 through 63.
#     F means to take the lower half, keeping rows 32 through 47.
#     B means to take the upper half, keeping rows 40 through 47.
#     B keeps rows 44 through 47.
#     F keeps rows 44 through 45.
#     The final F keeps the lower of the two, row 44.
# 
# The last three characters will be either L or R; these specify exactly one of the 8 columns of seats 
# on the plane (numbered 0 through 7). The same process as above proceeds again, this time with only 
# three steps. L means to keep the lower half, while R means to keep the upper half.
# 
# For example, consider just the last 3 characters of FBFBBFFRLR:
# 
#     Start by considering the whole range, columns 0 through 7.
#     R means to take the upper half, keeping columns 4 through 7.
#     L means to take the lower half, keeping columns 4 through 5.
#     The final R keeps the upper of the two, column 5.
# 
# So, decoding FBFBBFFRLR reveals that it is the seat at row 44, column 5.
# 
# Every seat also has a unique seat ID: multiply the row by 8, then add the column. In this 
# example, the seat has ID 44 * 8 + 5 = 357.
# 
# Here are some other boarding passes:
# 
#     BFFFBBFRRR: row 70, column 7, seat ID 567.
#     FFFBBBFRRR: row 14, column 7, seat ID 119.
#     BBFFBBFRLL: row 102, column 4, seat ID 820.
# 
# As a sanity check, look through your list of boarding passes. 
# What is the highest seat ID on a boarding pass?
# 

def test_equal(actual, expected, message):
    if actual != expected:
        print("FAIL: Found={0}  Expected={1}    {2}".format(actual, expected, message))




# sample_input_file = "2020_05_sample.txt"
input_file = "2020_05_input.txt"


class BoardingPass:  
    
    def __init__(self, encoded_boarding_pass):  
        self.row    = BoardingPass.decode_number(encoded_boarding_pass[:7], 0, 127)
        self.column = BoardingPass.decode_number(encoded_boarding_pass[7:10], 0, 7)
        self.id     = self.row * 8 + self.column

    @staticmethod
    def decode_number(encoded_information, lower, upper):
        FRONT_ = ["F", "L"]
        BACK_  = ["B", "R"]

        for c in encoded_information:
            # m = int(((0.5 + upper - lower - 0.5) / 2) + lower)
            m = ((upper - lower) / 2) + lower
            # print("decode: START  \t{0} \t{1} \t{2} \t{3}".format(c, lower, upper, m))

            if c in FRONT_:
                upper = m
                m = upper

            elif c in BACK_:
                lower = m+1
                m = lower

            # print("decode: END    \t{0} \t{1} \t{2} \t{3}".format(c, lower, upper, m))
            # print("")

        return m

    def get_row(self):
        return self.row

    def get_column(self):
        return self.column

    def get_id(self):
        return self.id

print("--- P1 sample input ---")

boarding_pass = BoardingPass("FBFBBFFRLR")
test_equal(boarding_pass.get_row(),    44, "sample input 1, get_row")
test_equal(boarding_pass.get_column(),  5, "sample input 1, get_column")
test_equal(boarding_pass.get_id(),    357, "sample input 1, get_id")


boarding_pass = BoardingPass("BFFFBBFRRR")
test_equal(boarding_pass.get_row(),    70, "sample input 2, get_row")
test_equal(boarding_pass.get_column(),  7, "sample input 2, get_column")
test_equal(boarding_pass.get_id(),    567, "sample input 2, get_id")

boarding_pass = BoardingPass("FFFBBBFRRR")
test_equal(boarding_pass.get_row(),     14, "sample input 3, get_row")
test_equal(boarding_pass.get_column(),   7, "sample input 3, get_column")
test_equal(boarding_pass.get_id(),     119, "sample input 3, get_id")

boarding_pass = BoardingPass("BBFFBBFRLL")
test_equal(boarding_pass.get_row(),    102, "sample input 4, get_row")
test_equal(boarding_pass.get_column(),   4, "sample input 4, get_column")
test_equal(boarding_pass.get_id(),     820, "sample input 4, get_id")

print("-------------------------")



with open(input_file) as f:
    max_id = -1
    for line in f:
        boarding_pass = BoardingPass(line.strip())
        
        if max_id < boarding_pass.get_id():
            max_id = boarding_pass.get_id()


print("Solution to day 5 part 1: {0}".format(max_id))


###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################
# 
# --- Part Two ---
# Ding! The "fasten seat belt" signs have turned on. Time to find your seat.
# 
# It's a completely full flight, so your seat should be the only missing boarding pass in your 
# list. However, there's a catch: some of the seats at the very front and back of the plane 
# don't exist on this aircraft, so they'll be missing from your list as well.
# 
# Your seat wasn't at the very front or back, though; the seats with IDs +1 and -1 from yours 
# will be in your list.
# 
# What is the ID of your seat?

# print("--- Testing P2 Sample ---")
# 
# print("-------------------------")

with open(input_file) as f:
    passenger_boarding_pass_ids = []
    for line in f:
        boarding_pass = BoardingPass(line.strip())
        passenger_boarding_pass_ids.append(boarding_pass.get_id())

    passenger_boarding_pass_ids = sorted(passenger_boarding_pass_ids)

    # start at beginning, look for the first gap.
    for i in range(len(passenger_boarding_pass_ids) -1):
        lower_buddy = passenger_boarding_pass_ids[i]

        # look for a gap.
        if passenger_boarding_pass_ids[i +1] == lower_buddy+2:
            empty_seat_with_buddies = lower_buddy +1


print("Solution to day 5 part 2: {0}".format(empty_seat_with_buddies))


