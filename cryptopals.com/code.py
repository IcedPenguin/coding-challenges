#!/bin/python
# -*- coding: utf-8 -*-
# Cryptopals.com


###################################################################################################################################################################
#
#   Utility functions
#
###################################################################################################################################################################
import binascii

def util__hex_string_to_bytearray(hex_string):
    return bytearray.fromhex(hex_string)
### util__hex_string_to_bytearray


def util__bytearray_to_hex_string(byte_array):
    return ''.join('{:02x}'.format(x) for x in byte_array)
### util__bytearray_to_hex_string


def util__base64_to_bytearray(base64):
    return binascii.a2b_base64(base64)
### util__base64_to_bytearray


def util__bytearray_to_base64(byte_array):
    return binascii.b2a_base64(byte_array).strip()
### util__bytearray_to_base64


def util__xor_equal_length_buffers(byte_array_1, byte_array_2):
    if len(byte_array_1) != len(byte_array_2):
        raise Exception("input byte arrays need to be the same length. b1={0} b2={1}".format(len(byte_array_1), len(byte_array_2)))

    xor_array = []
    for i in xrange(len(byte_array_1)):
        xor_array.append(byte_array_1[i] ^ byte_array_2[i])

    return xor_array
### util__xor_equal_length_buffers


def util__xor_single_byte(byte_array_1, xor_byte):
    xor_byte_array = [xor_byte] * len(byte_array_1)
    return util__xor_equal_length_buffers(byte_array_1, xor_byte_array)
### util__xor_single_byte



###################################################################################################################################################################
#
#   Scoring Functions
#
###################################################################################################################################################################



