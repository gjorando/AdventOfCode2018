#!/usr/bin/env python3

import numpy as np

serial_number = 9798 # Input for puzzle

grid = np.zeros((300, 300))

for i in range(300):
    for j in range(300):
        x = i+1
        y = j+1
        rack_id = x + 10 # Rack id is X coordinate plus 10
        grid[j,i] = rack_id*y # Power level set at rack id times Y coordinate
        grid[j,i]+= serial_number # Power level augmented by serial number
        grid[j,i]*= rack_id # Power level multiplied by rack id
        grid[j,i] = 0 if grid[j,i] < 100 else int(str(int(grid[j,i]))[-3]) # We keep only the hundreds digit
        grid[j,i]-= 5 # Substract 5

max_i = 0
max_j = 0
max_s = 0
max_power = None

# I'm pretty sure there is a way to make this piece of code faster (because a square of size n contains the square of size n-1), but I'm lazy
for s in range(1, 301):
    for i in range(301-s):
        for j in range(301-s):
            curr_power = grid[j:j+s,i:i+s].sum()
            if (max_power is None) or (curr_power > max_power):
                max_power = curr_power
                max_i = i
                max_j = j
                max_s = s

print(grid[max_j:max_j+3,max_i:max_i+3])

print("Answer for puzzle #22: {},{},{} with a power of {}".format(max_i+1, max_j+1, max_s, max_power))
