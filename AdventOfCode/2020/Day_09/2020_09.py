#!/bin/python
# -*- coding: utf-8 -*-
# https://adventofcode.com/2020/day/9


###################################################################################################################################################################
#  
#  Solution to day 9 part 1: 
#
#  Solution to day 9 part 2: 
#
###################################################################################################################################################################


###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################
#   
#   --- Day 9: Encoding Error ---
#   With your neighbor happily enjoying their video game, you turn your attention to an open data 
#   port on the little screen in the seat in front of you.
#   
#   Though the port is non-standard, you manage to connect it to your computer through the clever 
#   use of several paperclips. Upon connection, the port outputs a series of numbers (your puzzle input).
#   
#   The data appears to be encrypted with the eXchange-Masking Addition System (XMAS) which, 
#   conveniently for you, is an old cypher with an important weakness.
#   
#   XMAS starts by transmitting a preamble of 25 numbers. After that, each number you receive should 
#   be the sum of any two of the 25 immediately previous numbers. The two numbers will have different 
#   values, and there might be more than one such pair.
#   
#   For example, suppose your preamble consists of the numbers 1 through 25 in a random order. To be 
#   valid, the next number must be the sum of two of those numbers:
#   
#       26 would be a valid next number, as it could be 1 plus 25 (or many other pairs, like 2 and 24).
#       49 would be a valid next number, as it is the sum of 24 and 25.
#       100 would not be valid; no two of the previous 25 numbers sum to 100.
#       50 would also not be valid; although 25 appears in the previous 25 numbers, the two numbers in the pair must be different.
#   
#   Suppose the 26th number is 45, and the first number (no longer an option, as it is more than 25 
#   numbers ago) was 20. Now, for the next number to be valid, there needs to be some pair of numbers 
#   among 1-19, 21-25, or 45 that add up to it:
#   
#       26 would still be a valid next number, as 1 and 25 are still within the previous 25 numbers.
#       65 would not be valid, as no two of the available numbers sum to it.
#       64 and 66 would both be valid, as they are the result of 19+45 and 21+45 respectively.
#   
#   Here is a larger example which only considers the previous 5 numbers (and has a preamble of length 5):
#   
#       35
#       20
#       15
#       25
#       47
#       40
#       62
#       55
#       65
#       95
#       102
#       117
#       150
#       182
#       127
#       219
#       299
#       277
#       309
#       576
#   
#   In this example, after the 5-number preamble, almost every number is the sum of two of the previous 5 
#   numbers; the only number that does not follow this rule is 127.
#   
#   The first step of attacking the weakness in the XMAS data is to find the first number in the list 
#   (after the preamble) which is not the sum of two of the 25 numbers before it. What is the first 
#   number that does not have this property?
#   


def test_equal(actual, expected, message):
    if actual != expected:
        print("FAIL: Found={0}  Expected={1}    {2}".format(actual, expected, message))


sample_input_file   = "2020_09_sample.txt"
sample_input_file_2 = "2020_09_sample_2.txt"
input_file          = "2020_09_input.txt"


class XmasCipher:
    def __init__(self, preamble_length, preamble_sequence):
        self.preamble_length = preamble_length
        self.sequence = preamble_sequence.copy()
        

    def test_next_number(self, test_number):
        # return True if valid, False is not valid
        for i in range(self.preamble_length):
            for j in range(i+1, self.preamble_length, 1):
                a = self.sequence[i]
                b = self.sequence[j]

                # print("test: x={0}\ta={1}\tb={2}".format(test_number, a, b))
                if a + b == test_number:
                    # we found a pair 
                    return True


        return False


    def add_next_number(self, number, override_test=False):
        if override_test or self.test_next_number(number):
            # the provided number was valid, add to list.
            self.sequence.pop(0)
            self.sequence.append(number)
            return True

        else:
            # the provided number was bad. throw and error
            return False

    def print_sequence(self):
        print(self.sequence)

##### XmasCipher

def read_xmas_cipher_file(file_name):
    all_cipher_entrier = []
    with open(file_name) as f:
        for line in f:
            all_cipher_entrier.append(int(line.strip()))

    return all_cipher_entrier
### read_xmas_cipher_file


print("--- P1 sample input ---")
read_xmas_cipher_file_sample_1 = read_xmas_cipher_file(sample_input_file)
xmas_ciphter_sample_1 = XmasCipher(25, read_xmas_cipher_file_sample_1[:25])
test_equal(xmas_ciphter_sample_1.test_next_number(26), True, "P1A test 26 failed")
test_equal(xmas_ciphter_sample_1.test_next_number(49), True, "P1A test 49 failed")
test_equal(xmas_ciphter_sample_1.test_next_number(100), False, "P1A test 100 failed")
test_equal(xmas_ciphter_sample_1.test_next_number(50), False, "P1A test 50 failed")

# this mutates the object. not great for a unit test, but this is a coding comp. not production code.
test_equal(xmas_ciphter_sample_1.add_next_number(45), True, "P1A loading 45 failed")

test_equal(xmas_ciphter_sample_1.test_next_number(26), True, "P1A test 26 failed")
test_equal(xmas_ciphter_sample_1.test_next_number(65), False, "P1A test 65 failed")
test_equal(xmas_ciphter_sample_1.test_next_number(64), True, "P1A test 64 failed")
test_equal(xmas_ciphter_sample_1.test_next_number(66), True, "P1A test 66 failed")

test_equal(xmas_ciphter_sample_1.add_next_number(45), True, "P1A loading 45 failed")

# sample P1B - load the long list above, with preamble 5
read_xmas_cipher_file_sample_2 = read_xmas_cipher_file(sample_input_file_2)
xmas_ciphter_sample_2 = XmasCipher(5, read_xmas_cipher_file_sample_2[:5])

sample_found = False
for i in range(5, len(read_xmas_cipher_file_sample_2), 1):
    result = xmas_ciphter_sample_1.add_next_number(read_xmas_cipher_file_sample_2[i])
    if not result:
        test_equal(result, 127, "P1B first invalid number not 127")
        sample_found = True

test_equal(sample_found, True, "P1B No invalid numbers found")

print("-------------------------")





print("Solution to day 9 part 1: {0}".format(-1))


###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################


print("--- P2 sample input ---")

print("-------------------------")



print("Solution to day 9 part 2: {0}".format(-1))

 