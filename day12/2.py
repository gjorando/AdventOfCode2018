#!/usr/bin/env python3

import re

def next_generation(pots, rules, index_of_zero):
    new_index_of_zero = index_of_zero
    left_pots = ""
    right_pots = ""

    for i in range(-2, len(pots)+2):
        context = ""
        for j in range(i-2,i+3):
            try:
                context+= pots[j] if j >= 0 else "."
            except IndexError:
                context+= "."

        if context in rules:
            consequence = rules[context]
        else:
            consequence = "."

        if i-index_of_zero < 0:
            left_pots+= consequence
        else:
            right_pots+= consequence
    
    left_pots = re.match("^\.*(?P<left_pots>[#.]*)$", left_pots).group("left_pots")
    new_index_of_zero = len(left_pots)
    right_pots = re.match("(?P<right_pots>[#.]+#)\.*$", right_pots).group("right_pots")
    new_pots = left_pots+right_pots

    return new_pots, new_index_of_zero

parsing_regex = re.compile("(?P<rule>[#.]{5}) => (?P<consequence>[#.])")

rules = {}
with open("input") as input_file:
    pots = input_file.readline().replace("\n", "").split(": ")[1]
    input_file.readline()
    for _, raw_rule in enumerate(input_file):
        parsed_rule = parsing_regex.match(raw_rule.replace("\n", ""))
        rule = parsed_rule.group("rule")
        consequence = parsed_rule.group("consequence")
        
        rules[rule] = consequence

generations = [pots]

stable_pattern = None
trailing_on_first = None
index_of_escape = None

index_of_zero = 0
for i in range(int(5e10)):
    pots, index_of_zero = next_generation(pots, rules, index_of_zero)
    gen_match = re.match("(?P<trailing>\.*)(?P<gen>[#.]+)", pots)
    gen = gen_match.group("gen")
    trailing_on_first = len(gen_match.group("trailing"))
    if gen in generations:
        stable_pattern = gen
        index_of_escape = i
        break
    else:
        generations.append(gen)

result = int(sum([i+trailing_on_first+(5e10-index_of_escape-1) for i in range(len(stable_pattern)) if stable_pattern[i] == "#"]))

print("Answer for puzzle #24: {}".format(result))
