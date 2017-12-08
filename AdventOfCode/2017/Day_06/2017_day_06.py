#!/bin/python
# -*- coding: utf-8 -*-
# http://adventofcode.com/2017/day/6


###################################################################################################################################################################
#  
#  Solution to day 6 part 1: 7864
#  Solution to day 6 part 2: 1695
#
###################################################################################################################################################################


###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################


def haveWeSeenThisStateBefore(bank, bankStateHistory):
    bankHash =  hash(tuple(bank))
    if bankHash in bankStateHistory:
        return True
    else:
        bankStateHistory.append(bankHash)
        return False
### haveWeSeenThisStateBefore


def findBankToRedistribute(bank):
    orderByCount = {}
    for i in xrange(len(bank)):
        value = bank[i]
        if value in orderByCount:
            orderByCount[value].append(i)
        else:
            orderByCount[value] = [i]
    
    # print orderByCount

    maxValue = max(orderByCount.iterkeys())
    possibleIndices = orderByCount[maxValue]
    possibleIndices.sort()
    return possibleIndices[0]
### findBankToRedistribute


def redistributeBank(bank, index):
    blockCount = bank[index]

    bank[index] = 0

    while blockCount > 0:
        index += 1
        bank[index % len(bank)] += 1
        blockCount -= 1
### redistributeBank



# bank = [0, 2, 7, 0] # sample input
bank = [0, 5, 10, 0, 11, 14, 13, 4, 11, 8, 8, 7, 1, 4, 12,  11]
bankStateHistory = []
count = 0

while True:
    # print bank
    if haveWeSeenThisStateBefore(bank, bankStateHistory):
        break

    index = findBankToRedistribute(bank)
    redistributeBank(bank, index)
    count += 1


print "Solution to day 6 part 1: " + str(count)


###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################

count = 0
seenOnce = False
bankStateHistory = []

while True:
    # print bank
    if haveWeSeenThisStateBefore(bank, bankStateHistory):
        if not seenOnce:
            seenOnce = True
            bankStateHistory = []
            haveWeSeenThisStateBefore(bank, bankStateHistory)
            count = 0

        else:
            break

    index = findBankToRedistribute(bank)
    redistributeBank(bank, index)
    count += 1

print "Solution to day 6 part 2: " + str(count)

