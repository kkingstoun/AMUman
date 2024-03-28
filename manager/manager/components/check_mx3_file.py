import logging
import os
from pathlib import Path

log = logging.getLogger("rich")

SHARED_FOLDER = Path(os.environ.get("SHARED_FOLDER", "/shared"))


def validate_mx3_file(path_str: str) -> bool:
    path = SHARED_FOLDER / Path(path_str)

    if not path.exists():
        log.error(f"File does not exist: {path}")
        return False
    log.debug(f"Checking file: {path} {path.exists()}")
    return path.exists()
