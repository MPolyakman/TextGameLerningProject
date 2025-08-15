# НИЧЕГО СЮДА НЕ ИМПОРТИРОВАТЬ

#Список ивентов 
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

class SpawnEntityEvent(Event):
    def __init__(self, char, room):
        self.char = char
        self.item = room

class SayEvent(Event):
    def __init__(self, speaker, words: str, recepient):
        self.speaker = speaker
        self.words = words
        self.recepient = recepient

class AttackEvent(Event):
    def __init__(self, attacker, weapon, defender):
        self.attacker = attacker
        self.weapon = weapon
        self.defender = defender

class GiveItemEvent(Event):
    def __init__(self, gifter, item, recepient):
        self.gifter = gifter
        self.item = item
        self.recepient = recepient

class PutItemEvent(Event):
    def __init__(self, char, item, place):
        self.char = char
        self.item = item
        self.place = place

class TakeItemEvent(Event):
    def __init__(self, char, item, place):
        self.char = char
        self.item = item
        self.place = place
