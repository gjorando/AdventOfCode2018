#!/usr/bin/env python3

import re

def time_for_node(node):
    return ord(node) - ord("A") + 61

num_workers = 5

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
nodes_to_finish = len(available_nodes)
finished_nodes = []

result = 0
workers = [{"node": None, "time": 0} for i in range(num_workers)]

current_time = 0

while 1:
    for worker, _ in enumerate(workers):
        if not workers[worker]["node"] is None:
            workers[worker]["time"]-= 1
            if workers[worker]["time"] == 0:
                finished_nodes.append(workers[worker]["node"])
                workers[worker]["node"] = None
    
    if len(finished_nodes) == nodes_to_finish:
        break

    candidate_nodes = sorted(
        [
            node for node in available_nodes 
            if 
                (not node in constraints)
                or
                (sum([1 for prec in constraints[node] if not prec in finished_nodes]) == 0)
        ]
    )
    
    for curr_node in candidate_nodes:
        for curr_worker, _ in enumerate(workers):
            if workers[curr_worker]["node"] is None:
                workers[curr_worker]["node"] = curr_node
                workers[curr_worker]["time"] = time_for_node(curr_node)
                available_nodes.remove(curr_node)
                break
    print("{}:\t{}".format(current_time, "".join([(w["node"] if (not w["node"] is None) else "-") for w in workers])))
    current_time+= 1

print("Answer for puzzle #14: {}".format(current_time))
