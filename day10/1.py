#!/usr/bin/env python3

import re
import sys, os

def find_point(x, y, points):
    for i, point in enumerate(points):
        if (point["position"][0] == x) and (point["position"][1] == y):
            return i
    return -1

def move_points(points):
    for index in range(len(points)):
        points[index]["position"][0]+= points[index]["velocity"][0]
        points[index]["position"][1]+= points[index]["velocity"][1]

def compute_min_max(points):
    min_x = 3e8
    max_x = -1
    min_y = 3e8
    max_y = -1
    for index in range(len(points)):
        min_x = points[index]["position"][0] if points[index]["position"][0] < min_x else min_x
        max_x = points[index]["position"][0] if points[index]["position"][0] > max_x else max_x
        min_y = points[index]["position"][1] if points[index]["position"][1] < min_y else min_y
        max_y = points[index]["position"][1] if points[index]["position"][1] > max_y else max_y

    return min_x, max_x, min_y, max_y

parsing_regex = re.compile("position=< *(?P<p_x>-?\d+), *(?P<p_y>-?\d+)> velocity=< *(?P<v_x>-?\d+), *(?P<v_y>-?\d+)>")

points = []


with open("input") as input_file:
    for _, raw_point in enumerate(input_file):
        parsed_point = parsing_regex.match(raw_point.replace("\n", ""))
        p_x = int(parsed_point.group("p_x"))
        p_y = int(parsed_point.group("p_y"))
        v_x = int(parsed_point.group("v_x"))
        v_y = int(parsed_point.group("v_y"))

        points.append({"position": [p_x, p_y], "velocity": [v_x, v_y]})

result = ""

max_h, max_w = os.popen('stty size', 'r').read().split()
max_h = int(max_h)
max_w = int(max_w)

while result == "":
    min_x, max_x, min_y, max_y = compute_min_max(points)

    if (max_x-min_x > max_w) or (max_y-min_y > max_h):
        move_points(points)
        continue

    for j in range(min_y, max_y+1):
        line = ""
        for i in range(min_x, max_x+1):
            line+= "#" if find_point(i, j, points) != -1 else "."
        print(line)
    move_points(points)
    result = input("Result (if there is one, leave empty otherwise): ")

print("Answer for puzzle #19: {}".format(result))
