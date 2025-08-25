opposite = {'north' : 'south', 'west': 'east', 'south': 'north', 'east': 'west'}
directions = ['north', 'south', 'west', 'east']

import procedure_descr as pd
from aistuff.gamemaster import descr
# from items.UseObjects import Door
from random import shuffle, choice
from collections import deque

class Path:
    def __init__(self, next_room = None, door = None, description = ""):

        if description == "" and next_room != None:
            description = descr(pd.random_specs(pd.path_specifications))

        self.obstacle = door
        self.next_room = next_room
        self.description = description
        if door == None:
            self.visible_through = True
        else:
            self.visible_through = False

    def __str__(self):
        return self.description

class Room:
    def __init__(self, 
                 name,
                 north_room = None, north_obstacle = None,
                 east_room  = None, east_obstacle = None,
                 south_room  = None, south_obstacle = None,
                 west_room  = None, west_obstacle = None,
                 description = ''
                ):
        
        if description == "":
            description = descr(pd.random_specs(pd.room_specifications))
        
        self.name = name              
        self.items = {}
        self.chars = {}
        self.description = description

        self.north = Path(north_room, north_obstacle) # <Room объект, Door объект>
        self.east = Path(east_room, east_obstacle)
        self.south = Path(south_room, south_obstacle)
        self.west = Path(west_room, west_obstacle)
    
    def add_path(self, path: Path, direction):
        direction = direction.lower()
        if direction in directions and getattr(self, direction).next_room == None:
            setattr(self, direction, path)
            return True
        return False
    
    def __str__(self, max_distance = 4, distance = 0):
        items = [str(item) for item in self.items.values()]
        description = self.name + self.description + f"Предметы в комнате: {items}"
        return description
        """Возвращается в уже просмотренные комнаты во время обхода графа"""
        # for direction in directions: # Собирает описание с соседних комнат/тайлов если между ними нету препятсвие или есть другая видимость (для больших комнат)
        #     if getattr(self, direction).next_room != None and (getattr(self, direction).obstacle == None or getattr(self, direction).obstacle.visible_through == True) and distance <= max_distance:
        #         description += getattr(self, direction).next_room.__str__(distance = distance + 1)
        # return self.name + description
 
class Graph:
    def __init__(self):
        self.rooms = {}
        self.coordinates = {}
        self.room_coordinates = {}

    def repr(self):
        for r in self.rooms.values():
            print(f"{r.name} - {self.room_coordinates[r]}:")
            for d in directions:
                n_r = getattr(r, d, None)
                if n_r != None:
                    if n_r.next_room != None:
                        n_r = n_r.next_room
                        print(f"{d} - {n_r.name} ")
        print()
    
