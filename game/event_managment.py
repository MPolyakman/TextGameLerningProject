# Event-Based systems

from random import shuffle, choice, random
from collections import deque

from Characters.NPC.creatures import Entity
from Characters.player import Player
from items.UseObjects import Item, Door, Key
from map import Path, Room, Graph
from events import Event, MoveEvent, TryOpenDoor

opposite = {'north' : 'south', 'west': 'east', 'south': 'north', 'east': 'west'}
directions = ['north', 'south', 'west', 'east']

class EventDispatcher:
    def __init__(self):
        self.listeners = {}

    def subscribe(self, event_type, listener):
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(listener)

    def emit(self, event):
        event_type = type(event)
        for listener in self.listeners.get(event_type, []):
            listener(event)



class ItemSystem:
    def __init__(self, event_dispatcher):
        self.event_dispatcher = event_dispatcher

    def put_item(self, item, room):
        room.items.append(item)

    def on_take_item(self, item, char):
        char.inventory[item.name] = item

    def on_use_item(self, item):
        self.event_dispatcher.emit(f"use_{item.name}") 



class MovingSystem:
    def __init__(self, event_dispatcher):
        self.event_dispatcher = event_dispatcher
        on_move = self.on_move
        self.event_dispatcher.subscribe(MoveEvent, on_move)

    def on_set_position(self, entity, room):
        entity.current_room = room

    def on_move(self, move):
        direction = move.direction.lower()
        if direction not in directions:
            return False
        target_path = getattr(move.character.current_room, direction)
        if target_path.next_room == None:
            print('no_way')
            return False
        if target_path.obstacle != None:
            print(f"На пути стоит препятсвие")
            if isinstance(target_path.obstacle, Door):
                if target_path.obstacle.locked:
                    event = TryOpenDoor(move.character, target_path.obstacle)
                    print(f'{str(target_path.obstacle)}')
                    self.event_dispatcher.emit(event)
        else:
            self.on_set_position(move.character, target_path.next_room)
            return True



class ActionSystem:
    def __init__(self, event_dispatcher):
        self.event_dispatcher = event_dispatcher
        on_try_open_door = self.try_to_open_door
        self.event_dispatcher.subscribe(TryOpenDoor, on_try_open_door)

    def affect_health(self, entity, points: int):
        entity.hp += points
        if entity.hp > entity.max_hp:
            entity.hp = entity.max_hp
        if entity.hp <= 0:
            entity.hp = 0
            entity.die()
    
    def die(self, entity):
        entity.alive = False
        entity.description += "Существо мертво."

    def try_to_open_door(self, event):
        for item in event.character.inventory:
            if isinstance(item, Key):
                if item.name == event.door.key_name:
                    event.door.locked = False
                    print(f"дверь была открыта с помощью {item.name}")
        print("Дверь заперта")



class CharactersSystem:
    def __init__(self, event_dispatcher, player_name = "Default_name"):
        self.event_dispatcher = event_dispatcher
        self.player = Player(player_name)
        self.characters = {}



class MapSystem:
    def __init__(self, event_dispatcher, graph : Graph):
        self.event_dispatcher = event_dispatcher
        self.map = graph

    def add_room(self, room: Room):
        self.map.rooms[room.name] = room
    
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
    

    def generate_graph(self, rooms: list, doors: list):
        shuffle(rooms)
        starting_room = [r for r in rooms if r.name == "starting_room"][0]
        self.map.coordinates[(0, 0)] = starting_room
        self.map.room_coordinates[starting_room] = (0, 0)
        self.add_room(starting_room)
        rooms.remove(starting_room)
        occupied_coords = set()
        occupied_coords.add((0,0))
        x, y = 0, 0

        while rooms:
            r = choice(rooms)
            direct = choice(directions)
            node = choice(list(self.map.rooms.values()))
            x, y = (self.map.room_coordinates[node])
            match direct:
                case "north":
                    x, y = x, y + 1
                case "east":
                    x, y = x + 1, y
                case "south":
                    x, y = x, y - 1
                case "west":
                    x, y = x - 1, y
            if (x, y) not in occupied_coords:
                chance = random()
                door = None
                if chance <= 0.4:
                    door = choice(doors)
                if self.add_edge(node, direct, r, door):
                    rooms.remove(r)
                    self.add_room(r)
                    occupied_coords.add((x,y))
                    self.map.room_coordinates[r] = (x, y)
                    self.map.coordinates[(x, y)] = r

    def calculate_coordinates(self): # НЕ РАБОТАЕТ!!!
        # поиск точки отсчета графа 
        starting_room = self.map.rooms.get("starting_room")
        if not starting_room:
            return
        self.map.coordinates = {}
        self.map.room_coordinates = {}
        self.map.coordinates[(0,0)] = starting_room
        self.map.room_coordinates[starting_room] = (0,0)

        #BFS
        calculated = set()
        calculated.add(starting_room)
        q = deque()
        q.append(starting_room)
        x, y = 0, 0
        while q :
            current = q.popleft()
            if current != None:
                x, y = self.map.room_coordinates[current]
                for direction in directions:
                    next_room = getattr(current, direction).next_room
                    if next_room not in calculated:
                        if direction == "north":
                            x, y = x, y + 1
                            self.map.coordinates[x, y] = next_room
                            self.map.room_coordinates[next_room] = (x, y )
                        elif direction == "east":
                            x, y = x + 1, y
                            self.map.coordinates[x , y ] = next_room
                            self.map.room_coordinates[next_room] = (x , y)
                        elif direction == "south":
                            x, y = x, y - 1
                            self.map.coordinates[x , y ] = next_room
                            self.map.room_coordinates[next_room] = (x, y )
                        elif direction == "west":
                            x, y = x - 1, y
                            self.map.coordinates[x, y] = next_room
                            self.map.room_coordinates[next_room] = (x, y)
                        q.append(next_room)
                        calculated.add(next_room)

    def serialize(self):
        serialized_rooms = []
        for room_name, room_obj in self.map.rooms.items():
            room_data = room_obj.__dict__.copy()
            room_data['name'] = room_name
            if room_obj in self.map.room_coordinates:
                x, y = self.map.room_coordinates[room_obj]
                room_data['x'] = x
                room_data['y'] = y
            else:
                room_data['x'] = None
                room_data['y'] = None
            
            serialized_rooms.append(room_data)
        return {'Graph': serialized_rooms}
