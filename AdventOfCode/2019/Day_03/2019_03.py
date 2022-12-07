#!/bin/python
# -*- coding: utf-8 -*-
# https://adventofcode.com/2019/day/3


###################################################################################################################################################################
#  
#  Solution to day 3 part 1: 721
#  Solution to day 3 part 2: 7388
#
###################################################################################################################################################################


###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################

input_file = "sample.txt"
input_file = "input.txt"

def calculate_manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)
### calculate_manhattan_distance


class IntersectionMetadata(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.wires = []
    ### __init__

    def get_point(self):
        return str(self.x) + "," + str(self.y)
    ### get_point


    def add_wire(self, wire, steps):
        self.wires.append( (wire, steps) )
    ### add_wire


    def get_sum_of_wire_steps(self):
        total = 0
        for wire in self.wires:
            total += wire[1]

        return total
    ### get_sum_of_wire_steps

### IntersectionMetadata

def minimum_signal_timing(intersections):
    minimized_steps = float("inf")

    for intersection in intersections:
        intersection_step_sum = intersection.get_sum_of_wire_steps()
        if intersection_step_sum < minimized_steps:
            print "New minimum steps found: %f -> %d (%s)" % (minimized_steps, intersection_step_sum, intersection.get_point())
            minimized_steps = intersection_step_sum

    return minimized_steps
### minimum_signal_timing

class Grid(object):
    def __init__(self):
        self.grid = {}
        self.x = 0 # left / right
        self.y = 0 # up / down
        self.current_wire = None
        self.steps = 0
        self.intersections = None
    ### __init__

    def set_wire(self, wire):
        self.x = 0 # up / down
        self.y = 0 # left / right
        self.current_wire = wire
        self.steps = 0
        self.intersections = set()
    ### set_wire

    def trace_wire(self, directions):
        segments = directions.split(",")
        for segment in segments:
            direction = segment[0:1]
            length = int(segment[1:])

            # print "%s %d" % (direction, length)
            self.trace_wire_segment(direction, length)
    ### trace_wire

    def trace_wire_segment(self, direction, length):
        for i in xrange(length):

            # slide the pointer
            if direction == "D":
                self.y += -1

            elif direction == "U":
                self.y += 1

            elif direction == "L":
                self.x += -1

            elif direction == "R":
                self.x += 1

            # step the wire
            self.steps += 1

            # mark the new location for the wire
            self.write_wire_location()

    ### trace_wire

    def write_wire_location(self):
        key = str(self.x) + "," + str(self.y)

        # a wire has already crossed this point.
        if key in self.grid:
            wires_at_location = self.grid[key]

            if self.current_wire not in wires_at_location:
                wires_at_location[self.current_wire] = self.steps
                self.intersections.add(key) # add the key for grid location we are currently at
                print "interection found: (%s)" % (key)
                

            # wires_at_location = self.grid[key]
            # size_before = len(wires_at_location)
            # wires_at_location.add(self.current_wire)
            # size_after = len(wires_at_location)

            # # check if we have interected with a different wire
            # if size_before != size_after:
            #     self.intersections.append([self.x, self.y])
            #     print "interection found: (%d,%d)" % (self.x, self.y)

        # we are the first wire at the point
        else:
            # self.grid[key] = set(self.current_wire)
            self.grid[key] = {self.current_wire: self.steps}
    ### write_wire_location

    def get_interection_points(self):
        points = []
        for intersection in self.intersections:
            parts = intersection.split(",")
            x = int(parts[0])
            y = int(parts[1])

            intersection_metadata = IntersectionMetadata(x, y)

            for wire, steps in self.grid[intersection].items():
                intersection_metadata.add_wire(wire, steps)
            
            points.append(intersection_metadata)

        return points
    ### get_interection_points

### Grid





def find_smallest_manhattan_distance_to_origin(points):
    smallest_distance = float("inf")
    for point in points:
        x = point.x
        y = point.y

        manhattan_distance = calculate_manhattan_distance(x, y, 0, 0)

        if manhattan_distance != 0 and manhattan_distance < smallest_distance:
            smallest_distance = manhattan_distance

    return smallest_distance
### find_smallest_manhattan_distance_to_origin




with open(input_file) as f:
    
    while True:
        wire_one = f.readline()
        wire_two = f.readline()
        if not wire_two: break  # EOF

        grid = Grid()
        grid.set_wire("|")
        grid.trace_wire(wire_one)
        grid.set_wire("-")
        grid.trace_wire(wire_two)
        intersections = grid.get_interection_points()

        m = find_smallest_manhattan_distance_to_origin(intersections)
        print m
        


print "Solution to day 3 part 1: " + str(m)



###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################


minimized_timing = minimum_signal_timing(intersections)


print "Solution to day 3 part 2: " + str(minimized_timing)

