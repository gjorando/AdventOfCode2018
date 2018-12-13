#!/usr/bin/env python3

import numpy as np

def display(tracks_array, cars_array):
    for line, car in zip(tracks_array, cars_array):
        print("".join([t if c == "" else c for t, c in zip(line, car)]))

def move(tracks_array, cars_array, states_array, coord):
    car = cars_array[coord[0], coord[1]]
    
    if car == "":
        raise ValueError("There is no car at given coordinates: ({},{})".format(coord[1], coord[0]))
    elif car == ">":
        next_coord = [coord[0], coord[1]+1]
    elif car == "<":
        next_coord = [coord[0], coord[1]-1]
    elif car == "v":
        next_coord = [coord[0]+1, coord[1]]
    else:
        next_coord = [coord[0]-1, coord[1]]
    
    next_track = tracks_array[next_coord[0], next_coord[1]]

    if next_track == " ":
        raise ValueError("There is no track at given coordinates: ({},{})".format(next_coord[1], next_coord[0]))
    elif next_track == "\\":
        next_car = "<" if car == "^" else "v" if car == ">" else "^" if car == "<" else ">"
    elif next_track == "/":
        next_car = ">" if car == "^" else "^" if car == ">" else "v" if car == "<" else "<"
    elif next_track == "+":
        directions = ["^", ">", "v", "<"]
        next_car = directions[(directions.index(car) + (states_array[coord[0], coord[1]]-2))%4]
        states_array[coord[0], coord[1]]+= 1
        if states_array[coord[0], coord[1]] > 3:
            states_array[coord[0], coord[1]] = 1
    else:
        next_car = car

    states_array[next_coord[0], next_coord[1]] = states_array[coord[0], coord[1]]
    states_array[coord[0], coord[1]] = 0
    
    collision = cars_array[next_coord[0], next_coord[1]] != ""

    if collision:
        cars_array[next_coord[0], next_coord[1]] = "X"
        states_array[next_coord[0], next_coord[1]] = -1
    else:
        cars_array[next_coord[0], next_coord[1]] = next_car

    cars_array[coord[0], coord[1]] = ""

    return collision

lines = []

with open("input") as input_file:
    for _, line in enumerate(input_file):
        lines.append(list(line.replace("\n", "")))

tracks_array = np.array(lines) # NB: Don't forget that you access the coordinates X,Y using tracks_array[Y,X] !
cars_array = np.zeros_like(tracks_array)
states_array = np.zeros_like(tracks_array, dtype=int)

cars_on_tracks = np.add(np.add(tracks_array == "^", tracks_array == "v"), np.add(tracks_array == "<", tracks_array == ">"))

for coord in np.transpose(np.where(cars_on_tracks)):
    car = tracks_array[coord[0], coord[1]]
    cars_array[coord[0], coord[1]] = car
    states_array[coord[0], coord[1]] = 1
    if car in (">", "<"):
        tracks_array[coord[0], coord[1]] = "-"
    else:
        tracks_array[coord[0], coord[1]] = "|"

collision = False
while not collision:
    for coord in np.transpose(np.where(cars_on_tracks)):
        collision = collision or move(tracks_array, cars_array, states_array, coord)
    
    cars_on_tracks = cars_array != ""

result = list(np.transpose(np.where(states_array==-1)))[0]

print("Answer for puzzle #25: ({},{})".format(result[1], result[0]))
