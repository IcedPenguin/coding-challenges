#!/bin/python
# -*- coding: utf-8 -*-
# https://adventofcode.com/2022/day/14


###################################################################################################################################################################
#  
#  Solution to part 1: 994
#
#  Solution to part 2: 26283
#
###################################################################################################################################################################

import unittest

###################################################################################################################################################################
#   --- Day 14: Regolith Reservoir ---
#   
#   The distress signal leads you to a giant waterfall! Actually, hang on - the signal seems like it's coming from the 
#   waterfall itself, and that doesn't make any sense. However, you do notice a little path that leads behind the waterfall.
#   
#   Correction: the distress signal leads you behind a giant waterfall! There seems to be a large cave system here, and the 
#   signal definitely leads further inside.
#   
#   As you begin to make your way deeper underground, you feel the ground rumble for a moment. Sand begins pouring into the 
#   cave! If you don't quickly figure out where the sand is going, you could quickly become trapped!
#   
#   Fortunately, your familiarity with analyzing the path of falling material will come in handy here. You scan a two-dimensional 
#   vertical slice of the cave above you (your puzzle input) and discover that it is mostly air with structures made of rock.
#   
#   Your scan traces the path of each solid rock structure and reports the x,y coordinates that form the shape of the path, 
#   where x represents distance to the right and y represents distance down. Each path appears as a single line of text in 
#   your scan. After the first point of each path, each point indicates the end of a straight horizontal or vertical line to be 
#   drawn from the previous point. For example:
#   
#       498,4 -> 498,6 -> 496,6
#       503,4 -> 502,4 -> 502,9 -> 494,9
#   
#   This scan means that there are two paths of rock; the first path consists of two straight lines, and the second path 
#   consists of three straight lines. (Specifically, the first path consists of a line of rock from 498,4 through 498,6 
#   and another line of rock from 498,6 through 496,6.)
#   
#   The sand is pouring into the cave from point 500,0.
#   
#   Drawing rock as #, air as ., and the source of the sand as +, this becomes:
#   
#   
#         4     5  5
#         9     0  0
#         4     0  3
#       0 ......+...
#       1 ..........
#       2 ..........
#       3 ..........
#       4 ....#...##
#       5 ....#...#.
#       6 ..###...#.
#       7 ........#.
#       8 ........#.
#       9 #########.
#   
#   Sand is produced one unit at a time, and the next unit of sand is not produced until the previous unit of sand comes 
#   to rest. A unit of sand is large enough to fill one tile of air in your scan.
#   
#   A unit of sand always falls down one step if possible. If the tile immediately below is blocked (by rock or sand), 
#   the unit of sand attempts to instead move diagonally one step down and to the left. If that tile is blocked, the unit 
#   of sand attempts to instead move diagonally one step down and to the right. Sand keeps moving as long as it is able to 
#   do so, at each step trying to move down, then down-left, then down-right. If all three possible destinations are 
#   blocked, the unit of sand comes to rest and no longer moves, at which point the next unit of sand is created back at the source.
#   
#   So, drawing sand that has come to rest as o, the first unit of sand simply falls straight down and then stops:
#   
#       ......+...
#       ..........
#       ..........
#       ..........
#       ....#...##
#       ....#...#.
#       ..###...#.
#       ........#.
#       ......o.#.
#       #########.
#   
#   The second unit of sand then falls straight down, lands on the first one, and then comes to rest to its left:
#   
#       ......+...
#       ..........
#       ..........
#       ..........
#       ....#...##
#       ....#...#.
#       ..###...#.
#       ........#.
#       .....oo.#.
#       #########.
#   
#   After a total of five units of sand have come to rest, they form this pattern:
#   
#       ......+...
#       ..........
#       ..........
#       ..........
#       ....#...##
#       ....#...#.
#       ..###...#.
#       ......o.#.
#       ....oooo#.
#       #########.
#   
#   After a total of 22 units of sand:
#   
#       ......+...
#       ..........
#       ......o...
#       .....ooo..
#       ....#ooo##
#       ....#ooo#.
#       ..###ooo#.
#       ....oooo#.
#       ...ooooo#.
#       #########.
#   
#   Finally, only two more units of sand can possibly come to rest:
#   
#       ......+...
#       ..........
#       ......o...
#       .....ooo..
#       ....#ooo##
#       ...o#ooo#.
#       ..###ooo#.
#       ....oooo#.
#       .o.ooooo#.
#       #########.
#   
#   Once all 24 units of sand shown above have come to rest, all further sand flows out the bottom, falling into the endless 
#   void. Just for fun, the path any new sand takes before falling forever is shown here with ~:
#   
#       .......+...
#       .......~...
#       ......~o...
#       .....~ooo..
#       ....~#ooo##
#       ...~o#ooo#.
#       ..~###ooo#.
#       ..~..oooo#.
#       .~o.ooooo#.
#       ~#########.
#       ~..........
#       ~..........
#       ~..........
#   
#   Using your scan, simulate the falling sand. How many units of sand come to rest before sand starts flowing into the abyss below?
#   
############################################################################ PROBLEM 1 ############################################################################


puzzle_day          = 14
sample_input_file_1 = "2022_{0:02d}_sample_1.txt".format(puzzle_day)
input_file          = "2022_{0:02d}_input.txt".format(puzzle_day)


def load_file(file_path):
    file_ptr = open(file_path, "r")
    data = file_ptr.read()
    file_ptr.close()
    return data

# cave constants
FLOOR = "#"
AIR = "."
SAND_ENTRY = "+"
SAND = "o"


class Cave:
    def __init__(self):
        self.cave = {}
        self.sand_source = None
        self.x_min = float('inf')
        self.x_max = float('-inf')
        self.y_min = float('inf')
        self.y_max = float('-inf')


    def get_cave_contents(self):
        cave_contents = ""
        for y in range(self.y_min, self.y_max+1):
            line = ""
            for x in range(self.x_min, self.x_max+1):
                if (x,y) in self.cave:
                    line += self.cave[(x,y)]
                else:
                    line += AIR

            cave_contents += line
            cave_contents += "\n"

        return cave_contents
        

    def add_sand_entry(self, entry_point):
        point = self.get_point(entry_point)

        self.cave[point] = "+"
        self.sand_source = point

        y = point[1]
        if y < self.y_min:
            self.y_min = y
        elif y > self.y_max:
            self.y_max = y


    def add_floor(self):
        # determine X end-points of the floor.
        # determine Y height of the floor.
        self.y_max += 2
        
        diff = (self.x_max - self.x_min) * 2
        floor_x_left = self.x_min - diff
        floor_x_right = self.x_max + diff

        floor_line = "{0},{1} -> {2},{3}".format(floor_x_left, self.y_max, floor_x_right, self.y_max)
        self.add_line(floor_line)


    # 503,4 -> 502,4 -> 502,9 -> 494,9
    def add_line(self, raw_line):
        points = raw_line.split(" -> ")

        # work with pairs of points
        for i in range(len(points) -1):
            start = self.get_point(points[i])
            end   = self.get_point(points[i+1])

            if start[0] == end[0]:
                self.add_vertical_line(start[0], start[1], end[1])

            else:
                self.add_horizonal_line(start[1], start[0], end[0])


    def get_point(self, point_string):
        parts = point_string.split(",")
        return (int(parts[0]), int(parts[1]))


    def add_vertical_line(self, x, y_start, y_end):
        ordered = sorted([y_start, y_end])
        for i in range(ordered[0], ordered[1] + 1):
            self.cave[(x, i)] = FLOOR

            if i < self.y_min:
                self.y_min = i
            elif i > self.y_max:
                self.y_max = i


    def add_horizonal_line(self, y, x_start, x_end):
        ordered = sorted([x_start, x_end])
        for i in range(ordered[0], ordered[1] + 1):
            self.cave[(i, y)] = FLOOR

            if i < self.x_min:
                self.x_min = i
            elif i > self.x_max:
                self.x_max = i

    # True - if the sand came to a rest
    # False - if the sand fell into the void
    def drop_sand(self):
        sand_grain_location = self.sand_source

        if self.cave[sand_grain_location] == SAND:
            return False

        while True:
            on_map, next_sand_point = self.find_next_falling_sand_point(sand_grain_location)

            # same grain fell off of the map
            if not on_map:
                # TODO - draw the grain path
                return False

            # sand can fall no further
            elif next_sand_point == sand_grain_location:
                self.cave[sand_grain_location] = SAND
                return True

            # grain can keep falling
            else:
                sand_grain_location = next_sand_point


    def find_next_falling_sand_point(self, current_point):

        # move down, then down-left, then down-right.
        
        # fell off the map
        if current_point[1] > self.y_max:
            return False, current_point

        # move down
        point_down = (current_point[0], current_point[1]+1)
        if point_down not in self.cave:
            return True, point_down

        # move down-left
        point_down_left = (current_point[0]-1, current_point[1]+1)
        if point_down_left not in self.cave:
            return True, point_down_left

        # move down-right
        point_down_right = (current_point[0]+1, current_point[1]+1)
        if point_down_right not in self.cave:
            return True, point_down_right

        # come to a rest
        return True, current_point

def init_cave(file):
    raw_cave = load_file(file)
    raw_cave_parts = raw_cave.split("\n")

    cave = Cave()
    for row in raw_cave_parts:
        cave.add_line(row)

    cave.add_sand_entry("500,0")
    return cave


def fill_cave(cave):
    sand_count = 0
    while cave.drop_sand():
        sand_count += 1

    return cave, sand_count


class Day14PartOneTests(unittest.TestCase):

    def test__p1__sample1(self):
        cave = init_cave(sample_input_file_1)
        cave, sand_count = fill_cave(cave)
        self.assertEqual( sand_count, 24)



    def test__p1__cave(self):
        cave = Cave()
        cave.add_line("503,4 -> 502,4 -> 502,9 -> 494,9")
        cave.add_line("498,4 -> 498,6 -> 496,6")
        cave.add_sand_entry("500,0")
        actual = cave.get_cave_contents()
        expected = "......+...\n..........\n..........\n..........\n....#...##\n....#...#.\n..###...#.\n........#.\n........#.\n#########.\n"
        self.assertEqual(actual, expected, "initial cave state is bad")


        cave.drop_sand() #1
        actual = cave.get_cave_contents()
        expected = "......+...\n..........\n..........\n..........\n....#...##\n....#...#.\n..###...#.\n........#.\n......o.#.\n#########.\n"
        self.assertEqual(actual, expected, "grain of sand # 1 - invalid state")

 
        cave.drop_sand() #2
        actual = cave.get_cave_contents()
        expected = "......+...\n..........\n..........\n..........\n....#...##\n....#...#.\n..###...#.\n........#.\n.....oo.#.\n#########.\n"
        self.assertEqual(actual, expected, "grain of sand # 2 - invalid state")


        cave.drop_sand() #3
        cave.drop_sand() #4
        cave.drop_sand() #5
        actual = cave.get_cave_contents()
        expected = "......+...\n..........\n..........\n..........\n....#...##\n....#...#.\n..###...#.\n......o.#.\n....oooo#.\n#########.\n"
        self.assertEqual(actual, expected, "grain of sand # 5 - invalid state")


        for i in range(6,23): #6 - #22
            cave.drop_sand()
        actual = cave.get_cave_contents()
        expected = "......+...\n..........\n......o...\n.....ooo..\n....#ooo##\n....#ooo#.\n..###ooo#.\n....oooo#.\n...ooooo#.\n#########.\n"
        self.assertEqual(actual, expected, "grain of sand # 22 - invalid state")


        cave.drop_sand() #23
        cave.drop_sand() #24
        actual = cave.get_cave_contents()
        expected = "......+...\n..........\n......o...\n.....ooo..\n....#ooo##\n...o#ooo#.\n..###ooo#.\n....oooo#.\n.o.ooooo#.\n#########.\n"
        self.assertEqual(actual, expected, "grain of sand # 24 - invalid state")


    
    def test__part_1__challenge_input(self):
        print("")
        cave = init_cave(input_file)
        cave, sand_count = fill_cave(cave)
        print("Solution to day {0} part 1: {1}".format(puzzle_day, sand_count))
        


###################################################################################################################################################################
#   --- Part Two ---
#   
#   You realize you misread the scan. There isn't an endless void at the bottom of the scan - there's floor, and you're standing on it!
#   
#   You don't have time to scan the floor, so assume the floor is an infinite horizontal line with a y coordinate equal to two 
#   plus the highest y coordinate of any point in your scan.
#   
#   In the example above, the highest y coordinate of any point is 9, and so the floor is at y=11. (This is as if your scan contained 
#       one extra rock path like -infinity,11 -> infinity,11.) With the added floor, the example above now looks like this:
#   
#           ...........+........
#           ....................
#           ....................
#           ....................
#           .........#...##.....
#           .........#...#......
#           .......###...#......
#           .............#......
#           .............#......
#           .....#########......
#           ....................
#   <-- etc #################### etc -->
#   
#   To find somewhere safe to stand, you'll need to simulate falling sand until a unit of sand comes to rest at 500,0, blocking the 
#   source entirely and stopping the flow of sand into the cave. In the example above, the situation finally looks like this after 93 units of sand come to rest:
#   
#       ............o............
#       ...........ooo...........
#       ..........ooooo..........
#       .........ooooooo.........
#       ........oo#ooo##o........
#       .......ooo#ooo#ooo.......
#       ......oo###ooo#oooo......
#       .....oooo.oooo#ooooo.....
#       ....oooooooooo#oooooo....
#       ...ooo#########ooooooo...
#       ..ooooo.......ooooooooo..
#       #########################
#   
#   Using your scan, simulate the falling sand until the source of the sand becomes blocked. How many units of sand come to rest?
#   
############################################################################ PROBLEM 2 ############################################################################



class Day14PartTwoTests(unittest.TestCase):
    
    def test__p2__sample1(self):
        cave = init_cave(sample_input_file_1)
        cave.add_floor()
        cave, sand_count = fill_cave(cave)
        self.assertEqual( sand_count, 93)

        

    def test__part_2__challenge_input(self):
        print("")
        cave = init_cave(input_file)
        cave.add_floor()
        print(cave.get_cave_contents())
        cave, sand_count = fill_cave(cave)

        print(cave.get_cave_contents())

        print("Solution to day {0} part 2: {1}".format(puzzle_day, sand_count))


 
###################################################################################################################################################################
########################################################################## RUN THE TESTS ##########################################################################


# run then unit tests "last"
if __name__ == '__main__':
    unittest.main()
 

