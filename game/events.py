#Список ивентов 

from abc import ABC, abstractmethod

class Event:
    pass

class MoveEvent(Event):
    def __init__(self, char, direction):
        self.character = char
        self.direction = direction

class TryOpenDoor(Event):
    def __init__(self, char, door):
        self.character = char
        self.door = door

class ChangeCharacteristicEvent(Event):
    def __init__(self, char, changes: dict):
        self.char = char
        self.changes = changes

class SetCharacteristicEvent(Event):
    def __init__(self, char, changes: dict):
        self.char = char
        self.changes = changes

class DeathEvent(Event):
    def __init__(self, char):
        self.char = char

class UseItemEvent(Event):
    def __init__(self, char, item):
        self.char = char
        self.item = item
        