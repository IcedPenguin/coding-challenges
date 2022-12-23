#!/bin/python
# -*- coding: utf-8 -*-
# https://adventofcode.com/2022/day/2


###################################################################################################################################################################
#  
#  Solution to part 1: 11841
#
#  Solution to part 2: 13022
#
###################################################################################################################################################################

import unittest

###################################################################################################################################################################
#  --- Day 2: Rock Paper Scissors ---
#  
#  The Elves begin to set up camp on the beach. To decide whose tent gets to be closest to the snack storage, a giant 
#  Rock Paper Scissors tournament is already in progress.
#  
#  Rock Paper Scissors is a game between two players. Each game contains many rounds; in each round, the players each 
#  simultaneously choose one of Rock, Paper, or Scissors using a hand shape. Then, a winner for that round is selected: 
#  Rock defeats Scissors, Scissors defeats Paper, and Paper defeats Rock. If both players choose the same shape, the 
#  round instead ends in a draw.
#  
#  Appreciative of your help yesterday, one Elf gives you an encrypted strategy guide (your puzzle input) that they say 
#  will be sure to help you win. "The first column is what your opponent is going to play: A for Rock, B for Paper, and 
#  C for Scissors. The second column--" Suddenly, the Elf is called away to help with someone's tent.
#  
#  The second column, you reason, must be what you should play in response: X for Rock, Y for Paper, and Z for Scissors. 
#  Winning every time would be suspicious, so the responses must have been carefully chosen.
#  
#  The winner of the whole tournament is the player with the highest score. Your total score is the sum of your scores for 
#  each round. The score for a single round is the score for the shape you selected (1 for Rock, 2 for Paper, and 3 for 
#      Scissors) plus the score for the outcome of the round (0 if you lost, 3 if the round was a draw, and 6 if you won).
#  
#  Since you can't be sure if the Elf is trying to help you or trick you, you should calculate the score you would get 
#  if you were to follow the strategy guide.
#  
#  For example, suppose you were given the following strategy guide:
#  
#      A Y
#      B X
#      C Z
#  
#  This strategy guide predicts and recommends the following:
#  
#      In the first round, your opponent will choose Rock (A), and you should choose Paper (Y). This ends in a 
#      win for you with a score of 8 (2 because you chose Paper + 6 because you won).
#
#      In the second round, your opponent will choose Paper (B), and you should choose Rock (X). This ends in a 
#      loss for you with a score of 1 (1 + 0).
#
#      The third round is a draw with both players choosing Scissors, giving you a score of 3 + 3 = 6.
#  
#  In this example, if you were to follow the strategy guide, you would get a total score of 15 (8 + 1 + 6).
#  
#  What would your total score be if everything goes exactly according to your strategy guide?
#  
############################################################################ PROBLEM 1 ############################################################################


puzzle_day          = 2
sample_input_file_1 = "2022_{0:02d}_sample_1.txt".format(puzzle_day)
input_file          = "2022_{0:02d}_input.txt".format(puzzle_day)


def load_file(file_path):
    file_ptr = open(file_path, "r")
    data = file_ptr.read()
    file_ptr.close()
    return data


game_rules = {
    "AX": ("draw", 3), #
    "AY": ("win",  6),
    "AZ": ("lose", 0),
    "BX": ("lose", 0),
    "BY": ("draw", 3), #
    "BZ": ("win",  6),
    "CX": ("win",  6),
    "CY": ("lose", 0),
    "CZ": ("draw", 3),  
    "AA": ("draw", 3), 
    "AB": ("win",  6),
    "AC": ("lose", 0),
    "BA": ("lose", 0),
    "BB": ("draw", 3), #
    "BC": ("win",  6),
    "CA": ("win",  6),
    "CB": ("lose", 0),
    "CC": ("draw", 3)  # 
}

movement_score = {
    "A": 1, # Rock
    "B": 2, # Paper
    "C": 3, # Scissors
    "X": 1, # Rock
    "Y": 2, # Paper
    "Z": 3, # Scissors
}



def play_game(opponent_move, our_move, enhanced_moves=None):
    if enhanced_moves is not None:
        our_move = enhanced_moves[opponent_move + our_move]

    result, game_score = game_rules[opponent_move + our_move]
    move_score = movement_score[our_move]

    return game_score + move_score
### play_game


def play_rounds(file, enhanced_moves=None):
    total_score = 0
    rounds = load_file(file)
    rounds = rounds.split("\n")

    for game in rounds:
        moves = game.split()
        total_score += play_game(moves[0], moves[1], enhanced_moves)

    return total_score
### play_rounds


class Day2PartOneTests(unittest.TestCase):

    def test__p1__sample1(self):
        score = play_game("A", "Y")
        self.assertEqual( score, 8)
        
        score = play_game("B", "X")
        self.assertEqual( score, 1)

        score = play_game("C", "Z")
        self.assertEqual( score, 6)
        


    def test__p1__sample2(self):
        score = play_rounds(sample_input_file_1)
        self.assertEqual( score, 15)

    
    def test__part_1__challenge_input(self):
        print("")
        score = play_rounds(input_file)
        print("Solution to day {0} part 1: {1}".format(puzzle_day, score))
        


###################################################################################################################################################################
#   --- Part Two ---
#   
#   The Elf finishes helping with the tent and sneaks back over to you. "Anyway, the second column says how the 
#   round needs to end: X means you need to lose, Y means you need to end the round in a draw, and Z means you 
#   need to win. Good luck!"
#   
#   The total score is still calculated in the same way, but now you need to figure out what shape to choose so 
#   the round ends as indicated. The example above now goes like this:
#   
#       In the first round, your opponent will choose Rock (A), and you need the round to end in a draw (Y), so you 
#       also choose Rock. This gives you a score of 1 + 3 = 4.
#       
#       In the second round, your opponent will choose Paper (B), and you choose Rock so you lose (X) with a 
#       score of 1 + 0 = 1.
#       
#       In the third round, you will defeat your opponent's Scissors with Rock for a score of 1 + 6 = 7.
#   
#   Now that you're correctly decrypting the ultra top secret strategy guide, you would get a total score of 12.
#   
#   Following the Elf's instructions for the second column, what would your total score be if everything goes exactly 
#   according to your strategy guide?
#   
############################################################################ PROBLEM 2 ############################################################################



determine_move = {
    "AX": "C", 
    "AY": "A", 
    "AZ": "B", 
    "BX": "A", 
    "BY": "B", 
    "BZ": "C", 
    "CX": "B", 
    "CY": "C", 
    "CZ": "A"  
}



class Day2PartTwoTests(unittest.TestCase):
    
    def test__p2__sample1(self):
        score = play_game("A", "Y", determine_move)
        self.assertEqual( score, 4)
        
        score = play_game("B", "X", determine_move)
        self.assertEqual( score, 1)

        score = play_game("C", "Z", determine_move)
        self.assertEqual( score, 7)


    def test__p2__sample2(self):
        score = play_rounds(sample_input_file_1, determine_move)
        self.assertEqual( score, 12)


    def test__part_2__challenge_input(self):
        print("")
        score = play_rounds(input_file, determine_move)
        print("Solution to day {0} part 2: {1}".format(puzzle_day, score))


 
###################################################################################################################################################################
########################################################################## RUN THE TESTS ##########################################################################


# run then unit tests "last"
if __name__ == '__main__':
    unittest.main()
 

