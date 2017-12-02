#!/bin/python
# -*- coding: utf-8 -*-
# http://adventofcode.com/2016/day/2

###################################################################################################################################################################
#  
#  Solution to day 2 part 1: 56855
#  Solution to day 2 part 2: B3C27
#
###################################################################################################################################################################


###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################

directions = [
    "UDRLRRRUULUUDULRULUDRDRURLLDUUDURLUUUDRRRLUUDRUUDDDRRRLRURLLLDDDRDDRUDDULUULDDUDRUUUDLRLLRLDUDUUUUDLDULLLDRLRLRULDDDDDLULURUD" \
    "URDDLLRDLUDRRULDURDDLUDLLRRUDRUDDDLLURULRDDDRDRRLLUUDDLLLLRLRUULRDRURRRLLLLDULDDLRRRRUDRDULLLDDRRRDLRLRRRLDRULDUDDLDLUULRDDUL" \
    "RDRURRURLDULRUUDUUURDRLDDDURLDURLDUDURRLLLLRDDLDRUURURRRRDRRDLUULLURRDLLLDLDUUUDRDRULULRULUUDDULDUURRLRLRRDULDULDRUUDLLUDLLLL" \
    "UDDULDLLDLLURLLLRUDRDLRUDLULDLLLUDRLRLUDLDRDURDDULDURLLRRRDUUDLRDDRUUDLUURLDRRRRRLDDUUDRURUDLLLRRULLRLDRUURRRRRLRLLUDDRLUDRRD" \
    "UDUUUDRUDULRRULRDRRRDDRLUUUDRLLURURRLLDUDRUURDLRURLLRDUDUUDLLLUULLRULRLDLRDDDU",

    "DRRRDRUDRLDUUDLLLRLULLLUURLLRLDRLURDRDRDRLDUUULDRDDLDDDURURUDRUUURDRDURLRLUDRRRDURDRRRDULLRDRRLUUUURLRUULRRDUDDDDUURLDULUDLLL" \
    "RULUDUURRDUULRRDDURLURRUDRDRLDLRLLULULURLRDLRRRUUURDDUUURDRDRUURUDLULDRDDULLLLLRLRLLUDDLULLUDDLRLRDLDULURDUDULRDDRLUDUUDUDRLL" \
    "DRRLLDULLRLDURUDRLRRRDULUUUULRRLUDDDLDUUDULLUUURDRLLULRLDLLUUDLLUULUULUDLRRDDRLUUULDDRULDRLURUURDLURDDRULLLLDUDULUDURRDRLDDRR" \
    "LRURLLRLLLLDURDLUULDLDDLULLLRDRRRDLLLUUDDDLDRRLUUUUUULDRULLLDUDLDLURLDUDULRRRULDLRRDRUUUUUURRDRUURLDDURDUURURULULLURLLLLUURDU" \
    "DRRLRRLRLRRRRRULLDLLLRURRDULLDLLULLRDUULDUDUDULDURLRDLDRUUURLLDLLUUDURURUD",

    "UDUUUUURUDLLLRRRDRDRUDDRLLDRRLDRLLUURRULUULULRLLRUDDRLDRLUURDUDLURUULLLULLRRRULRLURRDDULLULULRUDDDUURDRLUDUURRRRUUULLRULLLDLU" \
    "RUDLDDLLRRRULDLLUURDRRRDRDURURLRUDLDLURDDRLLLUUDRUULLDLLLLUUDRRURLDDUDULUDLDURDLURUURDUUUURDLLLRUUURDUUUDLDUDDLUDDUDUDUDLDUDU" \
    "UULDULUURDDLRRRULLUDRRDLUDULDURUURULLLLUDDDLURURLRLRDLRULRLULURRLLRDUDUDRULLRULRUDLURUDLLDUDLRDRLRDURURRULLDDLRLDDRLRDRRDLRDD" \
    "LLLLDUURRULLRLLDDLDLURLRLLDULRURRRRDULRLRURURRULULDUURRDLURRDDLDLLLRULRLLURLRLLDDLRUDDDULDLDLRLURRULRRLULUDLDUDUDDLLUURDDDLUL" \
    "URRULDRRDDDUUURLLDRDURUDRUDLLDRUD",

    "ULRDULURRDDLULLDDLDDDRLDUURDLLDRRRDLLURDRUDDLDURUDRULRULRULULUULLLLDRLRLDRLLLLLRLRRLRLRRRDDULRRLUDLURLLRLLURDDRRDRUUUDLDLDRRR" \
    "UDLRUDDRURRDUUUDUUULRLDDRDRDRULRLLDLDDLLRLUDLLLLUURLDLRUDRLRDRDRLRULRDDURRLRUDLRLRLDRUDURLRDLDULLUUULDRLRDDRDUDLLRUDDUDURRRRD" \
    "LDURRUURDUULLDLRDUDDLUDDDRRRULRLULDRLDDRUURURLRRRURDURDRULLUUDURUDRDRLDLURDDDUDDURUDLRULULURRUULDRLDULRRRRDUULLRRRRLUDLRDDRLR" \
    "UDLURRRDRDRLLLULLUULRDULRDLDUURRDULLRULRLRRURDDLDLLRUUDLRLDLRUUDLDDLLULDLUURRRLRDULRLRLDRLDUDURRRLLRUUDLUURRDLDDULDLULUUUUDRR" \
    "ULLLLLLUULDRULDLRUDDDRDRDDURUURLURRDLDDRUURULLULUUUDDLRDULDDLULDUDRU",

    "LRLRLRLLLRRLUULDDUUUURDULLLRURLDLDRURRRUUDDDULURDRRDURLRLUDLLULDRULLRRRDUUDDRDRULLDDULLLUURDLRLRUURRRLRDLDUDLLRLLURLRLLLDDDUL" \
    "UDUDRDLRRLUDDLRDDURRDRDUUULLUURURLRRDUURLRDLLUDURLRDRLURUURDRLULLUUUURRDDULDDDRULURUULLUDDDDLRURDLLDRURDUDRRLRLDLRRDDRRDDRUDR" \
    "DLUDDDLUDLUDLRUDDUDRUDLLRURDLRUULRUURULUURLRDULDLDLLRDRDUDDDULRLDDDRDUDDRRRLRRLLRRRUUURRLDLLDRRDLULUUURUDLULDULLLDLULRLRDLDDD" \
    "DDDDLRDRDUDLDLRLUDRRDRRDRUURDUDLDDLUDDDDDDRUURURUURLURLDULUDDLDDLRUUUULRDRLUDLDDLLLRLLDRRULULRLRDURRRLDDRDDRLU"
]


class Key:
    def __init__(self, buttonValue):
        self.button = buttonValue
        self.up = None
        self.down = None
        self.left = None
        self.right = None
    ### __init__

    def linkButtons(self, up, down, left, right):
        self.up = up
        self.down = down
        self.left = left
        self.right = right
    ### linkButtons

    def returnSelfOrAdjacent(self, adjacent):
        if adjacent is None:
            return self
        else:
            return adjacent
    ### returnSelfOrAdjacent

    def getNextButton(self, direction):
        if direction == "U":
            return self.returnSelfOrAdjacent(self.up)
        elif direction == "D":
            return self.returnSelfOrAdjacent(self.down)
        elif direction == "L":
            return self.returnSelfOrAdjacent(self.left)
        elif direction == "R":
            return self.returnSelfOrAdjacent(self.right)
        else:
            return None
    ### getNextButton

    def __str__(self):
        return self.button


def findCombination(button, directions):
    combination = ""
    currentButton = button

    for line in directions:
        for step in line:
            currentButton = currentButton.getNextButton(step)

        combination += str(currentButton)

    return combination


################################################################################################################################################################
########################################################################### PART 1 #############################################################################


#
#  1 2 3
#  4 5 6
#  7 8 9  
#

one     = Key("1")
two     = Key("2")
three   = Key("3")
four    = Key("4")
five    = Key("5")
six     = Key("6")
seven   = Key("7")
eight   = Key("8")
nine    = Key("9")

# (up, down, left, right)
one.linkButtons(None, four, None, two)
two.linkButtons(None, five, one, three)
three.linkButtons(None, six, two, None)
four.linkButtons(one, seven, None, five)
five.linkButtons(two, eight, four, six)
six.linkButtons(three, nine, five, None)
seven.linkButtons(four, None, None, eight)
eight.linkButtons(five, None, seven, nine)
nine.linkButtons(six, None, eight, None)

print "Solution to day 2 part 1: " + findCombination(five, directions)


################################################################################################################################################################
########################################################################### PART 2 #############################################################################

#       1
#     2 3 4
#   5 6 7 8 9
#     A B C
#       D

a = Key("A")
b = Key("B")
c = Key("C")
d = Key("D")

# (up, down, left, right)
one.linkButtons(None, three, None, None)
two.linkButtons(None, six, None, three)
three.linkButtons(one, seven, two, four)
four.linkButtons(None, eight, three, None)
five.linkButtons(None, None, None, six)
six.linkButtons(two, a, five, seven)
seven.linkButtons(three, b, six, eight)
eight.linkButtons(four, c, seven, nine)
nine.linkButtons(None, None, eight, None)
a.linkButtons(six, None, None, b)
b.linkButtons(seven, d, a, c)
c.linkButtons(eight, None, b, None)
d.linkButtons(b, None, None, None)

print "Solution to day 2 part 2: " + findCombination(five, directions)
