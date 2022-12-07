#!/bin/python
# -*- coding: utf-8 -*-
# https://adventofcode.com/2021/day/4


###################################################################################################################################################################
#  
#  Solution to day 4 part 1: 45031
#
#  Solution to day 4 part 2: 2568
#
###################################################################################################################################################################

import unittest

###################################################################################################################################################################
############################################################################# Common ##############################################################################


sample_input_file_1 = "2021_sample_1.txt"
sample_input_file_2 = "2021_sample_2.txt"
input_file          = "2021_input.txt"


def read_file_into_array(filename, asInt):
    lines = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if asInt:
                lines.append(int(line))
            else:
                lines.append(line)

    return lines
### read_file_into_array

###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################
#  
#  --- Day 4: Giant Squid ---
#  You're already almost 1.5km (almost a mile) below the surface of the ocean, already so 
#  deep that you can't see any sunlight. What you can see, however, is a giant squid that has 
#  attached itself to the outside of your submarine.
#  
#  Maybe it wants to play bingo?
#  
#  Bingo is played on a set of boards each consisting of a 5x5 grid of numbers. Numbers are chosen 
#  at random, and the chosen number is marked on all boards on which it appears. (Numbers may not 
#      appear on all boards.) If all numbers in any row or any column of a board are marked, that 
#  board wins. (Diagonals don't count.)
#  
#  The submarine has a bingo subsystem to help passengers (currently, you and the giant squid) pass 
#  the time. It automatically generates a random order in which to draw numbers and a random set of 
#  boards (your puzzle input). For example:
#  
#      7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1
#  
#      22 13 17 11  0
#       8  2 23  4 24
#      21  9 14 16  7
#       6 10  3 18  5
#       1 12 20 15 19
#  
#       3 15  0  2 22
#       9 18 13 17  5
#      19  8  7 25 23
#      20 11 10 24  4
#      14 21 16 12  6
#  
#      14 21 17 24  4
#      10 16 15  9 19
#      18  8 23 26 20
#      22 11 13  6  5
#       2  0 12  3  7
#  
#  After the first five numbers are drawn (7, 4, 9, 5, and 11), there are no winners, but the boards are 
#  marked as follows (shown here adjacent to each other to save space):
#  
#      22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
#       8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
#      21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
#       6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
#       1 12 20 15 19        14 21 16 12  6         2  0 12  3  7
#  
#  After the next six numbers are drawn (17, 23, 2, 0, 14, and 21), there are still no winners:
#  
#      22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
#       8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
#      21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
#       6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
#       1 12 20 15 19        14 21 16 12  6         2  0 12  3  7
#  
#  Finally, 24 is drawn:
#  
#      22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
#       8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
#      21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
#       6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
#       1 12 20 15 19        14 21 16 12  6         2  0 12  3  7
#  
#  At this point, the third board wins because it has at least one complete row or column of marked 
#  numbers (in this case, the entire top row is marked: 14 21 17 24 4).
#  
#  The score of the winning board can now be calculated. Start by finding the sum of all unmarked 
#  numbers on that board; in this case, the sum is 188. Then, multiply that sum by the number that 
#  was just called when the board won, 24, to get the final score, 188 * 24 = 4512.
#  
#  To guarantee victory against the giant squid, figure out which board will win first. What will 
#  your final score be if you choose that board?
#  




class BingoBoard:

    MARK = "X"

    def __init__(self, board_numbers, board_id=-1):
        self.board_id = board_id
        self.numbers = board_numbers.split()
        self.marked = ["_"] * 25


    def print_board(self):
        for column in range(5):
            for row in range(5):
                print("{0:>4}:{1}".format( self.numbers[column*5 + row], self.marked[column*5 + row]), end="")
            print("")
        print("")
    ### print_board


    def has_bingo(self):
        if (
            # hard-code possible bingos
            # rows
            (self.marked[0]  == BingoBoard.MARK and self.marked[1]  == BingoBoard.MARK and self.marked[2]  == BingoBoard.MARK and self.marked[3]  == BingoBoard.MARK and self.marked[4]  == BingoBoard.MARK) or
            (self.marked[5]  == BingoBoard.MARK and self.marked[6]  == BingoBoard.MARK and self.marked[7]  == BingoBoard.MARK and self.marked[8]  == BingoBoard.MARK and self.marked[9]  == BingoBoard.MARK) or
            (self.marked[10] == BingoBoard.MARK and self.marked[11] == BingoBoard.MARK and self.marked[12] == BingoBoard.MARK and self.marked[13] == BingoBoard.MARK and self.marked[14] == BingoBoard.MARK) or
            (self.marked[15] == BingoBoard.MARK and self.marked[16] == BingoBoard.MARK and self.marked[17] == BingoBoard.MARK and self.marked[18] == BingoBoard.MARK and self.marked[19] == BingoBoard.MARK) or
            (self.marked[20] == BingoBoard.MARK and self.marked[21] == BingoBoard.MARK and self.marked[22] == BingoBoard.MARK and self.marked[23] == BingoBoard.MARK and self.marked[24] == BingoBoard.MARK) 
            or # columns
            (self.marked[0]  == BingoBoard.MARK and self.marked[5]  == BingoBoard.MARK and self.marked[10] == BingoBoard.MARK and self.marked[15] == BingoBoard.MARK and self.marked[20] == BingoBoard.MARK) or
            (self.marked[1]  == BingoBoard.MARK and self.marked[6]  == BingoBoard.MARK and self.marked[11] == BingoBoard.MARK and self.marked[16] == BingoBoard.MARK and self.marked[21] == BingoBoard.MARK) or
            (self.marked[2]  == BingoBoard.MARK and self.marked[7]  == BingoBoard.MARK and self.marked[12] == BingoBoard.MARK and self.marked[17] == BingoBoard.MARK and self.marked[22] == BingoBoard.MARK) or
            (self.marked[3]  == BingoBoard.MARK and self.marked[8]  == BingoBoard.MARK and self.marked[13] == BingoBoard.MARK and self.marked[18] == BingoBoard.MARK and self.marked[23] == BingoBoard.MARK) or
            (self.marked[4]  == BingoBoard.MARK and self.marked[9]  == BingoBoard.MARK and self.marked[14] == BingoBoard.MARK and self.marked[19] == BingoBoard.MARK and self.marked[24] == BingoBoard.MARK) 
            # or # diagonal
            # (self.marked[0]  == BingoBoard.MARK and self.marked[6]  == BingoBoard.MARK and self.marked[12] == BingoBoard.MARK and self.marked[18] == BingoBoard.MARK and self.marked[24] == BingoBoard.MARK) or
            # (self.marked[4]  == BingoBoard.MARK and self.marked[8]  == BingoBoard.MARK and self.marked[12] == BingoBoard.MARK and self.marked[16] == BingoBoard.MARK and self.marked[20] == BingoBoard.MARK) 
        ):
            return True
        else:
            return False
    ### has_bingo


    def next_number(self, number):

        try:
            idx = self.numbers.index(number)
            self.marked[idx] = BingoBoard.MARK
        except ValueError:
            pass
        
    ### next_number


    def get_board_value(self):
        score = 0
        for i in range(25):
            if self.marked[i] != BingoBoard.MARK:
                score += int(self.numbers[i])

        return score
    ### get_board_value

    def __str__(self):
        return "Board:{0}:{1}".format(self.board_id, self.get_board_value())

    def __repr__(self):
        return self.__str__()



def parse_input_file(file_name):
    input_array = read_file_into_array(file_name, False)

    moves = input_array.pop(0)

    boards = []
    while len(input_array) > 0:
        input_array.pop(0) # throw away empty line
        board_contents = input_array.pop(0) + " "
        board_contents += input_array.pop(0) + " "
        board_contents += input_array.pop(0) + " "
        board_contents += input_array.pop(0) + " "
        board_contents += input_array.pop(0)

        boards.append( BingoBoard(board_contents, len(boards) +1) )

    return moves, boards
### parse_input_file


def find_winning_board(moves, boards): 
    moves = moves.split(",")
    for move in moves:
        for board in boards:
            board.next_number(move)

            if board.has_bingo():
                return move, board

    raise NotImplementedError()
### find_winning_board


class Day4PartOneTests(unittest.TestCase):

    
    def test__part_1__sample_input_row_bingo(self):
        # print("")
        b = BingoBoard("1 2 3 4 8 6 7 5      9 10  11 12 13 14 15 16 17 18 19 20 21 22 23 24 25")

        b.next_number("1")
        b.next_number("2")
        b.next_number("3")
        b.next_number("4")
        self.assertFalse(b.has_bingo())

        b.next_number("8")
        self.assertTrue(b.has_bingo())



    def test__part_1__sample_input_column_bingo(self):
        # print("")
        b = BingoBoard("1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25")

        b.next_number("2")
        b.next_number("7")
        b.next_number("12")
        b.next_number("17")
        self.assertFalse(b.has_bingo())

        b.next_number("22")
        self.assertTrue(b.has_bingo())


    # def test__part_1__sample_input_diagonal_bingo(self):
    #     # print("")
    #     b = BingoBoard("1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25")

    #     b.next_number("5")
    #     b.next_number("9")
    #     b.next_number("13")
    #     b.next_number("17")
    #     self.assertFalse(b.has_bingo())
    #     b.next_number("21")
    #     self.assertTrue(b.has_bingo())
    #     # b.print_board()


    def test__part_1__sample_input(self):
        moves, boards = parse_input_file(sample_input_file_1)
        move, board = find_winning_board(moves, boards)
        board_score = board.get_board_value()

        self.assertEqual(move, "24")
        self.assertEqual(board_score, 188)
        

    def test__part_1__challenge_input(self):
        moves, boards = parse_input_file(input_file)
        boards.pop(0)
        boards.pop(0)
        move, board = find_winning_board(moves, boards)
        board_score = board.get_board_value()

        print("Solution to day 4 part 1: {0}".format(int(move) * board_score))
        


###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################
#
#  --- Part Two ---
#  On the other hand, it might be wise to try a different strategy: let the giant squid win.
#  
#  You aren't sure how many bingo boards a giant squid could play at once, so rather than waste time 
#  counting its arms, the safe thing to do is to figure out which board will win last and choose that 
#  one. That way, no matter which boards it picks, it will win for sure.
#  
#  In the above example, the second board is the last to win, which happens after 13 is eventually 
#  called and its middle column is completely marked. If you were to keep playing until this point, 
#  the second board would have a sum of unmarked numbers equal to 148 for a final score of 148 * 13 = 1924.
#  
#  Figure out which board will win last. Once it wins, what would its final score be?
#  


def find_board_that_wins_last(moves, boards):
    
    moves = moves.split(",")

    move_winners = []
    

    for move in moves:
        winning_boards = []
        still_playing = []
        
        for board in boards:
            board.next_number(move)

            if board.has_bingo():
                winning_boards.append(board)
            else:
                still_playing.append(board)

        boards = still_playing[:]

        if len(winning_boards) > 0:
            move_winners.append( (move, winning_boards) )


    # find loosing boards
    # print(move_winners[-1])

    return move_winners[-1][0], move_winners[-1][1]
### find_board_that_wins_last


class Day4PartTwoTests(unittest.TestCase):

    
    def test__part_2__sample_input(self):
        moves, boards = parse_input_file(sample_input_file_1)
        move, board = find_board_that_wins_last(moves, boards)
        board_score = board[0].get_board_value()

        self.assertEqual(move, "13")
        self.assertEqual(board_score, 148)


    def test__part_2__challenge_input(self):
        print("")
        moves, boards = parse_input_file(input_file)
        move, boards = find_board_that_wins_last(moves, boards)

        print(move)
        print(boards)

        print("Solution to day 4 part 2: {0}".format(int(move) * boards[0].get_board_value()))
        

 
###################################################################################################################################################################
########################################################################## RUN THE TESTS ##########################################################################


# run then unit tests "last"
if __name__ == '__main__':
    unittest.main()
 

