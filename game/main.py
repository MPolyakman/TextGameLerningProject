from Game_loop import Game
from GameAppTextual import GameApp

from map import Path, Room, Graph
from Characters.NPC.creatures import Entity
from Characters.NPC.NPC import NPC
from Characters.player import Player
from items.UseObjects import Item, Door, CharacteristicsItem
from events import MoveEvent

from event_managment import EventDispatcher, ItemSystem, ActionSystem, MovingSystem, MapSystem, CharactersSystem, InteractionSystem, UI_system

def main():
    dungeon = Graph()
    start = Room("starting_room")
    player = Player("Goobert Simpleton", position=start)
    door = Door("default door","Master key")
    medkit = CharacteristicsItem("medkit", 10, {"hp": 40, "max_hp": 10})
    items = [medkit]
    npc0 = NPC("gleb", position =  start, max_health = 100, biography= "You are homless man living in this basement")
    

    dispatcher = EventDispatcher()
    item_sys = ItemSystem(dispatcher)
    mov_sys = MovingSystem(dispatcher)
    act_sys = ActionSystem(dispatcher)
    char_sys = CharactersSystem(dispatcher)
    char_sys.player = player
    char_sys.characters[npc0.name] = npc0
    interaction_sys = InteractionSystem(dispatcher, player)
    map_sys = MapSystem(dispatcher, dungeon)
    char_sys.player.current_room = start
    UI_sys = UI_system(dispatcher, player)

    rooms = [start]
    for i in range(25):
        room = Room(f'room{i}')
        rooms.append(room)

    map_sys.generate_graph(rooms, [door], items)

    test_game = Game(dispatcher, char_sys, interaction_sys, mov_sys, act_sys, item_sys, map_sys, UI_sys)
    
    app = GameApp(game=test_game)
    app.run()

if __name__ == "__main__":
    main()
