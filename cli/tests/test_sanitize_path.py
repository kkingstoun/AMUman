from pathlib import Path

import pytest
from amuman_cli import sanitize_path


@pytest.fixture
def shared_dir(tmp_path) -> Path:
    # Create a temporary shared directory for the tests
    return tmp_path / "shared"


@pytest.fixture
def setup_files(shared_dir: Path) -> Path:
    # Create a correct .mx3 file within the shared directory
    shared_dir.mkdir(parents=True, exist_ok=True)

    valid_file = shared_dir / "valid.mx3"
    valid_file.write_text("Valid content")

    # Create an invalid file (wrong suffix) within the shared directory
    invalid_suffix_file = shared_dir / "invalid.txt"
    invalid_suffix_file.write_text("Wrong suffix")

    # Return paths for both files for testing
    return valid_file, invalid_suffix_file


def test_sanitize_path_valid(shared_dir: Path, setup_files: Path):
    valid_file, _ = setup_files
    result = sanitize_path(valid_file, shared_dir)
    assert (
        result == valid_file
    ), "Valid .mx3 file in shared directory should be returned as is"


def test_sanitize_path_invalid_suffix(shared_dir: Path, setup_files: Path, capsys):
    _, invalid_suffix_file = setup_files
    result = sanitize_path(invalid_suffix_file, shared_dir)
    captured = capsys.readouterr()  # Capture the print output
    assert result is None, "File with invalid suffix should return None"
    assert (
        "Skipping" in captured.out
    ), "Expected skip message for file with wrong suffix"


def test_sanitize_path_outside_shared_dir(tmp_path: Path, shared_dir: Path, capsys):
    # Create a .mx3 file outside the shared directory
    outside_file = tmp_path / "outside.mx3"
    outside_file.write_text("Outside content")

    result = sanitize_path(outside_file, shared_dir)
    captured = capsys.readouterr()  # Capture the print output
    assert result is None, "File outside shared directory should return None"
    assert (
        "Skipping" in captured.out
    ), "Expected skip message for file outside shared directory"
