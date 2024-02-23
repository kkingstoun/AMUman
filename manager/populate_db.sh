#!/bin/env bash
curl -X 'POST' \
  'http://localhost:8000/api/nodes/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'X-CSRFTOKEN: WIBHvhpkYbxaJ9YS0QFARrOYNa7vOMWDJQLFexeMGkt6tR35q3MwaTMgQ8crMQOx' \
  -d '{
  "ip": "123.123.123.123",
  "name": "string",
  "number_of_gpus": 2,
  "status": "WAITING",
  "connection_status": "CONNECTED",
  "last_seen": "2024-02-16T11:30:53.725Z"
}'

curl -X 'POST' \
  'http://localhost:8000/api/gpus/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'X-CSRFTOKEN: WIBHvhpkYbxaJ9YS0QFARrOYNa7vOMWDJQLFexeMGkt6tR35q3MwaTMgQ8crMQOx' \
  -d '{
  "device_id": 1,
  "uuid": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "model": "string",
  "speed": "SLOW",
  "util": 1,
  "is_running_amumax": true,
  "status": "WAITING",
  "last_update": "2024-02-16T11:31:37.512Z",
  "node": 1
}'

curl -X 'POST' \
  'http://localhost:8000/api/jobs/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'X-CSRFTOKEN: WIBHvhpkYbxaJ9YS0QFARrOYNa7vOMWDJQLFexeMGkt6tR35q3MwaTMgQ8crMQOx' \
  -d '{
  "path": "path/to/job1",
  "port": 1,
  "submit_time": "2024-02-16T11:30:03.610Z",
  "start_time": "2024-02-16T11:30:03.610Z",
  "end_time": "2024-02-16T11:30:03.610Z",
  "error_time": "2024-02-16T11:30:03.610Z",
  "priority": "HIGH",
  "gpu_partition": "FAST",
  "duration": 1,
  "status": "WAITING",
  "assigned_gpu_id": "string",
  "output": "",
  "error": "",
  "flags": "",
  "node": 1,
  "gpu": 1
}'

curl -X 'POST' \
  'http://localhost:8000/api/jobs/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'X-CSRFTOKEN: WIBHvhpkYbxaJ9YS0QFARrOYNa7vOMWDJQLFexeMGkt6tR35q3MwaTMgQ8crMQOx' \
  -d '{
  "path": "path/to/job2",
  "port": 12,
  "submit_time": "2024-02-16T11:30:03.610Z",
  "start_time": "2024-02-16T11:30:03.610Z",
  "end_time": "2024-02-16T11:30:03.610Z",
  "error_time": "2024-02-16T11:30:03.610Z",
  "priority": "LOW",
  "gpu_partition": "SLOW",
  "duration": 2,
  "status": "WAITING",
  "assigned_gpu_id": "string",
  "output": "string",
  "error": "string",
  "flags": "string",
  "node": 1,
  "gpu": 1
}'