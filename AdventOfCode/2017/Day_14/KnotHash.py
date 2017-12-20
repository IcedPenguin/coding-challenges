
# Code pulled from 2017 day 10.

arraySize = 256

def getFreshRope(length):
    rope = []
    for i in xrange(arraySize):
        rope.append(i)
    return rope
### getFreshRope


def convertAsciiToLengths(inputAscii):
    lengths = []

    for character in inputAscii:
        lengths.append(ord(character))

    # append standard post-fix
    lengths += [17, 31, 73, 47, 23]

    return lengths
### convertAsciiToLengths


def reversePortionOfRope(rope, position, length):
    ropeLen = len(rope)
    double = rope + rope
    section = double[position:position + length]
    section = section[::-1]

    for i in xrange(len(section)):
        rope[(position + i) % ropeLen] = section[i]

    return rope
### reversePortionOfRope


def getNextPosition(arraySize, currentPosition, length, skipSize):
    nextIndex = currentPosition + length + skipSize
    nextIndex %= arraySize
    skipSize += 1
    return nextIndex, skipSize
### getNextPosition


def convertSparseHashToDenseHash(rope):
    output = []
    for b in xrange(16):
        h = 0
        for i in xrange(16):
            h ^= rope[b*16 + i]

        output.append( format(h, '#04x')[2:] )
    output = "".join(output)
    return output
### convertSparseHashToDenseHash


def performKnotHasing(rope, rounds, inputLengths):
    length = 0
    position = 0
    skipSize = 0

    # perform the rounds
    for i in xrange(rounds):
        for part in inputLengths:
            if type(part) == str:
                length = int(part.strip())
            else:
                length = part
            rope = reversePortionOfRope(rope, position, length)
            position, skipSize = getNextPosition(arraySize, position, length, skipSize)

    # encode the output hash
    return convertSparseHashToDenseHash(rope)
### performKnotHasing


def computeKnotHash(key):
    rope = getFreshRope(arraySize)
    inputLengths = convertAsciiToLengths(key)
    return performKnotHasing(rope, 64, inputLengths)
### knothash
