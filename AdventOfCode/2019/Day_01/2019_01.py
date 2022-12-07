#!/bin/python
# -*- coding: utf-8 -*-
# https://adventofcode.com/2019/day/1


###################################################################################################################################################################
#  
#  Solution to day 1 part 1: 3405637
#  Solution to day 1 part 2: 5105597
#
###################################################################################################################################################################


###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################

input_file = "sample.txt"
input_file = "input.txt"



# Fuel required to launch a given module is based on its mass. Specifically, to find the fuel 
# required for a module, take its mass, divide by three, round down, and subtract 2.
def calculate_fuel_for_module(mass):
    fuel_required_for_module = (mass / 3) - 2
    if fuel_required_for_module < 0:
        fuel_required_for_module = 0

    return fuel_required_for_module
### calculate_fuel_for_module


with open(input_file) as f:
    total_fuel_required_for_modules = 0
    for line in f:
        mass = int(line)
        total_fuel_required_for_modules += calculate_fuel_for_module(mass)

        # print "%s -> %s" % (mass, total_fuel_required_for_modules)

print "Solution to day 1 part 1: " + str(total_fuel_required_for_modules)



###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################

def calculate_fuel_for_fuel(fuel_mass):
    total_fuel_for_fuel = 0

    partial_fuel_for_fuel = fuel_mass

    while partial_fuel_for_fuel > 0:
        partial_fuel_for_fuel = calculate_fuel_for_module(partial_fuel_for_fuel)
        total_fuel_for_fuel += partial_fuel_for_fuel

    return total_fuel_for_fuel
### calculate_fuel_for_fuel


def calculate_fuel_for_module_and_fuel(mass):
    total_fuel_required_for_module = calculate_fuel_for_module(mass)
    total_fuel_required_for_fuel = calculate_fuel_for_fuel(total_fuel_required_for_module)
    return total_fuel_required_for_module + total_fuel_required_for_fuel
### calculate_fuel_for_module_and_fuel

with open(input_file) as f:
    total_fuel_required_for_modules = 0
    
    for line in f:
        mass = int(line)
        fuel = calculate_fuel_for_module_and_fuel(mass)
        total_fuel_required_for_modules += fuel

        # print "%s -> %s" % (mass, fuel)


print "Solution to day 1 part 2: " + str(total_fuel_required_for_modules)

