#!/bin/python
# -*- coding: utf-8 -*-
# https://adventofcode.com/2020/day/4


###################################################################################################################################################################
#  
#  Solution to day 4 part 1: 226
#
#  Solution to day 4 part 2: 160
#
###################################################################################################################################################################


###################################################################################################################################################################
############################################################################ PROBLEM 1 ############################################################################

# 
# --- Day 4: Passport Processing ---
# You arrive at the airport only to realize that you grabbed your North Pole Credentials instead of your 
# passport. While these documents are extremely similar, North Pole Credentials aren't issued by a 
# country and therefore aren't actually valid documentation for travel in most of the world.
# 
# It seems like you're not the only one having problems, though; a very long line has formed for the 
# automatic passport scanners, and the delay could upset your travel itinerary.
# 
# Due to some questionable network security, you realize you might be able to solve both of these 
# problems at the same time.
# 
# The automatic passport scanners are slow because they're having trouble detecting which passports have all 
# required fields. The expected fields are as follows:
# 
#         byr (Birth Year)
#         iyr (Issue Year)
#         eyr (Expiration Year)
#         hgt (Height)
#         hcl (Hair Color)
#         ecl (Eye Color)
#         pid (Passport ID)
#         cid (Country ID)
# 
# Passport data is validated in batch files (your puzzle input). Each passport is represented as a sequence 
# of key:value pairs separated by spaces or newlines. Passports are separated by blank lines.
# 
# Here is an example batch file containing four passports:
# 
#         ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
#         byr:1937 iyr:2017 cid:147 hgt:183cm
#         
#         iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
#         hcl:#cfa07d byr:1929
#         
#         hcl:#ae17e1 iyr:2013
#         eyr:2024
#         ecl:brn pid:760753108 byr:1931
#         hgt:179cm
#         
#         hcl:#cfa07d eyr:2025 pid:166559648
#         iyr:2011 ecl:brn hgt:59in
# 
# The first passport is valid - all eight fields are present. The second passport is invalid - 
# it is missing hgt (the Height field).
# 
# The third passport is interesting; the only missing field is cid, so it looks like data from 
# North Pole Credentials, not a passport at all! Surely, nobody would mind if you made the 
# system temporarily ignore missing cid fields. Treat this "passport" as valid.
# 
# The fourth passport is missing two fields, cid and byr. Missing cid is fine, but missing any 
# other field is not, so this passport is invalid.
# 
# According to the above rules, your improved system would report 2 valid passports.
# 
# Count the number of valid passports - those that have all required fields. Treat cid as optional. 
# In your batch file, how many passports are valid?
# 




sample_input_file = "2020_04_sample.txt"
input_file = "2020_04_input.txt"


def process_batch_file(file_path, validation_function):
    valid_passport_count = 0
    invalid_passport_count = 0

    with open(file_path) as file_reader:
        file_lines = file_reader.readlines()

        all_passports_processed = False
        while not all_passports_processed:
            passport_found, passport = extract_next_passport(file_lines)

            if not passport_found:
                all_passports_processed = True
                continue

            # handle this passport
            is_valid_passport = validation_function(passport)

            if is_valid_passport:
                valid_passport_count += 1
            else:
                invalid_passport_count += 1

    return valid_passport_count, invalid_passport_count
### process_batch_file

def extract_next_passport(file_lines):
    line = -1
    data_found = False
    passport = {}
    fields_list = []
    fields_found = 0

    while len(file_lines) > 0:
        line = file_lines.pop(0)
        line = line.strip()

        if len(line) == 0:
            break

        data_found = True 

        parts = line.split(" ")
        for p in parts:
            # print (p)
            a = p.split(":")
            passport[a[0]] = a[1]
            fields_found += 1
            fields_list.append(a[0])

    # print("{0}  {1}  {2}".format(fields_found, len(fields_list) != len(passport), fields_list))
    return data_found, passport, 
### extract_next_passport


def validate_passport(passport):
    # print("validate_passport: ", passport)

    has_all_valid_fields = True

    has_all_valid_fields = has_all_valid_fields and "byr" in passport
    has_all_valid_fields = has_all_valid_fields and "iyr" in passport
    has_all_valid_fields = has_all_valid_fields and "eyr" in passport
    has_all_valid_fields = has_all_valid_fields and "hgt" in passport
    has_all_valid_fields = has_all_valid_fields and "hcl" in passport
    has_all_valid_fields = has_all_valid_fields and "ecl" in passport
    has_all_valid_fields = has_all_valid_fields and "pid" in passport
    # has_all_valid_fields = has_all_valid_fields and "cid" in passport # "cid" is optional, dont even check it
    # print(has_all_valid_fields)

    return has_all_valid_fields
### validate_passport


def test_equal(actual, expected, message):
    if actual != expected:
        print("FAIL: Expected={0}  Found={1}    {2}".format(actual, expected, message))


print("--- Testing P1 Sample ---")
valid_passports, invalid_passports = process_batch_file(sample_input_file, validate_passport)
test_equal(valid_passports, 2, "P1: valid passport count is wrong")
test_equal(invalid_passports, 2, "P1: invalid passport count is wrong")
print("-------------------------")
# if valid_passports == 2 and invalid_passports == 2:
#     print("P1: sample input looks good")
# else:
#     print("P1: +++++++++= FAIL =++++++++++++++")

valid_passports, invalid_passports = process_batch_file(input_file, validate_passport)

print("Solution to day 4 part 1: {0}".format(valid_passports))


###################################################################################################################################################################
############################################################################ PROBLEM 2 ############################################################################
# 
# --- Part Two ---
# The line is moving more quickly now, but you overhear airport security talking 
# about how passports with invalid data are getting through. Better add some data 
# validation, quick!
# 
# You can continue to ignore the cid field, but each other field has strict rules 
# about what values are valid for automatic validation:
# 
#     byr (Birth Year)      - four digits; at least 1920 and at most 2002.
#     iyr (Issue Year)      - four digits; at least 2010 and at most 2020.
#     eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
#     hgt (Height)          - a number followed by either cm or in:
#                           - If cm, the number must be at least 150 and at most 193.
#                           - If in, the number must be at least 59 and at most 76.
#     hcl (Hair Color)      - a # followed by exactly six characters 0-9 or a-f.
#     ecl (Eye Color)       - exactly one of: amb blu brn gry grn hzl oth.
#     pid (Passport ID)     - a nine-digit number, including leading zeroes.
#     cid (Country ID)      - ignored, missing or not.
# 
# Your job is to count the passports where all required fields are both present and 
# valid according to the above rules. Here are some example values:
# 
#     byr valid:   2002
#     byr invalid: 2003
# 
#     hgt valid:   60in
#     hgt valid:   190cm
#     hgt invalid: 190in
#     hgt invalid: 190
# 
#     hcl valid:   #123abc
#     hcl invalid: #123abz
#     hcl invalid: 123abc
# 
#     ecl valid:   brn
#     ecl invalid: wat
# 
#     pid valid:   000000001
#     pid invalid: 0123456789
# 
# Here are some invalid passports:
# 
#     eyr:1972 cid:100
#     hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926
# 
#     iyr:2019
#     hcl:#602927 eyr:1967 hgt:170cm
#     ecl:grn pid:012533040 byr:1946
# 
#     hcl:dab227 iyr:2012
#     ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277
# 
#     hgt:59cm ecl:zzz
#     eyr:2038 hcl:74454a iyr:2023
#     pid:3556412378 byr:2007
#
# Here are some valid passports:
# 
#     pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
#     hcl:#623a2f
# 
#     eyr:2029 ecl:blu cid:129 byr:1989
#     iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm
# 
#     hcl:#888785
#     hgt:164cm byr:2001 iyr:2015 cid:88
#     pid:545766238 ecl:hzl
#     eyr:2022
# 
#     iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719
# 
# Count the number of valid passports - those that have all required fields and valid values. 
# Continue to treat cid as optional. In your batch file, how many passports are valid?
# 

import re


def validate_byr(byr):
#     byr (Birth Year) - four digits; at least 1920 and at most 2002.
    return validate_number_range(byr, 1920, 2002)


def validate_iyr(iyr):
#     iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    return validate_number_range(iyr, 2010, 2020)
    
def validate_eyr(eyr):
#     eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    return validate_number_range(eyr, 2020, 2030)


def validate_number_range(number, lower, upper):
    try:
        if number is None:
            return False

        number_int = int(number)

        return lower <= number_int and number_int <= upper

    except:
        return False


def validate_hgt(hgt):
#     hgt (Height) - a number followed by either cm or in:
# If cm, the number must be at least 150 and at most 193.
# If in, the number must be at least 59 and at most 76.
    if hgt is None:
        return False

    if len(hgt) < 4:
        return None

    unit = hgt[-2:]

    if unit == "cm":
        return validate_number_range(hgt[:-2], 150, 193)
    elif unit == "in":
        return validate_number_range(hgt[:-2], 59, 76)
    else:
        return False


def validate_hcl(hcl):
#     hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    if hcl is None:
        return False

    m = re.match("#[0-9a-f]{6,6}", hcl)
    return m is not None


def validate_ecl(ecl):
#     ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    if ecl is None:
        return False

    return ecl in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]


def validate_pid(pid):
#     pid (Passport ID) - a nine-digit number, including leading zeroes.
    if pid is None:
        return False

    m = re.match("[0-9]{9,9}$", pid)
    return m is not None


def validate_cid(cid):
#     cid (Country ID) - ignored, missing or not.
    return True


def validate_passport_field_validation(passport):
    passport_mut = passport.copy()

    has_all_valid_fields = True
    has_all_valid_fields = validate_byr( passport_mut.pop("byr", None) )  and has_all_valid_fields
    has_all_valid_fields = validate_iyr( passport_mut.pop("iyr", None) )  and has_all_valid_fields
    has_all_valid_fields = validate_eyr( passport_mut.pop("eyr", None) )  and has_all_valid_fields
    has_all_valid_fields = validate_hgt( passport_mut.pop("hgt", None) )  and has_all_valid_fields
    has_all_valid_fields = validate_hcl( passport_mut.pop("hcl", None) )  and has_all_valid_fields
    has_all_valid_fields = validate_ecl( passport_mut.pop("ecl", None) )  and has_all_valid_fields
    has_all_valid_fields = validate_pid( passport_mut.pop("pid", None) )  and has_all_valid_fields
    has_all_valid_fields = validate_cid( passport_mut.pop("cid", None) )  and has_all_valid_fields

    if len(passport_mut) != 0: # and has_all_valid_fields:
        return False


    # if has_all_valid_fields:
    #     print("valid passport")
    #     for key, value in sorted(passport.items()):
    #         print("{} : {}".format(key, value))

    return has_all_valid_fields
### validate_passport

print("")
print("")


print("--- Testing P2A Sample ---")
valid_passports, invalid_passports = process_batch_file("2020_04_sample_valid.txt", validate_passport_field_validation)
test_equal(valid_passports,   4, "P2A: valid passport count is wrong")
test_equal(invalid_passports, 0, "P2A: invalid passport count is wrong")
print("-------------------------")


print("--- Testing P2B Sample ---")
valid_passports, invalid_passports = process_batch_file("2020_04_sample_invalid.txt", validate_passport_field_validation)
test_equal(valid_passports,   0, "P2B: valid passport count is wrong")
test_equal(invalid_passports, 4, "P2B: invalid passport count is wrong")
print("-------------------------")




valid_passports, invalid_passports = process_batch_file(input_file, validate_passport_field_validation)


print( "Solution to day 4 part 2: {0}".format(valid_passports))

# 161 is too high
