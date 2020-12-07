#!/bin/python
# -*- coding: utf-8 -*-
# https://adventofcode.com/2020/day/6


###################################################################################################################################################################
#  
#  Solution to day 6 part 1: 6630
#
#  Solution to day 6 part 2: 3437
#
###################################################################################################################################################################


###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################
#   --- Day 6: Custom Customs ---
#   As your flight approaches the regional airport where you'll switch to a much larger plane, 
#   customs declaration forms are distributed to the passengers.
#   
#   The form asks a series of 26 yes-or-no questions marked a through z. All you need to do is 
#   identify the questions for which anyone in your group answers "yes". Since your group is 
#   just you, this doesn't take very long.
#   
#   However, the person sitting next to you seems to be experiencing a language barrier and asks 
#   if you can help. For each of the people in their group, you write down the questions for 
#   which they answer "yes", one per line. For example:
#   
#       abcx
#       abcy
#       abcz
#   
#   In this group, there are 6 questions to which anyone answered "yes": a, b, c, x, y, and z. 
#   (Duplicate answers to the same question don't count extra; each question counts at most once.)
#   
#   Another group asks for your help, then another, and eventually you've collected answers 
#   from every group on the plane (your puzzle input). Each group's answers are separated by 
#   a blank line, and within each group, each person's answers are on a single line. For example:
#   
#       abc
#   
#       a
#       b
#       c
#   
#       ab
#       ac
#   
#       a
#       a
#       a
#       a
#   
#       b
#   
#   This list represents answers from five groups:
#   
#   The first group contains one person who answered "yes" to 3 questions: a, b, and c.
#   The second group contains three people; combined, they answered "yes" to 3 questions: a, b, and c.
#   The third group contains two people; combined, they answered "yes" to 3 questions: a, b, and c.
#   The fourth group contains four people; combined, they answered "yes" to only 1 question, a.
#   The last group contains one person who answered "yes" to only 1 question, b.
#   In this example, the sum of these counts is 3 + 3 + 3 + 1 + 1 = 11.
#   
#   For each group, count the number of questions to which anyone answered "yes". What is the sum of those counts?
#   


def test_equal(actual, expected, message):
    if actual != expected:
        print("FAIL: Found={0}  Expected={1}    {2}".format(actual, expected, message))



sample_input_file = "2020_06_sample.txt"
input_file = "2020_06_input.txt"


class Group:  
    def __init__(self):  
        self.unique_questions  = set()
        self.list_of_responses = []
        self.all_questions_and_counts = {}

    def add_group_member_response(self, response):
        self.list_of_responses.append(response)
        self.unique_questions.update(response)

        for q in response:
            if q in self.all_questions_and_counts:
                self.all_questions_and_counts[q] += 1
            else:
                self.all_questions_and_counts[q] = 1

    def get_count_unique_questions(self):
        return len(self.unique_questions)

    def get_count_of_questions_that_everyone_answered_yes(self):
        count = 0
        target = len(self.list_of_responses)
        for key in self.all_questions_and_counts:
            if self.all_questions_and_counts[key] == target:
                count += 1

        return count
### Class: Group


def get_count_of_unique_questions_for_all_groups(groups):
    count = 0

    for g in groups:
        count += g.get_count_unique_questions()

    return count
### get_count_of_unique_questions_for_all_groups


def read_file_and_track_groups(file_name):
    g = Group()
    groups = [g]

    with open(file_name) as f:
        for line in f:
            line = line.strip()

            if len(line) == 0:
                g = Group()
                groups.append(g)
                continue 
            else:
                g.add_group_member_response(line)

    return groups
### read_file_and_track_groups


print("--- P1 sample input ---")
groups_sample = read_file_and_track_groups(sample_input_file)
test_equal(get_count_of_unique_questions_for_all_groups(groups_sample), 11, "P1 count of unique questions within a group, summed across groups")
print("-------------------------")

groups = read_file_and_track_groups(input_file)
count = get_count_of_unique_questions_for_all_groups(groups)

print("Solution to day 6 part 1: {0}".format(count))


###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################
#   --- Part Two ---
#   As you finish the last group's customs declaration, you notice that you misread 
#   one word in the instructions:
#   
#   You don't need to identify the questions to which anyone answered "yes"; you need 
#   to identify the questions to which everyone answered "yes"!
#   
#   Using the same example as above:
#   
#       abc
#       
#       a
#       b
#       c
#       
#       ab
#       ac
#       
#       a
#       a
#       a
#       a
#       
#       b
#
#   This list represents answers from five groups:
#   
#       In the first group, everyone (all 1 person) answered "yes" to 3 questions: a, b, and c.
#       In the second group, there is no question to which everyone answered "yes".
#       In the third group, everyone answered yes to only 1 question, a. Since some people did 
#           not answer "yes" to b or c, they don't count.
#       In the fourth group, everyone answered yes to only 1 question, a.
#       In the fifth group, everyone (all 1 person) answered "yes" to 1 question, b.
#       In this example, the sum of these counts is 3 + 0 + 1 + 1 + 1 = 6.
#   
#   For each group, count the number of questions to which everyone answered "yes". What is the sum of those counts?
#   


def get_count_of_unanimous_answers_for_all_groups(groups):
    count = 0

    for g in groups:
        count += g.get_count_of_questions_that_everyone_answered_yes()

    return count
### get_count_of_unanimous_answers_for_all_groups


print("--- P2 sample input ---")
test_equal(get_count_of_unanimous_answers_for_all_groups(groups_sample), 6, "P2")
print("-------------------------")


print("Solution to day 6 part 2: {0}".format(get_count_of_unanimous_answers_for_all_groups(groups)))

