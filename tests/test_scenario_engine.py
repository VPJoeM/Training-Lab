"""scenario engine tests -- mocked SSH so we don't need a real target"""

import os
import pytest
from unittest.mock import patch, MagicMock


class TestScenarioEngine:

    def _make_engine(self):
        """fresh engine instance with test config"""
        with patch("app.scenario_engine.settings") as mock_settings:
            mock_settings.LAB_TARGET_HOST = "10.99.99.99"
            mock_settings.LAB_TARGET_PORT = 22
            mock_settings.LAB_TARGET_USER = "testuser"
            mock_settings.SSH_KEY_PATH = "/tmp/fake-ssh"
            from app.scenario_engine import ScenarioEngine
            return ScenarioEngine()

    def _mock_ssh_success(self, stdout_data="ok\n", exit_code=0):
        mock_client = MagicMock()
        mock_stdout = MagicMock()
        mock_stderr = MagicMock()
        mock_stdout.read.return_value = stdout_data.encode()
        mock_stdout.channel.recv_exit_status.return_value = exit_code
        mock_stderr.read.return_value = b""
        mock_client.exec_command.return_value = (MagicMock(), mock_stdout, mock_stderr)
        return mock_client

    def _mock_ssh_failure(self, stderr_data="something broke\n", exit_code=1):
        mock_client = MagicMock()
        mock_stdout = MagicMock()
        mock_stderr = MagicMock()
        mock_stdout.read.return_value = b""
        mock_stdout.channel.recv_exit_status.return_value = exit_code
        mock_stderr.read.return_value = stderr_data.encode()
        mock_client.exec_command.return_value = (MagicMock(), mock_stdout, mock_stderr)
        return mock_client

    def test_run_remote_command_success(self):
        engine = self._make_engine()
        mock_client = self._mock_ssh_success("hello from server\n")

        with patch.object(engine, "_get_ssh_client", return_value=mock_client):
            code, stdout, stderr = engine.run_remote_command("echo hello")
            assert code == 0
            assert "hello from server" in stdout
            mock_client.close.assert_called_once()

    def test_run_remote_command_failure(self):
        engine = self._make_engine()
        mock_client = self._mock_ssh_failure("permission denied\n")

        with patch.object(engine, "_get_ssh_client", return_value=mock_client):
            code, stdout, stderr = engine.run_remote_command("restricted-cmd")
            assert code == 1
            assert "permission denied" in stderr

    def test_run_scenario_script_file_not_found(self):
        engine = self._make_engine()
        code, stdout, stderr = engine.run_scenario_script("/nonexistent/script.sh")
        assert code == 1
        assert "not found" in stderr.lower()

    def test_run_scenario_script_from_file(self, tmp_path):
        engine = self._make_engine()
        script = tmp_path / "test.sh"
        script.write_text("#!/bin/bash\necho 'running'\n")

        mock_client = self._mock_ssh_success("running\n")
        with patch.object(engine, "_get_ssh_client", return_value=mock_client):
            code, stdout, stderr = engine.run_scenario_script(str(script))
            assert code == 0
            assert "running" in stdout

    def test_setup_scenario(self, tmp_path):
        engine = self._make_engine()
        sc_dir = tmp_path / "scenario"
        sc_dir.mkdir()
        (sc_dir / "setup.sh").write_text("#!/bin/bash\necho 'broken state created'\nexit 0\n")

        mock_client = self._mock_ssh_success("broken state created\n")
        with patch.object(engine, "_get_ssh_client", return_value=mock_client):
            success, output = engine.setup_scenario(str(sc_dir))
            assert success is True
            assert "broken state" in output

    def test_verify_scenario_pass(self, tmp_path):
        engine = self._make_engine()
        sc_dir = tmp_path / "scenario"
        sc_dir.mkdir()
        (sc_dir / "verify.sh").write_text("#!/bin/bash\nexit 0\n")

        mock_client = self._mock_ssh_success("all good\n")
        with patch.object(engine, "_get_ssh_client", return_value=mock_client):
            passed, output = engine.verify_scenario(str(sc_dir))
            assert passed is True

    def test_verify_scenario_fail(self, tmp_path):
        engine = self._make_engine()
        sc_dir = tmp_path / "scenario"
        sc_dir.mkdir()
        (sc_dir / "verify.sh").write_text("#!/bin/bash\nexit 1\n")

        mock_client = self._mock_ssh_failure("not fixed yet\n")
        with patch.object(engine, "_get_ssh_client", return_value=mock_client):
            passed, output = engine.verify_scenario(str(sc_dir))
            assert passed is False

    def test_teardown_scenario(self, tmp_path):
        engine = self._make_engine()
        sc_dir = tmp_path / "scenario"
        sc_dir.mkdir()
        (sc_dir / "teardown.sh").write_text("#!/bin/bash\nexit 0\n")

        mock_client = self._mock_ssh_success("cleaned up\n")
        with patch.object(engine, "_get_ssh_client", return_value=mock_client):
            success, output = engine.teardown_scenario(str(sc_dir))
            assert success is True

    def test_connection_test_success(self):
        engine = self._make_engine()
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "ok\ngpu-server-01\n"
        mock_result.stderr = ""

        with patch("subprocess.run", return_value=mock_result):
            connected, msg = engine.test_connection()
            assert connected is True
            assert "gpu-server-01" in msg

    def test_connection_test_failure(self):
        engine = self._make_engine()
        mock_result = MagicMock()
        mock_result.returncode = 255
        mock_result.stdout = ""
        mock_result.stderr = "Connection refused"

        with patch("subprocess.run", return_value=mock_result):
            connected, msg = engine.test_connection()
            assert connected is False
            assert "refused" in msg.lower()
