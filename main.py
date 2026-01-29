import time

from textual.app import App, ComposeResult
from textual.events import Key
from textual.reactive import reactive
from textual.widgets import Footer, Header, Static

DEMOTXT = "the quick brown fox jumps over the lazy dog"


class WordDisplay(Static):
    user_input = reactive("")
    show_cursor = reactive(True)

    def on_mount(self):
        self.blink_timer = self.set_interval(0.5, self.toggle_cursor, pause=True)
        self.afk_timer = self.set_timer(2.0, self.start_blinking, pause=False)

    def toggle_cursor(self):
        self.show_cursor = not self.show_cursor

    def start_blinking(self):
        self.blink_timer.resume()

    def key_pressed(self):
        self.blink_timer.pause()
        self.afk_timer.reset()
        self.show_cursor = True

    def render(self) -> str:
        txt = ""
        ptr = len(self.user_input)
        for i, char in enumerate(DEMOTXT):
            if i == ptr and self.show_cursor:
                style = "reverse"
            elif i < ptr:
                if self.user_input[i] == char:
                    style = "green"
                else:
                    style = "red"
            else:
                style = "dim"
            txt += f"[{style}]{char}[/]"

        return txt


class TypingApp(App):
    CSS = """
    Screen {
        align: center middle;
    }
    WordDisplay {
        width: 50;
        height: 3;
        border: heavy white;
        content-align: center middle;
        text-style: bold;
    }
        """
    BINDINGS = [("ctrl+c", "quit", "Quit App"), ("ctrl+r", "reset", "Reset")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield WordDisplay()
        yield Footer()

    # def on_mount(self):
    #     self.user_input = ""
    #     self.query_one("#display", WordDisplay).update_text("")
    def action_reset(self):
        self.query_one(WordDisplay).user_input = " "

    def on_key(self, event):
        display = self.query_one(WordDisplay)
        display.key_pressed()
        # if len(event.key) > 1 and event.key != "space" and event.key != "backspace":
        #     return
        if event.key == "backspace":
            display.user_input = display.user_input[:-1]
        elif event.key == "space":
            display.user_input += " "
        elif len(event.key) > 1:
            return
        else:
            display.user_input += event.character

        # display.update_text(self.user_input)


if __name__ == "__main__":
    app = TypingApp()
    app.run()
