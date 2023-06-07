import typer
from bs4 import BeautifulSoup
import requests
from rich.console import Console
from rich.table import Table

categories_data = [
    "world",
    "us",
    "politics",
    "business",
    "opinion",
    "science",
    "health",
    "sports"
]

console = Console(record=True)

app = typer.Typer()
categories_comm = typer.Typer()
app.add_typer(categories_comm, name="category")


@app.command("categories")
def categories():
    table = Table(title="Categories of News")
    table.add_column("Id")
    table.add_column("Category")
    for index, category in enumerate(categories_data):
        table.add_row(f"{index}", f"{category}")
    console.print(table)


@categories_comm.command("get")
def get(category: str):
    table = Table(title=f"News for {category}")
    resp = requests.get(f"https://www.nytimes.com/international/section/{category}")
    soup = BeautifulSoup(resp.text, features="html.parser")
    titles = soup.select('section#stream-panel div.css-13mho3u ol li div.css-1cp3ece div.css-1l4spti a h2')
    descriptions = soup.select('section#stream-panel div.css-13mho3u ol li div.css-1cp3ece div.css-1l4spti a p')
    table.add_column("Id", style="cyan")
    table.add_column("Title", style="green")
    table.add_column("Description", style="blue")
    for i in range(len(titles)):
        table.add_row(f"{i}", titles[i].text, descriptions[i].text)
    console.print(table)
    console.save_html("data.html")


if __name__ == "__main__":
    app()
