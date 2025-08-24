
from Game_loop import Game

from textual import events
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Input, RichLog
from textual.containers import VerticalScroll, Horizontal

class GameApp(App):
    CSS = """
    Screen {
        overflow: auto;
    }

    #main_container {
        layout: horizontal;
        height: 90%;
    }

    #map_view {
        width: 50%;
        height: 100%;
        border: round white;
        overflow: auto;
    }

    #game_log {
        width: 50%;
        height: 100%;
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
        with Horizontal(id="main_container"):
            yield Static(id="map_view", name="Map")
            yield RichLog(id="game_log", name="Game Log")
            yield Input(placeholder="What do you want to do?")
        yield Footer()

    def on_mount(self) -> None:
        self.query_one(RichLog).write("Welcome to the game! Type 'exit' to quit.")
        self.game.set_output_log(self.query_one(RichLog))
        self.update_map_display()
        self.query_one(Input).focus()

    def on_input_submitted(self, message: Input.Submitted):
        command = message.value
        self.query_one(RichLog).write(f"> {command}")
        if command.lower() == "exit":
            self.exit("Thank you for playing.")
        else:
            self.game.handle_turn(command)
            self.update_map_display()

    def update_map_display(self):
        map_content = self.game.draw_map()
        self.query_one("#map_view").update(map_content)
