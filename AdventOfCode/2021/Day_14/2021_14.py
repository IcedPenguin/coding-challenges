#!/bin/python
# -*- coding: utf-8 -*-
# https://adventofcode.com/2021/day/14


###################################################################################################################################################################
#  
#  Solution to day 14 part 1: 2657
#
#  Solution to day 14 part 2: 2911561572630
#
###################################################################################################################################################################

import unittest
import copy

###################################################################################################################################################################
############################################################################# Common ##############################################################################


sample_input_file_1 = "2021_sample_1.txt"
sample_input_file_2 = "2021_sample_2.txt"
input_file          = "2021_input.txt"


###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################
#   
#   --- Day 14: Extended Polymerization ---
#   The incredible pressures at this depth are starting to put a strain on your submarine. The submarine has polymerization 
#   equipment that would produce suitable materials to reinforce the submarine, and the nearby volcanically-active caves 
#   should even have the necessary input elements in sufficient quantities.
#   
#   The submarine manual contains instructions for finding the optimal polymer formula; specifically, it offers a polymer 
#   template and a list of pair insertion rules (your puzzle input). You just need to work out what polymer would result 
#   after repeating the pair insertion process a few times.
#   
#   For example:
#   
#       NNCB
#   
#       CH -> B
#       HH -> N
#       CB -> H
#       NH -> C
#       HB -> C
#       HC -> B
#       HN -> C
#       NN -> C
#       BH -> H
#       NC -> B
#       NB -> B
#       BN -> B
#       BB -> N
#       BC -> B
#       CC -> N
#       CN -> C
#   
#   The first line is the polymer template - this is the starting point of the process.
#   
#   The following section defines the pair insertion rules. A rule like AB -> C means that when elements A and B are 
#   immediately adjacent, element C should be inserted between them. These insertions all happen simultaneously.
#   
#   So, starting with the polymer template NNCB, the first step simultaneously considers all three pairs:
#   
#   The first pair (NN) matches the rule NN -> C, so element C is inserted between the first N and the second N.
#   The second pair (NC) matches the rule NC -> B, so element B is inserted between the N and the C.
#   The third pair (CB) matches the rule CB -> H, so element H is inserted between the C and the B.
#   
#   Note that these pairs overlap: the second element of one pair is the first element of the next pair. Also, because 
#   all pairs are considered simultaneously, inserted elements are not considered to be part of a pair until the next step.
#   
#   After the first step of this process, the polymer becomes NCNBCHB.
#   
#   Here are the results of a few steps using the above rules:
#   
#       Template:     NNCB
#       After step 1: NCNBCHB
#       After step 2: NBCCNBBBCBHCB
#       After step 3: NBBBCNCCNBBNBNBBCHBHHBCHB
#       After step 4: NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB
#   
#   This polymer grows quickly. After step 5, it has length 97; After step 10, it has length 3073. After step 10, B 
#   occurs 1749 times, C occurs 298 times, H occurs 161 times, and N occurs 865 times; taking the quantity of the most 
#   common element (B, 1749) and subtracting the quantity of the least common element (H, 161) produces 1749 - 161 = 1588.
#   
#   Apply 10 steps of pair insertion to the polymer template and find the most and least common elements in the result. 
#   What do you get if you take the quantity of the most common element and subtract the quantity of the least common element?
#   


def read_polymer_instructions(filename):

    with open(filename) as f:
        lines = f.read().splitlines()

    polymer = lines.pop(0)

    lines.pop(0)

    pair_insertion_rules = {}
    for pair in lines:
        parts = pair.split(" -> ")
        pair_insertion_rules[parts[0]] = parts[1]

    return polymer, pair_insertion_rules



def apply_insertion_steps(polymer, pair_insertion_rules, count):
    for _ in range(count):
        polymer = apply_insertion_step(polymer, pair_insertion_rules)

    return polymer



def apply_insertion_step(polymer, pair_insertion_rules):
    updated_polymer = []

    polymer_length = len(polymer)
    for i in range(polymer_length-1, 0, -1):
        pair = polymer[i-1: i+1]
        insert = pair_insertion_rules[pair]

        updated_polymer.insert(0, pair[1])
        updated_polymer.insert(0, insert)

    updated_polymer.insert(0, polymer[0])

    return "".join(updated_polymer)


def find_most_and_least_common_elements(polymer):
    element_counter = {}

    for element in polymer:
        if element in element_counter:
            element_counter[element] += 1
        else:
            element_counter[element] = 1

    e_min = float("inf")
    e_min_value = None
    e_max = -1
    e_max_value = None

    for element in element_counter:
        count = element_counter[element]
        if count < e_min:
            e_min = count
            e_min_value = element

        if count > e_max:
            e_max = count
            e_max_value = element

    return e_min, e_min_value, e_max, e_max_value, element_counter


# data to be used in part 2, as a comparison to debug why pair/element counts aren't correct
part_1_sample_data = {}
part_1_solution_data = {}

class Day14PartOneTests(unittest.TestCase):

    
    def test__part_1__sample_input(self):
        print("")
        polymer, pair_insertion_rules = read_polymer_instructions(sample_input_file_1)
        
        polymer = apply_insertion_step(polymer, pair_insertion_rules)
        e_min, e_min_value, e_max, e_max_value, element_counter = find_most_and_least_common_elements(polymer)
        part_1_sample_data[0] = {"polymer": polymer, "element_counter": element_counter}
        self.assertEqual("NCNBCHB", polymer)

        polymer = apply_insertion_step(polymer, pair_insertion_rules)
        e_min, e_min_value, e_max, e_max_value, element_counter = find_most_and_least_common_elements(polymer)
        part_1_sample_data[1] = {"polymer": polymer, "element_counter": element_counter}
        self.assertEqual("NBCCNBBBCBHCB", polymer)

        polymer = apply_insertion_step(polymer, pair_insertion_rules)
        e_min, e_min_value, e_max, e_max_value, element_counter = find_most_and_least_common_elements(polymer)
        part_1_sample_data[2] = {"polymer": polymer, "element_counter": element_counter}
        self.assertEqual("NBBBCNCCNBBNBNBBCHBHHBCHB", polymer)

        polymer = apply_insertion_step(polymer, pair_insertion_rules)
        e_min, e_min_value, e_max, e_max_value, element_counter = find_most_and_least_common_elements(polymer)
        part_1_sample_data[3] = {"polymer": polymer, "element_counter": element_counter}
        self.assertEqual("NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB", polymer)


        for count in range(6):
            polymer = apply_insertion_steps(polymer, pair_insertion_rules, 1)
            e_min, e_min_value, e_max, e_max_value, element_counter = find_most_and_least_common_elements(polymer)
            part_1_sample_data[count+4] = {"polymer": polymer, "element_counter": element_counter}


        e_min, e_min_value, e_max, e_max_value, _ = find_most_and_least_common_elements(polymer)
        self.assertEqual("B", e_max_value)
        self.assertEqual(1749, e_max)
        self.assertEqual("H", e_min_value)
        self.assertEqual(161, e_min)



    def test__part_1__challenge_input(self):
        print("")
        # Known working code. Original solution
        # polymer, pair_insertion_rules = read_polymer_instructions(input_file)
        # polymer = apply_insertion_steps(polymer, pair_insertion_rules, 10)
        # e_min, e_min_value, e_max, e_max_value, _ = find_most_and_least_common_elements(polymer)

        polymer, pair_insertion_rules = read_polymer_instructions(input_file)
        for count in range(10):
            polymer = apply_insertion_steps(polymer, pair_insertion_rules, 1)
            e_min, e_min_value, e_max, e_max_value, element_counter = find_most_and_least_common_elements(polymer)
            part_1_solution_data[count] = {"polymer": polymer, "element_counter": element_counter}


        self.assertEqual(2657, e_max - e_min)  # changing above logic to assist with solution 2. Ensure we don't break our correct answer.
        print("Solution to day 14 part 1: {0}".format(e_max - e_min))
        


###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################
#  
#  --- Part Two ---
#  The resulting polymer isn't nearly strong enough to reinforce the submarine. You'll need to run more 
#  steps of the pair insertion process; a total of 40 steps should do it.
#  
#  In the above example, the most common element is B (occurring 2192039569602 times) and the least common 
#  element is H (occurring 3849876073 times); subtracting these produces 2188189693529.
#  
#  Apply 40 steps of pair insertion to the polymer template and find the most and least common elements in the 
#  result. What do you get if you take the quantity of the most common element and subtract the quantity of 
#  the least common element?
#  


###
# Thoughts
#   * Solution needs to change. Cannot simply build the string. It would be terabytes in size.
#   * Count common substrings/ pairs
#     * Help from https://www.reddit.com/r/adventofcode/comments/rg57dz/day_14_part_2_algorithm/

def extract_element_pairs(polymer):
    # part 2
    ploymer_pairs = {}
    for i in range(0, len(polymer)-1):
        if polymer[i:i+2] in ploymer_pairs:
            ploymer_pairs[polymer[i:i+2]] += 1
        else:
            ploymer_pairs[polymer[i:i+2]] = 1

    element_counter = {}
    for e in polymer:
        if e in element_counter:
            element_counter[e] += 1
        else:
            element_counter[e] = 1

    return ploymer_pairs, element_counter



def apply_insertion_steps_2(ploymer_pairs, element_counter, pair_insertion_rules, count):
    for _ in range(count):
        ploymer_pairs = apply_insertion_step_2(ploymer_pairs, element_counter, pair_insertion_rules)

    return ploymer_pairs


def apply_insertion_step_2(ploymer_pairs, element_counter, pair_insertion_rules):
    new_ploymer_pairs = {}
    
    for pair in ploymer_pairs:
        insert_element = pair_insertion_rules[pair]
        pair_count = ploymer_pairs[pair]
        front_pair = pair[0] + insert_element
        back_pair =  insert_element + pair[1]


        # keep track of newly inserted elements
        if insert_element in element_counter:
            element_counter[insert_element] += pair_count 
        else:
            element_counter[insert_element] = pair_count 
    

        # keep track of the new pairs
        if front_pair in new_ploymer_pairs:
            new_ploymer_pairs[front_pair] += pair_count
        else:
            new_ploymer_pairs[front_pair] = pair_count 

        if back_pair in new_ploymer_pairs:
            new_ploymer_pairs[back_pair] += pair_count
        else:
            new_ploymer_pairs[back_pair] = pair_count 


    return new_ploymer_pairs


def find_most_and_least_common_elements_2(element_counter):

    e_min = float("inf")
    e_min_value = None
    e_max = -1
    e_max_value = None

    for element in element_counter:
        count = element_counter[element]
        if count < e_min:
            e_min = count
            e_min_value = element

        if count > e_max:
            e_max = count
            e_max_value = element

    return e_min, e_min_value, e_max, e_max_value



def get_element_count(polymer, ploymer_pairs):
    element_counter = {}

    for poly in ploymer_pairs:
        element = poly[0]
        if element in element_counter:
            element_counter[element] += ploymer_pairs[poly]
        else:
            element_counter[element] = ploymer_pairs[poly]

    last_element = polymer[-1]
    if last_element in element_counter:
        element_counter[last_element] += 1
    else:
        element_counter[last_element] = 1

    return element_counter


class Day14PartTwoTests(unittest.TestCase):

    def test__part_2__nn_n(self):
        ploymer_pairs = {"NN": 1}
        element_counter = {"N": 2}
        pair_insertion_rules = {"NN": "N"}
        
        ploymer_pairs = apply_insertion_step_2(ploymer_pairs, element_counter, pair_insertion_rules)
        self.assertEqual(len(ploymer_pairs), 1)
        self.assertEqual(ploymer_pairs["NN"], 2)
        self.assertEqual(element_counter["N"], 3)
        
        ploymer_pairs = apply_insertion_step_2(ploymer_pairs, element_counter, pair_insertion_rules)
        self.assertEqual(len(ploymer_pairs), 1)
        self.assertEqual(ploymer_pairs["NN"], 4)
        self.assertEqual(element_counter["N"], 5)

        ploymer_pairs = apply_insertion_step_2(ploymer_pairs, element_counter, pair_insertion_rules)
        self.assertEqual(len(ploymer_pairs), 1)
        self.assertEqual(ploymer_pairs["NN"], 8)
        self.assertEqual(element_counter["N"], 9)
        

    def test__part_2__sample_input(self):
        print("")
        polymer, pair_insertion_rules = read_polymer_instructions(sample_input_file_1)
        ploymer_pairs, element_counter = extract_element_pairs(polymer)
        
        for count in range(10):
            # print("----- Sample {0} -----".format(count))
            ploymer_pairs = apply_insertion_steps_2(ploymer_pairs, element_counter, pair_insertion_rules, 1)

            if count == 0:
                self.assertEqual(1, ploymer_pairs["NC"])
                self.assertEqual(6, len(ploymer_pairs)) # six unique pairs
                
            elif count == 1:
                self.assertEqual(2, ploymer_pairs["CB"])
                self.assertEqual(8, len(ploymer_pairs)) # 8 unique pairs, 4 have 2 copies

            # Compare against data from part 1.
            p1_pairs, p1_elements = extract_element_pairs(part_1_sample_data[count]["polymer"])
            self.assertEqual(part_1_sample_data[count]["element_counter"], p1_elements) #sanity check
            self.assertEqual(p1_pairs, ploymer_pairs)
            self.assertEqual(p1_elements, element_counter)


        e_min, e_min_value, e_max, e_max_value = find_most_and_least_common_elements_2(element_counter)
        self.assertEqual("B", e_max_value)
        self.assertEqual(1749, e_max)
        self.assertEqual("H", e_min_value)
        self.assertEqual(161, e_min)

    

    def test__part_2__challenge_input(self):        
        print("")

        polymer, pair_insertion_rules = read_polymer_instructions(input_file)
        ploymer_pairs, element_counter = extract_element_pairs(polymer)

        for count in range(10): # match part 1
            # print("----- Challenge {0} -----".format(count))
            ploymer_pairs = apply_insertion_steps_2(ploymer_pairs, element_counter, pair_insertion_rules, 1)
            p1_pairs, p1_elements = extract_element_pairs(part_1_solution_data[count]["polymer"])

            # Compare against data from part 1.
            self.assertEqual(part_1_solution_data[count]["element_counter"], p1_elements) #sanity check
            self.assertEqual(p1_pairs, ploymer_pairs)
            self.assertEqual(p1_elements, element_counter)


        # Everything up to step 10 matched, complete the final 30 iterations
        ploymer_pairs = apply_insertion_steps_2(ploymer_pairs, element_counter, pair_insertion_rules, 30)

        e_min, e_min_value, e_max, e_max_value = find_most_and_least_common_elements_2(element_counter)
        
        print("Solution to day 14 part 2: {0}".format(e_max - e_min))
        # 2451826121744   Too Low
        # 1225908664416   Too low (didn't even submit)
        # 2911561572630   Correct
 

 
###################################################################################################################################################################
########################################################################## RUN THE TESTS ##########################################################################


# run then unit tests "last"
if __name__ == '__main__':
    unittest.main()
 

