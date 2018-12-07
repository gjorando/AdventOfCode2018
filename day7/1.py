#!/usr/bin/env python3

import re

parsing_regex = re.compile("Step (?P<node>[A-Z]) must be finished before step (?P<succ>[A-Z]) can begin.")

constraints = {}
available_nodes = []

with open("input") as input_file:
    for _, raw_arc in enumerate(input_file):
        parsed_arc = parsing_regex.match(raw_arc.replace("\n", ""))
        node = parsed_arc.group("node")
        succ = parsed_arc.group("succ")

        available_nodes.append(node)
        available_nodes.append(succ)

        if succ in constraints:
            constraints[succ].append(node)
        else:
            constraints[succ] = [node]
     
available_nodes = sorted(list(set(available_nodes)))

result = []

while len(available_nodes) != 0:
    candidate_nodes = sorted(
        [
            node for node in available_nodes 
            if 
                (not node in constraints)
                or
                (sum([1 for prec in constraints[node] if prec in available_nodes]) == 0)
        ]
    )
    
    chosen_node = candidate_nodes[0]
    available_nodes.remove(candidate_nodes[0])
    
    result.append(chosen_node)

print("Answer for puzzle #13: {}".format("".join(result)))
