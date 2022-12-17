#!/bin/python
# -*- coding: utf-8 -*-
# https://adventofcode.com/2021/day/21


###################################################################################################################################################################
#  
#  Solution to part 1: 675024
#
#  Solution to part 2: 
#
###################################################################################################################################################################

import unittest

###################################################################################################################################################################
#   --- Day 21: Dirac Dice ---
#   
#   There's not much to do as you slowly descend to the bottom of the ocean. The submarine computer challenges you to a nice game of Dirac Dice.
#   
#   This game consists of a single die, two pawns, and a game board with a circular track containing ten spaces marked 1 through 10 clockwise. 
#   Each player's starting space is chosen randomly (your puzzle input). Player 1 goes first.
#   
#   Players take turns moving. On each player's turn, the player rolls the die three times and adds up the results. Then, the player moves 
#   their pawn that many times forward around the track (that is, moving clockwise on spaces in order of increasing value, wrapping back around 
#       to 1 after 10). So, if a player is on space 7 and they roll 2, 2, and 1, they would move forward 5 times, to spaces 8, 9, 10, 1, and finally stopping on 2.
#   
#   After each player moves, they increase their score by the value of the space their pawn stopped on. Players' scores start at 0. So, if the 
#   first player starts on space 7 and rolls a total of 5, they would stop on space 2 and add 2 to their score (for a total score of 2). The game 
#   immediately ends as a win for any player whose score reaches at least 1000.
#   
#   Since the first game is a practice game, the submarine opens a compartment labeled deterministic dice and a 100-sided die falls out. This die 
#   always rolls 1 first, then 2, then 3, and so on up to 100, after which it starts over at 1 again. Play using this die.
#   
#   For example, given these starting positions:
#   
#       Player 1 starting position: 4
#       Player 2 starting position: 8
#   
#   This is how the game would go:
#   
#       Player 1 rolls 1+2+3 and moves to space 10 for a total score of 10.
#       Player 2 rolls 4+5+6 and moves to space 3 for a total score of 3.
#       Player 1 rolls 7+8+9 and moves to space 4 for a total score of 14.
#       Player 2 rolls 10+11+12 and moves to space 6 for a total score of 9.
#       Player 1 rolls 13+14+15 and moves to space 6 for a total score of 20.
#       Player 2 rolls 16+17+18 and moves to space 7 for a total score of 16.
#       Player 1 rolls 19+20+21 and moves to space 6 for a total score of 26.
#       Player 2 rolls 22+23+24 and moves to space 6 for a total score of 22.
#   
#   ...after many turns...
#   
#       Player 2 rolls 82+83+84 and moves to space 6 for a total score of 742.
#       Player 1 rolls 85+86+87 and moves to space 4 for a total score of 990.
#       Player 2 rolls 88+89+90 and moves to space 3 for a total score of 745.
#       Player 1 rolls 91+92+93 and moves to space 10 for a final score, 1000.
#   
#   Since player 1 has at least 1000 points, player 1 wins and the game ends. At this point, the losing player had 745 points and the die had been 
#   rolled a total of 993 times; 745 * 993 = 739785.
#   
#   Play a practice game using the deterministic 100-sided die. The moment either player wins, what do you get if you multiply the score of the 
#   losing player by the number of times the die was rolled during the game?
#   
############################################################################ PROBLEM 1 ############################################################################


puzzle_day          = 21
sample_input_file_1 = "2021_{0:02d}_sample_1.txt".format(puzzle_day)
input_file          = "2021_{0:02d}_input.txt".format(puzzle_day)


def load_file(file_path):
    file_ptr = open(file_path, "r")
    data = file_ptr.read()
    file_ptr.close()
    return data




class DeterministicDie:
    def __init__(self, sides=100):
        self.sides = sides
        self.currentFace = sides
        self.roll_count = 0        


    def __repr__(self):
        return "[DeterministicDie: sides={0}, face={1}, roll_count={2}]".format(self.sides, self.currentFace, self.roll_count)


    def roll(self):
        self.roll_count += 1
        self.currentFace += 1

        if self.currentFace > self.sides:
            self.currentFace = 1

        return self.currentFace



class Player:
    def __init__(self, player_id, staringPosition):
        self.player_id = player_id
        self.position = staringPosition
        self.score = 0
        


    def __repr__(self):
        return "[Player: if={0}, position={1}, score={2}]".format(self.player_id, self.position, self.score)


    def score_points(self, points):
        self.score += points



class DiracBoard:
    def __init__(self, spaces, die, winning_score):
        self.spaces = spaces
        self.die = die
        self.winning_score = winning_score
        self.players = []


    def add_player(self, player_id, staring_position):
        player = Player(player_id, staring_position -1)
        self.players.append(player)


    def play_game(self):
        game_over = False
        while not game_over:
            
            for player in self.players:
                game_over = self.move_player(player)
                if game_over:
                    break


    def move_player(self, player):
        m1 = self.die.roll()
        m2 = self.die.roll()
        m3 = self.die.roll()

        # position of 0 = start of board, 1 point.
        # position of self.spaces -1 = end of board, self.die points
        new_player_location = (player.position + m1 + m2 + m3) % self.spaces
        player.position = new_player_location
        player.score_points(new_player_location +1)

        # print("Player {0} rolls {1}+{2}+{3} and moves to space {4} for a total score of {5}.".format(player.player_id, m1, m2, m3, new_player_location+1, player.score))

        return player.score >= self.winning_score


    def is_winner(self, player):
        return self.winning_score <= player.score


def build_game_pieces(game_file):
    die = DeterministicDie(100)
    board = DiracBoard(10, die, 1000)

    file_contents = load_file(game_file)
    lines = file_contents.split("\n")
    parts = lines[0].split(" ")
    board.add_player(int(parts[1]), int(parts[4]))
    parts = lines[1].split(" ")
    board.add_player(int(parts[1]), int(parts[4]))

    return die, board



class Day21PartOneTests(unittest.TestCase):

    def test__p1__sample1(self):
        die = DeterministicDie(3)
        self.assertEqual(die.roll(), 1)
        self.assertEqual(die.roll(), 2)
        self.assertEqual(die.roll(), 3)
        self.assertEqual(die.roll(), 1)
        self.assertEqual(die.roll(), 2)

        self.assertEqual(die.roll_count, 5)


    def test__p1__sample2(self):
        die, board = build_game_pieces(sample_input_file_1)
        board.play_game()

        self.assertEqual(board.players[0].score, 1000)
        self.assertEqual(board.players[1].score, 745)
        self.assertEqual(die.roll_count, 993)
        self.assertEqual(board.players[1].score * die.roll_count, 739785)
        

    
    def test__part_1__challenge_input(self):
        print("")
        die, board = build_game_pieces(input_file)
        print (input_file)
        board.play_game()
        lossing_score = min(board.players[0].score, board.players[1].score)

        print("Solution to day 21 part 1: {0}".format(lossing_score * die.roll_count, None))
        


###################################################################################################################################################################
#   --- Part Two ---
#   
#   Now that you're warmed up, it's time to play the real game.
#   
#   A second compartment opens, this time labeled Dirac dice. Out of it falls a single three-sided die.
#   
#   As you experiment with the die, you feel a little strange. An informational brochure in the compartment explains that 
#   this is a quantum die: when you roll it, the universe splits into multiple copies, one copy for each possible outcome 
#   of the die. In this case, rolling the die always splits the universe into three copies: one where the outcome of the 
#   roll was 1, one where it was 2, and one where it was 3.
#   
#   The game is played the same as before, although to prevent things from getting too far out of hand, the game now ends 
#   when either player's score reaches at least 21.
#   
#   Using the same starting positions as in the example above, player 1 wins in 444356092776315 universes, while player 2 
#   merely wins in 341960390180808 universes.
#   
#   Using your given starting positions, determine every possible outcome. Find the player that wins in more universes; 
#   in how many universes does that player win?
#   
############################################################################ PROBLEM 2 ############################################################################



class Day21PartTwoTests(unittest.TestCase):
    
    def test__p2__sample1(self):
        pass
        

    def test__part_2__challenge_input(self):
        print("")
        print("Solution to day {0} part 2: {1}".format(puzzle_day, None))


 
###################################################################################################################################################################
########################################################################## RUN THE TESTS ##########################################################################


# run then unit tests "last"
if __name__ == '__main__':
    unittest.main()
 

