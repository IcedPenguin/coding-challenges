#!/bin/python
# -*- coding: utf-8 -*-
# https://adventofcode.com/2020/day/15


###################################################################################################################################################################
#  
#  Solution to day 15 part 1: 614
#
#  Solution to day 15 part 2: 1065
#
###################################################################################################################################################################

import unittest

###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################
#   
#   --- Day 15: Rambunctious Recitation ---
#   You catch the airport shuttle and try to book a new flight to your vacation island. Due to the 
#   storm, all direct flights have been cancelled, but a route is available to get around the storm. 
#   You take it.
#   
#   While you wait for your flight, you decide to check in with the Elves back at the North Pole. 
#   They're playing a memory game and are ever so excited to explain the rules!
#   
#   In this game, the players take turns saying numbers. They begin by taking turns reading from a list 
#   of starting numbers (your puzzle input). Then, each turn consists of considering the most recently spoken number:
#   
#    *  If that was the first time the number has been spoken, the current player says 0.
#    *  Otherwise, the number had been spoken before; the current player announces how many 
#       turns apart the number is from when it was previously spoken.
#   
#   So, after the starting numbers, each turn results in that player speaking aloud either 0 (if the 
#       last number is new) or an age (if the last number is a repeat).
#   
#   For example, suppose the starting numbers are 0,3,6:
#   
#       Turn 1: The 1st number spoken is a starting number, 0.
#       Turn 2: The 2nd number spoken is a starting number, 3.
#       Turn 3: The 3rd number spoken is a starting number, 6.
#       Turn 4: Now, consider the last number spoken, 6. Since that was the first time the number 
#               had been spoken, the 4th number spoken is 0.
#       Turn 5: Next, again consider the last number spoken, 0. Since it had been spoken before, 
#               the next number to speak is the difference between the turn number when it was 
#               last spoken (the previous turn, 4) and the turn number of the time it was most 
#               recently spoken before then (turn 1). Thus, the 5th number spoken is 4 - 1, 3.
#       Turn 6: The last number spoken, 3 had also been spoken before, most recently on turns 5 
#               and 2. So, the 6th number spoken is 5 - 2, 3.
#       Turn 7: Since 3 was just spoken twice in a row, and the last two turns are 1 turn apart, 
#               the 7th number spoken is 1.
#       Turn 8: Since 1 is new, the 8th number spoken is 0.
#       Turn 9: 0 was last spoken on turns 8 and 4, so the 9th number spoken is the difference between them, 4.
#       Turn 10: 4 is new, so the 10th number spoken is 0.
#       (The game ends when the Elves get sick of playing or dinner is ready, whichever comes first.)
#   
#   Their question for you is: what will be the 2020th number spoken? In the example above, 
#   the 2020th number spoken will be 436.
#   
#   Here are a few more examples:
#   
#       Given the starting numbers 1,3,2, the 2020th number spoken is 1.
#       Given the starting numbers 2,1,3, the 2020th number spoken is 10.
#       Given the starting numbers 1,2,3, the 2020th number spoken is 27.
#       Given the starting numbers 2,3,1, the 2020th number spoken is 78.
#       Given the starting numbers 3,2,1, the 2020th number spoken is 438.
#       Given the starting numbers 3,1,2, the 2020th number spoken is 1836.
#   
#   Given your starting numbers, what will be the 2020th number spoken?
#   
#   Your puzzle input is 14,3,1,0,9,5.
#   

def test_equal(actual, expected, message):
    if actual != expected:
        print("FAIL: Found={0}  Expected={1}    {2}".format(actual, expected, message))


sample_input_file_1 = "2020_15_sample_1.txt"
sample_input_file_2 = "2020_15_sample_2.txt"
input_file          = "2020_15_input.txt"


class ClassName:
    def __init__(self):
        pass


def find_next_number(starting_numbers, number_tracker, previous_number_spoken):
    # while there are still starting numbers -> assign that.
    if starting_numbers != None and len(starting_numbers) > 0:
        return starting_numbers.pop(0)

    turns_previous_number_spoken_during = number_tracker[previous_number_spoken]

    if len(turns_previous_number_spoken_during) == 1:
        return 0

    else:
        return turns_previous_number_spoken_during[1] - turns_previous_number_spoken_during[0]
    

def update_turn_count_for_number(number_tracker, turn, current_number):
    entry = number_tracker.get(current_number)

    if entry is None:
        number_tracker[current_number]  = [turn]

    elif len(entry) == 1:
        number_tracker[current_number].append(turn)  
        
    else:
        number_tracker[current_number].pop(0)           # throw away front of the list
        number_tracker[current_number].append(turn)    

def play_game(starting_numbers, turn_to_terminate_at):
    number_tracker = {}
    turn = 1
    next_number = None

    while turn <= turn_to_terminate_at:
        next_number = find_next_number(starting_numbers, number_tracker, next_number)
        update_turn_count_for_number(number_tracker, turn, next_number)

        # print("turn: t={0} \tnext={1} \tm={2}".format(turn, next_number, number_tracker))
        turn += 1

        # purely so I can watch the progress of the really long game.
        if turn % 100000 == 0:
            print("turn {0}".format(turn))

    return next_number

### play_game

class Day15PartOneTests(unittest.TestCase):

    def test__p1__sample1(self):
        self.assertEqual( play_game([0,3,6], 1), 0)
        self.assertEqual( play_game([0,3,6], 2), 3)
        self.assertEqual( play_game([0,3,6], 3), 6)
        self.assertEqual( play_game([0,3,6], 4), 0)
        self.assertEqual( play_game([0,3,6], 5), 3)
        self.assertEqual( play_game([0,3,6], 6), 3)
        self.assertEqual( play_game([0,3,6], 7), 1)
        self.assertEqual( play_game([0,3,6], 8), 0)
        self.assertEqual( play_game([0,3,6], 9), 4)
        self.assertEqual( play_game([0,3,6],10), 0)


    def test__p1__sample1(self):
        self.assertEqual( play_game([1,3,2], 2020), 1)
        self.assertEqual( play_game([2,1,3], 2020), 10)
        self.assertEqual( play_game([1,2,3], 2020), 27)
        self.assertEqual( play_game([2,3,1], 2020), 78)
        self.assertEqual( play_game([3,2,1], 2020), 438)
        self.assertEqual( play_game([3,1,2], 2020), 1836)

    
    def test__part_1__challenge_input(self):
        print("")
        last_number_spoken = play_game([14,3,1,0,9,5], 2020)
        print("Solution to day 15 part 1: {0}".format(last_number_spoken))
        




###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################


class Day15PartTwoTests(unittest.TestCase):
    
    def test__part_2__challenge_input(self):
        print("")
        last_number_spoken = play_game([14,3,1,0,9,5], 30000000)
        print("Solution to day 15 part 2: {0}".format(last_number_spoken))


 
###################################################################################################################################################################
########################################################################## RUN THE TESTS ##########################################################################


# run then unit tests "last"
if __name__ == '__main__':
    unittest.main()
 

