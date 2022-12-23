#!/bin/python
# -*- coding: utf-8 -*-
# https://adventofcode.com/2022/day/7


###################################################################################################################################################################
#  
#  Solution to part 1: 1118405
#
#  Solution to part 2: 12545514
#
###################################################################################################################################################################

import unittest

###################################################################################################################################################################
#   --- Day 7: No Space Left On Device ---
#   
#   You can hear birds chirping and raindrops hitting leaves as the expedition proceeds. Occasionally, you can even hear much 
#   louder sounds in the distance; how big do the animals get out here, anyway?
#   
#   The device the Elves gave you has problems with more than just its communication system. You try to run a system update:
#   
#       $ system-update --please --pretty-please-with-sugar-on-top
#       Error: No space left on device
#   
#   Perhaps you can delete some files to make space for the update?
#   
#   You browse around the filesystem to assess the situation and save the resulting terminal output (your puzzle input). For example:
#   
#       $ cd /
#       $ ls
#       dir a
#       14848514 b.txt
#       8504156 c.dat
#       dir d
#       $ cd a
#       $ ls
#       dir e
#       29116 f
#       2557 g
#       62596 h.lst
#       $ cd e
#       $ ls
#       584 i
#       $ cd ..
#       $ cd ..
#       $ cd d
#       $ ls
#       4060174 j
#       8033020 d.log
#       5626152 d.ext
#       7214296 k
#   
#   The filesystem consists of a tree of files (plain data) and directories (which can contain other directories or files). 
#   The outermost directory is called /. You can navigate around the filesystem, moving into or out of directories and 
#   listing the contents of the directory you're currently in.
#   
#   Within the terminal output, lines that begin with $ are commands you executed, very much like some modern computers:
#   
#       cd means change directory. This changes which directory is the current directory, but the specific result depends on the argument:
#           cd x moves in one level: it looks in the current directory for the directory named x and makes it the current directory.
#           cd .. moves out one level: it finds the directory that contains the current directory, then makes that directory the current directory.
#           cd / switches the current directory to the outermost directory, /.
#       ls means list. It prints out all of the files and directories immediately contained by the current directory:
#           123 abc means that the current directory contains a file named abc with size 123.
#           dir xyz means that the current directory contains a directory named xyz.
#   
#   Given the commands and output in the example above, you can determine that the filesystem looks visually like this:
#   
#       - / (dir)
#         - a (dir)
#           - e (dir)
#             - i (file, size=584)
#           - f (file, size=29116)
#           - g (file, size=2557)
#           - h.lst (file, size=62596)
#         - b.txt (file, size=14848514)
#         - c.dat (file, size=8504156)
#         - d (dir)
#           - j (file, size=4060174)
#           - d.log (file, size=8033020)
#           - d.ext (file, size=5626152)
#           - k (file, size=7214296)
#   
#   Here, there are four directories: / (the outermost directory), a and d (which are in /), and e (which is in a). These 
#   directories also contain files of various sizes.
#   
#   Since the disk is full, your first step should probably be to find directories that are good candidates for deletion. 
#   To do this, you need to determine the total size of each directory. The total size of a directory is the sum of the 
#   sizes of the files it contains, directly or indirectly. (Directories themselves do not count as having any intrinsic size.)
#   
#   The total sizes of the directories above can be found as follows:
#   
#       The total size of directory e is 584 because it contains a single file i of size 584 and no other directories.
#       The directory a has total size 94853 because it contains files f (size 29116), g (size 2557), and h.lst (size 62596), 
#          plus file i indirectly (a contains e which contains i).
#       Directory d has total size 24933642.
#       As the outermost directory, / contains every file. Its total size is 48381165, the sum of the size of every file.
#   
#   To begin, find all of the directories with a total size of at most 100000, then calculate the sum of their total sizes. 
#   In the example above, these directories are a and e; the sum of their total sizes is 95437 (94853 + 584). (As in this 
#   example, this process can count files more than once!)
#   
#   Find all of the directories with a total size of at most 100000. What is the sum of the total sizes of those directories?
#   
############################################################################ PROBLEM 1 ############################################################################


puzzle_day          = 7
sample_input_file_1 = "2022_{0:02d}_sample_1.txt".format(puzzle_day)
input_file          = "2022_{0:02d}_input.txt".format(puzzle_day)


def load_file(file_path):
    file_ptr = open(file_path, "r")
    data = file_ptr.read()
    file_ptr.close()
    return data



def process_terminal_log(terminal):
    current_directory = None
    directory_contents = {}
    directory_contents["/"] = (-1, [])

    while len(terminal) > 0:
        line = terminal.pop(0)
        # print("-----------------------")
        # print("Dir: {0}".format(current_directory))
        # print("Cmd: {0}".format(line))

        # Handle all the cases of changing directories
        if line == "$ cd /":
            current_directory = "/"

        elif line == "$ cd ..":
            current_directory = current_directory[:current_directory.rfind("/", 0, len(current_directory)-1) +1]

        elif line.startswith("$ cd "):
            parts = line.split(" ")
            current_directory += parts[2] + "/"


        # Handle listing of files.
        elif line == "$ ls":
            while len(terminal) > 0 and terminal[0][0] != "$":
                entry = terminal.pop(0)

                parts = entry.split(" ")
                if parts[0] == "dir":
                    directory_contents[current_directory + parts[1] + "/"] = (-1, [])

                else: # file entry
                    directory_contents[current_directory][1].append( (parts[1], int(parts[0])) )
        
        else:
            print("!!!!!!!!!!!!!!!!!!!!!!! UNKOWN / UNHANDLED COMMAND !!!!!!!!!!!!!!!!!!!!!!!")


    return directory_contents

def calculate_directory_total_size(directory_contents, path="/"):
    directory = directory_contents[path]
    # we do not yet have a size
    if directory[0] == -1:
        size = 0
        # get size of files in this directory
        for entry in directory[1]:
            size += entry[1]

        # get size of child directories
        for key in directory_contents:
            path_slashes = path.count("/")
            if key.startswith(path) and key.count('/') - path_slashes == 1: # key != path and 
                size += calculate_directory_total_size(directory_contents, key)

        directory_contents[path] = (size, directory[1])

    return directory_contents[path][0]



def count_directories_smaller_than_size(directory_contents, max_size):
    directory_count = 0
    total_size = 0

    calculate_directory_total_size(directory_contents)

    for key in directory_contents:
        if directory_contents[key][0] <= max_size:
            directory_count += 1 
            total_size += directory_contents[key][0]

    return directory_count, total_size



class Day7PartOneTests(unittest.TestCase):

    def test__p1__sample1(self):
        raw_commands = load_file(sample_input_file_1)
        commands = raw_commands.split("\n")
        directories = process_terminal_log(commands)

        size = calculate_directory_total_size(directories, "/a/e/")
        self.assertEqual(size, 584)

        size = calculate_directory_total_size(directories, "/a/")
        self.assertEqual(size, 94853)

        size = calculate_directory_total_size(directories, "/d/")
        self.assertEqual(size, 24933642)

        size = calculate_directory_total_size(directories)
        self.assertEqual(size, 48381165)
        

    def test__p1__sample2(self):
        raw_commands = load_file(sample_input_file_1)
        commands = raw_commands.split("\n")
        directories = process_terminal_log(commands)
        count, size = count_directories_smaller_than_size(directories, 100000)

        self.assertEqual(count, 2)
        self.assertEqual(size, 95437)

    
    def test__part_1__challenge_input(self):
        print("")
        raw_commands = load_file(input_file)
        commands = raw_commands.split("\n")
        directories = process_terminal_log(commands)
        count, size = count_directories_smaller_than_size(directories, 100000)
        print("Solution to day {0} part 1: {1}".format(puzzle_day, size))
        


###################################################################################################################################################################
#   --- Part Two ---
#   
#   Now, you're ready to choose a directory to delete.
#   
#   The total disk space available to the filesystem is 70000000. To run the update, you need unused space of at least 30000000. 
#   You need to find a directory you can delete that will free up enough space to run the update.
#   
#   In the example above, the total size of the outermost directory (and thus the total amount of used space) is 48381165; this 
#   means that the size of the unused space must currently be 21618835, which isn't quite the 30000000 required by the update. 
#   Therefore, the update still requires a directory with total size of at least 8381165 to be deleted before it can run.
#   
#   To achieve this, you have the following options:
#   
#       Delete directory e, which would increase unused space by 584.
#       Delete directory a, which would increase unused space by 94853.
#       Delete directory d, which would increase unused space by 24933642.
#       Delete directory /, which would increase unused space by 48381165.
#   
#   Directories e and a are both too small; deleting them would not free up enough space. However, directories d and / are both 
#   big enough! Between these, choose the smallest: d, increasing unused space by 24933642.
#   
#   Find the smallest directory that, if deleted, would free up enough space on the filesystem to run the update. What is the 
#   total size of that directory?
#   
############################################################################ PROBLEM 2 ############################################################################


def find_directory_to_delete(directory_contents, total_disk_space, space_needed):
    calculate_directory_total_size(directory_contents)
    
    used_space = directory_contents["/"][0]
    space_to_free = space_needed - (total_disk_space - used_space)
    closest_size_found = total_disk_space

    for path in directory_contents:
        directory_size = directory_contents[path][0]
        
        if space_to_free > directory_size:
            continue # deleting this folder will not free up enough space, keep looking

        excess_free_space = directory_size - space_to_free
        if excess_free_space < closest_size_found - space_to_free:
            closest_size_found = directory_size

    return closest_size_found

class Day7PartTwoTests(unittest.TestCase):
    
    def test__p2__sample1(self):        
        raw_commands = load_file(sample_input_file_1)
        commands = raw_commands.split("\n")
        directories = process_terminal_log(commands)
        space_to_free = find_directory_to_delete(directories, 70000000, 30000000)

        self.assertEqual(space_to_free, 24933642)

        

    def test__part_2__challenge_input(self):
        print("")
        raw_commands = load_file(input_file)
        commands = raw_commands.split("\n")
        directories = process_terminal_log(commands)
        space_to_free = find_directory_to_delete(directories, 70000000, 30000000)
        print("Solution to day {0} part 2: {1}".format(puzzle_day, space_to_free))


 
###################################################################################################################################################################
########################################################################## RUN THE TESTS ##########################################################################


# run then unit tests "last"
if __name__ == '__main__':
    unittest.main()
 

