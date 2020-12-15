#!/bin/python
# -*- coding: utf-8 -*-
# https://adventofcode.com/2020/day/12


###################################################################################################################################################################
#  
#  Solution to day 12 part 1: 998
#
#  Solution to day 12 part 2: 71586
#
###################################################################################################################################################################


###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################
#   
#   --- Day 12: Rain Risk ---
#   Your ferry made decent progress toward the island, but the storm came in faster than anyone 
#   expected. The ferry needs to take evasive actions!
#   
#   Unfortunately, the ship's navigation computer seems to be malfunctioning; rather than giving 
#   a route directly to safety, it produced extremely circuitous instructions. When the captain 
#   uses the PA system to ask if anyone can help, you quickly volunteer.
#   
#   The navigation instructions (your puzzle input) consists of a sequence of single-character 
#   actions paired with integer input values. After staring at them for a few minutes, you work 
#   out what they probably mean:
#   
#       Action N means to move north by the given value.
#       Action S means to move south by the given value.
#       Action E means to move east by the given value.
#       Action W means to move west by the given value.
#       Action L means to turn left the given number of degrees.
#       Action R means to turn right the given number of degrees.
#       Action F means to move forward by the given value in the direction the ship is currently facing.
#   
#   The ship starts by facing east. Only the L and R actions change the direction the ship is facing. 
#   (That is, if the ship is facing east and the next instruction is N10, the ship would move north 
#       10 units, but would still move east if the following action were F.)
#   
#   For example:
#   
#       F10
#       N3
#       F7
#       R90
#       F11
#   
#   These instructions would be handled as follows:
#   
#       F10 would move the ship 10 units east (because the ship starts by facing east) to east 10, north 0.
#       N3 would move the ship 3 units north to east 10, north 3.
#       F7 would move the ship another 7 units east (because the ship is still facing east) to east 17, north 3.
#       R90 would cause the ship to turn right by 90 degrees and face south; it remains at east 17, north 3.
#       F11 would move the ship 11 units south to east 17, south 8.
#   
#   At the end of these instructions, the ship's Manhattan distance (sum of the absolute values of 
#   its east/west position and its north/south position) from its starting position is 17 + 8 = 25.
#   
#   Figure out where the navigation instructions lead. What is the Manhattan distance between that 
#   location and the ship's starting position?
#   

def test_equal(actual, expected, message):
    if actual != expected:
        print("FAIL: Found={0}  Expected={1}    {2}".format(actual, expected, message))


sample_input_file_1 = "2020_12_sample_1.txt"
sample_input_file_2 = "2020_12_sample_2.txt"
input_file          = "2020_12_input.txt"



class Ferry:
    def __init__(self, initial_degrees):
        # self.direction = initial_direction
        self.degrees   = 0
        self.x = 0      # track north (pos) /south (neg)
        self.y = 0      # track east (pos) /west (neg)

    def perform_move_action(self, action, distance):
        if action == "N":
            self.x += distance

        elif action == "S":
            self.x -= distance

        elif action == "E":
            self.y += distance

        elif action == "W":
            self.y -= distance

        elif action == "F":
            self.perform_move_action(
                Ferry.convert_degrees_to_direction(self.degrees), 
                distance
            )

        elif action == "L":
            self.degrees += distance

        elif action == "R":
            self.degrees -= distance

    def get_position_information(self):
        return self.x, self.y, self.degrees


    def convert_degrees_to_direction(degrees):
        degrees = degrees % 360
        if degrees == 0:
            return "E"
        elif degrees == 90:
            return "N"

        elif degrees == 180:
            return "W"

        elif degrees == 270:
            return "S"


def process_ship_movement_instruction_file(file_name):
    boat = Ferry(0) # facing east

    with open(file_name) as f:
        for line in f:
            line = line.strip()

            action = line[0]
            distance = int(line[1:])

            boat.perform_move_action(action, distance)
            x, y, degrees = boat.get_position_information()

            # print("Step: action={0} dist={1} \tx={2} \ty={3} \tdegree={4}".format(action, distance, x, y, degrees))

    # calculate Manhattan distance
    return abs(boat.x) + abs(boat.y)


print("--- P1 sample input ---")
result_sample = process_ship_movement_instruction_file(sample_input_file_1)
test_equal(result_sample, 25, "P1 distance sum wrong")
print("-------------------------")


result = process_ship_movement_instruction_file(input_file)


print("Solution to day 12 part 1: {0}".format(result))


###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################
#   
#   --- Part Two ---
#   Before you can give the destination to the captain, you realize that the actual action meanings 
#   were printed on the back of the instructions the whole time.
#   
#   Almost all of the actions indicate how to move a waypoint which is relative to the ship's position:
#   
#       Action N means to move the waypoint north by the given value.
#       Action S means to move the waypoint south by the given value.
#       Action E means to move the waypoint east by the given value.
#       Action W means to move the waypoint west by the given value.
#       Action L means to rotate the waypoint around the ship left (counter-clockwise) the given number of degrees.
#       Action R means to rotate the waypoint around the ship right (clockwise) the given number of degrees.
#       Action F means to move forward to the waypoint a number of times equal to the given value.
#   
#   The waypoint starts 10 units east and 1 unit north relative to the ship. The waypoint is relative 
#   to the ship; that is, if the ship moves, the waypoint moves with it.
#   
#   For example, using the same instructions as above:
#   
#       F10 moves the ship to the waypoint 10 times (a total of 100 units east and 10 units north), 
#           leaving the ship at east 100, north 10. The waypoint stays 10 units east and 1 unit north of the ship.
#       N3  moves the waypoint 3 units north to 10 units east and 4 units north of the ship. The 
#           ship remains at east 100, north 10.
#       F7  moves the ship to the waypoint 7 times (a total of 70 units east and 28 units north), 
#           leaving the ship at east 170, north 38. The waypoint stays 10 units east and 4 units north of the ship.
#       R90 rotates the waypoint around the ship clockwise 90 degrees, moving it to 4 units east 
#           and 10 units south of the ship. The ship remains at east 170, north 38.
#       F11 moves the ship to the waypoint 11 times (a total of 44 units east and 110 units south), 
#           leaving the ship at east 214, south 72. The waypoint stays 4 units east and 10 units south of the ship.
#   
#   After these operations, the ship's Manhattan distance from its starting position is 214 + 72 = 286.
#   
#   Figure out where the navigation instructions actually lead. What is the Manhattan distance 
#   between that location and the ship's starting position?
#   


class Ferry2:
    def __init__(self):
        self.waypoint_east_west   = 10
        self.waypoint_north_south = 1

        self.boat_east_west   = 0      # track north (pos) /south (neg)
        self.boat_north_south = 0      # track east (pos) /west (neg)


    def perform_move_action(self, action, distance):
        if action == "N":
            self.waypoint_north_south += distance

        elif action == "S":
            self.waypoint_north_south -= distance

        elif action == "E":
            self.waypoint_east_west += distance

        elif action == "W":
            self.waypoint_east_west -= distance

        elif action == "F":
            for i in range(distance):
                self.boat_east_west += self.waypoint_east_west
                self.boat_north_south += self.waypoint_north_south

        elif action == "R":
            # convert all left turns into right turns
            action = "L"
            distance = 360 - distance

        if action == "L":

            degrees = distance # for my sanity in the below statements
            x = self.waypoint_east_west
            y = self.waypoint_north_south

            if degrees == 90:
                self.waypoint_east_west     = -y
                self.waypoint_north_south   =  x
                

            elif degrees == 180:
                self.waypoint_east_west     = -x
                self.waypoint_north_south   = -y
                

            elif degrees == 270:
                self.waypoint_east_west     =  y
                self.waypoint_north_south   = -x
                

            # print("  L{0} \tx_1={1}\ty1={2} \t -> \tx_2={3}\ty2={4} ".format(distance, x, y, self.waypoint_east_west, self.waypoint_north_south))

            # elif degrees == 360: # no point, end where you started
            # skipping the case of more than 360, simply apply modulus before if block.


    def get_waypoint_information(self):
        return self.waypoint_east_west, self.waypoint_north_south

    def get_boat_information(self):
        return self.boat_east_west, self.boat_north_south


def process_ship_movement_instruction_file_2(file_name):
    boat = Ferry2()

    with open(file_name) as f:
        for line in f:
            line = line.strip()

            action = line[0]
            distance = int(line[1:])

            boat.perform_move_action(action, distance)
            
            boat_east_west, boat_north_south = boat.get_boat_information()
            waypoint_east_west, waypoint_north_south = boat.get_waypoint_information()

            # print("Step: action={0} dist={1} \tb_x={2} \tb_y={3} \tw_x={4} \tw_y={5}".format(action, distance, boat_east_west, boat_north_south, waypoint_east_west, waypoint_north_south))

    # calculate Manhattan distance
    return abs(boat.boat_east_west) + abs(boat.boat_north_south)


print("--- P2 sample input ---")
result_sample = process_ship_movement_instruction_file_2(sample_input_file_1)
test_equal(result_sample, 286, "P2 distance sum wrong")
print("-------------------------")


result = process_ship_movement_instruction_file_2(input_file)



print("Solution to day 12 part 2: {0}".format(result))

 