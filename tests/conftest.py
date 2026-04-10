import os
import sys
import json
import shutil
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport

# make sure app imports work from project root
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


@pytest.fixture(scope="session")
def sample_curriculum(tmp_path_factory):
    """create a minimal curriculum tree for testing"""
    base = tmp_path_factory.mktemp("curriculum")
    track = base / "track-baremetal"
    track.mkdir()

    # module 1 -- has lesson + scripts, no scenarios
    m1 = track / "01-test-module"
    m1.mkdir()
    (m1 / "lesson.md").write_text("# Test Module\n\nThis is a test lesson.\n\n## Section One\n\nSome content here.\n")
    (m1 / "scripts.yaml").write_text(
        '- name: test-script.sh\n  description: "a test script"\n  path: scripts/test-script.sh\n'
    )

    # module 2 -- has lesson + scenario
    m2 = track / "02-scenario-module"
    m2.mkdir()
    (m2 / "lesson.md").write_text("# Scenario Module\n\nThis module has a lab.\n")

    sc_dir = m2 / "scenarios" / "fix-the-thing"
    sc_dir.mkdir(parents=True)
    (sc_dir / "scenario.yaml").write_text(
        'title: "Fix The Thing"\n'
        'difficulty: "Easy"\n'
        'time_estimate: "5 min"\n'
        'description: "Something is broken. Fix it."\n'
        'instructions: "Run the diagnostic and apply the fix."\n'
        'hints:\n'
        '  - "Check the logs first"\n'
        '  - "Try restarting the service"\n'
        'relevant_scripts:\n'
        '  - "scripts/gpu/check-ecc.sh"\n'
    )
    (sc_dir / "setup.sh").write_text("#!/bin/bash\necho 'setting up broken state'\nexit 0\n")
    (sc_dir / "verify.sh").write_text("#!/bin/bash\necho 'checking fix'\nexit 0\n")
    (sc_dir / "teardown.sh").write_text("#!/bin/bash\necho 'cleaning up'\nexit 0\n")

    return str(base)


@pytest.fixture
def temp_db(tmp_path):
    """provide a fresh temp SQLite path for each test"""
    return str(tmp_path / "test_progress.db")


@pytest.fixture
def mock_settings(sample_curriculum, temp_db):
    """patch settings to use test curriculum and temp DB"""
    with patch("app.config.settings") as mock:
        mock.LAB_TARGET_HOST = "10.99.99.99"
        mock.LAB_TARGET_PORT = 22
        mock.LAB_TARGET_USER = "testuser"
        mock.LAB_SSH_CMD = "ssh"
        mock.WEB_PORT = 8080
        mock.TERMINAL_PORT = 7681
        mock.SUPPORT_TOOLING_PATH = "/tmp/fake-support-tooling"
        mock.DB_PATH = temp_db
        mock.CURRICULUM_PATH = sample_curriculum
        mock.TERMINAL_URL = "http://localhost:7681"
        mock.SSH_KEY_PATH = "/tmp/fake-ssh"
        yield mock


@pytest_asyncio.fixture
async def client(mock_settings):
    """async test client for the FastAPI app"""
    # re-import after patching settings so the app picks up test config
    from app.main import app
    from app.models import init_db

    await init_db(mock_settings.DB_PATH)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def mock_ssh():
    """mock paramiko SSH client -- returns configurable command results"""
    mock_client = MagicMock()
    mock_stdout = MagicMock()
    mock_stderr = MagicMock()

    # default: commands succeed
    mock_stdout.read.return_value = b"command output\n"
    mock_stdout.channel.recv_exit_status.return_value = 0
    mock_stderr.read.return_value = b""

    mock_client.exec_command.return_value = (MagicMock(), mock_stdout, mock_stderr)

    return mock_client, mock_stdout, mock_stderr
