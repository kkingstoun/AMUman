import logging
from pathlib import Path

log = logging.getLogger("rich")


def validate_mx3_file(path_str: str) -> bool:
    path = Path(path_str)
    if not path.exists():
        log.error(f"File does not exist: {path}")
        return False
    log.debug(f"Checking file: {path} {path.exists()}")
    return path.exists()
