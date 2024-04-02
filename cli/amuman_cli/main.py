import dataclasses
import logging
from dataclasses import asdict, dataclass
from enum import Enum
from pathlib import Path
from typing import List, Optional

import httpx
import toml
import typer
from rich import print
from rich.logging import RichHandler
from rich.prompt import Prompt
from typing_extensions import Annotated
from xdg_base_dirs import xdg_config_home

app = typer.Typer(rich_markup_mode="rich")
default_config_path: Path = xdg_config_home().joinpath("amuman/amuman.toml")


logging.basicConfig(
    level="NOTSET",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()],
)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
log = logging.getLogger("rich")


class JobPriority(str, Enum):
    LOW = "LOW"
    NORMAL = "NORMAL"
    HIGH = "HIGH"


class GPUPartition(str, Enum):
    SLOW = "SLOW"
    NORMAL = "NORMAL"
    FAST = "FAST"
    # This next field is only to remove the enum conflict with the GPU speed
    UNDEF = "UNDEF"


@dataclass
class Config:
    manager_url: str
    shared_dir_root: str
    token: str


@dataclass
class Job:
    path: str
    user: str
    priority: str = JobPriority.NORMAL.value
    gpu_partition: str = GPUPartition.NORMAL.value
    duration: int = 1


def warning(message: str) -> None:
    print(f"[bold orange1]Warning: {message}[/bold orange1]")


def authenticate(manager_url: str, username: str, password: str) -> str:
    response = httpx.post(
        f"{manager_url}/api/token/",
        data={"username": username, "password": password},
    )
    response.raise_for_status()
    return response.json()["refresh"]


def init_config(config_path: Path) -> Config:
    print(
        f"[bold red]No config was found[/bold red] at `{config_path}`,[bold green] creating one:[/bold green]"
    )
    config_path.parent.mkdir(parents=True, exist_ok=True)
    manager_url: str = Prompt.ask(
        "[bold green]AMUman manager URL [/bold green]",
        default="http://amuman-manager-dev:8000",
    )
    shared_dir_root: str = Prompt.ask(
        "[bold green]Full path to the shared storage. [/bold green]",
        default="/shared",
    )
    refresh_token: str
    while True:
        username: str = Prompt.ask(
            "[bold green]Your username [/bold green]",
        )
        password: str = Prompt.ask(
            "[bold green]Your password [/bold green]",
            password=True,
        )
        try:
            refresh_token = authenticate(manager_url, username, password)
            break
        except httpx.HTTPStatusError:
            print("[bold red]Invalid credentials")
            continue
        except httpx.HTTPError as e:
            print(f"[bold red]An HTTP error occurred: {e}")
            continue

    config: Config = Config(
        manager_url=manager_url,
        shared_dir_root=shared_dir_root,
        token=refresh_token,
    )
    config_path.write_text(toml.dumps(asdict(config)))
    print("[bold green]Successfully created the config file.[/bold green]")
    print(
        "[bold blue]Run `amuman-cli --install-completion` to benefit from shell completion. [/bold blue]"
    )
    print("")
    return config


def read_config(config_path: Path) -> Config:
    try:
        config_dict = toml.loads(config_path.read_text())
        config = Config(
            manager_url=config_dict["manager_url"],
            shared_dir_root=config_dict["shared_dir_root"],
            token=config_dict["token"],
        )
    except FileNotFoundError:
        print(f"Configuration file not found at {config_path}, initializing...")
        config = init_config(config_path)

    required_keys: List[str] = ["manager_url", "shared_dir_root", "token"]
    missing_keys: List[str] = [
        key for key in required_keys if key not in asdict(config)
    ]

    if missing_keys:
        print(f"Missing keys: {missing_keys}")
        config = init_config(config_path)
    return config


def sanitize_path(path: Path, shared_dir_root: Path) -> Optional[Path]:
    path = path.resolve()
    shared_dir_root = shared_dir_root.resolve()
    if shared_dir_root in path.parents:
        if path.suffix == ".mx3":
            # remove the shared directory root from the path
            path = path.relative_to(shared_dir_root)
            return path
        else:
            print(f"[bold red] \u274C {path}: the path does not end in `.mx3`.")
    else:
        print(
            f"[bold red] \u274C {path}: the path is not in the shared directory `{shared_dir_root}`."
        )
    return None


def warning_if_not_mounted(shared_dir_root: Path) -> None:
    shared_dir_root = shared_dir_root.resolve()
    with open("/proc/mounts") as mounts:
        for line in mounts:
            mount_point: Path = Path(
                line.split()[1]
            ).resolve()  # Type casting might be required
            if shared_dir_root == mount_point:
                return
    warning(
        f"the shared directory `{shared_dir_root}` does not appear to be a network drive. It might not be accessible to the nodes."
    )


@app.command()
def queue(  # noqa: C901
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
        JobPriority,
        typer.Option(
            "--priority",
            "-p",
            help="Job priority in the queue.",
            case_sensitive=False,
        ),
    ] = JobPriority.NORMAL,
    gpu_partition: Annotated[
        GPUPartition,
        typer.Option(
            "--gpu-partition",
            "-g",
            help="Speed of GPUs that will run your jobs.",
            case_sensitive=False,
        ),
    ] = GPUPartition.NORMAL,
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
    verbose: Annotated[
        int,
        typer.Option(
            "--verbose",
            "-v",
            count=True,
        ),
    ] = 0,
    quiet: Annotated[
        int,
        typer.Option(
            "--quiet",
            "-q",
            count=True,
        ),
    ] = 0,
) -> None:
    if verbose > 0:
        log.setLevel("DEBUG")
    elif quiet == 1:
        log.setLevel("WARNING")
    elif quiet > 1:
        log.setLevel("ERROR")
    else:
        log.setLevel("INFO")
    if None in [shared_dir_root_input, manager_url_input]:
        if config_path.is_file():
            config = read_config(config_path)
        else:
            config = init_config(config_path)
    if manager_url_input is None:
        manager_url: str = str(config.manager_url)
    else:
        manager_url = manager_url_input

    if shared_dir_root_input is None:
        shared_dir_root: Path = Path(config.shared_dir_root)
    else:
        shared_dir_root = shared_dir_root_input

    warning_if_not_mounted(shared_dir_root)
    if log.level <= 20:
        print(f"[bold blue3]Submitting jobs to {manager_url}/jobs/")
    token = get_access_token(manager_url, config.token)
    for input_path in paths:
        path = sanitize_path(input_path, shared_dir_root)
        if path is None:
            continue
        data = Job(
            path=str(path),
            user="test",
            priority=priority.value,
            gpu_partition=gpu_partition.value,
            duration=estimated_time,
        )
        try:
            response = httpx.post(
                f"{manager_url}/api/jobs/",
                data=dataclasses.asdict(data),
                headers={"Authorization": f"Bearer {token}"},
            )
            if log.level <= 20 and response.status_code < 400:
                print(f"[bold green] \u2713 {path}")
            if response.status_code >= 400:
                print(f"[bold red] \u274C {path}")
            log.debug(f"Path: {path} - Response Status: {response.status_code}")
        except httpx.HTTPError as e:
            print(f"[bold red] \u274C {path}")
            log.error(f"An HTTP error occurred: {e}")


def get_access_token(manager_url: str, refresh_token: str) -> str:
    response = httpx.post(
        f"{manager_url}/api/token/refresh/",
        data={"refresh": refresh_token},
    )
    response.raise_for_status()
    return response.json()["access"]


def entrypoint() -> None:
    app()


if __name__ == "__main__":
    entrypoint()
