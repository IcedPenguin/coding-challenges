#!/bin/python
# -*- coding: utf-8 -*-
# Cryptopals.com

import code

###################################################################################################################################################################
#
#   Crypto Challenge Set 1
#   https://cryptopals.com/sets/1
#
###################################################################################################################################################################

def check_answer(challenge, expected, actual):
    if expected != actual:
        print "---------------------------------"
        print "Challenge %s Failed" % (challenge)
        print "Expected: %s" % (expected)
        print "Actual:   %s" % (actual)
        print "---------------------------------"
    else:
        print "Challenge %s Passed" % (challenge)
 

###################################################################################################################################################################
# 
# 1.1 Convert hex to base64
#
set_1_challenge_1_input = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
set_1_challenge_1_output_expected = "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"

set_1_challenge_1_output_actual = code.util__bytearray_to_base64( code.util__hex_string_to_bytearray(set_1_challenge_1_input) )

check_answer(1, set_1_challenge_1_output_expected, set_1_challenge_1_output_actual)


###################################################################################################################################################################
# 
# 1.2 Fixed XOR
#
set_1_challenge_2_input_1 = "1c0111001f010100061a024b53535009181c"
set_1_challenge_2_input_2 = "686974207468652062756c6c277320657965"
set_1_challenge_2_output_expected = "746865206b696420646f6e277420706c6179"

input_2_1 = code.util__hex_string_to_bytearray(set_1_challenge_2_input_1)
input_2_2 = code.util__hex_string_to_bytearray(set_1_challenge_2_input_2)

output_2 = code.util__xor_equal_length_buffers(input_2_1, input_2_2)
set_1_challenge_2_output_actual = code.util__bytearray_to_hex_string(output_2)

check_answer(2, set_1_challenge_2_output_expected, set_1_challenge_2_output_actual)


###################################################################################################################################################################
# 
# 1.3 Single-byte XOR cipher
#




###################################################################################################################################################################
# 
# 1.4 Detect single-character XOR
#




###################################################################################################################################################################
# 
# 1.5 Implement repeating-key XOR
#




###################################################################################################################################################################
# 
# 1.6 Break repeating-key XOR
#




###################################################################################################################################################################
# 
# 1.7 AES in ECB mode
#




###################################################################################################################################################################
# 
# 1.8 Detect AES in ECB mode
#




