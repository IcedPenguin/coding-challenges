#!/bin/python
# -*- coding: utf-8 -*-
# https://adventofcode.com/2020/day/9


###################################################################################################################################################################
#  
#  Solution to day 9 part 1: 1492208709
#
#  Solution to day 9 part 2: 238243506
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
        self.sequence = list(preamble_sequence)
        

    def test_next_number(self, test_number):
        # return True if valid, False is not valid
        # print("Test: x={0}\tsq={1}".format(test_number, self.sequence))

        for i in range(self.preamble_length):
            for j in range(i+1, self.preamble_length, 1):
                a = self.sequence[i]
                b = self.sequence[j]

                
                if a + b == test_number:
                    # print("test: x={0}\ta={1}\tb={2}".format(test_number, a, b))
                    # we found a pair 
                    return True


        return False


    def add_next_number(self, number, override_test=False):
        if override_test or self.test_next_number(number):
            self.sequence.pop(0)
            self.sequence.append(number)
            return True

        else:
            # the provided number was bad. ignore it.
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


def find_first_non_sum_value(sequences, xmas_ciphter, preamble_length):

    for i in range(len(sequences)):
        result = xmas_ciphter.add_next_number(sequences[i])
        if not result:
            # test_equal(sequences[i], 127, "P1B first invalid number not 127")
            return True, sequences[i]

    return False, None
### find_first_non_sum_value

print("--- P1 sample input ---")
read_xmas_cipher_file_sample_1 = read_xmas_cipher_file(sample_input_file)
xmas_ciphter_sample_1 = XmasCipher(25, read_xmas_cipher_file_sample_1[:25])
test_equal(xmas_ciphter_sample_1.test_next_number(26), True, "P1A test 26 failed")
test_equal(xmas_ciphter_sample_1.test_next_number(49), True, "P1A test 49 failed")
test_equal(xmas_ciphter_sample_1.test_next_number(100), False, "P1A test 100 failed")
test_equal(xmas_ciphter_sample_1.test_next_number(50), False, "P1A test 50 failed")

test_equal(xmas_ciphter_sample_1.add_next_number(45), True, "P1A loading 45 failed")

test_equal(xmas_ciphter_sample_1.test_next_number(26), True, "P1A test 26 failed")
test_equal(xmas_ciphter_sample_1.test_next_number(65), False, "P1A test 65 failed")
test_equal(xmas_ciphter_sample_1.test_next_number(64), True, "P1A test 64 failed")
test_equal(xmas_ciphter_sample_1.test_next_number(66), True, "P1A test 66 failed")

test_equal(xmas_ciphter_sample_1.add_next_number(45), True, "P1A loading 45 failed")

# sample P1B - load the long list above, with preamble 5
read_xmas_cipher_file_sample_2 = read_xmas_cipher_file(sample_input_file_2)
xmas_ciphter_sample_2 = XmasCipher(5, read_xmas_cipher_file_sample_2[:5])

found, non_sum_value = find_first_non_sum_value(read_xmas_cipher_file_sample_2[5:], xmas_ciphter_sample_2, 5)
test_equal(non_sum_value, 127, "P1B first invalid number not 127")
test_equal(found, True, "P1B No invalid numbers found")

print("-------------------------")



read_xmas_cipher_file_contents = read_xmas_cipher_file(input_file)
xmas_ciphter = XmasCipher(25, read_xmas_cipher_file_contents[:25])

found, non_sum_value = find_first_non_sum_value(read_xmas_cipher_file_contents[25:], xmas_ciphter, 25)

print("Solution to day 9 part 1: {0}".format(non_sum_value))


###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################
#
#   --- Part Two ---
#   The final step in breaking the XMAS encryption relies on the invalid number you just found: you 
#   must find a contiguous set of at least two numbers in your list which sum to the invalid number 
#   from step 1.
#   
#   Again consider the above example:
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
#   In this list, adding up all of the numbers from 15 through 40 produces the invalid number from 
#   step 1, 127. (Of course, the contiguous set of numbers in your actual list might be much longer.)
#   
#   To find the encryption weakness, add together the smallest and largest number in this contiguous 
#   range; in this example, these are 15 and 47, producing 62.
#   

def find_contiguous_set_summing_to_target_return_smallest_and_largest(sequence, target):
    len_sequence = len(sequence)
    for i in range(len_sequence -1):

        sum_of_numbers = 0
        j = 0

        while sum_of_numbers < target and i + j < len_sequence:
            sum_of_numbers += sequence[i + j]
            j += 1


        if sum_of_numbers == target:
            sequence_slice = sequence[i : i+j]
            # print("slice found: i={0}\tj={1}\tx={2}\tl={3}".format(i, i+j, target, sequence_slice))
            sorted_numbers = sorted(sequence_slice)
            
            return True, sorted_numbers[0], sorted_numbers[-1]

    # we failed to find the sum
    return False, None, None

### find_contiguous_set_summing_to_target_return_smallest_and_largest

print("--- P2 sample input ---")

xmas_cipher_file_sample_2_contents = read_xmas_cipher_file(sample_input_file_2)
xmas_ciphter_sample_2 = XmasCipher(5, read_xmas_cipher_file_sample_2[:5])
found, smallest, largest = find_contiguous_set_summing_to_target_return_smallest_and_largest(read_xmas_cipher_file_sample_2, 127)

test_equal(found, True, "P2A List of contiguous numbers was not found.")
test_equal(smallest, 15, "P2A returned smallest was incorrect")
test_equal(largest, 47, "P2A returned largest was incorrect")
test_equal(smallest + largest, 62, "P2A math doesn't work")

print("-------------------------")



found, smallest, largest = find_contiguous_set_summing_to_target_return_smallest_and_largest(read_xmas_cipher_file_contents, non_sum_value)

print("Solution to day 9 part 2: {0}".format(smallest + largest))

 