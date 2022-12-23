#!/bin/python
# -*- coding: utf-8 -*-
# https://adventofcode.com/2022/day/13


###################################################################################################################################################################
#  
#  Solution to part 1: 5625
#
#  Solution to part 2: 23111
#
###################################################################################################################################################################

import unittest

###################################################################################################################################################################
#   --- Day 13: Distress Signal ---
#   
#   You climb the hill and again try contacting the Elves. However, you instead receive a signal you weren't expecting: a distress signal.
#   
#   Your handheld device must still not be working properly; the packets from the distress signal got decoded 
#   out of order. You'll need to re-order the list of received packets (your puzzle input) to decode the message.
#   
#   Your list consists of pairs of packets; pairs are separated by a blank line. You need to identify how many pairs of packets are in the right order.
#   
#       For example:
#   
#       [1,1,3,1,1]
#       [1,1,5,1,1]
#   
#       [[1],[2,3,4]]
#       [[1],4]
#   
#       [9]
#       [[8,7,6]]
#   
#       [[4,4],4,4]
#       [[4,4],4,4,4]
#   
#       [7,7,7,7]
#       [7,7,7]
#   
#       []
#       [3]
#   
#       [[[]]]
#       [[]]
#   
#       [1,[2,[3,[4,[5,6,7]]]],8,9]
#       [1,[2,[3,[4,[5,6,0]]]],8,9]
#   
#   Packet data consists of lists and integers. Each list starts with [, ends with ], and contains zero or 
#   more comma-separated values (either integers or other lists). Each packet is always a list and appears on its own line.
#   
#   When comparing two values, the first value is called left and the second value is called right. Then:
#   
#     1 If both values are integers, the lower integer should come first. If the left integer is lower 
#       than the right integer, the inputs are in the right order. If the left integer is higher than the 
#       right integer, the inputs are not in the right order. Otherwise, the inputs are the same integer; 
#       continue checking the next part of the input.
#   
#     2 If both values are lists, compare the first value of each list, then the second value, and so on. 
#       If the left list runs out of items first, the inputs are in the right order. If the right list runs 
#       out of items first, the inputs are not in the right order. If the lists are the same length and no 
#       comparison makes a decision about the order, continue checking the next part of the input.
#   
#     3 If exactly one value is an integer, convert the integer to a list which contains that integer as its 
#       only value, then retry the comparison. For example, if comparing [0,0,0] and 2, convert the right 
#       value to [2] (a list containing 2); the result is then found by instead comparing [0,0,0] and [2].
#   
#   Using these rules, you can determine which of the pairs in the example are in the right order:
#   
#       == Pair 1 ==
#       - Compare [1,1,3,1,1] vs [1,1,5,1,1]
#         - Compare 1 vs 1
#         - Compare 1 vs 1
#         - Compare 3 vs 5
#           - Left side is smaller, so inputs are in the right order
#   
#       == Pair 2 ==
#       - Compare [[1],[2,3,4]] vs [[1],4]
#         - Compare [1] vs [1]
#           - Compare 1 vs 1
#         - Compare [2,3,4] vs 4
#           - Mixed types; convert right to [4] and retry comparison
#           - Compare [2,3,4] vs [4]
#             - Compare 2 vs 4
#               - Left side is smaller, so inputs are in the right order
#   
#       == Pair 3 ==
#       - Compare [9] vs [[8,7,6]]
#         - Compare 9 vs [8,7,6]
#           - Mixed types; convert left to [9] and retry comparison
#           - Compare [9] vs [8,7,6]
#             - Compare 9 vs 8
#               - Right side is smaller, so inputs are not in the right order
#   
#       == Pair 4 ==
#       - Compare [[4,4],4,4] vs [[4,4],4,4,4]
#         - Compare [4,4] vs [4,4]
#           - Compare 4 vs 4
#           - Compare 4 vs 4
#         - Compare 4 vs 4
#         - Compare 4 vs 4
#         - Left side ran out of items, so inputs are in the right order
#   
#       == Pair 5 ==
#       - Compare [7,7,7,7] vs [7,7,7]
#         - Compare 7 vs 7
#         - Compare 7 vs 7
#         - Compare 7 vs 7
#         - Right side ran out of items, so inputs are not in the right order
#   
#       == Pair 6 ==
#       - Compare [] vs [3]
#         - Left side ran out of items, so inputs are in the right order
#   
#       == Pair 7 ==
#       - Compare [[[]]] vs [[]]
#         - Compare [[]] vs []
#           - Right side ran out of items, so inputs are not in the right order
#   
#       == Pair 8 ==
#       - Compare [1,[2,[3,[4,[5,6,7]]]],8,9] vs [1,[2,[3,[4,[5,6,0]]]],8,9]
#         - Compare 1 vs 1
#         - Compare [2,[3,[4,[5,6,7]]]] vs [2,[3,[4,[5,6,0]]]]
#           - Compare 2 vs 2
#           - Compare [3,[4,[5,6,7]]] vs [3,[4,[5,6,0]]]
#             - Compare 3 vs 3
#             - Compare [4,[5,6,7]] vs [4,[5,6,0]]
#               - Compare 4 vs 4
#               - Compare [5,6,7] vs [5,6,0]
#                 - Compare 5 vs 5
#                 - Compare 6 vs 6
#                 - Compare 7 vs 0
#                   - Right side is smaller, so inputs are not in the right order
#   
#   What are the indices of the pairs that are already in the right order? (The first pair has index 1, 
#   the second pair has index 2, and so on.) In the above example, the pairs in the right order 
#   are 1, 2, 4, and 6; the sum of these indices is 13.
#   
#   Determine which pairs of packets are already in the right order. What is the sum of the indices of those pairs?
#   
############################################################################ PROBLEM 1 ############################################################################


puzzle_day          = 13
sample_input_file_1 = "2022_{0:02d}_sample_1.txt".format(puzzle_day)
input_file          = "2022_{0:02d}_input.txt".format(puzzle_day)


def load_file(file_path):
    file_ptr = open(file_path, "r")
    data = file_ptr.read()
    file_ptr.close()
    return data



# [[1],[2,3,4]]
#  [1],[2,3,4]
def convert_packet_element(raw_element):
    # print("convert_packet_element: {0}".format(raw_element))
    packet = []

    # check for literal.
    if raw_element[0] != "[":
        # print("literal found: {0}".format(raw_element))
        return int(raw_element)
        
    raw_element = raw_element[1:len(raw_element)-1]
    brackets_found = 0
    start_of_slice = 0
    idx = 0

    while idx < len(raw_element):
        if raw_element[idx] == "[":
            brackets_found += 1
            # print("open found \t {0}".format(raw_element[:idx]))
            idx += 1
            continue

        if raw_element[idx] == "]":
            brackets_found -= 1
            # print("close found \t {0}".format(raw_element[:idx]))


        if idx == len(raw_element) -1:
            element = raw_element[start_of_slice:idx+1]
            # print("end of string encountered, pull the last element \t {0}".format(element))
            packet.append(convert_packet_element(element))

        elif raw_element[idx] == "," and brackets_found == 0:
            element = raw_element[start_of_slice:idx]
            # print("non-last element found. \t {0}".format(element))
            packet.append(convert_packet_element(element))
            start_of_slice = idx + 1

        idx += 1

    return packet



#   When comparing two values, the first value is called left and the second value is called right. Then:
#   
#     1 If both values are integers, the lower integer should come first. If the left integer is lower 
#       than the right integer, the inputs are in the right order. If the left integer is higher than the 
#       right integer, the inputs are not in the right order. Otherwise, the inputs are the same integer; 
#       continue checking the next part of the input.
#   
#     2 If both values are lists, compare the first value of each list, then the second value, and so on. 
#       If the left list runs out of items first, the inputs are in the right order. If the right list runs 
#       out of items first, the inputs are not in the right order. If the lists are the same length and no 
#       comparison makes a decision about the order, continue checking the next part of the input.
#   
#     3 If exactly one value is an integer, convert the integer to a list which contains that integer as its 
#       only value, then retry the comparison. For example, if comparing [0,0,0] and 2, convert the right 
#       value to [2] (a list containing 2); the result is then found by instead comparing [0,0,0] and [2].
def compair_packets(packet_1, packet_2, layer=1):
    # loop over the two lists, for the longest
    max_element_count = max(len(packet_1), len(packet_2))

    # print("comparison:  range={0}\tleft={1}\tright={2}".format(max_element_count, packet_1, packet_2))
    for i in range(max_element_count):
        
        if i < len(packet_1):
            left = packet_1[i]
        else:
            left = None


        if i < len(packet_2):
            right = packet_2[i]
        else:
            right = None


        # Criteria 2)   Length of list check
        if left is None and right is not None:
            return "in_order"

        elif left is not None and right is None:
            return "out_of_order"

        elif left is None and right is None:
            return "wat!" #should not be reachable



        # Criteria 1)  Both are numbers
        if type(left) == int and  type(right) == int:
            # print("--- Both are numbers.")
            if left < right:
                return "in_order"

            elif left > right:
                return "out_of_order"

            else:
                # in order so far, continue to next element.
                continue


        # Criteria 2)   Both are lists
        if type(left) == list and type(right) == list:
            # print("--- Both are lists.")
            result = compair_packets(left, right, layer+1)
            if result == "still_looking":
                continue
            else:
                return result



        # Criteria 3)   List and Number.
        if type(left) == int:
            left = [left]
        else:
            right = [right]

        result = compair_packets(left, right, layer+1)
        if result == "still_looking":
            continue
        else:
            return result


    if layer == 1:
        return "in_order"
    else:
        return "still_looking"




def process_packet_capture(packets):
    equal_idx_count = 0
    for i in range(0, len(packets), 3):
        packet_1 = convert_packet_element(packets[i])
        packet_2 = convert_packet_element(packets[i+1])

        if compair_packets(packet_1, packet_2) == "in_order":
            equal_idx_count += i / 3 +1


    return equal_idx_count


class Day13PartOneTests(unittest.TestCase):

    def test__p1__convert_packet_element(self):
        self.assertEqual(convert_packet_element("4"), 4)
        self.assertEqual(convert_packet_element("456"), 456)

        self.assertEqual(convert_packet_element("[]"), [])
        self.assertEqual(convert_packet_element("[1]"), [1])
        self.assertEqual(convert_packet_element("[123]"), [123])
        self.assertEqual(convert_packet_element("[1,2]"), [1,2])
        self.assertEqual(convert_packet_element("[[1,2]]"), [[1,2]])

        self.assertEqual(convert_packet_element("[[1],[2,3,4]]"), [[1],[2,3,4]])
        self.assertEqual(convert_packet_element("[[[9,3,[9,4,3],[0,0,0],0],[3,0,[6,7,6,8]]],[[[9,10,4,4],[1,1,4,1],4,[1,3]],[],[3],[[9],7]],[9],[[1],[4,8]],[9,9,5,[[5,8,2]],[10]]]")
            , [[[9,3,[9,4,3],[0,0,0],0],[3,0,[6,7,6,8]]],[[[9,10,4,4],[1,1,4,1],4,[1,3]],[],[3],[[9],7]],[9],[[1],[4,8]],[9,9,5,[[5,8,2]],[10]]])



    def test__p1__compair_packets(self):
        self.assertEqual(compair_packets([1],           [2]),           "in_order") 
        self.assertEqual(compair_packets([2],           [1]),           "out_of_order") 
        self.assertEqual(compair_packets([1,2,3],       [1,2,4]),       "in_order") 
        self.assertEqual(compair_packets([1,2,3],       [1,2,3]),       "in_order") 
        self.assertEqual(compair_packets([1,2],         [1,2]),         "in_order") 

        self.assertEqual(compair_packets([1,1,3,1,1],                 [1,1,5,1,1]),                 "in_order")     # pair 1
        self.assertEqual(compair_packets([[1],[2,3,4]],               [[1],4]),                     "in_order")     # pair 2
        self.assertEqual(compair_packets([9],                         [[8,7,6]]),                   "out_of_order") # pair 3
        self.assertEqual(compair_packets([[4,4],4,4],                 [[4,4],4,4,4]),               "in_order")     # pair 4
        self.assertEqual(compair_packets([7,7,7,7],                   [7,7,7]),                     "out_of_order") # pair 5
        self.assertEqual(compair_packets([],                          [3]),                         "in_order")     # pair 6
        self.assertEqual(compair_packets([[[]]],                      [[]]),                        "out_of_order") # pair 7
        self.assertEqual(compair_packets([1,[2,[3,[4,[5,6,7]]]],8,9], [1,[2,[3,[4,[5,6,0]]]],8,9]), "out_of_order") # pair 8

        

    def test__p1__process_packet_capture(self):
        raw_packets = load_file(sample_input_file_1)
        raw_packets = raw_packets.split("\n")
        count = process_packet_capture(raw_packets)

        self.assertEqual(count, 13)


    
    def test__part_1__challenge_input(self):
        print("")
        raw_packets = load_file(input_file)
        raw_packets = raw_packets.split("\n")
        count = process_packet_capture(raw_packets)

        print("Solution to day {0} part 1: {1}".format(puzzle_day, count))
        self.assertEqual(count, 5625.0)
        
        


###################################################################################################################################################################
#   --- Part Two ---
#   Now, you just need to put all of the packets in the right order. Disregard the blank lines in your list of received packets.
#   
#   The distress signal protocol also requires that you include two additional divider packets:
#   
#       [[2]]
#       [[6]]
#
#   Using the same rules as before, organize all packets - the ones in your list of received packets as well as the 
#   two divider packets - into the correct order.
#   
#   For the example above, the result of putting the packets in the correct order is:
#   
#       []
#       [[]]
#       [[[]]]
#       [1,1,3,1,1]
#       [1,1,5,1,1]
#       [[1],[2,3,4]]
#       [1,[2,[3,[4,[5,6,0]]]],8,9]
#       [1,[2,[3,[4,[5,6,7]]]],8,9]
#       [[1],4]
#       [[2]]
#       [3]
#       [[4,4],4,4]
#       [[4,4],4,4,4]
#       [[6]]
#       [7,7,7]
#       [7,7,7,7]
#       [[8,7,6]]
#       [9]
#   
#   Afterward, locate the divider packets. To find the decoder key for this distress signal, you need to determine 
#   the indices of the two divider packets and multiply them together. (The first packet is at index 1, the second 
#   packet is at index 2, and so on.) In this example, the divider packets are 10th and 14th, and so the decoder 
#   key is 140.
#   
#   Organize all of the packets into the correct order. What is the decoder key for the distress signal?
############################################################################ PROBLEM 2 ############################################################################

# N^2 complexity.
def order_packets(input_packets):
    ordered_packets = []

    while len(input_packets) > 0:
        packet = input_packets.pop()

        inserted = False
        for i in range(len(ordered_packets)):
            if compair_packets(packet, ordered_packets[i]) == "in_order":
                ordered_packets.insert(i, packet)
                inserted = True 
                break

        if not inserted:
            ordered_packets.append(packet)

    return ordered_packets



def get_packet_list(raw_packets):
    packets = []

    while len(raw_packets) > 0:
        line = raw_packets.pop()
        if line == "":
            continue
        packets.append(convert_packet_element(line))

    return packets


def get_decoder_key(packets):
    a = packets.index([[2]])
    b = packets.index([[6]])

    return (a+1) * (b+1)


class Day13PartTwoTests(unittest.TestCase):
    
    def test__p2__sample1(self):
        raw_packets = load_file(sample_input_file_1)
        raw_packets = raw_packets.split("\n")

        packets = get_packet_list(raw_packets)
        packets.append(convert_packet_element("[[2]]"))
        packets.append(convert_packet_element("[[6]]"))

        ordered_packets = order_packets(packets)
        # print(ordered_packets)

        key = get_decoder_key(ordered_packets)
        self.assertEqual(key, 140)
        

    def test__part_2__challenge_input(self):
        print("")
        raw_packets = load_file(input_file)
        raw_packets = raw_packets.split("\n")

        packets = get_packet_list(raw_packets)
        packets.append(convert_packet_element("[[2]]"))
        packets.append(convert_packet_element("[[6]]"))

        ordered_packets = order_packets(packets)
        key = get_decoder_key(ordered_packets)
        
        print("Solution to day {0} part 2: {1}".format(puzzle_day, key))


 
###################################################################################################################################################################
########################################################################## RUN THE TESTS ##########################################################################


# run then unit tests "last"
if __name__ == '__main__':
    unittest.main()
 

