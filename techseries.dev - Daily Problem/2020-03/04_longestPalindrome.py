
class Solution: 
    def longestPalindrome(self, s):
        if s is None:
            return None

        forewards = list(s)
        forewards_size = len(forewards)
        backwards = list(reversed(forewards))

        # prepend backwards with a bunch of None entries to get proper slide starting position.
        backwards = ["~"]*(forewards_size -1) + backwards

        # record keeping array
        longest_palindrome_found = [] # defined here for scope access.

        while min(len(backwards), forewards_size) > 0 :
            current_palindrome = []

            # hunt for palendrone
            for i in range( min(len(backwards), forewards_size) ):
                if forewards[i] == backwards[i]:
                    current_palindrome.append(forewards[i])
                    
                    # check if the newly built palendrome is longer than longest on this pass
                    if len(current_palindrome) > len(longest_palindrome_found):
                        longest_palindrome_found = current_palindrome
                else:
                    current_palindrome = []

            # DEBUG message
            print("Pass: forwards={} backwards={} longest_palindrome_found={}".format("".join(forewards), "".join(backwards), "".join(longest_palindrome_found) ) )

            # remove a character from the front of backwards
            del backwards[0]

        # Additional palindrome definition.
        # If the source string is longer than 1 character, then any palendrone found must be longer than 1 character.
        if forewards_size > 1 and len(longest_palindrome_found) == 1:
            longest_palindrome_found = []

        return "".join(longest_palindrome_found)
    ### longestPalindrome
### Class: Solution
        

test_cases = [
    (None, None),
    ("", ""),
    ("a","a"),
    ("ab",""),
    ("abb","bb"),
    ("abc",""),
    ("banana", "anana"),
    ("million", "illi"),
    ("tracecars", "racecar"),
    ("abcdedc44abcdefedcba45hhhjhhk", "4abcdefedcba4"),
]

for test_case in test_cases:
    test_input = test_case[0]
    expected_output = test_case[1]
    actual_output = Solution().longestPalindrome(test_input)
    
    print("result={} input={} expected={} actual={} ".format(expected_output == actual_output, test_input, expected_output, actual_output))
