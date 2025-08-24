
from Game_loop import Game

from textual import events
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Input, RichLog
from textual.containers import VerticalScroll, Horizontal, Vertical

class GameApp(App):
    CSS = """
    Screen {
        overflow: auto;
    }

    #main_container {
        layout: vertical;
        height: 100%;
    }
    #windows_container {
        layout: horizontal;
        height: 60%;
    }
    #room_view {
        width: 70%;
        height: 100%;
        border: round white;
        overflow: auto;
    }

    #inspect_view {
        width: 30%;
        height: 100%;
        border: round white;
        overflow: auto;
    }

    #game_log {
        width: 100%;
        height: 40%;
        border: round white;
        overflow: auto;
    }
    
    Input {
        dock: bottom;
        height: 10%;
    }
    """

    def __init__(self, game: Game, **kwargs):
        super().__init__(**kwargs)
        self.game = game

    def compose(self) -> ComposeResult:
        yield Header(name="AI Adventure")
        with Vertical(id= "main_container"):
            with Horizontal(id="windows_container"):
                yield Static(id="room_view", name="Room")
                yield Static(id="inspect_view", name="Inspect window")
            yield RichLog(id="game_log", name="Game Log")
            yield Input(placeholder="What do you want to do?")
        yield Footer()

    def on_mount(self) -> None:
        self.query_one(RichLog).write("Welcome to the game! Type 'exit' to quit.")
        self.update_map_display()
        self.update_room_view()
        self.query_one(Input).focus()

    def on_input_submitted(self, message: Input.Submitted):
        command = message.value
        self.query_one(RichLog).write(f"> {command}")
        if command.lower() == "exit":
            self.exit("Thank you for playing.")
        else:
            self.game.handle_turn(command)
            self.update_map_display()
        self.query_one(Input).clear()
        self.query_one(RichLog).write(self.game.UI_system.output["log"])

    def update_map_display(self):
        map_content = self.game.draw_map()
        self.query_one("#inspect_view").update(map_content)

    def update_room_view(self):
        room_content = self.game.UI_system.room_view()
        self.query_one("#room_view").update(room_content)
