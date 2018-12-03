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

result = 0

for index1 in plans:
    plan1 = plans[index1]
    curr_plan_collide = False
    for index2 in plans:
        if index1 == index2:
            continue

        plan2 = plans[index2]

        curr_plan_collide = not ((plan2["x"] >= plan1["x"] + plan1["w"]) or (plan1["x"] >= plan2["x"] + plan2["w"]) or (plan2["y"] >= plan1["y"] + plan1["h"]) or (plan1["y"] >= plan2["y"] + plan2["h"]))
        
        if curr_plan_collide:
            break
        
    if not curr_plan_collide:
        result = index1
        break

print("Answer for puzzle #6: {}".format(result))
