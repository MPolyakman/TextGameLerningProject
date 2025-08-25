#список предметов
#список предметов
from abc import ABC, abstractmethod

from events import Event, ChangeCharacteristicEvent
import procedure_descr as pd
from aistuff.gamemaster import descr

class Item():
    def __init__(self, name: str, hp = 100, description = ''):
        self.name = name
        self.description = description

    def __str__(self) -> str:
        return self.name + getattr(self, "description", "")
    
class Object():
    def __init__(self, name: str, description = '', hp = 2000):
        self.name = name
        self.description = description
        self.hp = hp

    def __str__(self) -> str:
        return self.name + getattr(self, "description", "")
    
class StorageObj(Object):
    def __init__(self, name: str, description = '', hp = 2000):
        super().__init__(name, description, hp)
        items = {}

    
class Obstacle(Object):
    def __init__(self, name, description = "", hp = 5000, visibility_through = False):
        super().__init__(name, description, hp)
        self.visible_through = visibility_through

class Door(Obstacle):
    def __init__(self,name, key_name, locked = True, hp = 3000, description = ''):
        super().__init__(name, description, hp, visibility_through=False)

        if description == "":
            description = descr(pd.random_specs(pd.door_specifications))

        self.locked = locked
        self.key_name = key_name

    def __str__(self):
        return f"Это дверь. Ее открывает {self.key_name}"

class Key(Item):
    def __str__(self) -> str:
        return f"Это ключ. {getattr(self, 'description', '')}"
    
class UseItem(Item):
    @abstractmethod
    def use(self, char) -> Event:
        pass

class CharacteristicsItem(UseItem):
    def __init__(self, name, hp = 10, changes = dict(), description = ""):
        super().__init__(name, hp, description)
        self.changes = changes

    def use(self, char) -> Event:
        return ChangeCharacteristicEvent(char, self.changes)

