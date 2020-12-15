#!/bin/python
# -*- coding: utf-8 -*-
# https://adventofcode.com/2020/day/11


###################################################################################################################################################################
#  
#  Solution to day 11 part 1: 2316
#
#  Solution to day 11 part 2: 2128
#
###################################################################################################################################################################


###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################
#   
#   --- Day 11: Seating System ---
#   Your plane lands with plenty of time to spare. The final leg of your journey is a ferry 
#   that goes directly to the tropical island where you can finally start your vacation. As 
#   you reach the waiting area to board the ferry, you realize you're so early, nobody else 
#   has even arrived yet!
#   
#   By modeling the process people use to choose (or abandon) their seat in the waiting area, 
#   you're pretty sure you can predict the best place to sit. You make a quick map of the seat 
#   layout (your puzzle input).
#   
#   The seat layout fits neatly on a grid. Each position is either floor (.), an empty 
#   seat (L), or an occupied seat (#). For example, the initial seat layout might look like this:
#   
#       L.LL.LL.LL
#       LLLLLLL.LL
#       L.L.L..L..
#       LLLL.LL.LL
#       L.LL.LL.LL
#       L.LLLLL.LL
#       ..L.L.....
#       LLLLLLLLLL
#       L.LLLLLL.L
#       L.LLLLL.LL
#   
#   Now, you just need to model the people who will be arriving shortly. Fortunately, people are 
#   entirely predictable and always follow a simple set of rules. All decisions are based on the 
#   number of occupied seats adjacent to a given seat (one of the eight positions immediately up, 
#   down, left, right, or diagonal from the seat). The following rules are applied to every 
#   seat simultaneously:
#   
#       *   If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
#       *   If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
#       *   Otherwise, the seat's state does not change.
#   
#   Floor (.) never changes; seats don't move, and nobody sits on the floor.
#   
#   After one round of these rules, every seat in the example layout becomes occupied:
#   
#       #.##.##.##
#       #######.##
#       #.#.#..#..
#       ####.##.##
#       #.##.##.##
#       #.#####.##
#       ..#.#.....
#       ##########
#       #.######.#
#       #.#####.##
#   
#   After a second round, the seats with four or more occupied adjacent seats become empty again:
#   
#       #.LL.L#.##
#       #LLLLLL.L#
#       L.L.L..L..
#       #LLL.LL.L#
#       #.LL.LL.LL
#       #.LLLL#.##
#       ..L.L.....
#       #LLLLLLLL#
#       #.LLLLLL.L
#       #.#LLLL.##
#   
#   This process continues for three more rounds:
#   
#       #.##.L#.##
#       #L###LL.L#
#       L.#.#..#..
#       #L##.##.L#
#       #.##.LL.LL
#       #.###L#.##
#       ..#.#.....
#       #L######L#
#       #.LL###L.L
#       #.#L###.##
#       #.#L.L#.##
#       #LLL#LL.L#
#       L.L.L..#..
#       #LLL.##.L#
#       #.LL.LL.LL
#       #.LL#L#.##
#       ..L.L.....
#       #L#LLLL#L#
#       #.LLLLLL.L
#       #.#L#L#.##
#       #.#L.L#.##
#       #LLL#LL.L#
#       L.#.L..#..
#       #L##.##.L#
#       #.#L.LL.LL
#       #.#L#L#.##
#       ..L.L.....
#       #L#L##L#L#
#       #.LLLLLL.L
#       #.#L#L#.##
#   
#   At this point, something interesting happens: the chaos stabilizes and further applications of 
#   these rules cause no seats to change state! Once people stop moving around, you count 37 occupied seats.
#   
#   Simulate your seating area by applying the seating rules repeatedly until no seats change 
#   state. How many seats end up occupied?
#   

def test_equal(actual, expected, message):
    if actual != expected:
        print("FAIL: Found={0}  Expected={1}    {2}".format(actual, expected, message))


sample_input_file_1 = "2020_11_sample_1.txt"
sample_input_file_2 = "2020_11_sample_2.txt"
input_file          = "2020_11_input.txt"


EMPTY = "L"
OCCUPIED = "#"
FLOOR = "."


class Grid:
    def __init__(self, matrix=None, source_grid=None, width=None, height=None):
        if source_grid is not None:
            self.grid = source_grid
            self.width = width
            self.height = height

        else:
            self.grid = []

            for row in matrix:
                self.grid.append(list(row))

            self.height = len(self.grid)
            self.width = len(self.grid[0]) # assumes atleast one row
    ### __init__
        

    def deep_copy(self):
        result = []

        for row in self.grid:
            result.append(row.copy())

        return Grid(source_grid=result, width=self.width, height=self.height)
    ### copy


    def get_point_value(self, x, y):
        if 0 <= y and y < len(self.grid):
            row = self.grid[y]

            if 0 <= x and x < len(row):
                return row[x]

        return None
    ### get_point_value


    def set_point_value(self, x, y, value):
        if 0 <= y and y < len(self.grid):
            row = self.grid[y]

            if 0 <= x and x < len(row):
                row[x] = value
                return True

        return False
    ### set_point_value


    def get_list_of_adjacent_values(self, x, y):
        result = []
        result.append( self.get_point_value(x-1, y-1) )
        result.append( self.get_point_value(x-1, y  ) )
        result.append( self.get_point_value(x-1, y+1) )
        result.append( self.get_point_value(x  , y-1) )
        # ignore center cell. not adjacent to itself
        result.append( self.get_point_value(x  , y+1) )
        result.append( self.get_point_value(x+1, y-1) )
        result.append( self.get_point_value(x+1, y  ) )
        result.append( self.get_point_value(x+1, y+1) )

        result = list(filter(lambda a: a != None, result))
        return result

    ### get_list_of_adjacent_values


    # added to support part 2
    def get_list_of_adjacent_values_ignoring_empty_seats(self, x, y):

        result = []

        directions = [(-1, -1), (-1, 0), (-1, 1), 
                      ( 0, -1),          ( 0, 1), 
                      ( 1, -1), ( 1, 0), ( 1, 1)]

        for direction in directions:
            x_test = x
            y_test = y

            done = False
            while not done:
                x_test += direction[0]
                y_test += direction[1]
                tile    = self.get_point_value(x_test, y_test)


                if tile is None:
                    # we fell off of the map.
                    done = True

                elif tile is FLOOR:
                    # still looking at floor, keep going
                    continue

                else:
                    done = True

                result.append(tile)
                # print("searching: x={0} y={1} \tdir={5} \tx_t={2} \ty_t={3} \ttile={4}".format(x, y, x_test, y_test, tile, direction))



        result = list(filter(lambda a: a != None, result))
        return result

    ### get_list_of_adjacent_values



    def __str__(self):
        result = ""
        for row in self.grid:
            result += "".join(row)
            result += "\n"

        return result
    ### __str__

    # https://stackoverflow.com/questions/390250/elegant-ways-to-support-equivalence-equality-in-python-classes
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

##### Grid





def apply_part_1_rules(original_grid):
    updated_grid = original_grid.deep_copy()

    for x in range(original_grid.width):
        for y in range(original_grid.height):
            value = original_grid.get_point_value(x, y)
            adjacent_cells = original_grid.get_list_of_adjacent_values(x, y)

            if value == EMPTY and adjacent_cells.count(OCCUPIED) == 0:
                updated_grid.set_point_value(x, y, OCCUPIED)

            elif value == OCCUPIED and adjacent_cells.count(OCCUPIED) >= 4:
                updated_grid.set_point_value(x, y, EMPTY)  

    return updated_grid      
### apply_part_1_rules


def apply_part_2_rules(original_grid):
    updated_grid = original_grid.deep_copy()

    for x in range(original_grid.width):
        for y in range(original_grid.height):
            value = original_grid.get_point_value(x, y)
            adjacent_cells = original_grid.get_list_of_adjacent_values_ignoring_empty_seats(x, y)

            if value == EMPTY and adjacent_cells.count(OCCUPIED) == 0:
                updated_grid.set_point_value(x, y, OCCUPIED)

            elif value == OCCUPIED and adjacent_cells.count(OCCUPIED) >= 5:
                updated_grid.set_point_value(x, y, EMPTY)  

    return updated_grid      
### apply_part_2_rules




def loop_until_seats_stabilize(grid, rules_to_apply):
    stable = False
    iteration_count = 0

    while not stable:
        updated_grid = rules_to_apply(grid)

        if updated_grid == grid:
            grid_string = grid.__str__()
            occupied_seats = grid_string.count(OCCUPIED)
            print("stable arangement found. steps={0} \toccupied_seats={1}".format(iteration_count, occupied_seats))
            print(grid_string)
            stable = True

        else:
            iteration_count += 1
            # print(updated_grid)
            grid = updated_grid

    return occupied_seats
### loop_until_seats_stabilize


def read_seating_layout_file(file_name):
    seating_layout = []

    with open(file_name) as f:
        for line in f:
            seating_layout.append(line.strip())

    return seating_layout
### read_seating_layout_file


print("--- P1 sample input ---")
# test_matrix = ["1234", "5678", "abcd"]
# test_grid = Grid(matrix=test_matrix)
# print(test_grid)
# print( test_grid.get_point_value(0,0) )
# print( test_grid.get_point_value(0,1) )
# test_grid_2 = test_grid.deep_copy()
# print(test_grid == test_grid_2)

# print( test_grid.set_point_value(0,1, "Q") )
# print( test_grid.get_point_value(0,1) )
# print( test_grid.get_point_value(0,2) )

# print(test_grid == test_grid_2)

# print("\n")
# print(test_grid)
# print("\n")
# print(test_grid_2)

print("~~ Testing sample input 1 ~~")
sample_seating_layout = read_seating_layout_file(sample_input_file_1)
sample_1_grid = Grid(matrix=sample_seating_layout)
loop_until_seats_stabilize(sample_1_grid, apply_part_1_rules)




print("-------------------------")


seating_layout = read_seating_layout_file(input_file)
grid = Grid(matrix=seating_layout)
occupied_seats = loop_until_seats_stabilize(grid, apply_part_1_rules)
occupied_seats = 2316


print("Solution to day 11 part 1: {0}".format(occupied_seats))


###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################
#   
#   --- Part Two ---
#   As soon as people start to arrive, you realize your mistake. People don't just care about adjacent 
#   seats - they care about the first seat they can see in each of those eight directions!
#   
#   Now, instead of considering just the eight immediately adjacent seats, consider the first seat in 
#   each of those eight directions. For example, the empty seat below would see eight occupied seats:
#   
#       .......#.
#       ...#.....
#       .#.......
#       .........
#       ..#L....#
#       ....#....
#       .........
#       #........
#       ...#.....
#   
#   The leftmost empty seat below would only see one empty seat, but cannot see any of the occupied ones:
#   
#       .............
#       .L.L.#.#.#.#.
#       .............
#   
#   The empty seat below would see no occupied seats:
#   
#       .##.##.
#       #.#.#.#
#       ##...##
#       ...L...
#       ##...##
#       #.#.#.#
#       .##.##.
#   
#   Also, people seem to be more tolerant than you expected: it now takes five or more visible occupied 
#   seats for an occupied seat to become empty (rather than four or more from the previous rules). The 
#   other rules still apply: empty seats that see no occupied seats become occupied, seats matching no 
#   rule don't change, and floor never changes.
#   
#   Given the same starting layout as above, these new rules cause the seating area to shift around as follows:
#   
#       L.LL.LL.LL
#       LLLLLLL.LL
#       L.L.L..L..
#       LLLL.LL.LL
#       L.LL.LL.LL
#       L.LLLLL.LL
#       ..L.L.....
#       LLLLLLLLLL
#       L.LLLLLL.L
#       L.LLLLL.LL
#
#       #.##.##.##
#       #######.##
#       #.#.#..#..
#       ####.##.##
#       #.##.##.##
#       #.#####.##
#       ..#.#.....
#       ##########
#       #.######.#
#       #.#####.##
#
#       #.LL.LL.L#
#       #LLLLLL.LL
#       L.L.L..L..
#       LLLL.LL.LL
#       L.LL.LL.LL
#       L.LLLLL.LL
#       ..L.L.....
#       LLLLLLLLL#
#       #.LLLLLL.L
#       #.LLLLL.L#
#
#       #.L#.##.L#
#       #L#####.LL
#       L.#.#..#..
#       ##L#.##.##
#       #.##.#L.##
#       #.#####.#L
#       ..#.#.....
#       LLL####LL#
#       #.L#####.L
#       #.L####.L#
#
#       #.L#.L#.L#
#       #LLLLLL.LL
#       L.L.L..#..
#       ##LL.LL.L#
#       L.LL.LL.L#
#       #.LLLLL.LL
#       ..L.L.....
#       LLLLLLLLL#
#       #.LLLLL#.L
#       #.L#LL#.L#
#
#       #.L#.L#.L#
#       #LLLLLL.LL
#       L.L.L..#..
#       ##L#.#L.L#
#       L.L#.#L.L#
#       #.L####.LL
#       ..#.#.....
#       LLL###LLL#
#       #.LLLLL#.L
#       #.L#LL#.L#
# 
#       #.L#.L#.L#
#       #LLLLLL.LL
#       L.L.L..#..
#       ##L#.#L.L#
#       L.L#.LL.L#
#       #.LLLL#.LL
#       ..#.L.....
#       LLL###LLL#
#       #.LLLLL#.L
#       #.L#LL#.L#
#   
#   Again, at this point, people stop shifting around and the seating area reaches equilibrium. 
#   Once this occurs, you count 26 occupied seats.
#   
#   Given the new visibility method and the rule change for occupied seats becoming empty, once 
#   equilibrium is reached, how many seats end up occupied?
#   



print("--- P2 sample input ---")
# test_matrix_2 = [".............", ".L.L.#.#.#.#.", "............."]
# test_grid_2 = Grid(matrix=test_matrix_2)
# print(test_grid_2)

# print( test_grid_2.get_point_value(1,1) )
# print( test_grid_2.get_list_of_adjacent_values_ignoring_empty_seats(1,1) )

# print( test_grid_2.get_point_value(3,1) )
# print( test_grid_2.get_list_of_adjacent_values_ignoring_empty_seats(3,1) )


print("~~ Testing sample input 1 ~~")
sample_seating_layout = read_seating_layout_file(sample_input_file_1)
sample_1_grid = Grid(matrix=sample_seating_layout)
occupied_seats = loop_until_seats_stabilize(sample_1_grid, apply_part_2_rules)
test_equal(occupied_seats, 26, "P1 seat count wrong")

print("-------------------------")


seating_layout = read_seating_layout_file(input_file)
grid = Grid(matrix=seating_layout)
occupied_seats = loop_until_seats_stabilize(grid, apply_part_2_rules)

print("Solution to day 11 part 2: {0}".format(occupied_seats))

 