#!/bin/python
# -*- coding: utf-8 -*-
# https://adventofcode.com/2021/day/12


###################################################################################################################################################################
#  
#  Solution to day 12 part 1: 4573
#
#  Solution to day 12 part 2: 117509
#
###################################################################################################################################################################

import re
import unittest

###################################################################################################################################################################
############################################################################# Common ##############################################################################


sample_input_file_1 = "2021_sample_1.txt"
sample_input_file_2 = "2021_sample_2.txt"
sample_input_file_3 = "2021_sample_3.txt"
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
#  --- Day 12: Passage Pathing ---
#  With your submarine's subterranean subsystems subsisting suboptimally, the only way you're getting out of this 
#  cave anytime soon is by finding a path yourself. Not just a path - the only way to know if you've found the best 
#  path is to find all of them.
#  
#  Fortunately, the sensors are still mostly working, and so you build a rough map of the remaining caves 
#  (your puzzle input). For example:
#  
#      start-A
#      start-b
#      A-c
#      A-b
#      b-d
#      A-end
#      b-end
#  
#  This is a list of how all of the caves are connected. You start in the cave named start, and your destination is 
#  the cave named end. An entry like b-d means that cave b is connected to cave d - that is, you can move between them.
#  
#  So, the above cave system looks roughly like this:
#  
#          start
#          /   \
#      c--A-----b--d
#          \   /
#           end
#  
#  Your goal is to find the number of distinct paths that start at start, end at end, and don't visit small caves 
#  more than once. There are two types of caves: big caves (written in uppercase, like A) and small caves (written 
#  in lowercase, like b). It would be a waste of time to visit any small cave more than once, but big caves are 
#  large enough that it might be worth visiting them multiple times. So, all paths you find should visit small caves 
#  at most once, and can visit big caves any number of times.
#  
#  Given these rules, there are 10 paths through this example cave system:
#  
#      start,A,b,A,c,A,end
#      start,A,b,A,end
#      start,A,b,end
#      start,A,c,A,b,A,end
#      start,A,c,A,b,end
#      start,A,c,A,end
#      start,A,end
#      start,b,A,c,A,end
#      start,b,A,end
#      start,b,end
#  
#  (Each line in the above list corresponds to a single path; the caves visited by that path are listed in 
#  the order they are visited and separated by commas.)
#  
#  Note that in this cave system, cave d is never visited by any path: to do so, cave b would need to be visited 
#  twice (once on the way to cave d and a second time when returning from cave d), and since cave b is small, 
#  this is not allowed.
#  
#  Here is a slightly larger example:
#  
#      dc-end
#      HN-start
#      start-kj
#      dc-start
#      dc-HN
#      LN-dc
#      HN-end
#      kj-sa
#      kj-HN
#      kj-dc
#  
#  The 19 paths through it are as follows:
#  
#      start,HN,dc,HN,end
#      start,HN,dc,HN,kj,HN,end
#      start,HN,dc,end
#      start,HN,dc,kj,HN,end
#      start,HN,end
#      start,HN,kj,HN,dc,HN,end
#      start,HN,kj,HN,dc,end
#      start,HN,kj,HN,end
#      start,HN,kj,dc,HN,end
#      start,HN,kj,dc,end
#      start,dc,HN,end
#      start,dc,HN,kj,HN,end
#      start,dc,end
#      start,dc,kj,HN,end
#      start,kj,HN,dc,HN,end
#      start,kj,HN,dc,end
#      start,kj,HN,end
#      start,kj,dc,HN,end
#      start,kj,dc,end
#  
#  Finally, this even larger example has 226 paths through it:
#  
#      fs-end
#      he-DX
#      fs-he
#      start-DX
#      pj-DX
#      end-zg
#      zg-sl
#      zg-pj
#      pj-he
#      RW-he
#      fs-DX
#      pj-RW
#      zg-RW
#      start-pj
#      he-WI
#      zg-he
#      pj-fs
#      start-RW
#  
#  How many paths through this cave system are there that visit small caves at most once?
#  
#  

def parse_cave_system(rough_map):
    cave_system = {}
    for map_sections in rough_map:
        edges = map_sections.split("-")


        if cave_system.get(edges[0]) is None:
            cave_system[edges[0]] = [edges[1]]

        else:
            cave_system[edges[0]].append(edges[1] )


        if cave_system.get(edges[1]) is None:
            cave_system[edges[1]] = [edges[0]]

        else:
            cave_system[edges[1]].append(edges[0] )

    return cave_system


lower_case_regex = re.compile('[a-z]+') # slight speed improvement by not recompiling regex on ever call...
def is_small_cave(cave):
    lower_case_matches = lower_case_regex.findall(cave)
    return len(lower_case_matches) != 0



def count_distinct_paths_visiting_small_caves_at_most_once(cave_system, starting_node, ending_node):
    visited_paths = []
    visit_node(cave_system, ending_node, visited_paths, "", starting_node)
    
    return len(visited_paths)



def visit_node(cave_system, ending_node, visited_paths, current_path, current_node):

    new_path = current_path + current_node

    # Has the path terminated?
    if current_node == ending_node:
        visited_paths.append(new_path)
        return


    # avoid visiting a small cave more than once
    if is_small_cave(current_node) and current_node in current_path:
        return


    # continue on through the cave
    for connected_node  in cave_system[current_node]:
        visit_node(cave_system, ending_node, visited_paths, new_path, connected_node)




class ClassName:
    def __init__(self):
        pass



class Day12PartOneTests(unittest.TestCase):


    def test__part_1__sample_input_1(self):
        print("")
        rough_map = read_file_into_array(sample_input_file_1, False)
        cave_system = parse_cave_system(rough_map)
        distinct_paths = count_distinct_paths_visiting_small_caves_at_most_once(cave_system, "start", "end")
        self.assertEqual(10, distinct_paths)


    def test__part_1__sample_input_2(self):
        print("")
        rough_map = read_file_into_array(sample_input_file_2, False)
        cave_system = parse_cave_system(rough_map)
        distinct_paths = count_distinct_paths_visiting_small_caves_at_most_once(cave_system, "start", "end")
        self.assertEqual(19, distinct_paths)


    def test__part_1__sample_input_3(self):
        print("")
        rough_map = read_file_into_array(sample_input_file_3, False)
        cave_system = parse_cave_system(rough_map)
        distinct_paths = count_distinct_paths_visiting_small_caves_at_most_once(cave_system, "start", "end")
        self.assertEqual(226, distinct_paths)


    def test__part_1__challenge_input(self):
        print("")
        rough_map = read_file_into_array(input_file, False)
        cave_system = parse_cave_system(rough_map)
        distinct_paths = count_distinct_paths_visiting_small_caves_at_most_once(cave_system, "start", "end")

        print("Solution to day 12 part 1: {0}".format(distinct_paths))
        



###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################
#  
#  --- Part Two ---
#  After reviewing the available paths, you realize you might have time to visit a single small cave twice. Specifically, 
#  big caves can be visited any number of times, a single small cave can be visited at most twice, and the remaining small 
#  caves can be visited at most once. However, the caves named start and end can only be visited exactly once each: once you 
#  leave the start cave, you may not return to it, and once you reach the end cave, the path must end immediately.
#  
#  Now, the 36 possible paths through the first example above are:
#  
#      start,A,b,A,b,A,c,A,end
#      start,A,b,A,b,A,end
#      start,A,b,A,b,end
#      start,A,b,A,c,A,b,A,end
#      start,A,b,A,c,A,b,end
#      start,A,b,A,c,A,c,A,end
#      start,A,b,A,c,A,end
#      start,A,b,A,end
#      start,A,b,d,b,A,c,A,end
#      start,A,b,d,b,A,end
#      start,A,b,d,b,end
#      start,A,b,end
#      start,A,c,A,b,A,b,A,end
#      start,A,c,A,b,A,b,end
#      start,A,c,A,b,A,c,A,end
#      start,A,c,A,b,A,end
#      start,A,c,A,b,d,b,A,end
#      start,A,c,A,b,d,b,end
#      start,A,c,A,b,end
#      start,A,c,A,c,A,b,A,end
#      start,A,c,A,c,A,b,end
#      start,A,c,A,c,A,end
#      start,A,c,A,end
#      start,A,end
#      start,b,A,b,A,c,A,end
#      start,b,A,b,A,end
#      start,b,A,b,end
#      start,b,A,c,A,b,A,end
#      start,b,A,c,A,b,end
#      start,b,A,c,A,c,A,end
#      start,b,A,c,A,end
#      start,b,A,end
#      start,b,d,b,A,c,A,end
#      start,b,d,b,A,end
#      start,b,d,b,end
#      start,b,end
#      
#  The slightly larger example above now has 103 paths through it, and the even larger example now has 3509 paths through it.
#  
#  Given these new rules, how many paths through this cave system are there?
#  


def count_distinct_paths_visiting_small_caves_at_most_once_except_for_one_small_cave_visited_twice(cave_system, starting_node, ending_node):
    visited_paths = []
    visit_node_2(cave_system, starting_node, ending_node, visited_paths, "", starting_node, False)

    return len(visited_paths)

        


def visit_node_2(cave_system, start_node, ending_node, visited_paths, current_path, current_node, one_small_visited_twice):

    # Do not return to the beginning
    if current_node == start_node and current_path != "":
        return

    if current_node == start_node:
        new_path = ""
    else:
        new_path = current_path + current_node

    # Has the path terminated?
    if current_node == ending_node:
        visited_paths.append(new_path)
        return

    if is_small_cave(current_node):
        if current_node in current_path:
            if not one_small_visited_twice:
                # we are good to visit this small cave a second time
                one_small_visited_twice = True
            else:
                # we have already visited a small cave, abort route
                return


    # continue on through the cave
    for connected_node  in cave_system[current_node]:
        visit_node_2(cave_system, start_node, ending_node, visited_paths, new_path, connected_node, one_small_visited_twice)




class Day12PartTwoTests(unittest.TestCase):


    def test__part_2__sample_input_1(self):
        print("")
        rough_map = read_file_into_array(sample_input_file_1, False)
        cave_system = parse_cave_system(rough_map)
        distinct_paths = count_distinct_paths_visiting_small_caves_at_most_once_except_for_one_small_cave_visited_twice(cave_system, "start", "end")
        self.assertEqual(36, distinct_paths)


    def test__part_2__sample_input_2(self):
        print("")
        rough_map = read_file_into_array(sample_input_file_2, False)
        cave_system = parse_cave_system(rough_map)
        distinct_paths = count_distinct_paths_visiting_small_caves_at_most_once_except_for_one_small_cave_visited_twice(cave_system, "start", "end")
        self.assertEqual(103, distinct_paths)


    def test__part_2__sample_input_3(self):
        print("")
        rough_map = read_file_into_array(sample_input_file_3, False)
        cave_system = parse_cave_system(rough_map)
        distinct_paths = count_distinct_paths_visiting_small_caves_at_most_once_except_for_one_small_cave_visited_twice(cave_system, "start", "end")
        self.assertEqual(3509, distinct_paths)


    def test__part_2__challenge_input(self):
        print("")
        rough_map = read_file_into_array(input_file, False)
        cave_system = parse_cave_system(rough_map)
        distinct_paths = count_distinct_paths_visiting_small_caves_at_most_once_except_for_one_small_cave_visited_twice(cave_system, "start", "end")

        print("Solution to day 12 part 2: {0}".format(distinct_paths))
     
 

 
###################################################################################################################################################################
########################################################################## RUN THE TESTS ##########################################################################


# run then unit tests "last"
if __name__ == '__main__':
    unittest.main()
 

