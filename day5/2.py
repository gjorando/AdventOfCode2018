#!/usr/bin/env python3

import string

original_string = None

with open("input") as input_file:
    original_string = input_file.readline().replace("\n", "")

min_length = None
min_letter = None

for letter in string.ascii_lowercase:
    input_string = original_string.replace(letter, "").replace(letter.upper(), "")
    if len(input_string) == len(original_string):
        continue

    reacted = True
    while reacted:
        reacted = False
        new_string = ""
        i = 1
        while i < len(input_string):
            unit = input_string[i]
            prev_unit = input_string[i-1]

            unit_polarity = unit.isupper()
            prev_unit_polarity = prev_unit.isupper()

            if (unit.lower() != prev_unit.lower()) or (unit_polarity == prev_unit_polarity):
                new_string+= prev_unit
                i+= 1
            else:
                reacted = True
                i+= 2
            if i == len(input_string):
                new_string+= input_string[-1]
        input_string = new_string

    tested_length = len(input_string)

    if (min_length is None) or (tested_length < min_length):
        min_length = tested_length
        min_letter = letter

print("Answer for puzzle #10: {} with unit {}".format(min_length, min_letter))
