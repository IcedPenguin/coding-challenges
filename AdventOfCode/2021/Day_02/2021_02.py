#!/bin/python
# -*- coding: utf-8 -*-
# https://adventofcode.com/2021/day/02


###################################################################################################################################################################
#  
#  Solution to day 2 part 1: 1924923
#
#  Solution to day 2 part 2: 1982495697
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

###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################
#  
#  --- Day 2: Dive! ---
#  Now, you need to figure out how to pilot this thing.
#  
#  It seems like the submarine can take a series of commands like forward 1, down 2, or up 3:
#  
#          forward X    increases the horizontal position by X units.
#          down X       increases the depth by X units.
#          up X         decreases the depth by X units.
#  
#  Note that since you're on a submarine, down and up affect your depth, and so they have the opposite result 
#  of what you might expect.
#  
#  The submarine seems to already have a planned course (your puzzle input). You should probably figure out 
#  where it's going. For example:
#  
#          forward 5
#          down 5
#          forward 8
#          up 3
#          down 8
#          forward 2
#  
#  Your horizontal position and depth both start at 0. The steps above would then modify them as follows:
#  
#          forward 5    adds 5 to your horizontal position, a total of 5.
#          down 5       adds 5 to your depth, resulting in a value of 5.
#          forward 8    adds 8 to your horizontal position, a total of 13.
#          up 3         decreases your depth by 3, resulting in a value of 2.
#          down 8       adds 8 to your depth, resulting in a value of 10.
#          forward 2    adds 2 to your horizontal position, a total of 15.
#  
#  After following these instructions, you would have a horizontal position of 15 and a depth of 10. 
#  (Multiplying these together produces 150.)
#  
#  Calculate the horizontal position and depth you would have after following the planned course. What do you 
#  get if you multiply your final horizontal position by your final depth?
#  




class SubmarineCommand:
    def __init__(self, command):
        parts = command.split(" ")
        self.direction = parts[0]
        self.distance = int(parts[1])

    def get_direction(self):
        return self.direction

    def get_distance(self):
        return self.distance

    def get_horizontal_detla(self):
        if self.direction == "forward":
            return self.distance
        else:
            return 0

    def get_vertical_delta(self):
        if self.direction == "up":
            return -self.distance
        elif self.direction == "down":
            return self.distance
        else:
            return 0

def build_submarine_commands(raw_commands):
    submarine_commands = []
    for cmd in raw_commands:
        submarine_commands.append(SubmarineCommand(cmd))

    return submarine_commands
### buildSubmarineCommands


def calculate_submarine_position(submarine_commands):
    horizontal = 0
    depth = 0

    for cmd in submarine_commands:
        horizontal += cmd.get_horizontal_detla()
        depth += cmd.get_vertical_delta()

    return horizontal, depth
### calculate_submarine_position


class DayXXPartOneTests(unittest.TestCase):

    
    def test__part_1__sample_input(self):
        raw_commands = read_file_into_array(sample_input_file_1, False)
        submarine_commands = build_submarine_commands(raw_commands)
        horizontal, depth = calculate_submarine_position(submarine_commands)
            
        self.assertEqual(horizontal, 15)
        self.assertEqual(depth, 10)


    def test__part_1__challenge_input(self):
        print("")
        
        raw_commands = read_file_into_array(input_file, False)
        submarine_commands = build_submarine_commands(raw_commands)
        horizontal, depth = calculate_submarine_position(submarine_commands)
        print("Solution to day XX part 1: {0}".format(horizontal * depth))
        

# print("Solution to day XX part 1: {0}".format(-1))


###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################
#  
#  --- Part Two ---
#  Based on your calculations, the planned course doesn't seem to make any sense. You find the submarine manual and discover 
#  that the process is actually slightly more complicated.
#  
#  In addition to horizontal position and depth, you'll also need to track a third value, aim, which also starts at 0. The 
#  commands also mean something entirely different than you first thought:
#  
#      down X increases your aim by X units.
#      up X decreases your aim by X units.
#      forward X does two things:
#          It increases your horizontal position by X units.
#          It increases your depth by your aim multiplied by X.
#  
#  Again note that since you're on a submarine, down and up do the opposite of what you might expect: "down" means aiming in 
#  the positive direction.
#  
#  Now, the above example does something different:
#  
#      forward 5 adds 5 to your horizontal position, a total of 5. Because your aim is 0, your depth does not change.
#      down 5 adds 5 to your aim, resulting in a value of 5.
#      forward 8 adds 8 to your horizontal position, a total of 13. Because your aim is 5, your depth increases by 8*5=40.
#      up 3 decreases your aim by 3, resulting in a value of 2.
#      down 8 adds 8 to your aim, resulting in a value of 10.
#      forward 2 adds 2 to your horizontal position, a total of 15. Because your aim is 10, your depth increases by 2*10=20 to a total of 60.
#  
#  After following these new instructions, you would have a horizontal position of 15 and a depth of 60. (Multiplying these produces 900.)
#  
#  Using this new interpretation of the commands, calculate the horizontal position and depth you would have after following the planned course. 
#  What do you get if you multiply your final horizontal position by your final depth?
#  


def calculate_submarine_position_part_2(submarine_commands):
    horizontal = 0
    depth = 0
    aim = 0

    for cmd in submarine_commands:
        if cmd.get_direction() == "down":
            aim += cmd.get_distance()

        elif cmd.get_direction() == "up":
            aim -= cmd.get_distance()

        elif cmd.get_direction() == "forward":
            horizontal += cmd.get_distance()
            depth += aim * cmd.get_distance()

        # print("step: h={0}\td={1}\ta={2}\tcmd={3} {4}".format(horizontal, depth, aim, cmd.get_direction(), cmd.get_distance()))


    return horizontal, depth, aim
### calculate_submarine_position

class DayXXPartTwoTests(unittest.TestCase):

    

    def test__part_2__sample_input(self):
        raw_commands = read_file_into_array(sample_input_file_1, False)
        submarine_commands = build_submarine_commands(raw_commands)
        horizontal, depth, aim = calculate_submarine_position_part_2(submarine_commands)
            
        self.assertEqual(horizontal, 15)
        self.assertEqual(depth, 60)


    def test__part_2__challenge_input(self):
        print("")
        
        raw_commands = read_file_into_array(input_file, False)
        submarine_commands = build_submarine_commands(raw_commands)
        horizontal, depth, aim = calculate_submarine_position_part_2(submarine_commands)
        print("Solution to day 2 part 2: {0}".format(horizontal * depth))
 

 
###################################################################################################################################################################
########################################################################## RUN THE TESTS ##########################################################################


# run then unit tests "last"
if __name__ == '__main__':
    unittest.main()
 

