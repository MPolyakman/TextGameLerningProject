from Game_loop import Game

from map import Path, Room, Graph
from Characters.NPC.creatures import Entity
from Characters.player import Player
from items.UseObjects import Item, Door, CharacteristicsItem
from events import MoveEvent

from event_managment import EventDispatcher, ItemSystem, ActionSystem, MovingSystem, MapSystem, CharactersSystem

def main():
    dungeon = Graph()
    player = Player("Goobert Simpleton")
    start = Room("starting_room")
    door = Door("default door","Master key")
    medkit = CharacteristicsItem("medkit", 10, {"hp": 40, "max_hp": 10})
    items = [medkit]
    

    dispatcher = EventDispatcher()
    item_sys = ItemSystem(dispatcher)
    mov_sys = MovingSystem(dispatcher)
    act_sys = ActionSystem(dispatcher)
    char_sys = CharactersSystem(dispatcher)
    char_sys.player = player
    map_sys = MapSystem(dispatcher, dungeon)

    char_sys.player.current_room = start

    rooms = [start]
    for i in range(25):
        room = Room(f'room{i}')
        rooms.append(room)

    map_sys.generate_graph(rooms, [door], items)

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

if __name__ == "__main__":
    main()
