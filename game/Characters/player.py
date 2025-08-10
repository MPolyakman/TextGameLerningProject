from Characters.NPC.creatures import Entity

class Player(Entity):
    def __init__(self, name, position = None, max_health = 100):
        super().__init__(name, max_health)
        self.history = ''