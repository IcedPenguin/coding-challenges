#!/bin/python
# -*- coding: utf-8 -*-
# https://adventofcode.com/2021/day/10


###################################################################################################################################################################
#  
#  Solution to day 10 part 1: 387363
#
#  Solution to day 10 part 2: 4330777059
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

def read_and_parse_single_line_input(filename, delimeter, asInt):
    array = read_file_into_array(filename, False)
    parts = array[0].split(delimeter)
    return parts
### read_and_parse_single_line_input


###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################
#  
#  --- Day 10: Syntax Scoring ---
#  You ask the submarine to determine the best route out of the deep-sea cave, but it only replies:
#  
#  Syntax error in navigation subsystem on line: all of them
#  All of them?! The damage is worse than you thought. You bring up a copy of the navigation subsystem (your puzzle input).
#  
#  The navigation subsystem syntax is made of several lines containing chunks. There are one or more chunks 
#  on each line, and chunks contain zero or more other chunks. Adjacent chunks are not separated by any 
#  delimiter; if one chunk stops, the next chunk (if any) can immediately start. Every chunk must open 
#  and close with one of four legal pairs of matching characters:
#  
#  If a chunk opens with (, it must close with ).
#  If a chunk opens with [, it must close with ].
#  If a chunk opens with {, it must close with }.
#  If a chunk opens with <, it must close with >.
#  So, () is a legal chunk that contains no other chunks, as is []. More complex but valid chunks 
#  include ([]), {()()()}, <([{}])>, [<>({}){}[([])<>]], and even (((((((((()))))))))).
#  
#  Some lines are incomplete, but others are corrupted. Find and discard the corrupted lines first.
#  
#  A corrupted line is one where a chunk closes with the wrong character - that is, where the characters 
#  it opens and closes with do not form one of the four legal pairs listed above.
#  
#  Examples of corrupted chunks include (], {()()()>, (((()))}, and <([]){()}[{}]). Such a chunk can appear 
#      anywhere within a line, and its presence causes the whole line to be considered corrupted.
#  
#  For example, consider the following navigation subsystem:
#  
#      [({(<(())[]>[[{[]{<()<>>
#      [(()[<>])]({[<{<<[]>>(
#      {([(<{}[<>[]}>{[]{[(<()>
#      (((({<>}<{<{<>}{[]{[]{}
#      [[<[([]))<([[{}[[()]]]
#      [{[{({}]{}}([{[{{{}}([]
#      {<[[]]>}<{[{[{[]{()[[[]
#      [<(<(<(<{}))><([]([]()
#      <{([([[(<>()){}]>(<<{{
#      <{([{{}}[<[[[<>{}]]]>[]]
#  
#  Some of the lines aren't corrupted, just incomplete; you can ignore these lines for now. The remaining five lines are corrupted:
#  
#      {([(<{}[<>[]}>{[]{[(<()> - Expected ], but found } instead.
#      [[<[([]))<([[{}[[()]]] - Expected ], but found ) instead.
#      [{[{({}]{}}([{[{{{}}([] - Expected ), but found ] instead.
#      [<(<(<(<{}))><([]([]() - Expected >, but found ) instead.
#      <{([([[(<>()){}]>(<<{{ - Expected ], but found > instead.
#  
#  Stop at the first incorrect closing character on each corrupted line.
#  
#  Did you know that syntax checkers actually have contests to see who can get the high score for syntax errors in a 
#  file? It's true! To calculate the syntax error score for a line, take the first illegal character on the line and 
#  look it up in the following table:
#  
#      ): 3 points.
#      ]: 57 points.
#      }: 1197 points.
#      >: 25137 points.
#  
#  In the above example, an illegal ) was found twice (2*3 = 6 points), an illegal ] was found once (57 points), an 
#  illegal } was found once (1197 points), and an illegal > was found once (25137 points). So, the total syntax error 
#  score for this file is 6+57+1197+25137 = 26397 points!
#  
#  Find the first illegal character in each corrupted line of the navigation subsystem. 
#  What is the total syntax error score for those errors?
#  
#  



# h (, it must close with ).
# If a chunk opens with [, it must close with ].
# If a chunk opens with {, it must close with }.
# If a chunk opens with <, it must close with >.

opening_symbols = ["(", "[", "{", "<"]
closing_symbpls = [")", "]", "}", ">"]
closing_symbols_map = {"(": ")", "[": "]", "{": "}", "<": ">"}
corrupt_symbol_points= {")": 3, "]": 57, "}": 1197, ">": 25137}


def process_chunk(chunk):
    # print(chunk)
    stack = []

    for symbol in chunk:
        if symbol in opening_symbols:
            stack.append(symbol)
            # print("opening:  \t{0}".format(symbol))

        elif symbol in closing_symbpls:
            tail = stack.pop()

            if closing_symbols_map[tail] == symbol:
                # we pared an opening with a closing. great.
                # print("closing:  \t{0}".format(symbol))
                pass 

            else:
                # print("corrupt:  \t{0}".format(symbol))
                return "corrupted", symbol


        else:
            raise Error()

    # we are out of symbols
    if len(stack) == 0:
        return "complete", None

    else: 
        return "incomplete", stack


def score_all_illegal_characters(chunks):
    score = 0
    for chunk in chunks:
        result, char = process_chunk(chunk)

        if result == "corrupted":
            score += corrupt_symbol_points[char]

    return score


class Day10PartOneTests(unittest.TestCase):

    
    def test__part_1__corrupt_chunks(self):

        result, char = process_chunk("{([(<{}[<>[]}>{[]{[(<()>")
        self.assertEqual("corrupted", result)
        self.assertEqual("}", char)

        result, char = process_chunk("[[<[([]))<([[{}[[()]]]")
        self.assertEqual("corrupted", result)
        self.assertEqual(")", char)

        result, char = process_chunk("[{[{({}]{}}([{[{{{}}([]")
        self.assertEqual("corrupted", result)
        self.assertEqual("]", char)

        result, char = process_chunk("[<(<(<(<{}))><([]([]()")
        self.assertEqual("corrupted", result)
        self.assertEqual(")", char)

        result, char = process_chunk("<{([([[(<>()){}]>(<<{{")
        self.assertEqual("corrupted", result)
        self.assertEqual(">", char)


    def test__part_1__sample_input(self):
        print("")
        chunks = read_file_into_array(sample_input_file_1, False)
        score = score_all_illegal_characters(chunks)
        self.assertEqual(26397, score)

    def test__part_1__challenge_input(self):
        print("")
        chunks = read_file_into_array(input_file, False)
        score = score_all_illegal_characters(chunks)
        print("Solution to day 10 part 1: {0}".format(score))
        


###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################
#   
#   --- Part Two ---
#   Now, discard the corrupted lines. The remaining lines are incomplete.
#   
#   Incomplete lines don't have any incorrect characters - instead, they're missing some closing characters 
#   at the end of the line. To repair the navigation subsystem, you just need to figure out the sequence of 
#   closing characters that complete all open chunks in the line.
#   
#   You can only use closing characters (), ], }, or >), and you must add them in the correct order so that 
#   only legal pairs are formed and all chunks end up closed.
#   
#   In the example above, there are five incomplete lines:
#   
#       [({(<(())[]>[[{[]{<()<>> - Complete by adding }}]])})].
#       [(()[<>])]({[<{<<[]>>( - Complete by adding )}>]}).
#       (((({<>}<{<{<>}{[]{[]{} - Complete by adding }}>}>)))).
#       {<[[]]>}<{[{[{[]{()[[[] - Complete by adding ]]}}]}]}>.
#       <{([{{}}[<[[[<>{}]]]>[]] - Complete by adding ])}>.
#   
#   Did you know that autocomplete tools also have contests? It's true! The score is determined by considering 
#   the completion string character-by-character. Start with a total score of 0. Then, for each character, 
#   multiply the total score by 5 and then increase the total score by the point value given for the character 
#   in the following table:
#   
#       ): 1 point.
#       ]: 2 points.
#       }: 3 points.
#       >: 4 points.
#   
#   So, the last completion string above - ])}> - would be scored as follows:
#   
#       Start with a total score of 0.
#       Multiply the total score by 5 to get 0, then add the value of ] (2) to get a new total score of 2.
#       Multiply the total score by 5 to get 10, then add the value of ) (1) to get a new total score of 11.
#       Multiply the total score by 5 to get 55, then add the value of } (3) to get a new total score of 58.
#       Multiply the total score by 5 to get 290, then add the value of > (4) to get a new total score of 294.
#   
#   The five lines' completion strings have total scores as follows:
#   
#       }}]])})] - 288957 total points.
#       )}>]}) - 5566 total points.
#       }}>}>)))) - 1480781 total points.
#       ]]}}]}]}> - 995444 total points.
#       ])}> - 294 total points.
#   
#   Autocomplete tools are an odd bunch: the winner is found by sorting all of the scores and then taking the 
#   middle score. (There will always be an odd number of scores to consider.) In this example, the middle score 
#   is 288957 because there are the same number of scores smaller and larger than it.
#   
#   Find the completion string for each incomplete line, score the completion strings, and sort the scores. 
#   What is the middle score?
#   

incomplete_symbol_points= {")": 1, "]": 2, "}": 3, ">": 4}
def score_incomplete_chunk(chunk):
    score = 0

    while len(chunk) != 0:
        symbol = chunk.pop()
        closing_symbol = closing_symbols_map[symbol]
        symbol_score = incomplete_symbol_points[closing_symbol]
        tmp_score = (score * 5) + symbol_score

        # print("{0} -> {1}  symbol_s={2} old_score={3} new_score={4}".format(symbol, closing_symbol, symbol_score, score, tmp_score))

        score = tmp_score
    return score

def get_winning_incomplete_score(chunks):
    scores = []

    for chunk in chunks:
        result, stack = process_chunk(chunk)
        if result == "incomplete":
            score = score_incomplete_chunk(stack)
            scores.append(score)

    scores = sorted(scores)
    return scores[int( len(scores) * 0.5)]


class Day10PartTwoTests(unittest.TestCase):
    
    def test__part_1__corrupt_chunks(self):

        result, stack = process_chunk("[({(<(())[]>[[{[]{<()<>>") # - Complete by adding }}]])})].
        score = score_incomplete_chunk(stack)
        self.assertEqual("incomplete", result)
        self.assertEqual(288957, score)


        result, stack = process_chunk("[(()[<>])]({[<{<<[]>>(") # - Complete by adding )}>]}).
        score = score_incomplete_chunk(stack)
        self.assertEqual("incomplete", result)
        self.assertEqual(5566, score)


        result, stack = process_chunk("(((({<>}<{<{<>}{[]{[]{}") # - Complete by adding }}>}>)))).
        score = score_incomplete_chunk(stack)
        self.assertEqual("incomplete", result)
        self.assertEqual(1480781, score)


        result, stack = process_chunk("{<[[]]>}<{[{[{[]{()[[[]") # - Complete by adding ]]}}]}]}>.
        score = score_incomplete_chunk(stack)
        self.assertEqual("incomplete", result)
        self.assertEqual(995444, score)

        result, stack = process_chunk("<{([{{}}[<[[[<>{}]]]>[]]") # - Complete by adding ])}>.
        score = score_incomplete_chunk(stack)
        self.assertEqual("incomplete", result)
        self.assertEqual(294, score)


    def test__part_2__sample_input(self):
        print("")
        chunks = read_file_into_array(sample_input_file_1, False)
        score = get_winning_incomplete_score(chunks)
        self.assertEqual(288957, score)



    def test__part_2__challenge_input(self):
        print("")
        chunks = read_file_into_array(input_file, False)
        score = get_winning_incomplete_score(chunks)
        print("Solution to day 10 part 2: {0}".format(score))
        

 

 
###################################################################################################################################################################
########################################################################## RUN THE TESTS ##########################################################################


# run then unit tests "last"
if __name__ == '__main__':
    unittest.main()
 

