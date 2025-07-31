opposite = {'north' : 'south', 'west': 'east', 'south': 'north', 'east': 'west'}
directions = ['north', 'south', 'west', 'east']

from items.UseObjects import Door

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
                 west_room  = None, west_obstacle = None
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
        if direction in directions and getattr(self, direction, None) == None:
            setattr(self, direction, path)
            return True
        return False
    def __str__(self, distance = 0):
        description = self.description
        for direction in directions: # Собирает описание с соседних комнат/тайлов если между ними нету препятсвие или есть другая видимость (для больших комнат)
            if getattr(self, direction).next_room != None and (getattr(self, direction).obstacle == None or getattr(self, direction).visible_through == True):
                description += getattr(self, direction).next_room.__str__(distance + 1)
    
class Graph:
    def __init__(self, starting_room: Room):
        self.rooms = {starting_room.name: starting_room}
    
    def add_room(self, room: Room):
        self.rooms[room.name] = room
    
    def add_edge(self, from_room: Room, direction, to_room: Room, str, path: Path, door):
        from_path = Path(from_room, door)
        to_path = Path(to_room, door)
        direction = direction.lower()
        from_room_slot_free = getattr(from_room, direction, None) is None
        to_room_slot_free = getattr(path, opposite[direction], None) is None
        if direction in directions and from_room_slot_free and to_room_slot_free:
            from_room.add_path(from_path, direction)
            to_room.add_path(to_path, opposite[direction])
            return True
        return False