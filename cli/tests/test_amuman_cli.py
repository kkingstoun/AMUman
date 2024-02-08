from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import toml
from amuman_cli import (
    GPUPartition,
    Priority,
    init_config,
    queue,
    read_config,
)

# Mock the configuration file path to avoid interference with real configurations
MOCK_CONFIG_PATH = Path("/tmp/amuman_test.toml")


@pytest.fixture
def mock_config_path(tmp_path):
    config_path = tmp_path / "amuman.toml"
    return config_path


@pytest.fixture
def mock_config_data(tmp_path):
    shared_dir = tmp_path / "shared"
    shared_dir.mkdir(exist_ok=True)  # Ensure the shared directory exists
    return {
        "manager_url": "http://test-manager:8000",
        "shared_dir_root": str(shared_dir.resolve()),
    }


@pytest.fixture
def mock_paths(mock_config_data):
    # Extract shared_dir_root from the mock_config_data fixture
    shared_dir_root = Path(mock_config_data["shared_dir_root"])

    # Ensure the shared directory exists (if not already handled in mock_config_data)
    shared_dir_root.mkdir(parents=True, exist_ok=True)

    # Create temporary .mx3 files inside the shared directory
    paths = [shared_dir_root / f"simulation_{i}.mx3" for i in range(3)]
    for path in paths:
        print(path)
        path.write_text("simulation data")
    return paths


def test_init_config(mock_config_path, mocker):
    mocker.patch(
        "rich.prompt.Prompt.ask", side_effect=["http://mock-url", "/mock/shared"]
    )
    config = init_config(mock_config_path)
    assert config["manager_url"] == "http://mock-url"
    assert config["shared_dir_root"] == "/mock/shared"
    assert mock_config_path.exists()


def test_read_config(mock_config_path, mock_config_data):
    mock_config_path.write_text(toml.dumps(mock_config_data))
    config = read_config(mock_config_path)
    assert config == mock_config_data


@patch("httpx.post")
def test_queue(mock_post, mock_paths, mock_config_path, mock_config_data, mocker):
    mock_post.return_value = MagicMock(status_code=200)
    mocker.patch("amuman_cli.read_config", return_value=mock_config_data)
    mocker.patch(
        "rich.prompt.Prompt.ask", return_value=mock_config_data["shared_dir_root"]
    )
    # Use a mock for warning_if_not_mounted to skip system-specific checks
    # mocker.patch("amuman_cli.warning_if_not_mounted")
    print(type(Priority.Normal))
    print("*" * 100)
    queue(paths=mock_paths, config_path=mock_config_path)
    # Assert httpx.post was called correctly
    assert mock_post.call_count == len(mock_paths)
    for call in mock_post.call_args_list:
        data = call[1]["data"]
        assert data["path"].startswith(mock_config_data["shared_dir_root"])
        assert data["priority"] == Priority.Normal
        assert data["gpu_partition"] == GPUPartition.Normal
