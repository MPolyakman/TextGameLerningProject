from abc import ABC, abstractmethod
from game.Characters.player import  Player

opposite = {'north' : 'south', 'west': 'east', 'south': 'north', 'east': 'west'}
directions = ['north', 'south', 'west', 'east']

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