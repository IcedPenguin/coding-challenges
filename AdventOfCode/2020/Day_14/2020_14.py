#!/bin/python
# -*- coding: utf-8 -*-
# https://adventofcode.com/2020/day/14


###################################################################################################################################################################
#  
#  Solution to day 14 part 1: 8471403462063
#
#  Solution to day 14 part 2: 2667858637669
#
###################################################################################################################################################################

import unittest


###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################
#   
#   --- Day 14: Docking Data ---
#   As your ferry approaches the sea port, the captain asks for your help again. The computer system that runs 
#   this port isn't compatible with the docking program on the ferry, so the docking parameters aren't being 
#   correctly initialized in the docking program's memory.
#   
#   After a brief inspection, you discover that the sea port's computer system uses a strange bitmask system 
#   in its initialization program. Although you don't have the correct decoder chip handy, you can emulate it 
#   in software!
#   
#   The initialization program (your puzzle input) can either update the bitmask or write a value to memory. 
#   Values and memory addresses are both 36-bit unsigned integers. For example, ignoring bitmasks for a moment, 
#   a line like mem[8] = 11 would write the value 11 to memory address 8.
#   
#   The bitmask is always given as a string of 36 bits, written with the most significant bit (representing 2^35) 
#   on the left and the least significant bit (2^0, that is, the 1s bit) on the right. The current bitmask is 
#   applied to values immediately before they are written to memory: a 0 or 1 overwrites the corresponding bit 
#   in the value, while an X leaves the bit in the value unchanged.
#   
#   For example, consider the following program:
#   
#       mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
#       mem[8] = 11
#       mem[7] = 101
#       mem[8] = 0
#   
#   This program starts by specifying a bitmask (mask = ....). The mask it specifies will overwrite two bits 
#   in every written value: the 2s bit is overwritten with 0, and the 64s bit is overwritten with 1.
#   
#   The program then attempts to write the value 11 to memory address 8. By expanding everything out to 
#   individual bits, the mask is applied as follows:
#   
#       value:  000000000000000000000000000000001011  (decimal 11)
#       mask:   XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
#       result: 000000000000000000000000000001001001  (decimal 73)
#   
#   So, because of the mask, the value 73 is written to memory address 8 instead. Then, the program tries 
#   to write 101 to address 7:
#   
#       value:  000000000000000000000000000001100101  (decimal 101)
#       mask:   XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
#       result: 000000000000000000000000000001100101  (decimal 101)
#   
#   This time, the mask has no effect, as the bits it overwrote were already the values the mask tried to 
#   set. Finally, the program tries to write 0 to address 8:
#   
#       value:  000000000000000000000000000000000000  (decimal 0)
#       mask:   XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
#       result: 000000000000000000000000000001000000  (decimal 64)
#   
#   64 is written to address 8 instead, overwriting the value that was there previously.
#   
#   To initialize your ferry's docking program, you need the sum of all values left in memory after 
#   the initialization program completes. (The entire 36-bit address space begins initialized to the 
#   value 0 at every address.) In the above example, only two values in memory are not zero - 101 
#   (at address 7) and 64 (at address 8) - producing a sum of 165.
#   
#   Execute the initialization program. What is the sum of all values left in memory after it completes? 
#   (Do not truncate the sum to 36 bits.)
#   


sample_input_file_1 = "2020_14_sample_1.txt"
sample_input_file_2 = "2020_14_sample_2.txt"
input_file          = "2020_14_input.txt"



def set_bit(value, bit):
    return value | (1<<bit)

def clear_bit(value, bit):
    return value & ~(1<<bit)

def apply_bit_mask(bit_mask, value):
    bit_mask_length = len(bit_mask)
    
    for i in range(bit_mask_length):
        current_bit_mask_value = bit_mask[bit_mask_length -i -1]
        
        if current_bit_mask_value == "X":
            pass

        elif current_bit_mask_value == "1":
            value = set_bit(value, i)

        elif current_bit_mask_value == "0" :
            value = clear_bit(value, i)

        else:
            pass

    return value
### apply_bit_mask


def process_program_file(file_name):
    mem = {}
    bit_mask = 0

    with open(file_name) as f:
        for line in f:
            parts = line.split("=")   #line.strip()

            if parts[0] == "mask ":
                bit_mask = parts[1].strip()
            
            else: 
                address = int( parts[0].replace("mem[", "").replace("]", "") )
                value = int( parts[1].strip() )
                mem[address] = apply_bit_mask(bit_mask, value)

    return mem
### process_program_file


def sum_all_memory_addresses(memory):
    total = 0
    for key in memory:
        total += memory[key]

    return total
### sum_all_memory_addresses



class Day14PartOneTests(unittest.TestCase):

    def test__apply_bit_mask__input_1(self):
        self.assertEqual(apply_bit_mask("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X",  11), 73)


    def test__apply_bit_mask__input_2(self):
        self.assertEqual(apply_bit_mask("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X", 101), 101)

    def test__apply_bit_mask__input_3(self):
        self.assertEqual(apply_bit_mask("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X",   0),  64)

    def test__part_2__sample_input(self):
        memory_example = process_program_file(sample_input_file_1)
        self.assertEqual(sum_all_memory_addresses(memory_example), 165)


memory = process_program_file(input_file)
total = sum_all_memory_addresses(memory)


print("Solution to day 14 part 1: {0}".format(total))



###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################
#   
#   --- Part Two ---
#   For some reason, the sea port's computer system still can't communicate with your ferry's 
#   docking program. It must be using version 2 of the decoder chip!
#   
#   A version 2 decoder chip doesn't modify the values being written at all. Instead, it acts 
#   as a memory address decoder. Immediately before a value is written to memory, each bit in 
#   the bitmask modifies the corresponding bit of the destination memory address in the following way:
#   
#       If the bitmask bit is 0, the corresponding memory address bit is unchanged.
#       If the bitmask bit is 1, the corresponding memory address bit is overwritten with 1.
#       If the bitmask bit is X, the corresponding memory address bit is floating.
#   
#   A floating bit is not connected to anything and instead fluctuates unpredictably. In practice, 
#   this means the floating bits will take on all possible values, potentially causing many memory 
#   addresses to be written all at once!
#   
#   For example, consider the following program:
#   
#       mask = 000000000000000000000000000000X1001X
#       mem[42] = 100
#       mask = 00000000000000000000000000000000X0XX
#       mem[26] = 1
#   
#   When this program goes to write to memory address 42, it first applies the bitmask:
#   
#       address: 000000000000000000000000000000101010  (decimal 42)
#       mask:    000000000000000000000000000000X1001X
#       result:  000000000000000000000000000000X1101X
#   
#   After applying the mask, four bits are overwritten, three of which are different, and two of 
#   which are floating. Floating bits take on every possible combination of values; with two floating 
#   bits, four actual memory addresses are written:
#   
#       000000000000000000000000000000011010  (decimal 26)
#       000000000000000000000000000000011011  (decimal 27)
#       000000000000000000000000000000111010  (decimal 58)
#       000000000000000000000000000000111011  (decimal 59)
#   
#   Next, the program is about to write to memory address 26 with a different bitmask:
#   
#       address: 000000000000000000000000000000011010  (decimal 26)
#       mask:    00000000000000000000000000000000X0XX
#       result:  00000000000000000000000000000001X0XX
#   
#   This results in an address with three floating bits, causing writes to eight memory addresses:
#   
#       000000000000000000000000000000010000  (decimal 16)
#       000000000000000000000000000000010001  (decimal 17)
#       000000000000000000000000000000010010  (decimal 18)
#       000000000000000000000000000000010011  (decimal 19)
#       000000000000000000000000000000011000  (decimal 24)
#       000000000000000000000000000000011001  (decimal 25)
#       000000000000000000000000000000011010  (decimal 26)
#       000000000000000000000000000000011011  (decimal 27)
#   
#   The entire 36-bit address space still begins initialized to the value 0 at every address, and 
#   you still need the sum of all values left in memory at the end of the program. In this example, 
#   the sum is 208.
#   
#   Execute the initialization program using an emulator for a version 2 decoder chip. What is the 
#   sum of all values left in memory after it completes?
#   

def enumberate_addresses(masked_address):
    idx = masked_address.find("X")

    if idx == -1:
        return [int(masked_address, 2)]
    
    # there was at least 1 "X"
    new_mask_to_one  = masked_address[:idx] + "1" + masked_address[idx+1:]
    new_mask_to_zero = masked_address[:idx] + "0" + masked_address[idx+1:]

    return enumberate_addresses(new_mask_to_one) + enumberate_addresses(new_mask_to_zero)
### enumberate_addresses


def apply_bit_mask_chip_2(bit_mask, address):
    bit_mask_length = len(bit_mask)
    address_length = len(str(address))

    address = list( "{0:b}".format(address).zfill(bit_mask_length) )

 
    for i in range(bit_mask_length):
        current_bit_mask_value = bit_mask[i]
        
        if current_bit_mask_value == "X":
            address[i] = "X"

        elif current_bit_mask_value == "1":
            address[i] = "1"

        elif current_bit_mask_value == "0" :
            # leave the value alone
            pass

        else:
            pass


    return "".join(address)
### apply_bit_mask_chip_2


def get_set_of_memory_addresses_to_update(bit_mask, address):
    masked_address = apply_bit_mask_chip_2(bit_mask, address)
    unmasked_addresses = enumberate_addresses(masked_address)

    return unmasked_addresses
### get_set_of_memory_addresses_to_update


def process_program_file_decoder_chip_2(file_name):
    mem = {}
    bit_mask = 0

    with open(file_name) as f:
        for line in f:
            parts = line.split("=")

            if parts[0] == "mask ":
                bit_mask = parts[1].strip()
            
            else: 
                address = int( parts[0].replace("mem[", "").replace("]", "") )
                value = int( parts[1].strip() )

                addresses = get_set_of_memory_addresses_to_update(bit_mask, address)
                for prt in addresses:
                    mem[prt] = value

            # handle applying a memory value

    return mem
### process_program_file


class Day14PartTwoTests(unittest.TestCase):


    def test__apply_bit_mask_chip_2__input_1(self):
        self.assertEqual(apply_bit_mask_chip_2("000000000000000000000000000000X1001X", 42), "000000000000000000000000000000X1101X")

    def test__apply_bit_mask_chip_2__input_1(self):
        self.assertEqual(apply_bit_mask_chip_2("00000000000000000000000000000000X0XX", 26), "00000000000000000000000000000001X0XX")
        
    def test__enumberate_addresses__input_1(self):
        self.assertEqual(set(enumberate_addresses("000000000000000000000000000000X1101X")), set([26,27,58,59]))

    def test__enumberate_addresses__input_2(self):
        self.assertEqual(set(enumberate_addresses("00000000000000000000000000000001X0XX")), set([16, 17, 18, 19, 24, 25, 26, 27]))


    def test__part_2__sample_input(self):
        print("")
        memory_example = process_program_file_decoder_chip_2(sample_input_file_2)
        self.assertEqual(sum_all_memory_addresses(memory_example), 208)

        

memory = process_program_file_decoder_chip_2(input_file)
total = sum_all_memory_addresses(memory)
print("Solution to day 14 part 2: {0}".format(total))


# run then unit tests "last"
if __name__ == '__main__':
    unittest.main()
 
