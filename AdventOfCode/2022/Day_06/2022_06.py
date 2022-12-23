#!/bin/python
# -*- coding: utf-8 -*-
# https://adventofcode.com/2022/day/6


###################################################################################################################################################################
#  
#  Solution to part 1: 1361
#
#  Solution to part 2: 3263
#
###################################################################################################################################################################

import unittest

###################################################################################################################################################################
#   --- Day 6: Tuning Trouble ---
#   
#   The preparations are finally complete; you and the Elves leave camp on foot and begin to make your way toward the star fruit grove.
#   
#   As you move through the dense undergrowth, one of the Elves gives you a handheld device. He says that it has many fancy features, 
#   but the most important one to set up right now is the communication system.
#   
#   However, because he's heard you have significant experience dealing with signal-based systems, he convinced the other Elves that 
#   it would be okay to give you their one malfunctioning device - surely you'll have no problem fixing it.
#   
#   As if inspired by comedic timing, the device emits a few colorful sparks.
#   
#   To be able to communicate with the Elves, the device needs to lock on to their signal. The signal is a series of seemingly-random 
#   characters that the device receives one at a time.
#   
#   To fix the communication system, you need to add a subroutine to the device that detects a start-of-packet marker in the datastream. 
#   In the protocol being used by the Elves, the start of a packet is indicated by a sequence of four characters that are all different.
#   
#   The device will send your subroutine a datastream buffer (your puzzle input); your subroutine needs to identify the first position 
#   where the four most recently received characters were all different. Specifically, it needs to report the number of characters 
#   from the beginning of the buffer to the end of the first such four-character marker.
#   
#   For example, suppose you receive the following datastream buffer:
#   
#       mjqjpqmgbljsphdztnvjfqwrcgsmlb
#   
#   After the first three characters (mjq) have been received, there haven't been enough characters received yet to find the marker. 
#   The first time a marker could occur is after the fourth character is received, making the most recent four characters mjqj. 
#   Because j is repeated, this isn't a marker.
#   
#   The first time a marker appears is after the seventh character arrives. Once it does, the last four characters received are 
#   jpqm, which are all different. In this case, your subroutine should report the value 7, because the first start-of-packet 
#   marker is complete after 7 characters have been processed.
#   
#   Here are a few more examples:
#   
#       bvwbjplbgvbhsrlpgdmjqwftvncz: first marker after character 5
#       nppdvjthqldpwncqszvftbrmjlhg: first marker after character 6
#       nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg: first marker after character 10
#       zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw: first marker after character 11
#   
#   How many characters need to be processed before the first start-of-packet marker is detected?
#   
############################################################################ PROBLEM 1 ############################################################################


puzzle_day          = 6
sample_input_file_1 = "2022_{0:02d}_sample_1.txt".format(puzzle_day)
input_file          = "2022_{0:02d}_input.txt".format(puzzle_day)


def load_file(file_path):
    file_ptr = open(file_path, "r")
    data = file_ptr.read()
    file_ptr.close()
    return data


class MessageBuffer:
    def __init__(self, header_length=4):
        self.buffer = []
        self.header_length = header_length

    def next_character(self, character):
        # rotate the oldest character (if header buffer is full)
        if len(self.buffer) == self.header_length:
            ejected_character = self.buffer.pop(0)
        
        self.buffer.append(character)

        return len(set(self.buffer)) == self.header_length


    def find_message_header(self, message_buffer):
        for i in range(len(message_buffer)):
            found = self.next_character(message_buffer[i])

            if found:
                i += 1 # want the index after the header
                return i, message_buffer[i - self.header_length:i]

        return -1, None


class Day6PartOneTests(unittest.TestCase):

    def test__p1__sample1(self):
        buffer = MessageBuffer()
        idx, header = buffer.find_message_header("mjqjpqmgbljsphdztnvjfqwrcgsmlb")
        self.assertEqual(idx, 7)
        self.assertEqual(header, "jpqm")


    def test__p1__sample2(self):
        buffer = MessageBuffer()
        idx, header = buffer.find_message_header("bvwbjplbgvbhsrlpgdmjqwftvncz")
        self.assertEqual(idx, 5)

        buffer = MessageBuffer()
        idx, header = buffer.find_message_header("nppdvjthqldpwncqszvftbrmjlhg")
        self.assertEqual(idx, 6)

        buffer = MessageBuffer()
        idx, header = buffer.find_message_header("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg")
        self.assertEqual(idx, 10)

        buffer = MessageBuffer()
        idx, header = buffer.find_message_header("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw")
        self.assertEqual(idx,11)


    
    def test__part_1__challenge_input(self):
        print("")
        message = load_file(input_file).strip()
        buffer = MessageBuffer()
        idx, header = buffer.find_message_header(message)
        print("Solution to day {0} part 1: {1}".format(puzzle_day, idx))
        

###################################################################################################################################################################
#   --- Part Two ---
#   
#   Your device's communication system is correctly detecting packets, but still isn't working. It looks like it also needs to look for messages.
#   
#   A start-of-message marker is just like a start-of-packet marker, except it consists of 14 distinct characters rather than 4.
#   
#   Here are the first positions of start-of-message markers for all of the above examples:
#   
#       mjqjpqmgbljsphdztnvjfqwrcgsmlb: first marker after character 19
#       bvwbjplbgvbhsrlpgdmjqwftvncz: first marker after character 23
#       nppdvjthqldpwncqszvftbrmjlhg: first marker after character 23
#       nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg: first marker after character 29
#       zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw: first marker after character 26
#   
#   How many characters need to be processed before the first start-of-message marker is detected?
#   
############################################################################ PROBLEM 2 ############################################################################



class Day6PartTwoTests(unittest.TestCase):
    
    def test__p2__sample1(self):
        buffer = MessageBuffer(header_length=14)
        idx, header = buffer.find_message_header("mjqjpqmgbljsphdztnvjfqwrcgsmlb")
        self.assertEqual(idx, 19)

        buffer = MessageBuffer(header_length=14)
        idx, header = buffer.find_message_header("bvwbjplbgvbhsrlpgdmjqwftvncz")
        self.assertEqual(idx, 23)

        buffer = MessageBuffer(header_length=14)
        idx, header = buffer.find_message_header("nppdvjthqldpwncqszvftbrmjlhg")
        self.assertEqual(idx, 23)

        buffer = MessageBuffer(header_length=14)
        idx, header = buffer.find_message_header("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg")
        self.assertEqual(idx, 29)

        buffer = MessageBuffer(header_length=14)
        idx, header = buffer.find_message_header("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw")
        self.assertEqual(idx,26)
        

    def test__part_2__challenge_input(self):
        print("")
        message = load_file(input_file).strip()
        buffer = MessageBuffer(header_length=14)
        idx, header = buffer.find_message_header(message)
        print("Solution to day {0} part 2: {1}".format(puzzle_day, idx))


 
###################################################################################################################################################################
########################################################################## RUN THE TESTS ##########################################################################


# run then unit tests "last"
if __name__ == '__main__':
    unittest.main()
 

