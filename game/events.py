from dataclasses import dataclass

# НИЧЕГО СЮДА бОЛЬШЕ НЕ ИМПОРТИРОВАТЬ

# Список ивентов 

@dataclass
class Event:
    pass

@dataclass
class MoveEvent(Event):
    character: object
    direction: str

@dataclass
class TryOpenDoor(Event):
    character: object
    door: object

@dataclass
class ChangeCharacteristicEvent(Event):
    char: object
    changes: dict

@dataclass
class SetCharacteristicEvent(Event):
    char: object
    changes: dict

@dataclass
class DeathEvent(Event):
    char: object

@dataclass
class UseItemEvent(Event):
    char: object
    item: object

@dataclass
class SpawnEntityEvent(Event):
    char: object
    item: object

@dataclass
class SayEvent(Event):
    speaker: object
    words: str
    recipient: object

@dataclass
class AttackEvent(Event):
    attacker: object
    weapon: object
    defender: object

@dataclass
class GiveItemEvent(Event):
    gifter: object
    item_name: str
    recipient: object

@dataclass
class PutItemEvent(Event):
    char: object
    item_name: str
    place: object

@dataclass
class TakeItemEvent(Event):
    char: object
    item_name: str
    place: object

@dataclass
class JoinInteractionEvent(Event):
    char: object

@dataclass
class LeaveInteractionEvent(Event):
    char_name: str

@dataclass
class UpdateLogEvent(Event):
    message: str

@dataclass
class UpdateRoomEvent(Event):
    main: object

@dataclass
class UpdateInspectEvent(Event):
    inspect: object


@dataclass
class UpdateMessageEvent(Event):
    message: str