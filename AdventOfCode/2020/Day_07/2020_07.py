#!/bin/python
# -*- coding: utf-8 -*-
# https://adventofcode.com/2020/day/7


###################################################################################################################################################################
#  
#  Solution to day 7 part 1: 261
#
#  Solution to day 7 part 2: 3765
#
###################################################################################################################################################################


###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################
#   
#   --- Day 7: Handy Haversacks ---
#   
#   You land at the regional airport in time for your next flight. In fact, it looks like you'll even have time to grab 
#   some food: all flights are currently delayed due to issues in luggage processing.
#   
#   Due to recent aviation regulations, many rules (your puzzle input) are being enforced about bags and their contents; 
#   bags must be color-coded and must contain specific quantities of other color-coded bags. Apparently, nobody 
#   responsible for these regulations considered how long they would take to enforce!
#   
#   For example, consider the following rules:
#   
#           light red bags contain 1 bright white bag, 2 muted yellow bags.
#           dark orange bags contain 3 bright white bags, 4 muted yellow bags.
#           bright white bags contain 1 shiny gold bag.
#           muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
#           shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
#           dark olive bags contain 3 faded blue bags, 4 dotted black bags.
#           vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
#           faded blue bags contain no other bags.
#           dotted black bags contain no other bags.
#   
#   These rules specify the required contents for 9 bag types. In this example, every faded blue bag is empty, every 
#   vibrant plum bag contains 11 bags (5 faded blue and 6 dotted black), and so on.
#   
#   You have a shiny gold bag. If you wanted to carry it in at least one other bag, how many different bag colors 
#   would be valid for the outermost bag? (In other words: how many colors can, eventually, contain at least one shiny gold bag?)
#   
#   In the above rules, the following options would be available to you:
#   
#           A bright white bag, which can hold your shiny gold bag directly.
#           A muted yellow bag, which can hold your shiny gold bag directly, plus some other bags.
#           A dark orange bag, which can hold bright white and muted yellow bags, either of which could then hold your shiny gold bag.
#           A light red bag, which can hold bright white and muted yellow bags, either of which could then hold your shiny gold bag.
#   
#   So, in this example, the number of bag colors that can eventually contain at least one shiny gold bag is 4.
#   
#   How many bag colors can eventually contain at least one shiny gold bag? (The list of rules is quite long; make sure you get all of it.)
#   


def test_equal(actual, expected, message):
    if actual != expected:
        print("FAIL: Found={0}  Expected={1}    {2}".format(actual, expected, message))



sample_input_file   = "2020_07_sample.txt"
sample_input_file_2 = "2020_07_sample_2.py"
input_file          = "2020_07_input.txt"



class Rule:  
    def __init__(self):  
        self.name = None
        self.rules = {}
        self.regulations = None
        self.required_inner_bag_count = 0

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def add_rule(self, bag, max_count):
        self.rules[bag] = max_count

    def get_contains_rules(self):
        rules = []
        for key in self.rules:
            rules.append( (key, self.rules[key]))

        return rules

    def get_types_of_bags_possibly_containing(self):
        return self.rules.keys()

    def set_regulations(self, regulations):
        self.regulations = regulations

    def get_required_number_of_inner_bags(self):
        if self.regulations is None:
            return int("Die!")

        if self.required_inner_bag_count == 0:
            for bag_name, required_count in self.rules.items():
                self.required_inner_bag_count += required_count + required_count * self.regulations[bag_name].get_required_number_of_inner_bags()

        return self.required_inner_bag_count
### Class: Rule

def parse_rule(rule_line):
    rule_line = rule_line.strip()
    rule_line = rule_line.replace(" bags", "").replace(" bag", "").replace(" contain", "")
    rule_line = rule_line.replace(",", "").replace(".", "")

    rule_tokens = rule_line.split(" ")

    rule_parse_state = 0
    is_empty = None
    bag_name = ""
    contains_rules = []
    contains_temp_count = -1 
    contains_temp_name = ""

    r = Rule()
    # 0 & 1 -> name of bag
    # 2 -> either indicates back is empty, or 
    # 2 3 4 -> # and name of inner bags
    # [pairs of three] additional inner bags

    for t in rule_tokens:
        if rule_parse_state == 0:
            bag_name += t

        elif rule_parse_state == 1:
            bag_name += " " + t
            r.set_name(bag_name)

        if rule_parse_state == 2 and is_empty is None:
            is_empty = t == "no"

        if rule_parse_state >= 2 and not is_empty:
            contains_count = (rule_parse_state -2) % 3

            if contains_count == 0:
                contains_temp_count = int(t)

            elif contains_count == 1:
                contains_temp_name = t

            else:
                contains_temp_name += " " + t
                r.add_rule(contains_temp_name, contains_temp_count)

        rule_parse_state += 1

    return r
### parse_rule




def process_rules_file(file_name):
    regulations = {}

    with open(file_name) as f:
        for line in f:
            line = line.strip()

            rule = parse_rule(line)

            regulations[rule.get_name()] = rule
            rule.set_regulations(regulations)

    return regulations
### process_rules_file



#   You have a shiny gold bag. If you wanted to carry it in at least one other bag, how many different bag colors 
#   would be valid for the outermost bag? (In other words: how many colors can, eventually, contain at least one shiny gold bag?)
def which_bags_could_eventually_contain(regulations, colored_bag):

    candidate_bags = set()
    what_can_carry_these_bags = set()
    what_can_carry_these_bags.add(colored_bag)
    done = False

    while not done:
        start_length = len(candidate_bags)
        
        for bag_type, bag_rule in regulations.items():
            inner_bag_types = bag_rule.get_types_of_bags_possibly_containing()

            for bag in inner_bag_types:
                if bag in what_can_carry_these_bags:
                    what_can_carry_these_bags.add(bag_type)
                    candidate_bags.add(bag_type)

        if start_length == len(candidate_bags):
            done = True

    return candidate_bags

### which_bags_could_eventually_contain


print("--- P1 sample input ---")
regulations_sample = process_rules_file(sample_input_file)
test_equal(len(regulations_sample), 9, "P1 - found wrong total count of regulations_sample")
test_equal(regulations_sample["light red"].get_contains_rules(),   [("bright white", 1), ("muted yellow", 2)], "P1 failed to parse: light red bags contain 1 bright white bag, 2 muted yellow bags.")
test_equal(regulations_sample["dark orange"].get_contains_rules(), [("bright white", 3), ("muted yellow", 4)], "P1 failed to parse: dark orange bags contain 3 bright white bags, 4 muted yellow bags.")
test_equal(regulations_sample["shiny gold"].get_contains_rules(), [("dark olive", 1), ("vibrant plum", 2)], "P1 failed to parse: shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags")
test_equal(regulations_sample["faded blue"].get_contains_rules(), [], "P1 failed to parse: faded blue bags contain no other bags.")

outer_bags = which_bags_could_eventually_contain(regulations_sample, "shiny gold")
test_equal(len(outer_bags), 4, "P1 failed to identify outer bags: {0}".format(outer_bags))
test_equal(sorted(outer_bags), sorted(["bright white","muted yellow","dark orange","light red"]), "P1 failed to identify outer bags")
print("-------------------------")

regulations = process_rules_file(input_file)
outer_bags = which_bags_could_eventually_contain(regulations, "shiny gold")


print("Solution to day 7 part 1: {0}".format(len(outer_bags)))


###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################
#   
#   --- Part Two ---
#   
#   It's getting pretty expensive to fly these days - not because of ticket prices, but because of the 
#   ridiculous number of bags you need to buy!
#   
#   Consider again your shiny gold bag and the rules from the above example:
#   
#       faded blue bags contain 0 other bags.
#       dotted black bags contain 0 other bags.
#       vibrant plum bags contain 11 other bags: 5 faded blue bags and 6 dotted black bags.
#       dark olive bags contain 7 other bags: 3 faded blue bags and 4 dotted black bags.
#   
#   So, a single shiny gold bag must contain 1 dark olive bag (and the 7 bags within it) plus 2 vibrant 
#   plum bags (and the 11 bags within each of those): 1 + 1*7 + 2 + 2*11 = 32 bags!
#   
#   Of course, the actual rules have a small chance of going several levels deeper than this example; be 
#   sure to count all of the bags, even if the nesting becomes topologically impractical!
#   
#   Here's another example:
#   
#       shiny gold bags contain 2 dark red bags.
#       dark red bags contain 2 dark orange bags.
#       dark orange bags contain 2 dark yellow bags.
#       dark yellow bags contain 2 dark green bags.
#       dark green bags contain 2 dark blue bags.
#       dark blue bags contain 2 dark violet bags.
#       dark violet bags contain no other bags.
#   
#   In this example, a single shiny gold bag must contain 126 other bags.
#   
#   How many individual bags are required inside your single shiny gold bag?
#   


print("--- P2 sample input ---")
test_equal(regulations_sample["shiny gold"].get_required_number_of_inner_bags(), 32, "P2A count of inner bags is off.")

regulations_sample_2 = process_rules_file(sample_input_file_2)
test_equal(regulations_sample_2["shiny gold"].get_required_number_of_inner_bags(), 126, "P2B count of inner bags is off.")
print("-------------------------")

inner_bag_count = regulations["shiny gold"].get_required_number_of_inner_bags()

print("Solution to day 7 part 2: {0}".format(inner_bag_count))

 