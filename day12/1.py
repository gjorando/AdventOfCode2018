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
    new_pots = left_pots+re.match("(?P<right_pots>[#.]+#)\.*$", right_pots).group("right_pots")

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

generations = [(pots, 0)]

index_of_zero = 0
for _ in range(20):
    pots, index_of_zero = next_generation(pots, rules, index_of_zero)
    generations.append((pots, index_of_zero))

print("{}0<-pos of zero".format("".join([" " for _ in range(len(str(len(generations)))+2+index_of_zero)])))
for i, (gen, idx) in enumerate(generations):
    print("{}{}: {}{}".format("".join([" " for _ in range(len(str(len(generations)))-len(str(i)))]), i, "".join(["." for _ in range(index_of_zero-idx)]), gen))

result = sum([i-index_of_zero for i in range(len(pots)) if pots[i] == "#"])

print("Answer for puzzle #23: {}".format(result))
