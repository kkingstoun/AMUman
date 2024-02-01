from pathlib import Path
from typing import List

import httpx
import toml
import typer
from rich import print
from rich.prompt import Prompt
from typing_extensions import Annotated
from xdg_base_dirs import xdg_config_home

app = typer.Typer(rich_markup_mode="rich")
default_config_path = xdg_config_home().joinpath("amuman/amuman.toml")


def init_config(config_path):
    print(
        f"[bold red]No config was found[/bold red] at `{config_path}`,[bold green] creating one:[/bold green]"
    )
    config_path.parent.mkdir(parents=True, exist_ok=True)
    manager_url = Prompt.ask(
        "[bold green]AMUman manager URL [/bold green]",
        default="http://manager:8000",
    )
    with open(config_path, "w") as config_file:
        data = {"manager_url": manager_url}
        config_file.write(toml.dumps(data))


def read_config(config_path):
    with open(config_path, "r") as config_file:
        return toml.load(config_file)


@app.command()
def queue(
    paths: Annotated[
        List[Path],
        typer.Argument(
            exists=True,
            file_okay=True,
            dir_okay=False,
            writable=False,
            readable=True,
            resolve_path=True,
        ),
    ],
    config_path: Annotated[
        Path,
        typer.Option(
            "--config",
            "-c",
        ),
    ] = default_config_path,
    priority: Annotated[
        str,
        typer.Option(
            "--priority",
            "-p",
            help="Fast, Normal or Slow",
        ),
    ] = "Normal",
    gpu_partition: Annotated[
        str,
        typer.Option(
            "--gpu-partition",
            "-g",
            help="Fast, Normal or Slow",
        ),
    ] = "Normal",
    estimated_time: Annotated[
        int,
        typer.Option(
            "--estimated-time",
            "-e",
            help="Estimated time for one simulations in hours",
            min=0,
            max=300,
        ),
    ] = 1,
):
    if config_path.exists():
        config = read_config(config_path)
    else:
        init_config(config_path)
        config = read_config(config_path)

    url = f"{config['manager_url']}/manager/task/add_task/"
    for path in paths:
        data = {
            "path": str(path),
            "priority": priority,
            "gpu_partition": gpu_partition,
            "est": estimated_time,
        }
        print(data)
        try:
            response = httpx.post(url, data=data)
            typer.echo(f"Path: {path} - Response Status: {response.status_code}")
            typer.echo(f"Response Body: {response.text}\n---")
        except httpx.HTTPError as e:
            typer.echo(f"An HTTP error occurred for path {path}: {e}")


def entrypoint():
    app()
