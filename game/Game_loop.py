from map import Path, Room, Graph
# from Characters.NPC.creatures import Creature
# from Characters.NPC.NPC import 
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

    def draw_map(self):
        map = ""
        max_y = max_x = min_y = min_x = 0
        for coords in self.graph.coordinates.keys():
            max_x = max(max_x, coords[0])
            max_y = max(max_y, coords[1])
            min_x = min(min_x, coords[0])
            min_y = min(min_y, coords[1])
        i = 0
        previous_line = []
        for y in range(max_y, min_y - 1, -1):
            if i % 2 == 0:
                for x in range(min_x, max_x + 1, 1):
                    if (x, y) in self.graph.coordinates.keys():
                        map += "▇"
                        if self.graph.coordinates[(x,y)].east.next_room != None:
                            map += "-"
                        else:
                            map += " "
                        if self.graph.coordinates[(x,y)].south.next_room != None:
                            previous_line.append(x)
                    else:
                        map += "  "
            else:
                for x in range(min_x, max_x):
                    if x in previous_line:
                        map += "| "
                    else:
                        map += "  "
                previous_line.clear()
            map += "\n"
            i += 1
        return map
    
    def show_map(self):

        # self.graph.calculate_coordinates()
        print(self.draw_map())

""" ИИ сгенеированный слоп для отладки !!!!!"""

room1 = Room("starting_room", description = "A grand entrance with marble floors.")
room2 = Room("Armory", description="Walls lined with weapons and armor.")
room3 = Room("Great Hall", description="A large hall with a high ceiling.")
room4 = Room("Kitchen", description="Smells of roasted meat and herbs.")
room5 = Room("Treasure Vault", description="Glittering gold and gems everywhere!")
room6 = Room("Guard Room", description="Bunks and weapons racks fill this room.")
room7 = Room("Dining Hall", description="A long table set for a feast.")
room8 = Room("Library", description="Ancient tomes line the walls.")
room9 = Room("Alchemy Lab", description="Bubbling potions and strange smells.")
room10 = Room("Throne Room", description="An ornate throne on a raised dais.")

rooms = [room1, room2, room3, room4, room5, room6,room7, room8, room9, room10]

dungeon = Graph()
dungeon.generate_graph(rooms)
test_game = Game("Pl", dungeon, room1)
test_game.show_map()
   

