winget install podman
$env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")
podman machine init
podman machine start
podman machine ssh "curl -s -L https://nvidia.github.io/libnvidia-container/stable/rpm/nvidia-container-toolkit.repo | sudo tee /etc/yum.repos.d/nvidia-container-toolkit.repo && sudo yum install -y nvidia-container-toolkit && sudo nvidia-ctk cdi generate --output=/etc/cdi/nvidia.yaml"
podman run --rm -it --replace --tz local --pull newer     --name amuman-node-staging     --device=nvidia.com/gpu=all     -e MANAGER_DOMAIN=amuman-staging.nyx.zfns.eu.org     -e NODE_NAME=staging-node-1      -e SHARED_FOLDER=/shared      ghcr.io/kkingstoun/amuman/node:0.0.7