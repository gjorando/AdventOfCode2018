#!/usr/bin/env python3

import re

matching_regex = re.compile("(?P<num_players>\d+) players; last marble is worth (?P<num_marbles>\d+) points")

with open("input") as input_file:
    matched_values = matching_regex.match(input_file.readline().replace("\n", ""))
    num_players = int(matched_values.group("num_players"))
    num_marbles = int(matched_values.group("num_marbles"))

num_marbles*= 100

score_per_player = [0 for i in range(num_players)]

# marbles is a list, associating to each marble the index of the marble clockwise next to it
marbles = [0 if i==0 else None for i in range(num_marbles+1)]

curr_marble_index = 0
curr_user = 1
for marble in range(1, num_marbles+1):
    if marble % 23 == 0:
        popped_marble = marbles[marble-5]
        score_per_player[curr_user-1]+= marble + popped_marble
        marbles[marble-5] = marbles[popped_marble]
        curr_marble_index = marbles[popped_marble]
    else:
        marbles[marble] = marbles[marbles[curr_marble_index]]
        marbles[marbles[curr_marble_index]] = marble
        curr_marble_index = marble

    curr_user = curr_user+1 if curr_user < num_players else 1

result = max(score_per_player)

print("Answer for puzzle #18: {}".format(result))
