#!/bin/python
# -*- coding: utf-8 -*-
# https://adventofcode.com/2018/day/4

# from dateutil.parser import parse
import datetime

###################################################################################################################################################################
#  
#  Solution to day 4 part 1: 84636
#  Solution to day 4 part 2: 91679
#
###################################################################################################################################################################


###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################

# input_file = "2018_04_1_sample_1.txt"
input_file = "2018_04_input.txt"



def printRecordsFormatted(dayToRecord):
    # for i in xrange(304,311):
        # print "{0:3d} → {1}".format(i, dayToRecord[i])

    for day in dayToRecord:
        print "position: {0:5d}, fix id: {1} padded wait in seconds: {2:03d}".format(12, 453585, 89)
### printRecordsFormatted


def fillInTheLine(record):
    currentCharacter = "."

    for i in xrange(60):
        if record[i] == "?":
            record[i] = currentCharacter
        else:
            currentCharacter = record[i]
    return record
### fillInTheLine


def findGuardWithMostMinutesSleep(guardToDays, dayToRecord):
    sleepiestGuard = -1
    minutesAsleep = -1

    for guard in guardToDays:
        count = 0
        for day in guardToDays[guard]:
            c = 0
            for minute in dayToRecord[day]:
                if minute == [guard]:
                    c += 1
            count += c

        print "Guard %s ==> %s" % (guard, count)

        if count > minutesAsleep:
            sleepiestGuard = guard
            minutesAsleep = count

    return sleepiestGuard
### findGuardWithMostMinutesSleep


def findMinuteWhereGuardSleptTheMost(guard, guardToDays, dayToRecord):
    minutes = [0] * 60
    for day in guardToDays[guard]:
        for i in xrange(0, 60):
            if dayToRecord[day][i] == [guard]:
                minutes[i] += 1

    minute = -1
    timesAsleep = -1
    for i in xrange(0, 60):
        if minutes[i] > timesAsleep:
            timesAsleep = minutes[i]
            minute = i


    print "findMinuteWhereGuardSleptTheMost"
    print minutes
    print "timesAsleep: %s" % (timesAsleep)
    print "minute: %s" % (minute)
    return guard, minute, timesAsleep

### findMinuteWhereGuardSleptTheMost


def findGuardWhoSleepsMostOftenInTheSameMinute(guardToDays, dayToRecord):
    guardId = -1
    sleepiestMinute = -1
    timesAsleep = -1

    for guard in guardToDays:
        guard, minute, times = findMinuteWhereGuardSleptTheMost(guard, guardToDays, dayToRecord)

        if timesAsleep < times:
            guardId = guard
            sleepiestMinute = minute
            timesAsleep = times


    print "guard: %s" % (guardId)
    print "sleepiestMinute: %s" % (sleepiestMinute)
    print "timesAsleep: %s" % (timesAsleep)

    return guardId, sleepiestMinute, timesAsleep
### findGuardWhoSleepsMostOftenInTheSameMinute

def processLog(logEntries):

    k = logEntries.keys()
    k.sort()

    # structures
    guardToDays = {}
    dayToRecord = {}
    for day in xrange(365):
        dayToRecord[day + 1] = ["?"] * 60

    # read in all the data
    guardId = -1
    for key in k:
        line = logEntries[key]
        day = key.timetuple().tm_yday
        

        if "begins shift" in line:
            guardId = line[26:].replace(" begins shift\n", "")            
        
        elif "falls asleep" in line:
            record = dayToRecord[day]

            if guardId in guardToDays:
                guardToDays[guardId].add(day)
            else:
                guardToDays[guardId] = set([day])


            if record[key.minute] in ["?",  "."]:
                record[key.minute] = [guardId]
            else:
                record[key.minute].append(guardId)
            

        elif "wakes up" in line:
            record = dayToRecord[day]

            if record[key.minute] == "?":
                record[key.minute] = "."


        else: 
            print "unknown value found: " + line


    # fill in the missing regions in daily records.
    for day in dayToRecord:
        record = dayToRecord[day]
        record = fillInTheLine(record)
        dayToRecord[day] = record


    g = findGuardWithMostMinutesSleep(guardToDays, dayToRecord)
    g, m, l = findMinuteWhereGuardSleptTheMost(g, guardToDays, dayToRecord)

    # print various structures as check-points
    # pass
    # print guardToDays
    # print dayToGuard
    # printRecordsFormatted(dayToRecord)

    part1 =  int(g) * int(m)

    guardId, sleepiestMinute, timesAsleep = findGuardWhoSleepsMostOftenInTheSameMinute(guardToDays, dayToRecord)
    part2 = int(guardId) * int(sleepiestMinute)

    return part1, part2
### processLog

 
guards = {}
logEntries = {}

with open(input_file) as f:
    for line in f:
        a = line.strip()[1:17]
        d = datetime.datetime.strptime( a, "%Y-%m-%d %H:%M" )
        logEntries[d] = line



part1, part2 = processLog(logEntries)



print "Solution to day 4 part 1: " + str(part1)


###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################


print "Solution to day 4 part 2: " + str(part2)
