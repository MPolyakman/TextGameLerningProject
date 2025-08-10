from map import Path, Room, Graph
from Characters.NPC.creatures import Entity
from Characters.player import Player
from items.UseObjects import Item, Door
from events import MoveEvent

from event_managment import EventDispatcher, ItemSystem, ActionSystem, MovingSystem, MapSystem, CharactersSystem

opposite = {'north' : 'south', 'west': 'east', 'south': 'north', 'east': 'west'}
directions = ['north', 'south', 'west', 'east']

class Game:
    def __init__(self,
                 event_dispatcher: EventDispatcher,
                 character_system: CharactersSystem,
                 moving_system: MovingSystem,
                 action_system: ActionSystem,
                 item_system: ItemSystem,
                 map_system: MapSystem,
                 player_name = "Default name"):

        self.event_dispatcher = event_dispatcher

        self.character_system = character_system
        self.moving_system = moving_system
        self.action_system = action_system
        self.item_system = item_system
        self.map_system = map_system

        position = self.map_system.map.rooms['starting_room']
        self.player = Player(player_name, position = position)

    def handle_turn(self, player_action): 
        action, object = player_action.split(" ")
        match action:
            case "move":
                event = MoveEvent(char_sys.player, object)
                self.event_dispatcher.emit(event)
        


    def draw_map(self):
        map = ""
        x_values, y_values = zip(*self.map_system.map.coordinates.keys())
        min_x, max_x = min(x_values), max(x_values)
        min_y, max_y = min(y_values), max(y_values)
        previous_line = []
        for y in range(max_y, min_y-1, -1):
            for x in range(min_x, max_x + 1):
                if (x, y) in self.map_system.map.coordinates.keys():
                    if self.map_system.map.coordinates[x,y] == self.character_system.player.current_room:
                        map += "𓀠"
                    else:
                        map += "▇"
                    if self.map_system.map.coordinates[(x,y)].east.next_room != None:
                        map += "---"
                    else:
                        map += "   "
                    if self.map_system.map.coordinates[(x,y)].south.next_room != None:
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
        print(self.draw_map())

    def start_game(self):
        print('---START---')
        while True:
            self.show_map()
            player_action = input()
            player_action = player_action.lower()
            if "exit" in player_action:
                break
            self.handle_turn(player_action)
            



""" отладка """
dungeon = Graph()
player = Player("Goobert Simpleton")
start = Room("starting_room")

dispatcher = EventDispatcher()
item_sys = ItemSystem(dispatcher)
mov_sys = MovingSystem(dispatcher)
act_sys = ActionSystem(dispatcher)
char_sys = CharactersSystem(dispatcher)
char_sys.player = player
map_sys = MapSystem(dispatcher, dungeon)

char_sys.player.current_room = start

rooms = [start]
for i in range(50):
    room = Room(f'room{i}')
    rooms.append(room)

map_sys.generate_graph(rooms)

test_game = Game(dispatcher, char_sys, mov_sys, act_sys, item_sys, map_sys)
test_game.start_game()

# for r in dungeon.rooms.values():
#     print(f"{r.name} - {dungeon.room_coordinates[r]}:")
#     for d in directions:
#         n_r = getattr(r, d, None)
#         if n_r != None:
#             if n_r.next_room != None:
#                 n_r = n_r.next_room
#                 print(f"{d} - {n_r.name} ")
#     print()
