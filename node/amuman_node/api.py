import logging
import os
from typing import Any, Dict

import requests

from amuman_node.job import Job

log = logging.getLogger("rich")

Data = Dict[str, Any]


class API:
    def __init__(self):
        self.url = f"{os.environ['MANAGER_URL']}/api"
        self.node_user: str = os.environ["NODE_NAME"]
        self.node_password: str = os.environ["NODE_PASSWORD"]
        log.debug(f"API URL: {self.url}")
        self.access_token = None
        self.refresh_token = None
        self.headers = {}

    def authenticate(self) -> bool:
        try:
            response = requests.post(
                self.url + "/token/",
                json={
                    "username": self.node_user,
                    "password": self.node_password,
                },
            )
            log.debug(
                f"Authentication response: {response.status_code=}, {response.json()=}"
            )
        except requests.exceptions.RequestException as e:
            log.exception(f"Error authenticating the node: {e}")
            return False
        try:
            self.access_token = response.json()["access"]
            self.refresh_token = response.json()["refresh"]
            self.headers = {"Authorization": f"Bearer {self.access_token}"}
            return True
        except (KeyError, TypeError):
            log.error("Unable to authenticate with the manager")
        return False

    def register(self, data: Data) -> requests.Response:
        res = requests.post(
            self.url + "/nodes/",
            headers=self.headers,
            json=data,
        )
        return res

    def post_gpu(self, data: Data) -> requests.Response:
        res = requests.post(
            self.url + "/gpus/",
            headers=self.headers,
            json=data,
        )
        return res

    def update_job(self, job: Job) -> requests.Response:
        res = requests.put(
            self.url + f"/jobs/{job.id}/",
            headers=self.headers,
            json=job.asdict(),
        )
        return res

    def get_job(self, id: int) -> Job:
        res = requests.get(
            self.url + f"/jobs/{id}/",
            headers=self.headers,
        )
        return Job(**res.json())
