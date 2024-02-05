from enum import Enum
from pathlib import Path
from typing import List, Optional, Dict, Union

import httpx
import toml
import typer
from rich import print
from rich.progress import track
from rich.prompt import Prompt
from typing_extensions import Annotated
from xdg_base_dirs import xdg_config_home

app = typer.Typer(rich_markup_mode="rich")
default_config_path: Path = xdg_config_home().joinpath("amuman/amuman.toml")


class Priority(str, Enum):
    Fast = "Fast"
    Normal = "Normal"
    Slow = "Slow"


class GPUPartition(str, Enum):
    Fast = "Fast"
    Normal = "Normal"
    Slow = "Slow"


def init_config(config_path: Path) -> Dict[str, Union[str, Path]]:
    print(
        f"[bold red]No config was found[/bold red] at `{config_path}`,[bold green] creating one:[/bold green]"
    )
    config_path.parent.mkdir(parents=True, exist_ok=True)
    manager_url: str = Prompt.ask(
        "[bold green]AMUman manager URL [/bold green]",
        default="http://amuman-manager:8000",
    )
    shared_dir_root: str = Prompt.ask(
        "[bold green]Full path to the shared storage. [/bold green]",
        default="/shared",
    )
    config: Dict[str, Union[str, Path]] = {
        "manager_url": manager_url,
        "shared_dir_root": shared_dir_root,
    }
    config_path.write_text(toml.dumps(config))
    print("[bold green]Successfully created the config file.[/bold green]")
    print(
        "[bold blue]Run `amuman-cli --install-completion` to benefit from shell completion. [/bold blue]"
    )
    return config


def read_config(config_path: Path) -> Dict[str, Union[str, Path]]:
    config: Dict[str, Union[str, Path]] = toml.loads(config_path.read_text())
    required_keys: List[str] = ["manager_url", "shared_dir_root"]
    missing_keys: List[str] = [key for key in required_keys if key not in config]
    if missing_keys:
        print(f"Missing keys: {missing_keys}")
        config = init_config(config_path)
    return config  # Type casting might be required if your config has mixed types


def sanitize_path(path: Path, shared_dir_root: Path) -> Optional[Path]:
    path = path.resolve()
    shared_dir_root = shared_dir_root.resolve()
    if shared_dir_root in path.parents:
        if path.suffix == ".mx3":
            return path
        else:
            print(f"[bold red]Skipping `{path}`: the path does not end in `.mx3`.")
    else:
        print(
            f"[bold red]Skipping `{path}`: the path is not in the shared directory `{shared_dir_root}`."
        )
    return None


def warning_if_not_mounted(shared_dir_root: Path) -> None:
    shared_dir_root = shared_dir_root.resolve()
    with open("/proc/mounts", "r") as mounts:
        for line in mounts:
            mount_point: Path = Path(
                line.split()[1]
            ).resolve()  # Type casting might be required
            if shared_dir_root == mount_point:
                return
    print(
        f"[bold red]Warning: the shared directory `{shared_dir_root}` does not appear to be a network drive. It might not be accessible to the nodes."
    )


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
    manager_url_input: Annotated[
        Optional[str],
        typer.Option(
            "--manager-url",
            "-m",
            help="Override the manager URL from the configuration.",
        ),
    ] = None,
    shared_dir_root_input: Annotated[
        Optional[Path],
        typer.Option(
            "--shared-dir-path",
            "-s",
            help="Override the shared directory path from the configuration.",
            exists=True,
            file_okay=False,
            dir_okay=True,
            writable=False,
            readable=True,
            resolve_path=True,
        ),
    ] = None,
) -> None:
    if None in [shared_dir_root_input, manager_url_input]:
        if config_path.is_file():
            config = read_config(config_path)
        else:
            config = init_config(config_path)
    if manager_url_input is None:
        manager_url: str = str(config["manager_url"])
    else:
        manager_url = manager_url_input

    if shared_dir_root_input is None:
        shared_dir_root: Path = Path(config["shared_dir_root"])
    else:
        shared_dir_root = shared_dir_root_input

    warning_if_not_mounted(shared_dir_root)
    url = f"{manager_url}/manager/task/add_task/"
    print(f"[bold green]Submitting jobs to {manager_url}/manager/task/")
    for path in track(paths, description="[bold green]Progress:"):
        path = sanitize_path(path, shared_dir_root)
        if path is None:
            continue
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


def entrypoint() -> None:
    app()
