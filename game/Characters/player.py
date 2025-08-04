from .NPC.creatures import Creature

class Player(Creature):
    def __init__(self, name, position, max_health = 100):
        super().__init__(name, position, max_health)
        self.history = ''