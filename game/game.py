opposite = {'north' : 'south', 'west': 'east', 'south': 'north', 'east': 'west'}
directions = ['north', 'south', 'west', 'east']

class Room:
    def __init__(self, 
                 name,
                 north_room = None,
                 east_room  = None,
                 south_room  = None,
                 west_room  = None
                ):
        
        self.name = name              
        self.items = {}

        self.north = north_room # <Room объкты>
        self.east = east_room
        self.south = south_room
        self.west = west_room 
    
    def add_path(self, room, direction):
        direction = direction.lower()
        if direction in directions and getattr(self, direction, None) == None:
            setattr(self, direction, room)
            return True
        return False

class Graph:
    def __init__(self):
        self.rooms = {}
    
    def add_room(self, room: Room):
        self.rooms[room.name] = room
    
    def add_edge(self, from_room, direction, to_room):
        direction = direction.lower()
        from_room_slot_free = getattr(from_room, direction, None) is None
        to_room_slot_free = getattr(to_room, opposite[direction], None) is None
        if direction in directions and from_room_slot_free and to_room_slot_free:
            from_room.add_path(to_room, direction)
            to_room.add_path(from_room, opposite[direction])
            return True
        return False
    
class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description

class Door:
    def __ini__(self, locked = True, key_name = None, description = ''):
        self.locked = locked
        self.key_name = key_name
        self.description = description

class Player:
    def __init__(self, position):
        self.current_room = position
        self.inventory = {} # {"name': item}

    def set_position(self, room):
        self.current_room = room
    
    def move(self, direction):
        direction = direction.lower()
        if direction in directions and getattr(self.current_room, direction, None) != None:
            self.set_position(getattr( self.current_room, direction))
            return True
        print('no way')
        return False
    
    def take_an_item(self, item_name):
        if item_name in self.current_room.items:
            self.inventory[item_name] = self.current_room.items.pop(item_name)
            return True
        return False
