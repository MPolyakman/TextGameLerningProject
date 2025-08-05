from map import Path, Room, Graph
# from Characters.NPC.creatures import Creature
# from Characters.NPC.NPC import 
from Characters.player import Player

opposite = {'north' : 'south', 'west': 'east', 'south': 'north', 'east': 'west'}
directions = ['north', 'south', 'west', 'east']



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
        x_values, y_values = zip(*self.graph.coordinates.keys())
        min_x, max_x = min(x_values), max(x_values)
        min_y, max_y = min(y_values), max(y_values)
        previous_line = []
        for y in range(max_y, min_y-1, -1):
            for x in range(min_x, max_x + 1):
                if (x, y) in self.graph.coordinates.keys():
                    map += "▇"
                    if self.graph.coordinates[(x,y)].east.next_room != None:
                        map += "---"
                    else:
                        map += "   "
                    if self.graph.coordinates[(x,y)].south.next_room != None:
                        previous_line.append(x)
                else:
                    map += "    "
            map += '\n'
            for x in range(min_x, max_x + 1):
                if x in previous_line:
                    map += "|   "
                else:
                    map += "    "
            previous_line.clear()
            map += "\n"
        return map
    
    def show_map(self):

        # self.graph.calculate_coordinates()
        print(self.draw_map())

""" отладка """

start = Room("starting_room")
rooms = [start]
for i in range(100):
    room = Room(f'room{i}')
    rooms.append(room)

dungeon = Graph()
dungeon.generate_graph(rooms)
test_game = Game("Pl", dungeon, start)
test_game.show_map()

for r in dungeon.rooms.values():
    print(f"{r.name} - {dungeon.room_coordinates[r]}:")
    for d in directions:
        n_r = getattr(r, d, None)
        if n_r != None:
            if n_r.next_room != None:
                n_r = n_r.next_room
                print(f"{d} - {n_r.name} ")
    print()

