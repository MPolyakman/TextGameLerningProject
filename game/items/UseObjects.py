from abc import ABC, abstractmethod
from Characters.player import  Player

class UseObject(ABC):
    @abstractmethod
    def use(self, player: Player) -> str: #каждый use дает комментарий по произошедшему
        pass

    def __str__(self) -> str:
        return getattr(self, "description", "No comments lol")

class Item(UseObject):
    def __init__(self, name: str, description = ''):
        self.name = name
        self.description = description
        self.type = type
    
class Door(UseObject):
    def __init__(self, locked = True, key_name = None, description = ''):
        self.locked = locked
        self.key_name = key_name
        self.description = description

    def use(self, player: Player):
        pass
        
        # if self.key_name in player.inventory.keys():
        #     self.locked = False
        #     return f"{self.key_name} подошел и дверь открылась"
        # return f"{self.key_name} не подошел к двери"