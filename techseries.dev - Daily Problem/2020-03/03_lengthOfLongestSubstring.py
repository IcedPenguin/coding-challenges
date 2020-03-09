class Solution:
  def lengthOfLongestSubstring(self, s):
    length_of_sub_string = 0
    current_sub_string_contents = set()
    length_longest_substring = -1
    

    for i in range(len(s)):
        if s[i] not in current_sub_string_contents:
            current_sub_string_contents.add(s[i])
            length_of_sub_string += 1
        else:
            # we reached the end of a sub-string, save it
            if length_longest_substring < length_of_sub_string:
                length_longest_substring = length_of_sub_string

            # reset to start looking for a new substring.
            length_of_sub_string = 1
            current_sub_string_contents.clear()
            current_sub_string_contents.add(s[i])
        
    if length_longest_substring < length_of_sub_string:
        length_longest_substring = length_of_sub_string
        
    return length_longest_substring

print( Solution().lengthOfLongestSubstring('abrkaabcdefghijjxxx') )
# 10