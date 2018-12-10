#!/usr/bin/env python3

import re

matching_regex = re.compile("(?P<num_players>\d+) players; last marble is worth (?P<num_marbles>\d+) points")

with open("input") as input_file:
    matched_values = matching_regex.match(input_file.readline().replace("\n", ""))
    num_players = int(matched_values.group("num_players"))
    num_marbles = int(matched_values.group("num_marbles"))

score_per_player = [0 for i in range(num_players)]

marbles = [0]

curr_marble_index = 0
curr_user = 1
for marble in range(1, num_marbles+1):
    if marble % 23 == 0:
        curr_marble_index = (curr_marble_index-7)%len(marbles)
        score_per_player[curr_user-1]+= marble + marbles.pop(curr_marble_index)
    else:
        curr_marble_index = (curr_marble_index+1)%len(marbles) + 1
        marbles.insert(curr_marble_index, marble)

    curr_user = curr_user+1 if curr_user < num_players else 1

result = max(score_per_player)

print("Answer for puzzle #17: {}".format(result))
