#!/bin/python
# -*- coding: utf-8 -*-
# https://adventofcode.com/2021/day/8


###################################################################################################################################################################
#  
#  Solution to day 8 part 1: 409
#
#  Solution to day 8 part 2: 1024649
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
#  --- Day 8: Seven Segment Search ---
#  You barely reach the safety of the cave when the whale smashes into the cave mouth, collapsing it. 
#  Sensors indicate another exit to this cave at a much greater depth, so you have no choice but to press on.
#  
#  As your submarine slowly makes its way through the cave system, you notice that the four-digit seven-segment 
#  displays in your submarine are malfunctioning; they must have been damaged during the escape. You'll be 
#  in a lot of trouble without them, so you'd better figure out what's wrong.
#  
#  Each digit of a seven-segment display is rendered by turning on or off any of seven segments named a through g:
#  
#            0:      1:      2:      3:      4:
#           aaaa    ....    aaaa    aaaa    ....
#          b    c  .    c  .    c  .    c  b    c
#          b    c  .    c  .    c  .    c  b    c
#           ....    ....    dddd    dddd    dddd
#          e    f  .    f  e    .  .    f  .    f
#          e    f  .    f  e    .  .    f  .    f
#           gggg    ....    gggg    gggg    ....
#  
#            5:      6:      7:      8:      9:
#           aaaa    aaaa    aaaa    aaaa    aaaa
#          b    .  b    .  .    c  b    c  b    c
#          b    .  b    .  .    c  b    c  b    c
#           dddd    dddd    ....    dddd    dddd
#          .    f  e    f  .    f  e    f  .    f
#          .    f  e    f  .    f  e    f  .    f
#           gggg    gggg    ....    gggg    gggg
#  
#  So, to render a 1, only segments c and f would be turned on; the rest would be off. To render a 7, 
#  only segments a, c, and f would be turned on.
#  
#  The problem is that the signals which control the segments have been mixed up on each display. The 
#  submarine is still trying to display numbers by producing output on signal wires a through g, but 
#  those wires are connected to segments randomly. Worse, the wire/segment connections are mixed up 
#  separately for each four-digit display! (All of the digits within a display use the same connections, though.)
#  
#  So, you might know that only signal wires b and g are turned on, but that doesn't mean segments b and g 
#  are turned on: the only digit that uses two segments is 1, so it must mean segments c and f are meant to 
#  be on. With just that information, you still can't tell which wire (b/g) goes to which segment (c/f). For 
#  that, you'll need to collect more information.
#  
#  For each display, you watch the changing signals for a while, make a note of all ten unique signal patterns 
#  you see, and then write down a single four digit output value (your puzzle input). Using the signal patterns, 
#  you should be able to work out which pattern corresponds to which digit.
#  
#  For example, here is what you might see in a single entry in your notes:
#  
#          acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf
#  
#  Each entry consists of ten unique signal patterns, a | delimiter, and finally the four digit output value. 
#  Within an entry, the same wire/segment connections are used (but you don't know what the connections 
#  actually are). The unique signal patterns correspond to the ten different ways the submarine tries to 
#  render a digit using the current wire/segment connections. Because 7 is the only digit that uses three 
#  segments, dab in the above example means that to render a 7, signal lines d, a, and b are on. Because 4 is 
#  the only digit that uses four segments, eafb means that to render a 4, signal lines e, a, f, and b are on.
#  
#  Using this information, you should be able to work out which combination of signal wires corresponds to 
#  each of the ten digits. Then, you can decode the four digit output value. Unfortunately, in the above example, 
#  all of the digits in the output value (cdfeb fcadb cdfeb cdbaf) use five segments and are more difficult to deduce.
#  
#  For now, focus on the easy digits. Consider this larger example:
#  
#          be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
#          edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
#          fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
#          fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
#          aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
#          fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
#          dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
#          bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
#          egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
#          gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
#  
#  Because the digits 1, 4, 7, and 8 each use a unique number of segments, you should be able to tell which 
#  combinations of signals correspond to those digits. Counting only digits in the output values (the part 
#  after | on each line), in the above example, there are 26 instances of digits that use a unique 
#  number of segments (highlighted above).
#  
#  In the output values, how many times do digits 1, 4, 7, or 8 appear?
#  


###  Thoughts ###
# number of lite segments  |   possible numbers
# -------------------------+-------------------
#           2              |        1
#           3              |        7
#           4              |        4
#           5              |        2, 3, 5
#           6              |        0, 6, 9
#           7              |        8
#  
#  
#  order letters (for convienence)
#  toss into map: {length -> [strings]}
#  
#   
#  1   = string of length 2                 /
#  CF  = segments of 1 (any order)
#  7   = string of length 3                 /
#  A   = set difference (7, 1)
#  4   = string of length 4                 /
#  8   = string of length 7                 /
#  9   = set union of (1, 4, 7) plus one extra.
#  G   = set difference (9 , union(1, 4, 7))
#  
#  for strings of length 6: x  (error in this logic, corrected in code below)
#      8 set difference x intersect with 1 
#          -> if result is length 1
#              *   C = remaining segment
#              *   6 = x
#          -> if result is length 0
#              *   0 = x
#              *   D = set difference {8, 0}
#  
#  
#  3 = union (1, A, D, G)
#  
#  of the remaining 2 options
#  2 = entry with C on
#  5 = entry with C off
#  

def parse_input_line(line):
    halves = line.split("|")
    front = halves[0].split()
    back = halves[1].split()

    for i in range(len(front)):
        front[i] = ''.join(sorted(front[i]))

    for i in range(len(back)):
        back[i] = ''.join(sorted(back[i]))

    return front, back
### parse_input_line


class SevenSegmentDisplay:
    def __init__(self):
        self.length_map = {k: [] for k in range(10)}
        self.mapping = {
            # segments
            "a": None, 
            # "b": None, 
            "c": None, 
            "d": None, 
            # "e": None, 
            # "f": None, 
            "g": None,
            # numbers 
            0: None, 
            1: None, 
            2: None, 
            3: None, 
            4: None, 
            5: None, 
            6: None, 
            7: None, 
            8: None, 
            9: None
        }

    def parse_numbers(self, numbers):

        # find: 1, 4, 7, 8
        hunting = numbers[:]
        for num in hunting:
            if len(num) == 2:
                self.mapping[1] = num
                numbers.remove(num)
                # print("Found 1 - {0} \tnum= {1}".format(num, numbers))


            elif len(num) == 3:
                self.mapping[7] = num
                numbers.remove(num)
                # print("Found 7 - {0} \tnum= {1}".format(num, numbers))

            elif len(num) == 4:
                self.mapping[4] = num
                numbers.remove(num)
                # print("Found 4 - {0} \tnum= {1}".format(num, numbers))

            elif len(num) == 7:
                self.mapping[8] = num
                numbers.remove(num)
                # print("Found 8 - {0} \tnum= {1}".format(num, numbers))

        # find: a
        self.mapping["a"] = list(set(self.mapping[7]) - set(self.mapping[1]))[0]
        # print("Found a - {0} \tnum= {1}".format(num, self.mapping["a"]))

        # find: 9, G
        segments_in_1_4_7 = set(self.mapping[1]).union(set(self.mapping[4]), set(self.mapping[7]))
        hunting = numbers[:]
        for num in hunting:
            if len(num) == 6:
                diff = segments_in_1_4_7.difference(set(num))
                if len(diff) == 0:
                    self.mapping[9] = num
                    self.mapping["g"] = list(set(num).difference(segments_in_1_4_7))[0]
                    numbers.remove(num)
                    # print("Found 9 - {0} \tnum= {1}".format(num, numbers))
                    # print("Found g - {0} \tnum= {1}".format(num, self.mapping["g"]))

        # find: 6, C, 0, D
        hunting = numbers[:]
        for num in hunting:
            if len(num) == 6:

                diff = set(self.mapping[8]).difference(set(num))
                if len(diff) == 1 and diff & set(self.mapping[1]):
                    self.mapping[6] = num
                    self.mapping["c"] = list(diff)[0]
                    numbers.remove(num)
                    # print("Found 6 - {0} \tnum= {1}".format(num, numbers))
                    # print("Found c - {0} \tnum= {1}".format(num, self.mapping["c"]))

                elif len(diff) == 1:
                    self.mapping[0] = num
                    self.mapping["d"] = list(diff)[0]
                    numbers.remove(num)
                    # print("Found 0 - {0} \tnum= {1}".format(num, numbers))
                    # print("Found d - {0} \tnum= {1}".format(num, self.mapping["d"]))


        # find: 3
        chars_of_3 = set(self.mapping[1]).union(set(self.mapping["a"]), set(self.mapping["d"]), set(self.mapping["g"]))
        hunting = numbers[:]
        for num in hunting:
            if set(num) == chars_of_3:
                self.mapping[3] = num
                numbers.remove(num)
                # print("Found 3 - {0} \tnum= {1}".format(num, numbers))

        # find: 2, 5
        hunting = numbers[:]
        for num in hunting:
            if self.mapping["c"] in num:
                self.mapping[2] = num

            else: self.mapping[5] = num



    def decode_number(self, number):
        for k in self.mapping:
            if self.mapping[k] == number:
                return k
        
        return None


def count_digit_occurances(display, digits, matches):
    count = 0
    for d in digits:
        if display.decode_number(d) in matches:
            count += 1

    return count


def process_displays(filename, count_occurances):
    count = 0
    lines = read_file_into_array(filename, False)
    for line in lines:
        segments, numbers = parse_input_line(line)
        display = SevenSegmentDisplay()
        display.parse_numbers(segments)

        if count_occurances:
            count += count_digit_occurances(display, numbers, (1, 4, 7, 8))
        else:
            count += count_digits(display, numbers)

    return count
### process_displays


class Day8PartOneTests(unittest.TestCase):

    def test__part_1__sample_input_single_line(self):
        segments, numbers = parse_input_line("acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf")
        display = SevenSegmentDisplay()
        display.parse_numbers(segments)

        self.assertEqual(5, display.decode_number(numbers[0]))
        self.assertEqual(3, display.decode_number(numbers[1]))
        self.assertEqual(5, display.decode_number(numbers[2]))
        self.assertEqual(3, display.decode_number(numbers[3]))



    def test__part_1__sample_input(self):
        print("")
        count = process_displays(sample_input_file_1, True)

        self.assertEqual(26, count)


    def test__part_1__challenge_input(self):
        print("")
        count = process_displays(input_file, True)
        print("Solution to day 8 part 1: {0}".format(count))





###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################
#  
#  --- Part Two ---
#  Through a little deduction, you should now be able to determine the remaining digits. Consider a
#  gain the first example above:
#  
#      acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf
#      
#  After some careful analysis, the mapping between signal wires and segments only make sense in the 
#  following configuration:
#  
#       dddd
#      e    a
#      e    a
#       ffff
#      g    b
#      g    b
#       cccc
#  
#  So, the unique signal patterns would correspond to the following digits:
#  
#      acedgfb: 8
#      cdfbe: 5
#      gcdfa: 2
#      fbcad: 3
#      dab: 7
#      cefabd: 9
#      cdfgeb: 6
#      eafb: 4
#      cagedb: 0
#      ab: 1
#  
#  Then, the four digits of the output value can be decoded:
#  
#      cdfeb: 5
#      fcadb: 3
#      cdfeb: 5
#      cdbaf: 3
#  
#  Therefore, the output value for this entry is 5353.
#  
#  Following this same process for each entry in the second, larger example above, the output value of 
#  each entry can be determined:
#  
#      fdgacbe cefdb cefbgd gcbe: 8394
#      fcgedb cgb dgebacf gc: 9781
#      cg cg fdcagb cbg: 1197
#      efabcd cedba gadfec cb: 9361
#      gecf egdcabf bgf bfgea: 4873
#      gebdcfa ecba ca fadegcb: 8418
#      cefg dcbef fcge gbcadfe: 4548
#      ed bcgafe cdgba cbgef: 1625
#      gbdfcae bgc cg cgb: 8717
#      fgae cfgab fg bagce: 4315
#  
#  Adding all of the output values in this larger example produces 61229.
#  
#  For each entry, determine all of the wire/segment connections and decode the four-digit output values. 
#  What do you get if you add up all of the output values?
#  

def count_digits(display, digits):
    count  = 1000 * display.decode_number(digits[0])
    count +=  100 * display.decode_number(digits[1])
    count +=   10 * display.decode_number(digits[2])
    count +=    1 * display.decode_number(digits[3])

    return count
### count_digits

class Day8PartTwoTests(unittest.TestCase):

    
    def test__part_2__sample_input(self):
        print("")
        count = process_displays(sample_input_file_1, False)

        self.assertEqual(61229, count)




    def test__part_2__challenge_input(self):
        print("")
        count = process_displays(input_file, False)
        print("Solution to day 8 part 2: {0}".format(count))

        

    pass

# print("Solution to day 8 part 2: {0}".format(-1))
 

 
###################################################################################################################################################################
########################################################################## RUN THE TESTS ##########################################################################


# run then unit tests "last"
if __name__ == '__main__':
    unittest.main()
 

