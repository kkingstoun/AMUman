import logging
from typing import Any, Dict

import requests

from amuman_node.config import Config
from amuman_node.job import Job

log = logging.getLogger("rich")

Data = Dict[str, Any]


class API:
    def __init__(self, config: Config):
        self.config = config
        self.url = f"https://{config.manager_domain}/api"
        log.debug(f"API URL: {self.url}")
        self.access_token = None
        self.refresh_token = None
        self.headers = {}

    def create_user_if_doesnt_exist(self) -> None:
        log.debug("Checking if node user exists...")
        users = self.get_users().json()  # ["results"]
        log.debug(f"Users: {users}")
        node_user_exists = any(
            user["auth"]["username"] == self.config.name for user in users
        )
        if not node_user_exists:
            log.debug("Node user does not exist. Creating...")
            self.post_user()
        else:
            log.debug("Node user exists.")

    def authenticate(self) -> bool:
        # self.create_user_if_doesnt_exist()
        try:
            res = self.post_user()
            if res.status_code == 201:
                log.debug("Node user created successfully")
            else:
                log.debug(
                    f"Node user creation failed: {res.status_code=}, {res.json()=}"
                )
        except requests.exceptions.RequestException as e:
            log.exception(f"Error creating the node user: {e}")

        log.debug("Authenticating...")
        try:
            data = {
                "username": self.config.name,
                "password": self.config.password,
            }
            log.debug(f"Authenticating with {self.url}/token/ {data=}")
            response = requests.post(
                self.url + "/token/",
                json=data,
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

    def get_users(self) -> requests.Response:
        res = requests.get(
            self.url + "/users/",
            headers=self.headers,
        )
        return res

    def post_user(self) -> requests.Response:
        data = {
            "username": self.config.name,
            "password": self.config.password,
            "email": f"{self.config.name}@localhost",
        }
        res = requests.post(
            self.url + "/users/",
            headers=self.headers,
            json=data,
        )
        return res

    def post_node(self, data: Data) -> requests.Response:
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

    def put_job(self, job: Job) -> requests.Response:
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
