#!/bin/python
# -*- coding: utf-8 -*-
# https://adventofcode.com/2019/day/2


###################################################################################################################################################################
#  
#  Solution to day 2 part 1: 4484226
#  Solution to day 2 part 2: 5696
#
###################################################################################################################################################################


###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################

# input_file = "sample.txt"
input_file = "input.txt"


class IntcodeComputer(object):
    def __init__(self):
        self.memory = {}
        self.pointer = 0
    ### __init__

    def execute_program(self):
        running = 1
        while running:
            running = self.execute_current_instruction()
    ### execute_program

    def execute_current_instruction(self):
        op_code = self.memory[self.pointer]

        if op_code == 1:
            self.perform_add_operation()
            self.pointer += 4

        elif op_code == 2:
            self.perform_multiply_operation()
            self.pointer += 4

        elif op_code == 99:
            return 0

        else:
            print "invalid opcode"
            print op_code
            return -1

        return 1
    ### execute_current_instruction

    def get_operands_for_current_instruction(self):
        operand_1_pointer = self.memory[self.pointer +1]
        operand_2_pointer = self.memory[self.pointer +2]
        destination_address_pointer = self.memory[self.pointer +3]

        return self.memory[operand_1_pointer], self.memory[operand_2_pointer], destination_address_pointer
    ### get_operands_for_current_instruction

    def perform_add_operation(self):
        integer_1, integer_2, destination_address_pointer = self.get_operands_for_current_instruction()
        # print "add: %d + %d -> %d" % (integer_1, integer_2, destination_address_pointer)
        self.memory[destination_address_pointer] = integer_1 + integer_2
    ### perform_add_operation

    def perform_multiply_operation(self):
        integer_1, integer_2, destination_address_pointer = self.get_operands_for_current_instruction()
        # print "mul: %d + %d -> %d" % (integer_1, integer_2, destination_address_pointer)
        self.memory[destination_address_pointer] = integer_1 * integer_2
    ### perform_multiply_operation

    def get_state(self):
        s = ""
        for i in xrange(0, len(self.memory)):
            s += str(self.memory[i]) + ", "

        return s
    ### get_state

    def load_program(self, program):
        parts = program.split(",")
        for i in xrange(0, len(parts)):
            self.memory[i] = int(parts[i])
    ### load_program

    def set_position(self, address, value):
        self.memory[address] = value
    ### set_position

    def get_value_at_position(self, address):
        return self.memory[address]
    ### get_value_at_position
### IntcodeComputer

program = ""
with open(input_file) as f:
    
    for line in f:
        program = line
        computer = IntcodeComputer()
        computer.load_program(line)
        computer.set_position(1, 12)
        computer.set_position(2, 2)
        # print computer.get_state()
        computer.execute_program()
        # print computer.get_state()
        print "  "


print "Solution to day 2 part 1: " + str(computer.get_value_at_position(0))



###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################

solution = -1
for noun in xrange(0, 100):
    for verb in xrange(0, 100):
        computer = IntcodeComputer()
        computer.load_program(program)
        computer.set_position(1, noun)
        computer.set_position(2, verb)

        computer.execute_program()
        # print computer.get_state()

        if computer.get_value_at_position(0) == 19690720:
            print "Solution found: (noun = %d, verb = %d)" % (noun, verb)
            solution = 100 * noun + verb



# 19690720

print "Solution to day 2 part 2: " + str(solution)

