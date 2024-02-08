from pathlib import Path

import pytest
import toml
from amuman_cli import (
    init_config,
)


@pytest.fixture
def mock_config_path(tmp_path) -> Path:
    # Create a temporary directory and config file path for isolated testing
    return tmp_path / "amuman" / "amuman.toml"


@pytest.fixture
def mock_inputs(mocker):
    # Mock the Prompt.ask method to return predefined inputs
    mocker.patch(
        "rich.prompt.Prompt.ask",
        side_effect=["http://test-manager:8000", "/test/shared"],
    )


def test_init_config_creates_config_file(mock_config_path, mock_inputs):  # noqa: ARG001
    # Execute the init_config function with the mocked config path and inputs
    config = init_config(mock_config_path)

    # Assert the config file was created with correct content
    assert mock_config_path.exists()
    loaded_config = toml.loads(mock_config_path.read_text())
    assert loaded_config["manager_url"] == "http://test-manager:8000"
    assert loaded_config["shared_dir_root"] == "/test/shared"
    assert config == loaded_config


def test_init_config_output(mock_config_path, mock_inputs, capsys):  # noqa: ARG001
    # Execute the init_config function and capture the output
    init_config(mock_config_path)
    captured = capsys.readouterr()

    # Assert the expected output messages were printed
    assert "No config was found" in captured.out
    assert "Successfully created the config file." in captured.out
    assert "Run `amuman-cli --install-completion`" in captured.out
