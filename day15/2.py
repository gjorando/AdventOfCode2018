#!/usr/bin/env python3

import numpy as np

class Map:
    elf_identifier = "E"
    goblin_identifier = "G"

    def __init__(self, init_list, elf_power = 3):
        self._map = np.array(init_list)
        self._rounds_count = 0
        self._elves = []
        self._goblins = []
        for coord in np.transpose(np.where(np.multiply(self._map != "#", self._map != "."))):
            pos = (coord[1], coord[0])
            player = self._map[tuple(coord)]
            if player == self.goblin_identifier:
                self._goblins.append(Fighter(pos, str(player)))
            elif player == self.elf_identifier:
                self._elves.append(Fighter(pos, str(player), power=elf_power))
            else:
                raise ValueError("Unrecognized fighter: {}".format(player))
            self._map[tuple(coord)] = "."

    def __getitem__(self, key):
        if type(key) != tuple:
            raise IndexError("invalid index value: {}".format(key))
        elif len(key) != 2:
            raise IndexError("key tuple should be of size 2 ({} found)".format(len(key)))
        t_key = (key[1], key[0])
        for elf in self._elves:
            if elf._coord == key:
                return self.elf_identifier
        for goblin in self._goblins:
            if goblin._coord == key:
                return self.goblin_identifier
        return self._map[t_key]

    def __repr__(self):
        res = ""
        fighters = ""
        for y in range(self._map.shape[0]):
            for x in range(self._map.shape[1]):
                elem = self[x,y]
                res+= elem
                if elem in (self.elf_identifier, self.goblin_identifier):
                    fighters+= str(self.fighter_at((x,y))) + "\n"

            res+="\n"
        
        return res
        return res+fighters[:len(fighters)-1]

    def fighter_at(self, key):
        if type(key) != tuple:
            raise IndexError("invalid index value: {}".format(key))
        elif len(key) != 2:
            raise IndexError("key tuple should be of size 2 ({} found)".format(len(key)))

        for elf in self._elves:
            if elf._coord == key:
                return elf
        for goblin in self._goblins:
            if goblin._coord == key:
                return goblin
        raise IndexError("no fighter found at given coordinates: {}".format(key))

    def take_turn(self):
        fighters = sorted(self._elves + self._goblins, key=lambda x: (x._coord[1], x._coord[0])) # Ordered list of fighters
        for fighter in fighters: # We iterate through each fighter
            ## WINNER CHECKING PHASE ##

            if self.winner(): # If we already have a winner
                self._rounds_count-= 1 # We remove this round because it was not completed
                break

            if not fighter.is_alive(): # The fighter may have been killed by another fighter
                continue

            ## MOVING PHASE ##

            opponents = self._goblins if fighter._side == self.elf_identifier else self._elves # Get the list of opponents of the current fighter
            target_coords = sorted([item for sublist in [neighbour_coords(t._coord) for t in opponents] for item in sublist], key=lambda x: (x[1], x[0])) # Get the neighboring tiles for each opponent, and order them
            if not fighter._coord in target_coords: # If the fighter is already on a target, don't move it
                fighter_dijkstra, distances = self.dijkstra(fighter, target_coords) # Compute dijkstra for the current fighter
            
                min_dist = None
                min_targets = []
                for target_coord in target_coords: # We find the first reachable target coordinate
                    if distances[target_coord] == -1: # Target is unreachable
                        continue
                    if (min_dist == None) or (distances[target_coord] < min_dist):
                        min_dist = distances[target_coord]
                        min_targets = [target_coord]
                    elif (min_dist != None) and (distances[target_coord] == min_dist):
                        min_targets.append(target_coord)
                if len(min_targets) != 0: # If we have a reachable target
                    candidate_moves = [] # Each value is [move, destination tile], so that we can resolve a tie
                    for min_target in min_targets:
                        candidate_moves.append([fighter_dijkstra[min_target][0], min_target])

                    candidate_moves = sorted(candidate_moves, key=lambda x: (x[1][1], x[1][0], x[0][1], x[0][0]))
                    
                    fighter._coord = candidate_moves[0][0] # And we move the player

            ## ATTACKING PHASE ##

            neighbours = neighbour_coords(fighter._coord)
            targets = []
            for neighbour in neighbours: # We get each available target among fighter's neighbours
                try:
                    candidate = self.fighter_at(neighbour)
                    if candidate._side != fighter._side:
                        targets.append(candidate)
                except IndexError: # We skip this neighbour is there is no target
                    pass
            if len(targets) == 0: # If we have no target, the fighter doesn't attack
                continue

            targets = sorted(targets, key=lambda x: (x._health, x._coord[1], x._coord[0])) # We sort potential target by health, then by reading order
            target = targets[0]

            killed = fighter.hit(target)

            if killed:
                if target._side == self.goblin_identifier:
                    self._goblins.remove(target)
                else:
                    self._elves.remove(target)
                    return False # No elf must die!!
        
        # At last we increase the rounds counter
        self._rounds_count+= 1
        return True

    def dijkstra(self, origin, t_coords):
        target_coords = t_coords.copy()
        distances = np.transpose(np.ones_like(self._map, dtype=int)) # We use a transposed distance array, to work using our coordinate system (X,Y) instead of matrixes's one (Y,X)
        distances[:] = -1
        distances[origin._coord] = 0

        result = np.ones_like(distances, dtype=list) # An item looks like [<coord of the move to perform to eventually reach this point>, <next step>] (a coord is a 2-tuple)
        result[:] = None
        
        w, h = distances.shape
        nodes = [(a,b) for a,b in zip(list(np.repeat(np.arange(w), h)), list(np.arange(h))*w) if (self[a,b] == ".") or ((a,b) == origin._coord)]
        first_moves = neighbour_coords(origin._coord)
        
        while (len(nodes) != 0) and (len(target_coords) != 0):
            # We find the nearest non explored node from origin
            min_dist = -1
            nearest = None
            for node in nodes:
                dist = distances[node]
                if (dist != -1) and ((min_dist == -1) or (dist < min_dist)):
                    min_dist = dist
                    nearest = node
            
            if nearest is None: # No more reachable nodes
                break

            # We remove the nearest non explored node from the list of non explored nodes, and if it was a target node we remove it from the list of non explored target nodes as well
            nodes.remove(nearest)
            if nearest in target_coords:
                target_coords.remove(nearest)
            
            # We update distances for each neighbor of nearest
            neighbours = neighbour_coords(nearest)
            
            for neighbour in neighbours:
                if (self[neighbour] == ".") and ((distances[neighbour] == -1) or (distances[neighbour] >= distances[nearest] + 1)):
                    if neighbour in first_moves: # If we are computing the first moves around the origin
                        result[neighbour] = [neighbour, nearest] # Nearest is the origin here
                        distances[neighbour] = 1
                    else:
                        #if (distances[neighbour] != distances[nearest] + 1) or ((nearest[1], nearest[0]) < (result[neighbour][1], result[neighbour][0])):
                        if (distances[neighbour] != distances[nearest] + 1) or ((result[nearest][0][1], result[nearest][0][0]) < (result[neighbour][0][1], result[neighbour][0][0])):
                            result[neighbour] = [result[nearest][0], nearest]
                            distances[neighbour] = distances[nearest] + 1
        
        return result, distances

    def winner(self):
        return self.elf_identifier if len(self._goblins) == 0 else self.goblin_identifier if len(self._elves) == 0 else None

class Fighter:
    def __init__(self, pos, side, health=200, power=3):
        if (type(pos) != tuple) or (len(pos) != 2):
            raise ValueError("pos should be a tuple of size 2 ({} given)".format(type(pos)))
        if (type(health) != int) or (health <= 0):
            raise ValueError("health should be a positive integer ({} given)".format(health))
        if (type(power) != int) or (power <= 0):
            raise ValueError("power should be a positive integer ({} given)".format(power))
        if (type(side) != str):
            raise ValueError("side should be a string ({} given)".format(type(side)))
        self._coord = pos
        self._side = side
        self._health = health
        self._power = power

    def __repr__(self):
        return "{}({}, {})={}".format(self._side, self._coord[0], self._coord[1], self._health, self._power)

    def is_alive(self):
        return self._health > 0

    def hit(self, target):
        if type(target) != type(self):
            raise ValueError("target should be a Fighter ({} given)".format(type(target)))
        target._health-= self._power
        return target._health <= 0

def neighbour_coords(nearest):
    return [(nearest[0], nearest[1]-1), (nearest[0]-1, nearest[1]), (nearest[0]+1, nearest[1]), (nearest[0], nearest[1]+1)]

def play_file(path, verbose=False):
    raw_map = []
    with open(path) as input_file:
        for _, raw_line in enumerate(input_file):
            raw_map.append(list(raw_line.replace("\n", "")))
    no_dead_elf = False
    elf_power = 4
    while not no_dead_elf:
        print("## Trying for elf power of {} ##".format(elf_power))
        battle_map = Map(raw_map, elf_power)

        if verbose:
            pass
            print("Initial map")
            print(battle_map)
            print("")

        while battle_map.winner() is None:
            elf_killed = not battle_map.take_turn()
            if verbose:
                if battle_map.winner() is None:
                    print("Round #{}".format(battle_map._rounds_count))
                else:
                    print("We've got a winner!")
                print(battle_map)
                print("")
            if elf_killed:
                print("An elf was killed on round #{}".format(battle_map._rounds_count+1))
                break

        if not elf_killed:
            no_dead_elf = True
        else:
            elf_power+= 1

    print()

    score = sum([f._health for f in battle_map._elves])
    result = battle_map._rounds_count * score
    return result

print("Answer for puzzle #30: {}".format(play_file("input")))
