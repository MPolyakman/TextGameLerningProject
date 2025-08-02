from map import*
from Characters.NPC.creatures import*
from Characters.player import Player

class Game:
    def __init__(self, player_name: str, map: Graph, starting_room: Room):

        self.graph = map
        position = self.graph.rooms['starting_room']
        self.player = Player(player_name, position)
        self.characters = {}

    def handle_turn(self, move: str): # все дейтсвия определяем как (character_action__object)
        character, action, object = move.split("_")
        match action:
            case "use":
                self.characters[character].inventory[object].use()
            case "move":
                self.characters[character].move[object]
    
   

