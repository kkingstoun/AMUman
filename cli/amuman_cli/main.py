import typer
import httpx

app = typer.Typer()


@app.command()
def fetch(url: str):
    """Fetches a URL and displays the response status and content."""
    try:
        response = httpx.get(url)
        typer.echo(f"Response Status: {response.status_code}")
        typer.echo(f"Response Body: {response.text}")
    except httpx.HTTPError as e:
        typer.echo(f"An HTTP error occurred: {e}")


def entrypoint():
    app()
