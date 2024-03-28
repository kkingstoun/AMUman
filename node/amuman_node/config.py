import json
import logging
import os
import random
from pathlib import Path

log = logging.getLogger("rich")


class Config:
    def __init__(self):
        self.name: str
        self.password: str
        self.manager_domain: str
        self.read_config()

    def read_config(self):
        path = Path("/config/config.json")
        if path.exists():
            with open(path) as f:
                data = json.load(f)
                self.name = data.get("name")
                self.password = data.get("password")
                self.manager_domain = data.get("manager_domain")
            log.debug(
                f"Config read from file: {self.name=}, {self.password=}, {self.manager_domain=}"
            )

        self.name = os.getenv("NODE_NAME", os.getenv("HOST", str(int(1e12))))
        if self.password is None:
            self.password = str(random.randint(0, int(1e12)))
        self.manager_domain: str = os.getenv("MANAGER_DOMAIN", "localhost")
        self.write_config()
        log.debug(f"Config: {self.name=}, {self.password=}, {self.manager_domain=}")

    def write_config(self):
        path = Path("/config/config.json")
        config = {
            "name": self.name,
            "password": self.password,
            "manager_domain": self.manager_domain,
        }
        # create the directory if it doesn't exist
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            json.dump(config, f, indent=4)
