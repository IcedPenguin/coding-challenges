
# You are given a list of numbers, and a target number k. Return whether or not there are two numbers in the list that add up to k.

import sys
import traceback
import heapq

def formatParameters(param):
    return two_sum(param[0], param[1])

# time:  O(n)
# space: O(n)
def two_sum(operandList, targetSum):
    neededOperands = set()

    for i in operandList:
        complement = targetSum - i

        if i in neededOperands:
            return True
        else:
            neededOperands.add(complement)

    return False
### two_sum



test_cases = [
    (([],                   100), False),
    (([1,2],                  3), True),
    (([5],                   10), False),
    (([100, -60],            40), True),
    (([4, 7, 1 , -3, 2],      5), True),
]



for test_case in test_cases:
    try:
        result = formatParameters(test_case[0])

        if result == test_case[1]:
            print("PASS : ex={}  ac={}".format(test_case[0], result))
        else:
            print("FAIL : ex={}  ac={}".format(test_case[0], result))

    except:
        if test_case[1] == "exception":
            print("PASS : {}".format(test_case[0]))
        else:
            print("EXCEPTION : {} : {}".format(test_case[0], sys.exc_info()[1]))
            track = traceback.format_exc()
            print(track)

print("")
        