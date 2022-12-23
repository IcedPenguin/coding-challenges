#!/bin/python
# -*- coding: utf-8 -*-
# https://adventofcode.com/2022/day/11


###################################################################################################################################################################
#  
#  Solution to part 1: 54752
#
#  Solution to part 2: 13606755504
#
###################################################################################################################################################################

import unittest

###################################################################################################################################################################

############################################################################ PROBLEM 1 ############################################################################


puzzle_day          = 11
sample_input_file_1 = "2022_{0:02d}_sample_1.txt".format(puzzle_day)
input_file          = "2022_{0:02d}_input.txt".format(puzzle_day)


def load_file(file_path):
    file_ptr = open(file_path, "r")
    data = file_ptr.read()
    file_ptr.close()
    return data



class Monkey:
    def __init__(self, items, operation, test_value, monkey_list, monkey_true, monkey_false, divider=None, worry_level_reducer=3):
        self.items = [int(x) for x in items.split(", ")]
        self.inspected_item_count = 0

        parts = operation.split(" ")
        self.operation_left   = parts[0]
        self.operation        = parts[1]
        self.operation_right  = parts[2]

        self.test_value = test_value
        self.monkey_list = monkey_list
        self.monkey_true = monkey_true
        self.monkey_false = monkey_false

        self.divider = divider
        self.worry_level_reducer = worry_level_reducer

    def set_divider(self, divider):
        self.divider = divider

    def take_turn(self):
        while len(self.items) > 0:
            item = self.items.pop(0)

            item_post_inspection = self.inspect_item(item)
            item_post_relief = self.feel_relief(item_post_inspection)  
            self.test_worry_level(item_post_relief)



    def inspect_item(self, item):
        self.inspected_item_count += 1

        result = 1

        if self.operation_left == "old":
            left = item
        else:
            left = int(self.operation_left)


        if self.operation_right == "old":
            right = item
        else:
            right = int(self.operation_right)


        if self.operation == "*":
            result =  left * right

        elif self.operation == "+":
            result =  left + right

        else: # 
            print("unreachable, unknown operation")
            return -10000

        if self.divider is None:   
            return result

        else:
            return result % self.divider
        # return result


    def feel_relief(self, item):
        return item // self.worry_level_reducer # your worry level to be divided by three and rounded down to the nearest integer



    def test_worry_level(self, item):

        if item % self.test_value == 0:
            self.monkey_list[self.monkey_true].catch_item(item)

        else:
            self.monkey_list[self.monkey_false].catch_item(item)


    def catch_item(self, item):
        self.items.append(item)


def process_monkey_list(lines, worry_level_reducer=3):
    monkey_list = []

    # temp variables
    monkey_line_count = 0
    tmp_items = None
    tmp_operation = None
    tmp_test = None
    tmp_true = None
    tmp_false = None


    while len(lines) > 0:
        line = lines.pop(0)


        # reached end of monkey block
        if line == "":
            monkey = Monkey(tmp_items, tmp_operation, tmp_test, monkey_list, tmp_true, tmp_false, worry_level_reducer=worry_level_reducer)
            monkey_list.append(monkey)
            monkey_line_count = 0

        elif monkey_line_count == 0:
            monkey_line_count += 1

        elif monkey_line_count == 1:
            tmp_items = line[18:]
            monkey_line_count += 1

        elif monkey_line_count == 2:
            tmp_operation = line[19:]
            monkey_line_count += 1

        elif monkey_line_count == 3:
            parts = line.split(" ")
            tmp_test = int(parts[5])
            monkey_line_count += 1

        elif monkey_line_count == 4:
            parts = line.split(" ")
            tmp_true = int(parts[9])
            monkey_line_count += 1

        elif monkey_line_count == 5:
            parts = line.split(" ")
            tmp_false = int(parts[9])
            monkey_line_count += 1

    return monkey_list


def play_round(monkey_list, verbose=False):
    
    if verbose:
        print("before")
        for i in range(len(monkey_list)):
            print("Monkey {0}: {1}".format(i, monkey_list[i].items))

    # move all items
    for monkey in monkey_list:
        monkey.take_turn()

    
    if verbose:
        print("after")
        for i in range(len(monkey_list)):
            print("Monkey {0}: {1}".format(i, monkey_list[i].items))

        print("--------")



def play_rounds(monkey_list, rounds):
    for i in range(rounds):
        # if i % 100 == 0:
        #     print("round {0}".format(i))
        play_round(monkey_list)


def get_monkey_business_level(monkey_list):
    levels = []
    for monkey in monkey_list:
        levels.append(monkey.inspected_item_count)

    sorted_inspections = sorted(levels)
    return sorted_inspections[-1] * sorted_inspections[-2]


class Day11PartOneTests(unittest.TestCase):

    def test__p1__monkey_inspect(self):
        monkey_list = []
        monkey = Monkey("79, 98", "old * 19", 23, monkey_list, 2, 3)

        result = monkey.inspect_item(40)
        self.assertEqual(result, 40*19)

        result = monkey.feel_relief(40)
        self.assertEqual(result, 13)


    def test__p1__sample1(self):
        raw_monkeys = load_file(sample_input_file_1)
        monkey_list = process_monkey_list(raw_monkeys.split("\n"))
        play_rounds(monkey_list, 20)
        monkey_business_level = get_monkey_business_level(monkey_list)
        self.assertEqual(monkey_business_level, 10605)

    
    def test__part_1__challenge_input(self):
        print("")
        raw_monkeys = load_file(input_file)
        monkey_list = process_monkey_list(raw_monkeys.split("\n"))
        play_rounds(monkey_list, 20)
        monkey_business_level = get_monkey_business_level(monkey_list)

        self.assertEqual(monkey_business_level, 54752)
        print("Solution to day {0} part 1: {1}".format(puzzle_day, monkey_business_level))
        


###################################################################################################################################################################

############################################################################ PROBLEM 2 ############################################################################

from math import gcd




def find_common_monkey_divisor(monkey_list):
    base = []
    for monkey in monkey_list:
        base.append(monkey.test_value)

    product = 1
    for i in base:
        product *= i

    for monkey in monkey_list:
        monkey.set_divider(product)



class Day11PartTwoTests(unittest.TestCase):
        
    def test__part_2__challenge_input(self):
        print("")
        raw_monkeys = load_file(input_file)
        monkey_list = process_monkey_list(raw_monkeys.split("\n"), 1)
        find_common_monkey_divisor(monkey_list)
        play_rounds(monkey_list, 10000)
        monkey_business_level = get_monkey_business_level(monkey_list)

        print("Solution to day {0} part 2: {1}".format(puzzle_day, monkey_business_level))

 
###################################################################################################################################################################
########################################################################## RUN THE TESTS ##########################################################################


# run then unit tests "last"
if __name__ == '__main__':
    unittest.main()
 

