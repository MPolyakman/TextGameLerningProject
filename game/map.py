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
    def __str__(self, distance = 0):
        description = self.description
        for direction in directions: # Собирает описание с соседних комнат/тайлов если между ними нету препятсвие или есть другая видимость (для больших комнат)
            if getattr(self, direction).next_room != None and (getattr(self, direction).obstacle == None or getattr(self, direction).visible_through == True):
                description += getattr(self, direction).next_room.__str__(distance + 1)
        return description
    
class Graph:
    def __init__(self):
        self.rooms = {}
        self.coordinates = {}
        self.room_coordinates = {}
    
    def add_room(self, room: Room):
        self.rooms[room.name] = room
    
    def add_edge(self, from_room: Room, direction, to_room: Room, door = None):
        from_path = Path(to_room, door)
        to_path = Path(from_room, door)
        direction = direction.lower()
        from_room_slot_free = getattr(from_room, direction).next_room is None
        to_room_slot_free = getattr(to_room, opposite[direction]).next_room is None
        if direction in directions and from_room_slot_free and to_room_slot_free:
            from_room.add_path(from_path, direction)
            to_room.add_path(to_path, opposite[direction])
            return True
        return False
    
    def generate_graph(self, rooms: list):
        shuffle(rooms)
        starting_room = [r for r in rooms if r.name == "starting_room"][0]
        self.coordinates[(0,0)] = starting_room
        self.room_coordinates[starting_room] = (0,0)
        self.add_room(starting_room)
        rooms.remove(starting_room)
        occupied_coords = set()
        occupied_coords.add((0,0))
        x, y = 0, 0
        
        while rooms:
            r = choice(rooms)
            d = choice(directions)
            node = choice(list(self.rooms.values()))
            x, y = (self.room_coordinates[node])
            match d:
                case "north":
                    x, y = x, y + 1
                case "east":
                    x, y = x + 1, y
                case "south":
                    x, y = x, y - 1
                case "west":
                    x, y = x - 1, y
            if (x, y) not in occupied_coords:
                if self.add_edge(node, d, r):
                    rooms.remove(r)
                    self.add_room(r)
                    self.room_coordinates[r] = (x, y)
                    self.coordinates[(x, y)] = r
                        
        # n = len(rooms) // 3
        # main_root = []
        # for i in range(n):
        #     room = rooms[i]
        #     if room.name == "starting_room":
        #         starting_room = room
        #         rooms.remove(room)
        #         continue
        #     main_root.append(room)
        #     rooms.remove(room)

        # prev_node = starting_room
        # node = starting_room
        # for room in main_root:
        #     for direction in directions:
        #         if random.random()  <= 0.6 and getattr(node, direction).next_room == None:
        #             self.add_edge(node, direction, room)
        #             break
        #     else:
        #         for direction in directions:
        #             if getattr(prev_node, direction).next_room == None:
        #                 self.add_edge(prev_node, direction, room)
        #                 break
        #     prev_node = node
        #     node = room


    def calculate_coordinates(self):

        # поиск точки отсчета графа 
        starting_room = self.rooms.get("starting_room")
        if not starting_room:
            return
        self.coordinates = {}
        self.coordinates[(0,0)] = starting_room

        #BFS
        calculated = set()
        calculated.add(starting_room)
        q = deque()
        q.append(starting_room)
        x, y = 0, 0
        while q :
            current = q.popleft()
            for direction in directions:
                next_room = getattr(current, direction).next_room
                if next_room not in calculated:
                    if direction == "north": self.coordinates[x, y + 1] = next_room
                    elif direction == "east": self.coordinates[x + 1, y ] = next_room
                    elif direction == "south": self.coordinates[x , y - 1 ] = next_room
                    elif direction == "west": self.coordinates[x - 1, y] = next_room
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
