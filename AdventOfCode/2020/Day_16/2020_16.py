#!/bin/python
# -*- coding: utf-8 -*-
# https://adventofcode.com/2020/day/16


###################################################################################################################################################################
#  
#  Solution to day 16 part 1: 27898
#
#  Solution to day 16 part 2: 
#
###################################################################################################################################################################

import unittest

###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################
#
#   --- Day 16: Ticket Translation ---
#   As you're walking to yet another connecting flight, you realize that one of the legs of your re-routed 
#   trip coming up is on a high-speed train. However, the train ticket you were given is in a language you 
#   don't understand. You should probably figure out what it says before you get to the train station after 
#   the next flight.
#   
#   Unfortunately, you can't actually read the words on the ticket. You can, however, read the numbers, and 
#   so you figure out the fields these tickets must have and the valid ranges for values in those fields.
#   
#   You collect the rules for ticket fields, the numbers on your ticket, and the numbers on other nearby 
#   tickets for the same train service (via the airport security cameras) together into a single document 
#   you can reference (your puzzle input).
#   
#   The rules for ticket fields specify a list of fields that exist somewhere on the ticket and the valid 
#   ranges of values for each field. For example, a rule like class: 1-3 or 5-7 means that one of the fields 
#   in every ticket is named class and can be any value in the ranges 1-3 or 5-7 (inclusive, such that 3
#   and 5 are both valid in this field, but 4 is not).
#   
#   Each ticket is represented by a single line of comma-separated values. The values are the numbers on 
#   the ticket in the order they appear; every ticket has the same format. For example, consider this ticket:
#   
#       .--------------------------------------------------------.
#       | ????: 101    ?????: 102   ??????????: 103     ???: 104 |
#       |                                                        |
#       | ??: 301  ??: 302             ???????: 303      ??????? |
#       | ??: 401  ??: 402           ???? ????: 403    ????????? |
#       '--------------------------------------------------------'
#   
#   Here, ? represents text in a language you don't understand. This ticket might be represented as 
#   101,102,103,104,301,302,303,401,402,403; of course, the actual train tickets you're looking at are 
#   much more complicated. In any case, you've extracted just the numbers in such a way that the first number 
#   is always the same specific field, the second number is always a different specific field, and so on - you 
#   just don't know what each position actually means!
#   
#   Start by determining which tickets are completely invalid; these are tickets that contain values which 
#   aren't valid for any field. Ignore your ticket for now.
#   
#   For example, suppose you have the following notes:
#   
#       class: 1-3 or 5-7
#       row: 6-11 or 33-44
#       seat: 13-40 or 45-50
#   
#       your ticket:
#       7,1,14
#   
#       nearby tickets:
#       7,3,47
#       40,4,50
#       55,2,20
#       38,6,12
#   
#   It doesn't matter which position corresponds to which field; you can identify invalid nearby tickets by 
#   considering only whether tickets contain values that are not valid for any field. In this example, the 
#   values on the first nearby ticket are all valid for at least one field. This is not true of the other 
#   three nearby tickets: the values 4, 55, and 12 are are not valid for any field. Adding together all of 
#   the invalid values produces your ticket scanning error rate: 4 + 55 + 12 = 71.
#   
#   Consider the validity of the nearby tickets you scanned. What is your ticket scanning error rate?
#   

def test_equal(actual, expected, message):
    if actual != expected:
        print("FAIL: Found={0}  Expected={1}    {2}".format(actual, expected, message))


sample_input_file_1 = "2020_16_sample_1.txt"
sample_input_file_2 = "2020_16_sample_2.txt"
input_file          = "2020_16_input.txt"


class TicketRule:
    def __init__(self, rule_statement):

        idx = rule_statement.find(":")
        self.rule_name = rule_statement[:idx]
        rule_statement = rule_statement[idx+2:].strip()

        self.ranges = []
        parts = rule_statement.split(" or ") 
        for p in parts:
            parts_2 = p.split("-")
            self.ranges.append( (int(parts_2[0]), int(parts_2[1])) )
        
    def __str__(self):
        return "TicketRule: " + self.rule_name + " " + str(self.ranges)



class Ticket:
    def __init__(self, ticket_contents):
        self.ticket_numbers = [ int(i) for i in ticket_contents.strip().split(",")]

    def __str__(self):
        return "Ticket: " + "".join( str(self.ticket_numbers) )


def is_number_in_rule_range(rules, ticket_number):
    for rule in rules:
        for ticket_rule in rule.ranges:
            if ticket_rule[0] <= ticket_number and ticket_number <= ticket_rule[1]:
                # print("Rule met: r={0}   t={1}".format(ticket_rule, ticket_number))
                return True
    
    return False
### is_number_in_rule_range


def is_there_at_least_one_ticket_number_that_does_not_match_a_rule_range(rules, ticket):
    if ticket is None or rules is None:
        return True

    for ticket_number in ticket.ticket_numbers:
        passed_a_rule = is_number_in_rule_range(rules, ticket_number)
        

        if not passed_a_rule:
            return False, ticket_number

    return True, None


def process_all_tickets_and_rules_in_file(file_name):
    #------ process the file. ------
    rules = []
    my_ticket = None
    other_tickets = []

    capture_state = 1
    with open(file_name) as f:
        for line in f:
            line = line.strip()

            if line == "":
                capture_state += 1

            elif capture_state == 1:
                rules.append(TicketRule(line))

            elif capture_state == 2:
                if line != "your ticket:":
                    my_ticket = Ticket(line)

            elif capture_state ==3:
                if line != "nearby tickets:":
                    other_tickets.append(Ticket(line))

    #------ process the tickets and rules that were extracted ------
    sum_of_invalid_numbers = 0
    for ticket in other_tickets:
        result, number = is_there_at_least_one_ticket_number_that_does_not_match_a_rule_range(rules, ticket)

        if not result:
            sum_of_invalid_numbers += number
        # print("------:: T={0} \tR={1} \tN={2} \t\tS={3}".format(ticket, result, number, sum_of_invalid_numbers))

    return sum_of_invalid_numbers
### process_all_tickets_and_rules_in_file


class Day16PartOneTests(unittest.TestCase):

    def test__TicketRules__parsing(self):
        rule_1 = TicketRule("class: 1-3 or 5-7")
        self.assertEqual(str(rule_1), "TicketRule: class [(1, 3), (5, 7)]")

        rule_2 = TicketRule("row: 6-11 or 33-44")
        self.assertEqual(str(rule_2), "TicketRule: row [(6, 11), (33, 44)]")
        
        rule_3 = TicketRule("seat: 13-40 or 45-50")
        self.assertEqual(str(rule_3), "TicketRule: seat [(13, 40), (45, 50)]")
        

    def test__Ticket__parsing(self):
        ticket = Ticket("7,1,14")
        self.assertEqual(str(ticket), "Ticket: [7, 1, 14]")


        ticket = Ticket("7,3,47")
        self.assertEqual(str(ticket), "Ticket: [7, 3, 47]")

        ticket = Ticket("40,4,50")
        self.assertEqual(str(ticket), "Ticket: [40, 4, 50]")

        ticket = Ticket("55,2,20")
        self.assertEqual(str(ticket), "Ticket: [55, 2, 20]")

        ticket = Ticket("38,6,12")
        self.assertEqual(str(ticket), "Ticket: [38, 6, 12]")

    
    def test__is_there_at_least_one_ticket_number_that_does_not_match_a_rule_range__valid_ticket__is_valid(self):
        rules = []
        rules.append(TicketRule("class: 1-3 or 5-7"))
        rules.append(TicketRule("row: 6-11 or 33-44"))
        rules.append(TicketRule("seat: 13-40 or 45-50"))

        result, number = is_there_at_least_one_ticket_number_that_does_not_match_a_rule_range(rules, Ticket("7,1,14"))
        self.assertEqual(result, True)
        self.assertEqual(number, None)

        result, number = is_there_at_least_one_ticket_number_that_does_not_match_a_rule_range(rules, Ticket("7,3,47"))
        self.assertEqual(result, True)
        self.assertEqual(number, None)


    def test__is_ticket_completely_invalid__invalid_tickets__is_invalid(self):
        rules = []
        rules.append(TicketRule("class: 1-3 or 5-7"))
        rules.append(TicketRule("row: 6-11 or 33-44"))
        rules.append(TicketRule("seat: 13-40 or 45-50"))

        result, number_1 = is_there_at_least_one_ticket_number_that_does_not_match_a_rule_range(rules, Ticket("40,4,50"))
        self.assertEqual(result, False)
        self.assertEqual(number_1, 4)

        result, number_2 = is_there_at_least_one_ticket_number_that_does_not_match_a_rule_range(rules, Ticket("55,2,20"))
        self.assertEqual(result, False)
        self.assertEqual(number_2, 55)

        result, number_3 = is_there_at_least_one_ticket_number_that_does_not_match_a_rule_range(rules, Ticket("38,6,12"))
        self.assertEqual(result, False)
        self.assertEqual(number_3, 12)

        self.assertEqual(number_1 + number_2 + number_3, 71)
        

    def test__part_1__sample_input(self):
        self.assertEqual(process_all_tickets_and_rules_in_file(sample_input_file_1), 71)


    def test__part_1__challenge_input(self):
        print("")
        number = process_all_tickets_and_rules_in_file(input_file)
        print("Solution to day 16 part 1: {0}".format(number))
        



###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################
#   
#   --- Part Two ---
#   Now that you've identified which tickets contain invalid values, discard those tickets entirely. Use 
#   the remaining valid tickets to determine which field is which.
#   
#   Using the valid ranges for each field, determine what order the fields appear on the tickets. The order 
#   is consistent between all tickets: if seat is the third field, it is the third field on every ticket, 
#   including your ticket.
#   
#   For example, suppose you have the following notes:
#   
#       class: 0-1 or 4-19
#       row: 0-5 or 8-19
#       seat: 0-13 or 16-19
#   
#       your ticket:
#       11,12,13
#   
#       nearby tickets:
#       3,9,18
#       15,1,5
#       5,14,9
#   
#   Based on the nearby tickets in the above example, the first position must be row, the second position must 
#   be class, and the third position must be seat; you can conclude that in your ticket, class is 12, row is 11,
#   and seat is 13.
#   
#   Once you work out which field is which, look for the six fields on your ticket that start with the word 
#   departure. What do you get if you multiply those six values together?
#   




# class Day16PartTwoTests(unittest.TestCase):

#     def test__p2(self):
#         self.assertEqual(10, 11)

    

#     def test__part_2__sample_input(self):
#         print("")
#         # memory_example = process_program_file_decoder_chip_2(sample_input_file_2)
#         # self.assertEqual(sum_all_memory_addresses(memory_example), 208)
#         self.assertEqual(10, 11)


#     def test__part_2__challenge_input(self):
#         print("")
#         print("Solution to day 16 part 1: {0}".format(-1))
        



 

 
###################################################################################################################################################################
########################################################################## RUN THE TESTS ##########################################################################


# run then unit tests "last"
if __name__ == '__main__':
    unittest.main()
 

