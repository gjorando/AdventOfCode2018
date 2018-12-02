#!/usr/bin/env python3

reached_frequencies = set()
input_frequencies = []
result = 0
reached_twice = False

with open("input") as input_file:
    for _, freq in enumerate(input_file):
        input_frequencies.append(int(freq))

while not reached_twice:
    for frequency in input_frequencies:
        result+= frequency
        if result in reached_frequencies:
            reached_twice = True
            break

        reached_frequencies.add(result)
    
print("Answer for puzzle #2: {}".format(result))
