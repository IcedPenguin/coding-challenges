#!/bin/python
# -*- coding: utf-8 -*-
# https://adventofcode.com/2022/day/5


###################################################################################################################################################################
#  
#  Solution to part 1: VWLCWGSDQ
#
#  Solution to part 2: TCGLQSLPW
#
###################################################################################################################################################################

import unittest
import re

###################################################################################################################################################################
#   --- Day 5: Supply Stacks ---
#   
#   The expedition can depart as soon as the final supplies have been unloaded from the ships. Supplies are stored in stacks 
#   of marked crates, but because the needed supplies are buried under many other crates, the crates need to be rearranged.
#   
#   The ship has a giant cargo crane capable of moving crates between stacks. To ensure none of the crates get crushed or fall 
#   over, the crane operator will rearrange them in a series of carefully-planned steps. After the crates are rearranged, the 
#   desired crates will be at the top of each stack.
#   
#   The Elves don't want to interrupt the crane operator during this delicate procedure, but they forgot to ask her which crate 
#   will end up where, and they want to be ready to unload them as soon as possible so they can embark.
#   
#   They do, however, have a drawing of the starting stacks of crates and the rearrangement procedure (your puzzle input). For example:
#   
#           [D]    
#       [N] [C]    
#       [Z] [M] [P]
#        1   2   3 
#   
#       move 1 from 2 to 1
#       move 3 from 1 to 3
#       move 2 from 2 to 1
#       move 1 from 1 to 2
#   
#   In this example, there are three stacks of crates. Stack 1 contains two crates: crate Z is on the bottom, and crate N is 
#   on top. Stack 2 contains three crates; from bottom to top, they are crates M, C, and D. Finally, stack 3 contains a single crate, P.
#   
#   Then, the rearrangement procedure is given. In each step of the procedure, a quantity of crates is moved from one 
#   stack to a different stack. In the first step of the above rearrangement procedure, one crate is moved from 
#   stack 2 to stack 1, resulting in this configuration:
#   
#       [D]        
#       [N] [C]    
#       [Z] [M] [P]
#        1   2   3 
#   
#   In the second step, three crates are moved from stack 1 to stack 3. Crates are moved one at a time, so the first 
#   crate to be moved (D) ends up below the second and third crates:
#   
#               [Z]
#               [N]
#           [C] [D]
#           [M] [P]
#        1   2   3
#   
#   Then, both crates are moved from stack 2 to stack 1. Again, because crates are moved one at a time, crate C ends up below crate M:
#   
#               [Z]
#               [N]
#       [M]     [D]
#       [C]     [P]
#        1   2   3
#   
#   Finally, one crate is moved from stack 1 to stack 2:
#   
#               [Z]
#               [N]
#               [D]
#       [C] [M] [P]
#        1   2   3
#   
#   The Elves just need to know which crate will end up on top of each stack; in this example, the top crates are C in 
#   stack 1, M in stack 2, and Z in stack 3, so you should combine these together and give the Elves the message CMZ.
#   
#   After the rearrangement procedure completes, what crate ends up on top of each stack?
#   
############################################################################ PROBLEM 1 ############################################################################


puzzle_day          = 5
sample_input_file_1 = "2022_{0:02d}_sample_1.txt".format(puzzle_day)
input_file          = "2022_{0:02d}_input.txt".format(puzzle_day)


def load_file(file_path):
    file_ptr = open(file_path, "r")
    data = file_ptr.read()
    file_ptr.close()
    return data


def load_stacks_and_commands(lines):
    stacks = {}

    while len(lines) > 0 and "[" in lines[0]:
        line = lines.pop(0)

        for match in re.finditer('\[', line):
            idx = match.start()
            stack_id = idx//4 +1
            crate_id = line[idx +1]

            if stack_id in stacks:
                stacks[stack_id].append(crate_id)
            else:
                stacks[stack_id] = [crate_id]

    lines.pop(0)
    lines.pop(0)

    commands = []
    while(len(lines) > 0):
        line = lines.pop(0)
        commands.append(parse_command(line))

    return stacks, commands


"move 1 from 2 to 1"
def parse_command(commad):
    parts = commad.split()
    return {
        "cmd":parts[0],
        "amount": int(parts[1]),
        "from": int(parts[3]),
        "to": int(parts[5])
    }

def execute_move(stacks, amount, source, destination):
    for i in range(amount):
        crate = stacks[source].pop(0)
        stacks[destination].insert(0, crate)
    return stacks

def execute_commands(stacks, commands, move_cmd=execute_move):
    for command in commands:
        if command["cmd"] == "move":
            # for i in range(command["amount"]):
            move_cmd(stacks, command["amount"], command["from"], command["to"])


    
def get_top_items(stacks):
    top_crates = ""
    stack_ids = sorted(stacks.keys())
    for stack_id in stack_ids:
        top_crates += stacks[stack_id][0]

    return top_crates


class Day5PartOneTests(unittest.TestCase):

    def test__p1__load_stacks(self):

        stacks_cmds = ["    [D]    ",
                       "[N] [C]    ",
                       "[Z] [M] [P]",
                    "",
                    "move 1 from 2 to 1"
        ]
        load_stacks_and_commands(stacks_cmds)


    def test__p1__parse_command(self):
        self.assertEqual(parse_command("move 1 from 2 to 1"),{"cmd":"move", "amount": 1, "from":2, "to": 1})
        self.assertEqual(parse_command("eat 11 from 55 to 3"),{"cmd":"eat", "amount": 11, "from":55, "to": 3})


    def test__p1__execute_move(self):
        self.assertEqual(execute_move({1:['a'],2:[]},1,1,2),{1:[],2:['a']})
        self.assertEqual(execute_move({1:['a','b'],2:['c']},1,1,2),{1:['b'],2:['a','c']})

    def test__p1__sample1(self):
        lines = load_file(sample_input_file_1).split("\n")
        stacks, commands = load_stacks_and_commands(lines)
        execute_commands(stacks, commands)
        items = get_top_items(stacks)
        self.assertEqual(items,"CMZ")


    
    def test__part_1__challenge_input(self):
        print("")
        lines = load_file(input_file).split("\n")
        stacks, commands = load_stacks_and_commands(lines)
        execute_commands(stacks, commands)
        items = get_top_items(stacks)
        print("Solution to day {0} part 1: {1}".format(puzzle_day, items))
        


###################################################################################################################################################################
#   --- Part Two ---
#   
#   As you watch the crane operator expertly rearrange the crates, you notice the process isn't following your prediction.
#   
#   Some mud was covering the writing on the side of the crane, and you quickly wipe it away. The crane isn't a CrateMover 
#   9000 - it's a CrateMover 9001.
#   
#   The CrateMover 9001 is notable for many new and exciting features: air conditioning, leather seats, an extra cup holder, 
#   and the ability to pick up and move multiple crates at once.
#   
#   Again considering the example above, the crates begin in the same configuration:
#   
#           [D]    
#       [N] [C]    
#       [Z] [M] [P]
#        1   2   3 
#   
#   Moving a single crate from stack 2 to stack 1 behaves the same as before:
#   
#       [D]        
#       [N] [C]    
#       [Z] [M] [P]
#        1   2   3 
#   
#   However, the action of moving three crates from stack 1 to stack 3 means that those three moved crates stay in the same 
#   order, resulting in this new configuration:
#   
#               [D]
#               [N]
#           [C] [Z]
#           [M] [P]
#        1   2   3
#   
#   Next, as both crates are moved from stack 2 to stack 1, they retain their order as well:
#   
#               [D]
#               [N]
#       [C]     [Z]
#       [M]     [P]
#        1   2   3
#   
#   Finally, a single crate is still moved from stack 1 to stack 2, but now it's crate C that gets moved:
#   
#               [D]
#               [N]
#               [Z]
#       [M] [C] [P]
#        1   2   3
#   
#   In this example, the CrateMover 9001 has put the crates in a totally different order: MCD.
#   
#   Before the rearrangement process finishes, update your simulation so that the Elves know where they should stand to be 
#   ready to unload the final supplies. After the rearrangement procedure completes, what crate ends up on top of each stack?
#   
############################################################################ PROBLEM 2 ############################################################################

def execute_move_CrateMover9001(stacks, amount, source, destination):
    
    # -- remove from N items from old stack. 
    # -- add to front of new stack, in same order. 
    # -- looks like list slicing

    crates = stacks[source][:amount] 
    stacks[source] = stacks[source][amount:]
    stacks[destination] = crates + stacks[destination]
    return stacks

class Day5PartTwoTests(unittest.TestCase):
    
    def test__p2__sample1(self):
        lines = load_file(sample_input_file_1).split("\n")
        stacks, commands = load_stacks_and_commands(lines)
        execute_commands(stacks, commands, execute_move_CrateMover9001)
        items = get_top_items(stacks)
        self.assertEqual(items,"MCD")
        

    def test__part_2__challenge_input(self):
        print("")
        lines = load_file(input_file).split("\n")
        stacks, commands = load_stacks_and_commands(lines)
        execute_commands(stacks, commands, execute_move_CrateMover9001)
        items = get_top_items(stacks)
        print("Solution to day {0} part 2: {1}".format(puzzle_day, items))


 
###################################################################################################################################################################
########################################################################## RUN THE TESTS ##########################################################################


# run then unit tests "last"
if __name__ == '__main__':
    unittest.main()
 

