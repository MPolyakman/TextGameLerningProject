#Список ивентов 

from abc import ABC, abstractmethod

class Event:
    pass

class MoveEvent(Event):
    def __init__(self, char, direction):
        self.character = char
        self.direction = direction