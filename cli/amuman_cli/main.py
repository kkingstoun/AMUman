import typer
import httpx
from pathlib import Path
from typing_extensions import Annotated
from typing import List


app = typer.Typer()


@app.command()
def main(
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
    print(paths, priority, gpu_partition, estimated_time)
    url = "http://manager:8000/manager/task/add_task/"
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
