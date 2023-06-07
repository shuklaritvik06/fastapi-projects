from rich import print, print_json
from rich.console import Console
from rich.text import Text
from rich.theme import Theme
from rich.table import Table
from rich.markdown import Markdown
from rich.progress import track
from rich.prompt import Prompt
from rich.traceback import install
from rich.emoji import Emoji
import time

install()

theme = Theme({
    "success": "green",
    "error": "bold red"
})
console = Console(theme=theme, record=True)
text = Text("Hello World!")

text.stylize("bold green", 0, 5)

print(text)

print({
    "a": [1, 2, 34],
    "name": "Ramesh"
})

print_json('{"name":"Ramesh"}')

console.print("Hello", style="bold underline italic red on blue")
console.print("[bold]Hello [green]World![/][/]")

console.print("Success", style="success")

for i in range(2):
    console.log("Helloo World!")
    time.sleep(3)

console.save_html("Hello.html")

table = Table(title="My Fav Movies")
table.add_column("Name", style="green", justify="left")
table.add_column("On", style="blue")
table.add_row("Imitation Mind", "Alan Turing")
console.print(table)

MARKDOWN = """
# Hello I am a boss!

> Hey bro how are you!

"""

md = Markdown(MARKDOWN)
console.print(md)

for i in track(range(10), description="Doing!"):
    print("Hey!")

Prompt.ask("How are you?")
Prompt.get_input(console, "Hello", True)
emoji = Emoji("sparkles")
console.print(emoji)
