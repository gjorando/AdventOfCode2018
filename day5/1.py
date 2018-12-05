#!/usr/bin/env python3

input_string = None

with open("input") as input_file:
    input_string = input_file.readline().replace("\n", "")

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

result = len(input_string)

print("Answer for puzzle #9: {}".format(result))
