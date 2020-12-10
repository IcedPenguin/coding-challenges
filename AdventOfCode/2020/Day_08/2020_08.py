#!/bin/python
# -*- coding: utf-8 -*-
# https://adventofcode.com/2020/day/8


###################################################################################################################################################################
#  
#  Solution to day 8 part 1: 1654
#
#  Solution to day 8 part 2: 833
#
###################################################################################################################################################################


###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################
#   
#   --- Day 8: Handheld Halting ---
#   Your flight to the major airline hub reaches cruising altitude without incident. While you consider 
#   checking the in-flight menu for one of those drinks that come with a little umbrella, you are 
#   interrupted by the kid sitting next to you.
#   
#   Their handheld game console won't turn on! They ask if you can take a look.
#   
#   You narrow the problem down to a strange infinite loop in the boot code (your puzzle input) of 
#   the device. You should be able to fix it, but first you need to be able to run the code in isolation.
#   
#   The boot code is represented as a text file with one instruction per line of text. Each instruction 
#   consists of an operation (acc, jmp, or nop) and an argument (a signed number like +4 or -20).
#   
#       acc     increases or decreases a single global value called the accumulator by the value given in the 
#               argument. For example, acc +7 would increase the accumulator by 7. The accumulator starts at 0. 
#   
#   After an acc instruction, the instruction immediately below it is executed next.
#   
#       jmp     jumps to a new instruction relative to itself. The next instruction to execute is found 
#               using the argument as an offset from the jmp instruction; for example, jmp +2 would skip 
#               the next instruction, jmp +1 would continue to the instruction immediately below it, and 
#               jmp -20 would cause the instruction 20 lines above to be executed next.
#       nop     stands for No OPeration - it does nothing. The instruction immediately below it is executed next.
#   
#   For example, consider the following program:
#   
#       nop +0
#       acc +1
#       jmp +4
#       acc +3
#       jmp -3
#       acc -99
#       acc +1
#       jmp -4
#       acc +6
#   
#   These instructions are visited in this order:
#   
#       nop +0  | 1
#       acc +1  | 2, 8(!)
#       jmp +4  | 3
#       acc +3  | 6
#       jmp -3  | 7
#       acc -99 |
#       acc +1  | 4
#       jmp -4  | 5
#       acc +6  |
#   
#   First, the nop +0 does nothing. Then, the accumulator is increased from 0 to 1 (acc +1) 
#   and jmp +4 sets the next instruction to the other acc +1 near the bottom. After it 
#   increases the accumulator from 1 to 2, jmp -4 executes, setting the next instruction 
#   to the only acc +3. It sets the accumulator to 5, and jmp -3 causes the program to 
#   continue back at the first acc +1.
#   
#   This is an infinite loop: with this sequence of jumps, the program will run forever. The 
#   moment the program tries to run any instruction a second time, you know it will never terminate.
#   
#   Immediately before the program would run an instruction a second time, the value in the 
#   accumulator is 5.
#   
#   Run your copy of the boot code. Immediately before any instruction is executed a second 
#   time, what value is in the accumulator?
#   

def test_equal(actual, expected, message):
    if actual != expected:
        print("FAIL: Found={0}  Expected={1}    {2}".format(actual, expected, message))


sample_input_file   = "2020_08_sample.txt"
input_file          = "2020_08_input.txt"


class GameConsole:
    def __init__(self, instruction_file):
        self.instruction_file = instruction_file
        self.pointer = 0
        self.accumulator = 0
        self.instructions = None


    def load_instructions(self):
        # reset the program
        self.instructions = {}
        counter = 0

        # read in the instruction file, line by line
        with open(self.instruction_file) as f:
            for line in f:
                line = line.strip()

                if "nop" in line:
                    self.instructions[counter] = ("nop", int(line[4:]))

                elif "acc" in line:
                    self.instructions[counter] = ("acc", int(line[4:]))

                elif "jmp" in line:
                    self.instructions[counter] = ("jmp", int(line[4:]))

                else:
                    # unknown instruction, skip.
                    print("Unknown instruction!!! {0}".format(line))
                    continue
                    
                counter += 1
    ### load_instructions


    def find_infinite_loop(self, instructions=None):
        # assumption: input will not be "broken". guaranteed there will be an infinite loop to find.
        if instructions is None:
            mut_instructions = self.instructions.copy()
        else: 
            mut_instructions = instructions

        s = len(mut_instructions.keys())
        pointer = 0
        accumulator = 0

        complete = False

        while not complete:
            if pointer >= len(mut_instructions):
                # print("no infinite loop found!")
                return False, accumulator

            # print("size={0}\tprt={1}".format(s, pointer))
            operation = mut_instructions[pointer]
            # print("next: prt={0}\tacc={1}\toper={2}".format(pointer, accumulator, operation))

            if operation is None:
                #infinite loop has been found.
                return True, accumulator
            
            else:
                mut_instructions[pointer] = None

                if operation[0] == "nop":
                    pointer += 1

                elif operation[0] == "acc":
                    pointer += 1
                    accumulator += operation[1]

                elif operation[0] == "jmp":
                    pointer += operation[1]

    ### find_infinite_loop

    # Added for Part 2 solution, with some minor modifications to find_infinite_loop()
    def find_corrupt_instruction(self):
        # brute force the solution. walk through all instructions. substituting one at a time until it works.
        for i in range(len(self.instructions)):
            new_operation = None
            operation = self.instructions[i]

            if operation[0] == "nop":
                new_operation = ("jmp", operation[1])
                
            elif operation[0] == "jmp":
                new_operation = ("nop", operation[1])
                
            if new_operation is not None:
                mut_instructions = self.instructions.copy()
                mut_instructions[i] = new_operation

                # print("substitution instruction found: idx={0}\told_op={1}\tnew_op={2}\t".format(i, operation, new_operation))
                infinite_loop, acc = self.find_infinite_loop(mut_instructions)
                # print("\tsubstitution instruction found: idx={0}\told_op={1}\tnew_op={2}\tinf_loop={3}\tacc={4}".format(i, operation, new_operation, infinite_loop, acc))

                # if we halted.
                if not infinite_loop:
                    return acc

        # we failed?
        return None
    ### find_corrupt_instruction


print("--- P1 sample input ---")
gc_sample = GameConsole(sample_input_file)
gc_sample.load_instructions()
infinite_loop, acc = gc_sample.find_infinite_loop()
test_equal(acc, 5, "P1: Sample found the wrong accumulator value.")
print("-------------------------")



gc = GameConsole(input_file)
gc.load_instructions()
infinite_loop, acc = gc.find_infinite_loop()


print("Solution to day 8 part 1: {0}".format(acc))


###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################
#   --- Part Two ---
#   After some careful analysis, you believe that exactly one instruction is corrupted.
#   
#   Somewhere in the program, either a jmp is supposed to be a nop, or a nop is supposed to be a jmp. 
#   (No acc instructions were harmed in the corruption of this boot code.)
#   
#   The program is supposed to terminate by attempting to execute an instruction immediately after the 
#   last instruction in the file. By changing exactly one jmp or nop, you can repair the boot code and 
#   make it terminate correctly.
#   
#   For example, consider the same program from above:
#   
#       nop +0
#       acc +1
#       jmp +4
#       acc +3
#       jmp -3
#       acc -99
#       acc +1
#       jmp -4
#       acc +6
#   
#   If you change the first instruction from nop +0 to jmp +0, it would create a single-instruction 
#   infinite loop, never leaving that instruction. If you change almost any of the jmp instructions, 
#   the program will still eventually find another jmp instruction and loop forever.
#   
#   However, if you change the second-to-last instruction (from jmp -4 to nop -4), the program terminates! 
#   The instructions are visited in this order:
#   
#       nop +0  | 1
#       acc +1  | 2
#       jmp +4  | 3
#       acc +3  |
#       jmp -3  |
#       acc -99 |
#       acc +1  | 4
#       nop -4  | 5
#       acc +6  | 6
#   
#   After the last instruction (acc +6), the program terminates by attempting to run the instruction 
#   below the last instruction in the file. With this change, after the program terminates, the 
#   accumulator contains the value 8 (acc +1, acc +1, acc +6).
#   
#   Fix the program so that it terminates normally by changing exactly one jmp (to nop) or nop (to jmp). 
#   What is the value of the accumulator after the program terminates?
#   

print("--- P2 sample input ---")
acc = gc_sample.find_corrupt_instruction()
test_equal(acc, 8, "P2: Unable to find infinite loop fix.")
print("-------------------------")


acc = gc.find_corrupt_instruction()
print("Solution to day 8 part 2: {0}".format(acc))

 