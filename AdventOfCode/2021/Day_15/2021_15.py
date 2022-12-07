#!/bin/python
# -*- coding: utf-8 -*-
# https://adventofcode.com/2021/day/15


###################################################################################################################################################################
#  
#  Solution to day 15 part 1: 581
#
#  Solution to day 15 part 2: 2916
#
###################################################################################################################################################################

import resource
import unittest
import sys

sys.setrecursionlimit(15000) # is this necessary. probably not. I changed the algorithm.

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
#  --- Day 15: Chiton ---
#  You've almost reached the exit of the cave, but the walls are getting closer together. Your submarine can 
#  barely still fit, though; the main problem is that the walls of the cave are covered in chitons, and it would 
#  be best not to bump any of them.
#  
#  The cavern is large, but has a very low ceiling, restricting your motion to two dimensions. The shape 
#  of the cavern resembles a square; a quick scan of chiton density produces a map of risk level throughout 
#  the cave (your puzzle input). For example:
#  
#      1163751742
#      1381373672
#      2136511328
#      3694931569
#      7463417111
#      1319128137
#      1359912421
#      3125421639
#      1293138521
#      2311944581
#  
#  You start in the top left position, your destination is the bottom right position, and you cannot 
#  move diagonally. The number at each position is its risk level; to determine the total risk of an 
#  entire path, add up the risk levels of each position you enter (that is, don't count the risk level 
#  of your starting position unless you enter it; leaving it adds no risk to your total).
#  
#  Your goal is to find a path with the lowest total risk. In this example, a path with the lowest 
#  total risk is highlighted here:
#  
#      1163751742
#      1381373672
#      2136511328
#      3694931569
#      7463417111
#      1319128137
#      1359912421
#      3125421639
#      1293138521
#      2311944581
#  
#  The total risk of this path is 40 (the starting position is never entered, so its risk is not counted).
#  
#  What is the lowest total risk of any path from the top left to the bottom right?
#  


##### Build Dijkstra's Algo Impl

import heapq
  
#   # initializing list
#   priority_queue = [5, 7, 9, 1, 3]
#   heapq.heapify(priority_queue)       # using heapify to convert list into heap
#   heapq.heappush(priority_queue,4)    # add item to queue. 
#   heapq.heappop(priority_queue)       # remove the "smallest" element
#   print( list(priority_queue) )       # print contents (in heap order)


### https://www.geeksforgeeks.org/heapq-with-custom-predicate-in-python/

class Node:
 
    def __init__(self, x, y, risk_score):
        self.x = x
        self.y = y
        self.risk_score = risk_score
        self.min_distance = float('inf')
        self.previous_node = None

 
  # function for customized printing
    def __repr__(self):
        if self.previous_node is None:
            return "[Node: x={0}, y={1}, s={2}, d={3}, p={4}]".format(self.x, self.y, self.risk_score, self.min_distance, self.previous_node)
        else:
            return "[Node: x={0}, y={1}, s={2}, d={3}, p={4}]".format(self.x, self.y, self.risk_score, self.min_distance, (self.previous_node.x, self.previous_node.y))
 
   # override the comparison operator
    def __lt__(self, other):
        return self.min_distance < other.min_distance


    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

##### Node



def parse_chiton_map(raw_chiton_details):
    width = len(raw_chiton_details[0])
    height = len(raw_chiton_details)

    chiton_map = {}

    for y in range(height):
        for x in range(width):
            chiton_map[ (x,y) ] = Node(x, y, int(raw_chiton_details[y][x]))

    return chiton_map, width, height
### parse_chiton_map



def find_shortest_route_Dijkstra(chiton_map, start_point, end_point):
    # set priority of the start node.
    start_node = chiton_map[start_point]
    start_node.min_distance = 0

    # create priority queue
    priority_queue = list(chiton_map.values())
    heapq.heapify(priority_queue)

    # processed_nodes = []

    while len(priority_queue) > 0:  # while there are nodes left to process
        next_closest_node = heapq.heappop(priority_queue)
        # processed_nodes.append(next_closest_node)       # do we really need this. it was in the book. added for completeness.

        neighbors = get_neighbor_nodes(chiton_map, next_closest_node.x, next_closest_node.y)
        for neighbor in neighbors:
            # if neighbor has already been marked, skip it
            if neighbor.previous_node is None:
                neighbor.min_distance = next_closest_node.min_distance + neighbor.risk_score
                neighbor.previous_node = next_closest_node            

        # we have changed the value of several nodes. We need to maintain the heap invarient
        heapq.heapify(priority_queue)


    start_node.previous_node = None

    # print out the shortest path, from end to start
    node = chiton_map[end_point]
    print("::shortest route::")
    while node is not None:
        print(node)
        node = node.previous_node

    return chiton_map[end_point].min_distance


### find_shortest_route_Dijkstra


def get_neighbor_nodes(chiton_map, x, y):
    neighbors = []

    if chiton_map.get((x-1, y)) is not None:
        neighbors.append(chiton_map[(x-1, y)])

    if chiton_map.get((x+1, y)) is not None:
        neighbors.append(chiton_map[(x+1, y)])

    if chiton_map.get((x, y-1)) is not None:
        neighbors.append(chiton_map[(x, y-1)])

    if chiton_map.get((x,y+1)) is not None:
        neighbors.append(chiton_map[(x,y+1)])

    return neighbors
### get_neighbor_nodes



class Day15PartOneTests(unittest.TestCase):

    
    def test__part_1__sample_input_1(self):
        print("")
        lines = read_file_into_array(sample_input_file_1, False)
        chiton_map, width, height = parse_chiton_map(lines)
        risk_score = find_shortest_route_Dijkstra(chiton_map, (0,0), (width-1,height-1))
        self.assertEqual(40, risk_score)

    def test__part_1__sample_input_2(self):
        print("")
        lines = read_file_into_array(sample_input_file_2, False)
        chiton_map, width, height = parse_chiton_map(lines)
        risk_score = find_shortest_route_Dijkstra(chiton_map, (0,0), (width-1,height-1))
        self.assertEqual(6, risk_score)


    def test__part_1__challenge_input(self):
        print("")
        lines = read_file_into_array(input_file, False)
        chiton_map, width, height = parse_chiton_map(lines)
        risk_score = find_shortest_route_Dijkstra(chiton_map, (0,0), (width-1,height-1))

        print("Solution to day 15 part 1: {0}".format(risk_score))
        

#### implement a better path finding algo. DFS is too expensive. (works on sample input, barely works on part 1, will fail misribly on part 2)
### https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2


###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################
#  
#  --- Part Two ---
#  Now that you know how to find low-risk paths in the cave, you can try to find your way out.
#  
#  The entire cave is actually five times larger in both dimensions than you thought; the area you originally 
#  scanned is just one tile in a 5x5 tile area that forms the full map. Your original map tile repeats to the 
#  right and downward; each time the tile repeats to the right or downward, all of its risk levels are 1 higher 
#  than the tile immediately up or left of it. However, risk levels above 9 wrap back around to 1. So, if your 
#  original map had some position with a risk level of 8, then that same position on each of the 25 total tiles would be as follows:
#  
#      8 9 1 2 3
#      9 1 2 3 4
#      1 2 3 4 5
#      2 3 4 5 6
#      3 4 5 6 7
#      
#  Each single digit above corresponds to the example position with a value of 8 on the top-left tile. Because the full 
#  map is actually five times larger in both dimensions, that position appears a total of 25 times, once in each duplicated tile, with the values shown above.
#  
#  Here is the full five-times-as-large version of the first example above, with the original map in the top left corner highlighted:
#  
#      11637517422274862853338597396444961841755517295286
#      13813736722492484783351359589446246169155735727126
#      21365113283247622439435873354154698446526571955763
#      36949315694715142671582625378269373648937148475914
#      74634171118574528222968563933317967414442817852555
#      13191281372421239248353234135946434524615754563572
#      13599124212461123532357223464346833457545794456865
#      31254216394236532741534764385264587549637569865174
#      12931385212314249632342535174345364628545647573965
#      23119445813422155692453326671356443778246755488935
#      22748628533385973964449618417555172952866628316397
#      24924847833513595894462461691557357271266846838237
#      32476224394358733541546984465265719557637682166874
#      47151426715826253782693736489371484759148259586125
#      85745282229685639333179674144428178525553928963666
#      24212392483532341359464345246157545635726865674683
#      24611235323572234643468334575457944568656815567976
#      42365327415347643852645875496375698651748671976285
#      23142496323425351743453646285456475739656758684176
#      34221556924533266713564437782467554889357866599146
#      33859739644496184175551729528666283163977739427418
#      35135958944624616915573572712668468382377957949348
#      43587335415469844652657195576376821668748793277985
#      58262537826937364893714847591482595861259361697236
#      96856393331796741444281785255539289636664139174777
#      35323413594643452461575456357268656746837976785794
#      35722346434683345754579445686568155679767926678187
#      53476438526458754963756986517486719762859782187396
#      34253517434536462854564757396567586841767869795287
#      45332667135644377824675548893578665991468977611257
#      44961841755517295286662831639777394274188841538529
#      46246169155735727126684683823779579493488168151459
#      54698446526571955763768216687487932779859814388196
#      69373648937148475914825958612593616972361472718347
#      17967414442817852555392896366641391747775241285888
#      46434524615754563572686567468379767857948187896815
#      46833457545794456865681556797679266781878137789298
#      64587549637569865174867197628597821873961893298417
#      45364628545647573965675868417678697952878971816398
#      56443778246755488935786659914689776112579188722368
#      55172952866628316397773942741888415385299952649631
#      57357271266846838237795794934881681514599279262561
#      65719557637682166874879327798598143881961925499217
#      71484759148259586125936169723614727183472583829458
#      28178525553928963666413917477752412858886352396999
#      57545635726865674683797678579481878968159298917926
#      57944568656815567976792667818781377892989248891319
#      75698651748671976285978218739618932984172914319528
#      56475739656758684176786979528789718163989182927419
#      67554889357866599146897761125791887223681299833479
#  
#  Equipped with the full map, you can now find a path from the top left corner to the bottom right corner with the lowest total risk:
#  
#      11637517422274862853338597396444961841755517295286
#      13813736722492484783351359589446246169155735727126
#      21365113283247622439435873354154698446526571955763
#      36949315694715142671582625378269373648937148475914
#      ...
#      75698651748671976285978218739618932984172914319528
#      56475739656758684176786979528789718163989182927419
#      67554889357866599146897761125791887223681299833479
#  
#  The total risk of this path is 315 (the starting position is still never entered, so its risk is not counted).
#  
#  Using the full map, what is the lowest total risk of any path from the top left to the bottom right?
#

def increment_and_wrap_chiton_map(raw_chiton_details: [str]):
    # print("start: {0}".format(raw_chiton_details))
    new_raw_chiton_details = []
    for row in raw_chiton_details:
        line = ""
        for char in row:
            line +=  str(int(char) % 9 +1)

        new_raw_chiton_details.append(line)

        # print(type(line))
        # print(line)
    # print("########")
    # print(new_raw_chiton_details)
    return new_raw_chiton_details


def grow_chiton_map(raw_chiton_details, width, height):
    ### grow the map to the right
    raw_chiton_details_2 = increment_and_wrap_chiton_map(raw_chiton_details)
    raw_chiton_details_3 = increment_and_wrap_chiton_map(raw_chiton_details_2)
    raw_chiton_details_4 = increment_and_wrap_chiton_map(raw_chiton_details_3)
    raw_chiton_details_5 = increment_and_wrap_chiton_map(raw_chiton_details_4)

    composite_chiton_details = []
    for i in range(height):
        line = raw_chiton_details[i]
        line += raw_chiton_details_2[i]
        line += raw_chiton_details_3[i]
        line += raw_chiton_details_4[i]
        line += raw_chiton_details_5[i]

        composite_chiton_details.append(line)

    #### grow the map down.
    for i in range(height*4):
        new_line = increment_and_wrap_chiton_map([composite_chiton_details[i]])
        composite_chiton_details.append( new_line[0] )

    return composite_chiton_details


class Day15PartTwoTests(unittest.TestCase):


    def test__part_2__sample_input_1(self):
        print("")
        raw_chiton_map = read_file_into_array(sample_input_file_1, False)
        chiton_map, width, height = parse_chiton_map(raw_chiton_map)

        raw_chiton_map = grow_chiton_map(raw_chiton_map, width, height)
        chiton_map, width, height = parse_chiton_map(raw_chiton_map)
        risk_score = find_shortest_route_Dijkstra(chiton_map, (0,0), (width-1,height-1))        
        self.assertEqual(315, risk_score)
    

    def test__part_2__challenge_input(self):
        print("")
        raw_chiton_map = read_file_into_array(input_file, False)
        chiton_map, width, height = parse_chiton_map(raw_chiton_map)

        raw_chiton_map = grow_chiton_map(raw_chiton_map, width, height)
        chiton_map, width, height = parse_chiton_map(raw_chiton_map)
        risk_score = find_shortest_route_Dijkstra(chiton_map, (0,0), (width-1,height-1))        

        print("Solution to day 15 part 2: {0}".format(risk_score))


 
###################################################################################################################################################################
########################################################################## RUN THE TESTS ##########################################################################


# run then unit tests "last"
if __name__ == '__main__':
    unittest.main()
 

