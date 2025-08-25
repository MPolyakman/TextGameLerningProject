import pytest

# Assuming the project structure allows these imports from a 'game' root package
from game.Game_loop import Game
from game.event_managment import (
    EventDispatcher, ItemSystem, ActionSystem, MovingSystem, MapSystem, CharactersSystem
)
from game.map import Room, Graph
from game.Characters.player import Player
from game.Characters.NPC.creatures import Entity
from game.items.UseObjects import Item, CharacteristicsItem

# The Game class constructor requires an InteractionSystem, which was not provided in the context.
# A placeholder class is created to allow for instantiation and testing.
class InteractionSystem:
    def __init__(self, event_dispatcher):
        self.event_dispatcher = event_dispatcher

# A mock for the RichLog to capture output without needing the textual library
class MockRichLog:
    def __init__(self):
        self.log = []

    def write(self, message):
        if message is not None:
            self.log.append(message)

    @property
    def last_message(self):
        return self.log[-1] if self.log else None

class TestGame:
    def setup_method(self):
        """Set up a new game instance for each test."""
        self.event_dispatcher = EventDispatcher()
        self.map_system = MapSystem(self.event_dispatcher, Graph())
        self.character_system = CharactersSystem(self.event_dispatcher, player_name="Tester")
        self.item_system = ItemSystem(self.event_dispatcher)
        self.action_system = ActionSystem(self.event_dispatcher)
        self.moving_system = MovingSystem(self.event_dispatcher)
        self.interaction_system = InteractionSystem(self.event_dispatcher)

        self.game = Game(
            event_dispatcher=self.event_dispatcher,
            character_system=self.character_system,
            interaction_system=self.interaction_system,
            moving_system=self.moving_system,
            action_system=self.action_system,
            item_system=self.item_system,
            map_system=self.map_system,
            player_name="Tester"
        )

        self.output_log = MockRichLog()
        self.game.set_output_log(self.output_log)

        self.start_room = Room("start_room")
        self.north_room = Room("north_room")
        self.map_system.add_room(self.start_room)
        self.map_system.add_room(self.north_room)
        self.map_system.add_edge(self.start_room, "north", self.north_room)

        self.player = self.game.character_system.player
        self.moving_system.on_set_position(self.player, self.start_room)

    def test_handle_turn_with_valid_move_command(self):
        """Tests the core 'move' command, ensuring it correctly parses the direction, creates a MoveEvent, and that the event dispatcher is called, which should result in the player changing rooms."""
        # Arrange
        initial_room = self.player.current_room
        assert initial_room.name == "start_room"

        # Act
        self.game.handle_turn("move north")

        # Assert
        assert self.player.current_room == self.north_room

    def test_handle_turn_with_valid_take_command(self):
        """Verifies the 'take' command functionality, ensuring it correctly identifies the item, creates a TakeItemEvent, and that the event dispatcher is called to move the item to the player's inventory."""
        # Arrange
        sword = Item("sword")
        self.start_room.items["sword"] = sword
        assert "sword" not in self.player.inventory
        assert "sword" in self.start_room.items

        # Act
        self.game.handle_turn("take sword")

        # Assert
        assert "sword" in self.player.inventory
        assert "sword" not in self.start_room.items
        assert self.output_log.last_message == f'{self.player.name} took sword'

    def test_handle_turn_with_valid_use_command(self):
        """This test validates the 'use' command. It ensures the system checks the player's inventory, calls the item's 'use' method, and emits the resulting event, which could affect player stats or the environment."""
        # Arrange
        potion = CharacteristicsItem("potion", changes={"hp": 20})
        self.player.inventory["potion"] = potion
        self.player.hp = 50

        # Act
        self.game.handle_turn("use potion")

        # Assert
        assert self.player.hp == 70
        assert self.output_log.last_message == "hp изменился на 20"

    def test_handle_turn_with_unknown_command(self):
        """Tests the default case of the command parser in 'handle_turn' to ensure that invalid or unrecognized commands are handled gracefully with an 'Unknown command.' message, preventing crashes."""
        # Arrange
        initial_room = self.player.current_room

        # Act
        self.game.handle_turn("jump")

        # Assert
        assert self.player.current_room == initial_room
        assert self.output_log.last_message == "Unknown command."

    def test_handle_turn_with_invalid_move_direction_argument(self):
        """This test checks the conditional logic within the 'move' case to ensure that if a player provides a direction that isn't in the valid 'directions' list, the system provides appropriate feedback and does not attempt to process the invalid direction."""
        # Arrange
        initial_room = self.player.current_room

        # Act
        self.game.handle_turn("move up")

        # Assert
        assert self.player.current_room == initial_room
        assert self.output_log.last_message == "You can't move up."

    def test_handle_turn_with_incomplete_give_command(self):
        """Validates the robustness of the input parser. The system should correctly handle commands that lack necessary parameters and provide a clear error message to the user instead of crashing or behaving unpredictably."""
        # Arrange
        npc = Entity("goblin")
        self.character_system.characters["goblin"] = npc
        rock = Item("rock")
        self.player.inventory["rock"] = rock

        # Act
        self.game.handle_turn("give rock")

        # Assert
        assert self.output_log.last_message == "There is no one named  here."
        assert "rock" in self.player.inventory