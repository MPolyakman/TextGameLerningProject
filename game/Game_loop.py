from map import*
from Characters.NPC.creatures import*
from Characters.player import Player

class Game:
    def __init__(self, player_name: str, starting_room: Room):
        
        self.graph = self.generate_graph(starting_room)
        position = self.graph.rooms['Starting_room']
        self.player = Player(player_name, position)
        self.characters = {}

    def generate_graph(self, starting_room) -> Graph:
        #...
        return Graph(starting_room)
    
    def handle_turn(self, move: str): # все дейтсвия определяем как (character_action__object)
        character, action, object = move.split("_")
        match action:
            case "use":
                self.characters[character].inventory[object].use()
            case "move":
                self.characters[character].move[object]
