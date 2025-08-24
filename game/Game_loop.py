
from map import Path, Room, Graph
from Characters.NPC.creatures import Entity
from Characters.player import Player
from items.UseObjects import Item, Door, UseItem, CharacteristicsItem, Key
from events import MoveEvent, SayEvent, GiveItemEvent

from event_managment import (EventDispatcher,
                              ItemSystem,
                                ActionSystem,
                                  MovingSystem,
                                    MapSystem,
                                      CharactersSystem,
                                        InteractionSystem,
                                          UI_system)

opposite = {'north' : 'south', 'west': 'east', 'south': 'north', 'east': 'west'}
directions = ['north', 'south', 'west', 'east']

class Game:
    def __init__(self,
                 event_dispatcher: EventDispatcher,
                 character_system: CharactersSystem,
                 interaction_system: InteractionSystem,
                 moving_system: MovingSystem,
                 action_system: ActionSystem,
                 item_system: ItemSystem,
                 map_system: MapSystem,
                 UI_system: UI_system):

        self.event_dispatcher = event_dispatcher

        self.character_system = character_system
        self.interaction_system = interaction_system
        self.moving_system = moving_system
        self.action_system = action_system
        self.item_system = item_system
        self.map_system = map_system
        self.UI_system = UI_system

    def handle_turn(self, player_action): 
        input_parts = player_action.lower().split(" ")
        input_len = len(input_parts)
        
        action = input_parts[0]
        obj = ""
        recipient = ""
        
        if input_len > 1:
            obj = input_parts[1]
        if input_len > 2:
            if action == "say":
                message = " ".join(input_parts[1:-1])
                recipient = input_parts[-1]
            else:
                recipient = input_parts[2]
        
        player = self.character_system.player
        self.UI_system.output["log"] = ''

        match action:
            case "move":
                if obj in directions:
                    event = MoveEvent(player, obj)
                    self.event_dispatcher.emit(event)
                else:
                    self.UI_system.output['log'] = f"You can't move {obj}."
            case "use":
                if obj in player.inventory:
                    self.event_dispatcher.emit(player.inventory[obj].use(player))
                else:
                    self.UI_system.output['log'] = f"You don't have a {obj}."
            case "inspect":
                match obj:
                    case "room":
                        self.UI_system.output['log'] = str(player.current_room)
                    case "yourself":
                        self.UI_system.output['log'] = str(player)
                    case "stats":
                        self.UI_system.output['log'] = player.repr_stats()
                    case "chars":
                        self.UI_system.output['log'] = "\n".join([i.repr_stats() for i in self.character_system.characters.values()])
                    case "":
                        self.UI_system.output['log'] = "What do you want to inspect?"
                    case _:
                        if obj in player.inventory:
                            self.UI_system.output['log'] = str(player.inventory[obj])
                        else:
                            self.UI_system.output['log'] = f"You don't have a {obj}."
            case "say":
                if recipient in self.character_system.characters:
                    npc = self.character_system.characters[recipient]
                    self.event_dispatcher.emit(player.say(message, npc))
                else:
                     f"There is no one named {recipient} here."
            case "give":
                if recipient in self.character_system.characters:
                    npc = self.character_system.characters[recipient]
                    self.event_dispatcher.emit(player.give(obj, npc))
                else:
                    self.UI_system.output['log'] =  f"There is no one named {recipient} here."
            case "take":
                self.event_dispatcher.emit(player.take(obj))
            case "put":
                self.UI_system.output['log'] =self.event_dispatcher.emit(player.put(obj))
            case "leave":
                self.event_dispatcher.emit(player.leave())
            case _:
                self.UI_system.output['log'] = "Unknown command."


    def draw_map(self):
        map_str = ""
        if not self.map_system.map.coordinates:
            return "No map data."
            
        x_values, y_values = zip(*self.map_system.map.coordinates.keys())
        min_x, max_x = min(x_values), max(x_values)
        min_y, max_y = min(y_values), max(y_values)

        for y in range(max_y, min_y - 1, -1):
            line1 = ""
            line2 = ""
            for x in range(min_x, max_x + 1):
                if (x, y) in self.map_system.map.coordinates:
                    room = self.map_system.map.coordinates[(x, y)]
                    
                    if room == self.character_system.player.current_room:
                        line1 += "𓀠"
                    else:
                        line1 += "▇"
                    
                    # East path
                    if hasattr(room, 'east') and room.east and room.east.next_room:
                        if isinstance(room.east.obstacle, Door):
                            line1 += "-D-"
                        else:
                            line1 += "---"
                    else:
                        line1 += "   "
                        
                    # South path
                    if hasattr(room, 'south') and room.south and room.south.next_room:
                        if isinstance(room.south.obstacle, Door):
                            line2 += "D   "
                        else:
                            line2 += "|   "
                    else:
                        line2 += "    "
                else:
                    line1 += "    "
                    line2 += "    "
            
            map_str += line1 + "\n"
            map_str += line2 + "\n"
            
        return map_str

