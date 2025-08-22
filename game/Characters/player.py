from Characters.NPC.creatures import Entity
from Characters.NPC.NPC import NPC

from events import SayEvent

class Player(Entity):
    def __init__(self, name, position = None, max_health = 100):
        super().__init__(name, max_health)
        self.history = ''
        self.intelligence_bool = True

    def say(self, mes: str, NPC: NPC):
        return SayEvent(self, mes, NPC)
    
    def listen_and_decide(self, speaker, message):
        print(f"{speaker.name}: {message}")
