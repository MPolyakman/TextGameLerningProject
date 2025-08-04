# from map import Room, Path, Graph

opposite = {'north' : 'south', 'west': 'east', 'south': 'north', 'east': 'west'}
directions = ['north', 'south', 'west', 'east']

class Creature:
    def __init__(self, name, position, max_health: int):
        self.name = name
        self.current_room = position
        self.inventory = {} # {"name': item}
        self.hp = max_health
        self.max_hp = max_health
        self.alive = True
        self.description = ""
        self.game_log = ''

    def set_position(self, room):
        self.current_room = room
    
    def move(self, direction):
        direction = direction.lower()
        target_path = getattr(self.current_room, direction)
        if direction not in directions:
            return False
        if target_path.next_room == None:
            print('no_way')
            return False
        if target_path.door.locked:
            print(f'дверь {str(target_path.door)} заперта')
            return False
        self.set_position(target_path.next_room)
        return True
    
    def affect_health(self, points: int) -> None:
        self.hp += points
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        if self.hp <= 0:
            self.die()
    
    def die(self):
        self.alive = False
        self.description += "Существо мертво."
    
    def __str__(self):
        return getattr(self, "description", "No comments lol")