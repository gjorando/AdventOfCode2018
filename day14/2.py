#!/usr/bin/env python3

import re

puzzle_input = 607331
input_size = len(str(puzzle_input))

max_size = 100*puzzle_input

recipes = [3, 7] + [0 for _ in range(max_size)]

elf_1 = 0
elf_2 = 1

i = 2
found_at = -1
while True:
    recipes_sum = recipes[elf_1] + recipes[elf_2]
    if recipes_sum < 10:
        recipes[i] = recipes_sum
        i+= 1
    else:
        recipes[i] = 1
        recipes[i+1] = recipes_sum-10
        i+= 2
        if (i > input_size+1) and (int("".join([str(r) for r in recipes[i-input_size-2:i-2]])) == puzzle_input):
            found_at = i-input_size-2
            break

    if (i > input_size+1) and (int("".join([str(r) for r in recipes[i-input_size-1:i-1]])) == puzzle_input):
        found_at = i-input_size-1
        break

    elf_1 = (elf_1 + (recipes[elf_1] + 1))%i
    elf_2 = (elf_2 + (recipes[elf_2] + 1))%i
    
result = found_at

print("Answer for puzzle #28: {}".format(result))
