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
