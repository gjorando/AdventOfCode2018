#!/usr/bin/env python3

import re

puzzle_input = 607331

max_iters = puzzle_input+10

def join_pattern(recipes_slice):
    return "".join([str(r) for r in recipes_slice])

recipes = [3, 7] + [0 for i in range(max_iters-2)]

elf_1 = 0
elf_2 = 1

i = 2
while i < max_iters:
    recipes_sum = recipes[elf_1] + recipes[elf_2]
    if recipes_sum < 10:
        recipes[i] = recipes_sum
        i+= 1
    else:
        recipes[i] = 1
        recipes[i+1] = recipes_sum-10
        i+= 2

    elf_1 = (elf_1 + (recipes[elf_1] + 1))%i
    elf_2 = (elf_2 + (recipes[elf_2] + 1))%i
    
result = join_pattern(recipes[puzzle_input:puzzle_input+10])

print("Answer for puzzle #27: {}".format(result))
