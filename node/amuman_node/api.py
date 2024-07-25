from datetime import datetime
import json
import logging
from typing import Any, Dict

import requests

from amuman_node.config import Config


from amuman_node.job import Job
from amuman_node.node import Node
from amuman_node.gpu import GPU

log = logging.getLogger("rich")

Data = Dict[str, Any]


class API:
    def __init__(self, config: Config):
        self.config = config
        self.url = f"http://{config.manager_domain}/api"
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
    
    def put_node(self, node: Node) -> requests.Response:
        res = requests.put(
            self.url + f"/nodes/{node.id}/",
            headers=self.headers,
            json=node.asdict(),
        )
        print("res!!!", res)
        return res
    
    def put_gpu(self, gpu, gpu_id: int) -> requests.Response:
        print('gpu as dict ::: ', gpu )
        res = requests.put(
            self.url + f"/gpus/{gpu_id}/",
            headers=self.headers,
            json=gpu,
        )
        #print('res:', res)
        return res

    def get_job(self, id: int) -> Job:
        res = requests.get(
            self.url + f"/jobs/{id}/",
            headers=self.headers,
        )
        return Job(**res.json())
    
    def get_node(self, id: int) -> Node:
        res = requests.get(
            self.url + f"/nodes/{id}/",
            headers=self.headers,
        )
        return Node(**res.json())
    
    
    def get_gpu_id_by_device_id(self, device_id: int) -> int:
        res = requests.get(self.url + "/gpus/", headers=self.headers)
        log.debug(f"Response status code: {res.status_code}")
        log.debug(f"Response content: {res.text}")  
        if res.status_code == 200:
            try:
                gpus = res.json()
                if 'results' in gpus and isinstance(gpus['results'], list):
                    for gpu in gpus['results']:
                        if gpu['device_id'] == device_id:
                            return gpu['id']
                    raise ValueError(f"GPU with device_id {device_id} not found.")
                else:
                    raise ValueError("Unexpected response format: expected a dictionary with a 'results' list.")
            except ValueError as ve:
                raise ValueError(f"Error parsing JSON response: {ve}")
        else:
            raise ValueError(f"Failed to fetch GPUs list. Status code: {res.status_code}")


    def get_gpu(self, device_id: int) -> GPU:
        print("ID!!! :", device_id)
        #id_n = self.get_gpu_id_by_device_id(device_id)
        res = requests.get(
            self.url + f"/gpus/{device_id}/",
            headers=self.headers,
        )
        response_data = res.json()
        print(f"Response: {response_data}")
        k_t_rem = 'id'
        r_res = response_data[k_t_rem]
        del response_data[k_t_rem]
        #response_data['id_c'] = response_data.pop('device_id')
        #response_data['node_id'] = response_data.pop('node')
        response_data['gpu_util'] = response_data.pop('util')
        response_data['refresh_time'] = response_data.pop('last_update')
        #response_data['refresh_time'] = datetime.fromisoformat(response_data.pop('last_update'))
        #response_data['refresh_time'] = json.dumps(response_data['refresh_time'] .strftime("%Y-%m-%d %H:%M:%S")) 
        response_data['node'] = int(response_data['node'] )
        print('response after', response_data)
        
        return [GPU(**response_data), r_res]
