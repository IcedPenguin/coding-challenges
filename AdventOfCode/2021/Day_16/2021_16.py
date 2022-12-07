#!/bin/python
# -*- coding: utf-8 -*-
# https://adventofcode.com/2021/day/16


###################################################################################################################################################################
#  
#  Solution to day 16 part 1: 895
#
#  Solution to day 16 part 2: 1148595959144
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


def read_and_parse_single_line_input(filename, delimeter, asInt):
    array = read_file_into_array(filename, False)
    parts = array[0].split(delimeter)
    return parts
### read_and_parse_single_line_input


###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################
#  
#  --- Day 16: Packet Decoder ---
#  As you leave the cave and reach open waters, you receive a transmission from the Elves back on the ship.
#  
#  The transmission was sent using the Buoyancy Interchange Transmission System (BITS), a method of 
#  packing numeric expressions into a binary sequence. Your submarine's computer has saved the 
#  transmission in hexadecimal (your puzzle input).
#  
#  The first step of decoding the message is to convert the hexadecimal representation into binary. 
#  Each character of hexadecimal corresponds to four bits of binary data:
#  
#      0 = 0000
#      1 = 0001
#      2 = 0010
#      3 = 0011
#      4 = 0100
#      5 = 0101
#      6 = 0110
#      7 = 0111
#      8 = 1000
#      9 = 1001
#      A = 1010
#      B = 1011
#      C = 1100
#      D = 1101
#      E = 1110
#      F = 1111
#  
#  The BITS transmission contains a single packet at its outermost layer which itself contains many other 
#  packets. The hexadecimal representation of this packet might encode a few extra 0 bits at the end; these 
#  are not part of the transmission and should be ignored.
#  
#  Every packet begins with a standard header: the first three bits encode the packet version, and the next 
#  three bits encode the packet type ID. These two values are numbers; all numbers encoded in any packet are 
#  represented as binary with the most significant bit first. For example, a version encoded as the binary 
#  sequence 100 represents the number 4.
#  
#  Packets with type ID 4 represent a literal value. Literal value packets encode a single binary number. To do 
#  this, the binary number is padded with leading zeroes until its length is a multiple of four bits, and then 
#  it is broken into groups of four bits. Each group is prefixed by a 1 bit except the last group, which is 
#  prefixed by a 0 bit. These groups of five bits immediately follow the packet header. For example, the 
#  hexadecimal string D2FE28 becomes:
#  
#      110100101111111000101000
#      VVVTTTAAAAABBBBBCCCCC
#  
#  Below each bit is a label indicating its purpose:
#  
#      The three bits labeled V (110) are the packet version, 6.
#      The three bits labeled T (100) are the packet type ID, 4, which means the packet is a literal value.
#      The five bits labeled A (10111) start with a 1 (not the last group, keep reading) and contain the first four bits of the number, 0111.
#      The five bits labeled B (11110) start with a 1 (not the last group, keep reading) and contain four more bits of the number, 1110.
#      The five bits labeled C (00101) start with a 0 (last group, end of packet) and contain the last four bits of the number, 0101.
#      The three unlabeled 0 bits at the end are extra due to the hexadecimal representation and should be ignored.
#  
#  So, this packet represents a literal value with binary representation 011111100101, which is 2021 in decimal.
#  
#  Every other type of packet (any packet with a type ID other than 4) represent an operator that performs some 
#  calculation on one or more sub-packets contained within. Right now, the specific operations aren't important; 
#  focus on parsing the hierarchy of sub-packets.
#  
#  An operator packet contains one or more packets. To indicate which subsequent binary data represents its sub-packets, 
#  an operator packet can use one of two modes indicated by the bit immediately after the packet header; this is 
#  called the length type ID:
#  
#      If the length type ID is 0, then the next 15 bits are a number that represents the total length in bits of the sub-packets contained by this packet.
#      If the length type ID is 1, then the next 11 bits are a number that represents the number of sub-packets immediately contained by this packet.
#  
#  Finally, after the length type ID bit and the 15-bit or 11-bit field, the sub-packets appear.
#  
#  For example, here is an operator packet (hexadecimal string 38006F45291200) with length type ID 0 that contains two sub-packets:
#  
#      00111000000000000110111101000101001010010001001000000000
#      VVVTTTILLLLLLLLLLLLLLLAAAAAAAAAAABBBBBBBBBBBBBBBB
#  
#      The three bits labeled V (001) are the packet version, 1.
#      The three bits labeled T (110) are the packet type ID, 6, which means the packet is an operator.
#      The bit labeled I (0) is the length type ID, which indicates that the length is a 15-bit number representing the number of bits in the sub-packets.
#      The 15 bits labeled L (000000000011011) contain the length of the sub-packets in bits, 27.
#      The 11 bits labeled A contain the first sub-packet, a literal value representing the number 10.
#      The 16 bits labeled B contain the second sub-packet, a literal value representing the number 20.
#      After reading 11 and 16 bits of sub-packet data, the total length indicated in L (27) is reached, and so parsing of this packet stops.
#  
#  As another example, here is an operator packet (hexadecimal string EE00D40C823060) with length type ID 1 that contains three sub-packets:
#  
#      11101110000000001101010000001100100000100011000001100000
#      VVVTTTILLLLLLLLLLLAAAAAAAAAAABBBBBBBBBBBCCCCCCCCCCC
#  
#      The three bits labeled V (111) are the packet version, 7.
#      The three bits labeled T (011) are the packet type ID, 3, which means the packet is an operator.
#      The bit labeled I (1) is the length type ID, which indicates that the length is a 11-bit number representing the number of sub-packets.
#      The 11 bits labeled L (00000000011) contain the number of sub-packets, 3.
#      The 11 bits labeled A contain the first sub-packet, a literal value representing the number 1.
#      The 11 bits labeled B contain the second sub-packet, a literal value representing the number 2.
#      The 11 bits labeled C contain the third sub-packet, a literal value representing the number 3.
#      After reading 3 complete sub-packets, the number of sub-packets indicated in L (3) is reached, and so parsing of this packet stops.
#  
#  For now, parse the hierarchy of the packets throughout the transmission and add up all of the version numbers.
#  
#  Here are a few more examples of hexadecimal-encoded transmissions:
#  
#      8A004A801A8002F478 
#      represents an operator packet (version 4) 
#      which contains an operator packet (version 1) 
#      which contains an operator packet (version 5) 
#      which contains a literal value (version 6); 
#      this packet has a version sum of 16.
#  
#      620080001611562C8802118E34 
#      represents an operator packet (version 3) 
#      which contains two sub-packets; 
#      each sub-packet is an operator packet that contains two literal values. 
#      This packet has a version sum of 12.
#  
#      C0015000016115A2E0802F182340 
#      has the same structure as the previous example, 
#      but the outermost packet uses a different length type ID. 
#      This packet has a version sum of 23.
#  
#      A0016C880162017C3686B18A3D4780
#      is an operator packet that contains an operator packet that contains an 
#      operator packet that contains five literal values; 
#      it has a version sum of 31.
#  
#  Decode the structure of your hexadecimal-encoded BITS transmission; 
#  what do you get if you add up the version numbers in all packets?
#  



def extract_bit_string(hex_string):
    bit_string = ""
    for hex_char in hex_string:
        integer = int(hex_char, 16)
        bit_string += format(integer, '0>4b') # we need to keep leading zeros.
    return bit_string



def extract_bits(bit_string, number_bit_length):
    bits = bit_string[:number_bit_length]
    bits_remaining = bit_string[number_bit_length:]
    return bits, bits_remaining


def extract_number(bit_string, number_bit_length):
    bits, bits_remaining = extract_bits(bit_string, number_bit_length)
    number = convert_bits_to_number(bits)
    return number, bits_remaining


def convert_bits_to_number(bits):
    return int(bits, 2)


def extract_literal_number(bit_string):
    stop_condition_found = False
    literal_bits = ""

    # slice groups of 5 until 1 is found with a leading 0
    while not stop_condition_found:
        bits, bit_string = extract_bits(bit_string, 5)
        if bits[0] == "0":
            stop_condition_found = True

        literal_bits += bits[1:]

    return int(literal_bits, 2), bit_string


def parse_packets(bit_string):
    packet = {}

    ##### Parse packet header #####
    packet["version"], bit_string= extract_number(bit_string, 3)
    packet["type_id"], bit_string= extract_number(bit_string, 3)

    ##### Parse Body #####
    if packet["type_id"] == 4: # literal value
        packet["literal_number"], bit_string = extract_literal_number(bit_string)
    
    else: # Operator
        packet["sub_packets"] = []
        length_type_id, bit_string = extract_bits(bit_string, 1)
        if length_type_id == "0":
            # If the length type ID is 0, then the next 15 bits are a number that represents 
            # the total length in bits of the sub-packets contained by this packet.
            
            length_of_sub_packet_in_bits, bit_string = extract_bits(bit_string, 15)
            length_of_sub_packet = convert_bits_to_number(length_of_sub_packet_in_bits)

            sub_packet_bits, bit_string = extract_bits(bit_string, length_of_sub_packet)

            while len(sub_packet_bits) > 0:
                sub_packet, sub_packet_bits = parse_packets(sub_packet_bits)
                packet["sub_packets"].append(sub_packet)
            pass

        else:
            # If the length type ID is 1, then the next 11 bits are a number that represents 
            # the number of sub-packets immediately contained by this packet.

            sub_packet_count_in_bits, bit_string = extract_bits(bit_string, 11)
            sub_packet_count = convert_bits_to_number(sub_packet_count_in_bits)

            for _ in range(sub_packet_count):
                sub_packet, bit_string = parse_packets(bit_string)
                packet["sub_packets"].append(sub_packet)
            
    return packet, bit_string


def sum_version_numbers_in_packet_hierarchy(packet):
    version_sum = packet["version"]

    if packet.get("sub_packets") is not None:
        for sub_packet in packet["sub_packets"]:
            version_sum += sum_version_numbers_in_packet_hierarchy(sub_packet)

    return version_sum

class Day16PartOneTests(unittest.TestCase):


    def test__part_1__example_1(self):
        bit_string = extract_bit_string("D2FE28")
        self.assertEqual("110100101111111000101000", bit_string)
        packet, bit_string = parse_packets(bit_string) 
        self.assertEqual(6, packet["version"])
        self.assertEqual(4, packet["type_id"])
        self.assertEqual(2021, packet["literal_number"])



    def test__part_1__example_2(self):

        # For example, here is an operator packet (hexadecimal string 38006F45291200) with length type ID 0 that contains two sub-packets:
        #     00111000000000000110111101000101001010010001001000000000
        #     VVVTTTILLLLLLLLLLLLLLLAAAAAAAAAAABBBBBBBBBBBBBBBB
        #     The three bits labeled V (001) are the packet version, 1.
        #     The three bits labeled T (110) are the packet type ID, 6, which means the packet is an operator.
        #     The bit labeled I (0) is the length type ID, which indicates that the length is a 15-bit number representing the number of bits in the sub-packets.
        #     The 15 bits labeled L (000000000011011) contain the length of the sub-packets in bits, 27.
        #     The 11 bits labeled A contain the first sub-packet, a literal value representing the number 10.
        #     The 16 bits labeled B contain the second sub-packet, a literal value representing the number 20.
        # After reading 11 and 16 bits of sub-packet data, the total length indicated in L (27) is reached, and so parsing of this packet stops.
        # 
        bit_string = extract_bit_string("38006F45291200")
        self.assertEqual("00111000000000000110111101000101001010010001001000000000", bit_string)
        packet, bit_string = parse_packets(bit_string) 

        self.assertEqual(1, packet["version"])
        self.assertEqual(6, packet["type_id"])
        self.assertEqual(10, packet["sub_packets"][0]["literal_number"])
        self.assertEqual(20, packet["sub_packets"][1]["literal_number"])



    def test__part_1__example_3(self):

        # As another example, here is an operator packet (hexadecimal string EE00D40C823060) with length type ID 1 that contains three sub-packets:
        #     11101110000000001101010000001100100000100011000001100000
        #     VVVTTTILLLLLLLLLLLAAAAAAAAAAABBBBBBBBBBBCCCCCCCCCCC
        #     The three bits labeled V (111) are the packet version, 7.
        #     The three bits labeled T (011) are the packet type ID, 3, which means the packet is an operator.
        #     The bit labeled I (1) is the length type ID, which indicates that the length is a 11-bit number representing the number of sub-packets.
        #     The 11 bits labeled L (00000000011) contain the number of sub-packets, 3.
        #     The 11 bits labeled A contain the first sub-packet, a literal value representing the number 1.
        #     The 11 bits labeled B contain the second sub-packet, a literal value representing the number 2.
        #     The 11 bits labeled C contain the third sub-packet, a literal value representing the number 3.
        # After reading 3 complete sub-packets, the number of sub-packets indicated in L (3) is reached, and so parsing of this packet stops.
        bit_string = extract_bit_string("EE00D40C823060")
        self.assertEqual("11101110000000001101010000001100100000100011000001100000", bit_string)
        packet, bit_string = parse_packets(bit_string) 

        self.assertEqual(7, packet["version"])
        self.assertEqual(3, packet["type_id"])
        self.assertEqual(3, len(packet["sub_packets"]))
        self.assertEqual(1, packet["sub_packets"][0]["literal_number"])
        self.assertEqual(2, packet["sub_packets"][1]["literal_number"])
        self.assertEqual(3, packet["sub_packets"][2]["literal_number"])


    def test__part_1__example_4(self):
        bit_string = extract_bit_string("8A004A801A8002F478")
        packet, bit_string = parse_packets(bit_string) 

        self.assertEqual(4, packet["version"])
        self.assertEqual(1, packet["sub_packets"][0]["version"])
        self.assertEqual(5, packet["sub_packets"][0]["sub_packets"][0]["version"])
        self.assertEqual(6, packet["sub_packets"][0]["sub_packets"][0]["sub_packets"][0]["version"])
        self.assertEqual(16, sum_version_numbers_in_packet_hierarchy(packet))



    def test__part_1__example_5(self):
        bit_string = extract_bit_string("620080001611562C8802118E34")
        packet, bit_string = parse_packets(bit_string) 

        self.assertEqual(3, packet["version"])
        self.assertEqual(2, len(packet["sub_packets"][0]["sub_packets"]))
        self.assertEqual(2, len(packet["sub_packets"][1]["sub_packets"]))
        self.assertEqual(12, sum_version_numbers_in_packet_hierarchy(packet))


    def test__part_1__example_6(self):
        bit_string = extract_bit_string("C0015000016115A2E0802F182340")
        packet, bit_string = parse_packets(bit_string) 
        self.assertEqual(23, sum_version_numbers_in_packet_hierarchy(packet))


    def test__part_1__example_6(self):
        bit_string = extract_bit_string("A0016C880162017C3686B18A3D4780")
        packet, bit_string = parse_packets(bit_string) 
        self.assertEqual(31, sum_version_numbers_in_packet_hierarchy(packet))


    def test__part_1__challenge_input(self):
        print("")
        hex_string = read_file_into_array(input_file, False)
        bit_string = extract_bit_string(hex_string[0])
        packet, bit_string = parse_packets(bit_string) 

        print("Solution to day 16 part 1: {0}".format(sum_version_numbers_in_packet_hierarchy(packet)))
        


###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################

def execute_packet_instructions(packet) -> int:
    type_id = packet["type_id"]

    if type_id == 0: # sum
    # Packets with type ID 0 are sum packets - their value is the sum of the values of their sub-packets.
    # If they only have a single sub-packet, their value is the value of the sub-packet.
        total = 0
        for sub_packet in packet["sub_packets"]:
            total += execute_packet_instructions(sub_packet)
        return total

    elif type_id == 1: # product       
    # Packets with type ID 1 are product packets - their value is the result of multiplying together the values 
    # of their sub-packets. If they only have a single sub-packet, their value is the value of the sub-packet.
        total = 1
        for sub_packet in packet["sub_packets"]:
            total *= execute_packet_instructions(sub_packet)
        return total

    elif type_id == 2: # min
    # Packets with type ID 2 are minimum packets - their value is the minimum of the values of their sub-packets.
        contents = []
        for sub_packet in packet["sub_packets"]:
            contents.append(execute_packet_instructions(sub_packet))
        return min(contents)

    elif type_id == 3: # max
    # Packets with type ID 3 are maximum packets - their value is the maximum of the values of their sub-packets.
        contents = []
        for sub_packet in packet["sub_packets"]:
            contents.append(execute_packet_instructions(sub_packet))
        return max(contents)


    elif type_id == 4: # Literal
        return packet["literal_number"]

    elif type_id == 5: # greater than
    # Packets with type ID 5 are greater than packets - their value is 1 if the value of the first sub-packet is 
    # greater than the value of the second sub-packet; otherwise, their value is 0. These packets always have exactly two sub-packets.
        value_1 = execute_packet_instructions(packet["sub_packets"][0])
        value_2 = execute_packet_instructions(packet["sub_packets"][1])

        if value_1 > value_2:
            return 1
        else:
            return 0

    elif type_id == 6: # less than
    # Packets with type ID 6 are less than packets - their value is 1 if the value of the first sub-packet is less 
    # than the value of the second sub-packet; otherwise, their value is 0. These packets always have exactly two sub-packets.
        value_1 = execute_packet_instructions(packet["sub_packets"][0])
        value_2 = execute_packet_instructions(packet["sub_packets"][1])

        if value_1 < value_2:
            return 1
        else:
            return 0

    elif type_id == 7: # equal to
    # Packets with type ID 7 are equal to packets - their value is 1 if the value of the first sub-packet is equal 
    # to the value of the second sub-packet; otherwise, their value is 0. These packets always have exactly two sub-packets.
        value_1 = execute_packet_instructions(packet["sub_packets"][0])
        value_2 = execute_packet_instructions(packet["sub_packets"][1])

        if value_1 == value_2:
            return 1
        else:
            return 0

    else:
        print("unknown type_id")



class Day16PartTwoTests(unittest.TestCase):

    def test__part_2__example_1(self):
        bit_string = extract_bit_string("C200B40A82")
        packet, bit_string = parse_packets(bit_string) 
        result = execute_packet_instructions(packet)
        self.assertEqual(3, result)

    def test__part_2__example_2(self):
        bit_string = extract_bit_string("04005AC33890")
        packet, bit_string = parse_packets(bit_string) 
        result = execute_packet_instructions(packet)
        self.assertEqual(54, result)

    def test__part_2__example_3(self):
        bit_string = extract_bit_string("880086C3E88112")
        packet, bit_string = parse_packets(bit_string) 
        result = execute_packet_instructions(packet)
        self.assertEqual(7, result)

    def test__part_2__example_4(self):
        bit_string = extract_bit_string("CE00C43D881120")
        packet, bit_string = parse_packets(bit_string) 
        result = execute_packet_instructions(packet)
        self.assertEqual(9, result)
 
    def test__part_2__example_5(self):
        bit_string = extract_bit_string("D8005AC2A8F0")
        packet, bit_string = parse_packets(bit_string) 
        result = execute_packet_instructions(packet)
        self.assertEqual(1, result)

    def test__part_2__example_4(self):
        bit_string = extract_bit_string("F600BC2D8F")
        packet, bit_string = parse_packets(bit_string) 
        result = execute_packet_instructions(packet)
        self.assertEqual(0, result)

    def test__part_2__example_5(self):
        bit_string = extract_bit_string("9C005AC2F8F0")
        packet, bit_string = parse_packets(bit_string) 
        result = execute_packet_instructions(packet)
        self.assertEqual(0, result)

    def test__part_2__example_4(self):
        bit_string = extract_bit_string("9C0141080250320F1802104A08")
        packet, bit_string = parse_packets(bit_string) 
        result = execute_packet_instructions(packet)
        self.assertEqual(1, result)

    def test__part_2__challenge_input(self):
        print("")
        hex_string = read_file_into_array(input_file, False)
        bit_string = extract_bit_string(hex_string[0])
        packet, bit_string = parse_packets(bit_string) 
        result = execute_packet_instructions(packet)

        print("Solution to day 16 part 2: {0}".format(result))
         

 
###################################################################################################################################################################
########################################################################## RUN THE TESTS ##########################################################################


# run then unit tests "last"
if __name__ == '__main__':
    unittest.main()
 

