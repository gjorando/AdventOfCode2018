#!/usr/bin/env python3

import numpy as np

class Map:
    tiles = [".", "|", "#"]

    def __init__(self, init_list):
        x = max([len(e) for e in init_list])
        y = len(init_list)
        self._map = np.zeros((x,y), dtype=int)
        for i in range(x):
            for j in range(y):
                line = init_list[i]
                tile = self.tiles.index(line[j])
                try:
                    self._map[j,i] = tile
                except IndexError:
                    break

        self._has_changed = True

    def __getitem__(self, key):
        if type(key) != tuple:
            raise IndexError("invalid index value: {}".format(key))
        elif len(key) != 2:
            raise IndexError("key tuple should be of size 2 ({} found)".format(len(key)))

        return self._map[key]
    
    def __setitem__(self, key, value):
        if type(key) != tuple:
            raise IndexError("invalid index value: {}".format(key))
        elif len(key) != 2:
            raise IndexError("key tuple should be of size 2 ({} found)".format(len(key)))
        elif type(value) != int:
            raise ValueError("value should be an integer ({} given)".format(type(value)))

        if self._map[key] != value:
            self._has_changed = True
        self._map[t_key] = value

    def __repr__(self):
        res = ""
        for y in range(self._map.shape[1]):
            for x in range(self._map.shape[0]):
                res+= self.tiles[self[x,y]]
            res+="\n"

        return res[:len(res)-1]

    def flat_string(self):
        res = ""
        for y in range(self._map.shape[1]):
            for x in range(self._map.shape[0]):
                res+= str(self[x,y])

        return res

    def score(self):
        return np.sum(self._map == self.tiles.index("|"))*np.sum(self._map == self.tiles.index("#"))

    def neighbours_list(self, coord):
        x_min = max(coord[0]-1, 0)
        x_max = min(coord[0]+1, self._map.shape[0]-1)
        y_min = max(coord[1]-1, 0)
        y_max = min(coord[1]+1, self._map.shape[1]-1)

        return [self[x,y] for x in range(x_min, x_max+1) for y in range(y_min, y_max+1) if not ((x == coord[0]) and (y == coord[1]))]

    def next_iteration(self):
        self._has_changed = False
        new_map = np.zeros_like(self._map)

        for x in range(self._map.shape[0]):
            for y in range(self._map.shape[1]):
                tile = self[x,y]
                neighbours = self.neighbours_list((x,y))

                if tile == self.tiles.index("."):
                    new_tile = self.tiles.index("|") if sum([1 for n in neighbours if n == self.tiles.index("|")]) >= 3 else tile
                elif tile == self.tiles.index("|"):
                    new_tile = self.tiles.index("#") if sum([1 for n in neighbours if n == self.tiles.index("#")]) >= 3 else tile
                elif tile == self.tiles.index("#"):
                    new_tile = tile if (sum([1 for n in neighbours if n == self.tiles.index("#")]) >= 1) and (sum([1 for n in neighbours if n == self.tiles.index("|")]) >= 1) else self.tiles.index(".")
                
                if tile != new_tile:
                    self._has_changed = True

                new_map[x,y] = new_tile

        self._map = new_map

raw_map = []
with open("input") as input_file:
    for _, raw_line in enumerate(input_file):
        raw_map.append(list(raw_line.replace("\n", "")))

forest = Map(raw_map)

print("Initial state:")
print(forest)

maps = []

pattern_begin = None
pattern_end = None

for i in range(700):
    forest.next_iteration()
    print("After {} minute{}:".format(i, "s" if i>1 else ""))
    print(forest)
    flat_representation = forest.flat_string()
    if flat_representation in maps:
        print("Found a stable pattern")
        pattern_begin = maps.index(flat_representation)
        pattern_end = i-1
        break
    maps.append(flat_representation)

result_map = maps[pattern_begin+((1000000000-1-pattern_begin)%(1+pattern_end-pattern_begin))]

result = sum([1 for e in result_map if int(e)==forest.tiles.index("|")])*sum([1 for e in result_map if int(e)==forest.tiles.index("#")])

print("Answer for puzzle #36: {}".format(result))
