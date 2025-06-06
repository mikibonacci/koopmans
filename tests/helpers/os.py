"""IO-related pytest fixtures."""

from pathlib import Path

import pytest


@pytest.fixture
def datadir():
    """Return the directory where various reference QE files are stored."""
    return Path(__file__).parents[1] / 'data'


@pytest.fixture
def sys2file(capsys, tmp_path):
    """Python fixture to redirect stdout and stderr to file."""
    # Run the test
    yield

    # Write stdout and stderr to file
    out, err = capsys.readouterr()
    if out or err:
        with open(tmp_path.with_suffix('.stdout'), 'w') as f:
            f.write(out)
            f.write(err)
