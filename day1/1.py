#!/usr/bin/env python3

result = 0

with open("input") as input_frequencies:
    for _, frequency in enumerate(input_frequencies):
        result+= int(frequency)

print("Answer for puzzle #1: {}".format(result))
