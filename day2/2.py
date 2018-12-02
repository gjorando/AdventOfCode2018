#!/usr/bin/env python3

import numpy as np

ids = []
bytelist_ids = []

with open("input") as input_file:
    for _, curr_id in enumerate(input_file):
        parsed_id = curr_id.replace('\n', "")
        ids.append(parsed_id)
        bytelist_ids.append(np.array(list(bytearray(parsed_id.encode()))))

ids_count = len(ids)
result = None

for i in range(ids_count):
    for j in range(ids_count):
        if i == j:
            continue

        dissimilarity = bytelist_ids[i]-bytelist_ids[j] != 0

        if sum(dissimilarity) == 1:
            result = "".join([ids[i][letter] for letter in range(len(ids[i])) if not dissimilarity[letter]])

print("Answer for puzzle #4: {}".format(result))
