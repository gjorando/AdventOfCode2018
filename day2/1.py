#!/usr/bin/env python3

ids = []

with open("input") as input_file:
    for _, curr_id in enumerate(input_file):
        ids.append(curr_id.replace('\n', ""))

count_ids_2 = 0
count_ids_3 = 0

for curr_id in ids:
    counts = {}
    for letter in curr_id:
        if letter in counts:
            counts[letter]+= 1
        else:
            counts[letter] = 1

    if 2 in counts.values():
        count_ids_2+= 1
    if 3 in counts.values():
        count_ids_3+= 1

checksum = count_ids_2*count_ids_3

print("Answer for puzzle #3: {}".format(checksum))
