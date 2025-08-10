# Event-Based systems

from game.Characters.NPC.creatures import Entity
from game.Characters.player import Player
from game.items.UseObjects import Item, Door
from game.map import Path, Room, Graph

opposite = {'north' : 'south', 'west': 'east', 'south': 'north', 'east': 'west'}
directions = ['north', 'south', 'west', 'east']

class EventDispatcher:
    def __init__(self):
        self.listeners = {}

    def subscribe(self, event_type, listener):
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(listener)

    def emit(self, event_type, data = None):
        for listener in self.listeners.get(event_type, []):
            listener(data)

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

    def on_set_position(self, entity, room):
        entity.current_room = room

    def move(self, entity, direction):
        direction = direction.lower()
        target_path = getattr(entity.current_room, direction)
        if direction not in directions:
            return False
        if target_path.next_room == None:
            print('no_way')
            return False
        if isinstance(target_path.obstacle, Door):
            if target_path.obstacle.locked:
                print(f'дверь {str(target_path.obstacle)} заперта')
                return False
        self.on_set_position(entity, target_path.next_room)
        return True

class ActionSystem:
    def __init__(self, event_dispatcher):
        self.event_dispatcher = event_dispatcher

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

class CharactersSystem:
    def __init__(self, event_dispatcher, player_name, pl_position):
        self.event_dispatcher = event_dispatcher
        self.player = Player(player_name, pl_position)
        self.characters = {}

class MapSystem:
    pass
    

