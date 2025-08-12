#список предметов
from abc import ABC, abstractmethod

from events import Event, ChangeCharacteristicEvent

class Item():
    def __init__(self, name: str, description = ''):
        self.name = name
        self.description = description

    def __str__(self) -> str:
        return getattr(self, "description", "")
    
class Door():
    def __init__(self,name, key_name, locked = True, description = ''):
        self.name = name
        self.locked = locked
        self.key_name = key_name
        self.description = description

    def __str__(self):
        return f"Это дверь. Ее открывает {self.key_name}"

class Key(Item):
    def __str__(self) -> str:
        return f"Это ключ. {getattr(self, "description", "")}"
    
class UseItem(Item):
    @abstractmethod
    def use(self, char):
        pass

class CharacteristicsItem(UseItem):
    def __init__(self, name, changes = dict(), description = ""):
        super().__init__(name, description)
        self.changes = changes

    def use(self, char) -> Event:
        return ChangeCharacteristicEvent(char, self.changes)

