from abc import ABC, abstractmethod

opposite = {'north' : 'south', 'west': 'east', 'south': 'north', 'east': 'west'}
directions = ['north', 'south', 'west', 'east']

class Path:
    def __init__(self, next_room = None, door = None):
        self.obstacle = door
        self.next_room = next_room
        self.description = ''

    def __str__(self):
        return self.description

class Room:
    def __init__(self, 
                 name,
                 north_room = None, north_door = None,
                 east_room  = None, east_door = None,
                 south_room  = None, south_door = None,
                 west_room  = None, west_door = None
                ):
        
        self.name = name              
        self.items = {}

        self.north = Path(north_room, north_door) # <Room объект, Door объект>
        self.east = Path(east_room, east_door)
        self.south = Path(south_room, south_door)
        self.west = Path(west_room, west_door)
    
    def add_path(self, path: Path, direction):
        direction = direction.lower()
        if direction in directions and getattr(self, direction, None) == None:
            setattr(self, direction, path)
            return True
        return False
    

class Creature:
    def __init__(self, name, position: Room, max_health: int):
        self.name = name
        self.current_room = position
        self.inventory = {} # {"name': item}
        self.hp = max_health
        self.max_hp = max_health
        self.alive = True
        self.description = ""
        self.game_log = ''

    def set_position(self, room):
        self.current_room = room
    
    def move(self, direction):
        direction = direction.lower()
        target_path = getattr(self.current_room, direction)
        if direction not in directions:
            return False
        if target_path.next_room == None:
            print('no_way')
            return False
        if target_path.door.locked:
            print(f'дверь {str(target_path.door)} заперта')
            return False
        self.set_position(target_path.next_room)
        return True
    
    def affect_health(self, points: int) -> None:
        self.hp += points
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        if self.hp <= 0:
            self.die()
    
    def die(self):
        self.alive = False
        self.description += "Существо мертво."
    
    def __str__(self):
        return getattr(self, "description", "No comments lol")

class Player(Creature):
    def __init__(self, name, position, max_health):
        super().__init__(name, position, max_health)
        self.history = ''

class Graph:
    def __init__(self):
        self.rooms = {}
    
    def add_room(self, room: Room):
        self.rooms[room.name] = room
    
    def add_edge(self, from_room: Room, direction, to_room: Room, str, path: Path, door: Room):
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
    
class UseObject(ABC):
    @abstractmethod
    def use(self, player: Player) -> str: #каждый use дает комментарий по произошедшему
        pass

    def __str__(self) -> str:
        return getattr(self, "description", "No comments lol")

class Item(UseObject):
    def __init__(self, name: str, description: str, type: bool): # Type ??? если это разбиение на активки и пассивки добавить документацию
        self.name = name
        self.description = description
        self.type = type

    def use(self, player: Player):
        if self.name in player.current_room.items:
            player.inventory[self.name] = player.current_room.items.pop(self.name)
            return f"Ты взял {self.name} и положил в свой инвентарь"
        raise Exception('Нету в данной комнате такого предмета')
    
class Door(UseObject):
    def __init__(self, locked = True, key_name = None, description = ''):
        self.locked = locked
        self.key_name = key_name
        self.description = description

    def use(self, player: Player):
        
        if self.key_name in player.inventory.keys():
            self.locked = False
            return f"{self.key_name} подошел и дверь открылась"
        return f"{self.key_name} не подошел к двери"
