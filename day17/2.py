#!/usr/bin/env python3

import re
import numpy as np

class Map:
    tiles = [".", "+", "#", "|", "~"]
    def __init__(self, veins, source):
        x_min = -1
        x_max = -1
        y_min = -1
        y_max = -1
        for curr_x_min, curr_x_max, curr_y_min, curr_y_max in veins:
            if (x_min == -1) or (curr_x_min < x_min):
                x_min = curr_x_min
            if (y_min == -1) or (curr_y_min < y_min):
                y_min = curr_y_min
            if curr_x_max > x_max:
                x_max = curr_x_max
            if curr_y_max > y_max:
                y_max = curr_y_max
        
        self._y_min = y_min

        self._map = np.zeros((3+x_max-x_min, 1+y_max), dtype=int)
        self._map[:] = self.tiles.index(".")

        self._x_offset = x_min-1
        self._y_offset = 0
        
        self._has_changed = True

        for curr_x_min, curr_x_max, curr_y_min, curr_y_max in veins:
            for x in range(curr_x_min, curr_x_max+1):
                for y in range(curr_y_min, curr_y_max+1):
                    self[x,y] = self.tiles.index("#")

        self[source] = self.tiles.index("+")
    
    def __getitem__(self, key):
        if type(key) != tuple:
            raise IndexError("invalid index value: {}".format(key))
        elif len(key) != 2:
            raise IndexError("key tuple should be of size 2 ({} found)".format(len(key)))

        t_key = (key[0]-self._x_offset, key[1]-self._y_offset)

        return self._map[t_key]
    
    def __setitem__(self, key, value):
        if type(key) != tuple:
            raise IndexError("invalid index value: {}".format(key))
        elif len(key) != 2:
            raise IndexError("key tuple should be of size 2 ({} found)".format(len(key)))
        elif type(value) != int:
            raise ValueError("value should be an integer ({} given)".format(type(value)))

        t_key = (key[0]-self._x_offset, key[1]-self._y_offset)
        if self._map[t_key] != value:
            self._has_changed = True
        self._map[t_key] = value

    def __repr__(self):
        res = ""
        for y in range(self._map.shape[1]):
            for x in range(self._map.shape[0]):
        #for y in range(100):
        #    for x in range(122):
                res+= self.tiles[self[x+self._x_offset,y+self._y_offset]]
            res+="\n"

        return res

    def coords_from_np(self, coord):
        return (coord[0]+self._x_offset, coord[1]+self._y_offset)

    def score(self):
        return np.sum(self._map == self.tiles.index("~"))

    def next_frame(self):
        self._has_changed = False

        if np.sum(self._map == self.tiles.index("|")) == 0: # First iteration, so we spawn water from below the source
            source = self.coords_from_np(np.transpose(np.where(self._map == self.tiles.index("+")))[0])
            self[source[0], source[1]+1] = self.tiles.index("|")
        else:
            flows = np.transpose(np.where(self._map == self.tiles.index("|")))
            for flow in flows:
                flow_coords = self.coords_from_np(flow)
                
                try:
                    if self[flow_coords[0], flow_coords[1]+1] == self.tiles.index("|"): # We skip flows that are not the end of a flow (does that make sense?)
                        continue
                except IndexError: # We also skip those at the bottom
                    continue

                continue_flowing = True
                while continue_flowing:
                    try:
                        value_below = self[flow_coords[0], flow_coords[1]+1]
                        if value_below == self.tiles.index("."):
                            self[flow_coords[0], flow_coords[1]+1] = self.tiles.index("|")
                            flow_coords = (flow_coords[0], flow_coords[1]+1)
                        else:
                            continue_flowing = False
                    except IndexError: # This occurs if we reach the bottom
                        continue_flowing = False
                
                if value_below in (self.tiles.index("#"), self.tiles.index("~")): # Otherwise if there is water or clay below the flow, we try to fill cavities or extend the flow on the sides
                    min_border = flow_coords[0]
                    max_border = flow_coords[0]
                    min_border_found = False
                    max_border_found = False
                    while not (min_border_found and max_border_found):
                        if not min_border_found:
                            min_border -= 1
                            if (min_border-self._x_offset < 0) or (self[min_border+1,flow_coords[1]+1] == self.tiles.index(".")):
                                break
                            if (self[min_border, flow_coords[1]] == self.tiles.index("#")):
                                min_border_found = True

                        if not max_border_found:
                            max_border += 1
                            if (max_border-self._x_offset >= self._map.shape[0]) or (self[max_border-1,flow_coords[1]+1] == self.tiles.index(".")) :
                                break
                            if self[max_border, flow_coords[1]] == self.tiles.index("#"):
                                max_border_found = True

                    if min_border_found and max_border_found: # If we have a proper cavity that can be filled
                        for x in range(min_border+1,max_border):
                            self[x, flow_coords[1]] = self.tiles.index("~")
                    else: # Otherwise, we are going to extend the flow
                        min_extension = flow_coords[0]
                        max_extension = flow_coords[0]
                        min_extension_found = False
                        max_extension_found = False
                        while not (min_extension_found and max_extension_found):
                            if not min_extension_found:
                                min_extension-= 1
                                if self[min_extension, flow_coords[1]] == self.tiles.index("#"):
                                    min_extension+= 1
                                    min_extension_found = True
                                elif (min_extension-1-self._x_offset < 0) or (self[min_extension, flow_coords[1]+1] in (self.tiles.index("."), self.tiles.index("|"))):
                                    min_extension_found = True
                            if not max_extension_found:
                                max_extension+= 1
                                if self[max_extension, flow_coords[1]] == self.tiles.index("#"):
                                    max_extension-= 1
                                    max_extension_found = True
                                elif (max_extension+1-self._x_offset >= self._map.shape[0]) or (self[max_extension, flow_coords[1]+1] in (self.tiles.index("."), self.tiles.index("|"))):
                                    max_extension_found = True
                    
                            if min_extension_found and max_extension_found: # If we can extend the flow
                                for x in range(min_extension,max_extension+1):
                                    self[x, flow_coords[1]] = self.tiles.index("|")
        return self._has_changed
   
veins = [] # list of 4-tuples as: (x_min, x_max, y_min, y_max)
with open("input") as input_file:
    for _, raw_line in enumerate(input_file):
        vein = [0]*4
        for raw_coord in raw_line.replace("\n", "").split(", "):
            coord = raw_coord.split("=")
            coord_offset = 0 if coord[0] == "x" else 2
            try:
                coord_min_max = int(coord[1])
                vein[coord_offset] = coord_min_max
                vein[coord_offset+1] = coord_min_max
            except ValueError:
                coord_min, coord_max = coord[1].split("..")
                vein[coord_offset] = int(coord_min)
                vein[coord_offset+1] = int(coord_max)

        veins.append(tuple(vein))

underground = Map(veins, (500, 0))

while underground.next_frame():
    pass

result = underground.score()

print("Answer for puzzle #34: {}".format(result))
