opposite = {'north' : 'south', 'west': 'east', 'south': 'north', 'east': 'west'}
directions = ['north', 'south', 'west', 'east']

# from items.UseObjects import Door
from random import shuffle, choice
from collections import deque

class Path:
    def __init__(self, next_room = None, door = None):
        self.obstacle = door
        self.next_room = next_room
        self.description = ''
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
        
        self.name = name              
        self.items = {}
        self.description = ""

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
        description = self.description
        for direction in directions: # Собирает описание с соседних комнат/тайлов если между ними нету препятсвие или есть другая видимость (для больших комнат)
            if getattr(self, direction).next_room != None and (getattr(self, direction).obstacle == None or getattr(self, direction).visible_through == True) and distance <= max_distance:
                description += getattr(self, direction).next_room.__str__(distance + 1)
        return self.name + description
 
class Graph:
    def __init__(self):
        self.rooms = {}
        self.coordinates = {}
        self.room_coordinates = {}
    
    def calculate_coordinates(self): # НЕ РАБОТАЕТ!!!

        # поиск точки отсчета графа 
        starting_room = self.rooms.get("starting_room")
        if not starting_room:
            return
        self.coordinates = {}
        self.room_coordinates = {}
        self.coordinates[(0,0)] = starting_room
        self.room_coordinates[starting_room] = (0,0)

        #BFS
        calculated = set()
        calculated.add(starting_room)
        q = deque()
        q.append(starting_room)
        x, y = 0, 0
        while q :
            current = q.popleft()
            if current != None:
                x, y = self.room_coordinates[current]
                for direction in directions:
                    next_room = getattr(current, direction).next_room
                    if next_room not in calculated:
                        if direction == "north":
                            x, y = x, y + 1
                            self.coordinates[x, y] = next_room
                            self.room_coordinates[next_room] = (x, y )
                        elif direction == "east":
                            x, y = x + 1, y
                            self.coordinates[x , y ] = next_room
                            self.room_coordinates[next_room] = (x , y)
                        elif direction == "south":
                            x, y = x, y - 1
                            self.coordinates[x , y ] = next_room
                            self.room_coordinates[next_room] = (x, y )
                        elif direction == "west":
                            x, y = x - 1, y
                            self.coordinates[x, y] = next_room
                            self.room_coordinates[next_room] = (x, y)
                        q.append(next_room)
                        calculated.add(next_room)

    def serialize(self):
        serialized_rooms = []
        for room_name, room_obj in self.rooms.items():
            room_data = room_obj.__dict__.copy()
            room_data['name'] = room_name
            if room_obj in self.room_coordinates:
                x, y = self.room_coordinates[room_obj]
                room_data['x'] = x
                room_data['y'] = y
            else:
                room_data['x'] = None
                room_data['y'] = None
            
            serialized_rooms.append(room_data)
        return {'Graph': serialized_rooms}
