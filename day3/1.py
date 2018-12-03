#!/usr/bin/env python3

import re
import numpy as np

plans = {}

parsing_regex = re.compile("^#(?P<id>\d+) @ (?P<x>\d+),(?P<y>\d+): (?P<w>\d+)x(?P<h>\d+)")

max_x = 0
max_y = 0

with open("input") as input_file:
    for _, raw_plan in enumerate(input_file):
        regex_plan = parsing_regex.match(raw_plan.replace("\n", ""))

        plan_id = int(regex_plan.group("id"))
        plan_x = int(regex_plan.group("x"))
        plan_y = int(regex_plan.group("y"))
        plan_w = int(regex_plan.group("w"))
        plan_h = int(regex_plan.group("h"))
        
        new_max_x = plan_x+plan_w
        if new_max_x > max_x:
            max_x = new_max_x
        new_max_y = plan_y+plan_h
        if new_max_y > max_y:
            max_y = new_max_y

        plans[plan_id] = {
            "x": plan_x,
            "y": plan_y,
            "w": plan_w,
            "h": plan_h
        }

fabric = np.zeros((max_x+1, max_y+1))

for index in plans:
    plan = plans[index]
    for i in range(plan["x"], plan["x"]+plan["w"]):
        for j in range(plan["y"], plan["y"]+plan["h"]):
            fabric[i,j]+= 1

result = np.sum(fabric > 1)

print("Answer for puzzle #5: {}".format(result))
