from pathlib import Path
from typing import List
from enum import Enum


import httpx
import toml
import typer
from rich import print
from rich.prompt import Prompt
from typing_extensions import Annotated
from xdg_base_dirs import xdg_config_home

app = typer.Typer(rich_markup_mode="rich")
default_config_path = xdg_config_home().joinpath("amuman/amuman.toml")


class Priority(str, Enum):
    Fast = "Fast"
    Normal = "Normal"
    Slow = "Slow"


class GPUPartition(str, Enum):
    Fast = "Fast"
    Normal = "Normal"
    Slow = "Slow"


def init_config(config_path):
    print(
        f"[bold red]No config was found[/bold red] at `{config_path}`,[bold green] creating one:[/bold green]"
    )
    config_path.parent.mkdir(parents=True, exist_ok=True)
    manager_url = Prompt.ask(
        "[bold green]AMUman manager URL [/bold green]",
        default="http://manager:8000",
    )
    shared_dir_path = Prompt.ask(
        "[bold green]Full path to the shared storage. [/bold green]",
        default="/shared",
    )
    with open(config_path, "w") as config_file:
        data = {
            "manager_url": manager_url,
            "shared_dir_path": shared_dir_path,
        }
        config = toml.dumps(data)
        config_file.write(config)
    print("[bold green]Successfully created the config file.[/bold green]")
    print(
        "[bold blue]Run `amuman-cli --install-completion` to benefit from shell completion. [/bold blue]"
    )
    return config


def read_config(config_path):
    with open(config_path, "r") as config_file:
        config = toml.load(config_file)
    required_keys = ["manager_url", "shared_dir_path"]
    missing_keys = [key for key in required_keys if key not in config]
    if missing_keys:
        print(f"Missing keys: {missing_keys}")
    return config


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
            help="Paths to .mx3 files.",
        ),
    ],
    config_path: Annotated[
        Path,
        typer.Option(
            "--config",
            "-c",
            help="Paths to the amuman-cli config file.",
        ),
    ] = default_config_path,
    priority: Annotated[
        Priority,
        typer.Option(
            "--priority",
            "-p",
            help="Job priority in the queue.",
            case_sensitive=False,
        ),
    ] = Priority.Normal.name,
    gpu_partition: Annotated[
        GPUPartition,
        typer.Option(
            "--gpu-partition",
            "-g",
            help="Speed of GPUs that will run your jobs.",
            case_sensitive=False,
        ),
    ] = GPUPartition.Normal.name,
    estimated_time: Annotated[
        int,
        typer.Option(
            "--estimated-time",
            "-e",
            help="Estimated time for one simulations in hours.",
            min=0,
            max=300,
        ),
    ] = 1,
):
    if config_path.exists():
        config = read_config(config_path)
    else:
        config = init_config(config_path)

    url = f"{config['manager_url']}/manager/task/add_task/"
    for path in paths:
        data = {
            "path": str(path),
            "priority": priority.name,
            "gpu_partition": gpu_partition.name,
            "est": estimated_time,
        }
        try:
            response = httpx.post(url, data=data)
            print(f"Path: {path} - Response Status: {response.status_code}")
            # print(f"Response Body: {response.text}\n---")
        except httpx.HTTPError as e:
            print(f"An HTTP error occurred for path {path}: {e}")


def entrypoint():
    app()
