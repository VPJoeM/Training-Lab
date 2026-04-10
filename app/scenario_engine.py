import os
import subprocess
import logging
from pathlib import Path
from app.config import settings

logger = logging.getLogger(__name__)


class ScenarioEngine:
    """handles SSH to the target server for scenario setup/verify/teardown
    
    Uses subprocess + sshv so 1Password SSH agent works properly.
    """

    def __init__(self):
        self.host = settings.LAB_TARGET_HOST
        self.port = settings.LAB_TARGET_PORT
        self.user = settings.LAB_TARGET_USER

    def _get_ssh_env(self) -> dict:
        """get environment with 1Password SSH agent socket if available"""
        env = dict(os.environ)
        op_sock = Path.home() / "Library" / "Group Containers" / "2BUA8C4S2C.com.1password" / "t" / "agent.sock"
        if op_sock.exists():
            env["SSH_AUTH_SOCK"] = str(op_sock)
        return env

    def _get_ssh_cmd(self) -> str:
        """get the ssh command to use (sshv or ssh)"""
        return settings.LAB_SSH_CMD or "sshv"

    def run_remote_command(self, command: str, timeout: int = 120) -> tuple[int, str, str]:
        """run a command on the target via ssh, returns (exit_code, stdout, stderr)"""
        cmd_preview = command.split('\n')[0][:80]
        logger.debug(f"SSH exec → {cmd_preview}...")

        ssh_cmd = self._get_ssh_cmd()
        full_cmd = [
            ssh_cmd,
            "-o", "ConnectTimeout=15",
            "-o", "StrictHostKeyChecking=no",
            "-o", "BatchMode=yes",
            "-p", str(self.port),
            f"{self.user}@{self.host}",
            command,
        ]

        try:
            result = subprocess.run(
                full_cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                env=self._get_ssh_env(),
            )
            logger.debug(f"SSH exec ← exit={result.returncode} stdout={len(result.stdout)}b stderr={len(result.stderr)}b")
            if result.returncode != 0:
                logger.debug(f"SSH stderr: {result.stderr[:500]}")
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            logger.error(f"SSH command timed out after {timeout}s")
            return 1, "", f"Command timed out after {timeout}s"
        except Exception as e:
            logger.error(f"SSH command failed: {e}")
            return 1, "", str(e)

    def run_scenario_script(self, script_path: str) -> tuple[int, str, str]:
        """read a local script and pipe it to bash on the target"""
        if not os.path.exists(script_path):
            logger.debug(f"Script not found: {script_path}")
            return 1, "", f"Script not found: {script_path}"

        with open(script_path, "r") as f:
            script = f.read()

        logger.debug(f"Piping script to target: {script_path} ({len(script)} chars)")

        # pipe script via stdin to bash on remote
        ssh_cmd = self._get_ssh_cmd()
        full_cmd = [
            ssh_cmd,
            "-o", "ConnectTimeout=15",
            "-o", "StrictHostKeyChecking=no",
            "-p", str(self.port),
            f"{self.user}@{self.host}",
            "bash -s",
        ]

        try:
            result = subprocess.run(
                full_cmd,
                input=script,
                capture_output=True,
                text=True,
                timeout=120,
                env=self._get_ssh_env(),
            )
            logger.debug(f"Script exec ← exit={result.returncode}")
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return 1, "", "Script execution timed out"
        except Exception as e:
            return 1, "", str(e)

    def setup_scenario(self, scenario_path: str) -> tuple[bool, str]:
        """run setup.sh -- creates the broken state on the target"""
        script = os.path.join(scenario_path, "setup.sh")
        code, stdout, stderr = self.run_scenario_script(script)
        if code == 0:
            logger.info(f"Scenario setup OK: {scenario_path}")
            return True, stdout
        else:
            logger.error(f"Scenario setup failed ({code}): {stderr}")
            return False, stderr

    def verify_scenario(self, scenario_path: str) -> tuple[bool, str]:
        """run verify.sh -- did the trainee fix it?"""
        script = os.path.join(scenario_path, "verify.sh")
        code, stdout, stderr = self.run_scenario_script(script)
        return code == 0, stdout or stderr

    def teardown_scenario(self, scenario_path: str) -> tuple[bool, str]:
        """run teardown.sh -- restore the target to a clean state"""
        script = os.path.join(scenario_path, "teardown.sh")
        code, stdout, stderr = self.run_scenario_script(script)
        if code == 0:
            logger.info(f"Scenario teardown OK: {scenario_path}")
            return True, stdout
        else:
            logger.error(f"Scenario teardown failed ({code}): {stderr}")
            return False, stderr

    def test_connection(self) -> tuple[bool, str]:
        """quick connectivity check using the real ssh/sshv command so 1Password agent works"""
        import subprocess
        from pathlib import Path

        ssh_cmd = settings.LAB_SSH_CMD or "ssh"

        # use the 1Password SSH agent socket if available
        env = dict(os.environ)
        op_sock = Path.home() / "Library" / "Group Containers" / "2BUA8C4S2C.com.1password" / "t" / "agent.sock"
        if op_sock.exists():
            env["SSH_AUTH_SOCK"] = str(op_sock)

        cmd = [
            ssh_cmd,
            "-o", "ConnectTimeout=10",
            "-o", "StrictHostKeyChecking=no",
            "-o", "BatchMode=yes",
            "-p", str(self.port),
            f"{self.user}@{self.host}",
            "echo ok && hostname",
        ]

        logger.debug(f"Connection test: {' '.join(cmd)}")

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=20, env=env)
            if result.returncode == 0 and "ok" in result.stdout:
                hostname = result.stdout.strip().split("\n")[-1]
                return True, hostname
            else:
                err = result.stderr.strip() or result.stdout.strip() or "Connection failed"
                return False, err
        except subprocess.TimeoutExpired:
            return False, "Timed out"
        except Exception as e:
            return False, str(e)


# singleton -- initialized once, used everywhere
scenario_engine = ScenarioEngine()
