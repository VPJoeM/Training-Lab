import os
from pathlib import Path
from dotenv import load_dotenv

# .env lives at the project root (one level up from app/)
_base_dir = Path(__file__).resolve().parent.parent
ENV_FILE = _base_dir / ".env"
load_dotenv(ENV_FILE)


class Settings:
    """lab config -- pulls from env vars / .env, falls back to sane defaults"""

    # flip this on during dev -- lights up verbose logging everywhere
    DEBUG: bool = os.getenv("DEBUG", "").lower() in ("1", "true", "yes")

    # target server (the GPU box trainees connect to)
    LAB_TARGET_HOST: str = os.getenv("LAB_TARGET_HOST", "")
    LAB_TARGET_PORT: int = int(os.getenv("LAB_TARGET_PORT", "4747"))
    LAB_TARGET_USER: str = os.getenv("LAB_TARGET_USER", "")
    LAB_SSH_CMD: str = os.getenv("LAB_SSH_CMD", "sshv")

    # web dashboard
    WEB_PORT: int = int(os.getenv("WEB_PORT", "8080"))
    TERMINAL_PORT: int = int(os.getenv("TERMINAL_PORT", "7681"))

    # support-tooling repo path (inside the container)
    SUPPORT_TOOLING_PATH: str = os.getenv("SUPPORT_TOOLING_PATH", "/opt/support-tooling")

    # inside the container, the db and curriculum live under /app
    DB_PATH: str = os.getenv("DB_PATH", str(_base_dir / "data" / "progress.db"))
    CURRICULUM_PATH: str = os.getenv("CURRICULUM_PATH", str(_base_dir / "curriculum"))

    # the terminal URL that gets embedded in the UI
    # this is from the trainee's browser perspective (localhost on their laptop)
    TERMINAL_URL: str = os.getenv("TERMINAL_URL", f"http://localhost:{os.getenv('TERMINAL_PORT', '7681')}")

    # SSH key path inside the container (mounted from host ~/.ssh)
    SSH_KEY_PATH: str = os.getenv("SSH_KEY_PATH", "/app/.ssh")

    @property
    def is_configured(self) -> bool:
        """true if someone has actually set a real target host"""
        return bool(self.LAB_TARGET_HOST) and self.LAB_TARGET_HOST not in ("localhost", "127.0.0.1", "")

    def reload(self):
        """re-read .env after it's been written by the setup page"""
        load_dotenv(ENV_FILE, override=True)
        self.LAB_TARGET_HOST = os.getenv("LAB_TARGET_HOST", "")
        self.LAB_TARGET_PORT = int(os.getenv("LAB_TARGET_PORT", "22"))
        self.LAB_TARGET_USER = os.getenv("LAB_TARGET_USER", "")
        self.LAB_SSH_CMD = os.getenv("LAB_SSH_CMD", "sshv")
        self.WEB_PORT = int(os.getenv("WEB_PORT", "8080"))
        self.TERMINAL_PORT = int(os.getenv("TERMINAL_PORT", "7681"))
        self.TERMINAL_URL = f"http://localhost:{self.TERMINAL_PORT}"
        self.DEBUG = os.getenv("DEBUG", "").lower() in ("1", "true", "yes")


settings = Settings()
