import json
import os
import time
import yaml
import markdown
import logging
from pathlib import Path
from datetime import datetime
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from app.config import settings, ENV_FILE
from app.models import (
    init_db,
    get_progress,
    update_progress,
    get_scenario_state,
    update_scenario_state,
    get_active_scenarios,
    clear_all_progress,
    get_quiz_result,
    save_quiz_result,
)
from app.scenario_engine import scenario_engine

# set log level based on DEBUG flag
log_level = logging.DEBUG if settings.DEBUG else logging.INFO
logging.basicConfig(
    level=log_level,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s" if settings.DEBUG
    else "%(levelname)s: %(message)s",
)
logger = logging.getLogger(__name__)

# keep third-party libs quiet even in debug mode -- we only want OUR debug output
if settings.DEBUG:
    for noisy_lib in ["aiosqlite", "asyncio", "paramiko", "uvicorn.access", "MARKDOWN", "markdown"]:
        logging.getLogger(noisy_lib).setLevel(logging.WARNING)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db(settings.DB_PATH)
    logger.info(
        f"Training Lab up -- target: {settings.LAB_TARGET_HOST}:{settings.LAB_TARGET_PORT}"
    )
    if settings.DEBUG:
        logger.debug(f"DEBUG MODE ON -- verbose logging active")
        logger.debug(f"  DB: {settings.DB_PATH}")
        logger.debug(f"  Curriculum: {settings.CURRICULUM_PATH}")
        logger.debug(f"  Terminal URL: {settings.TERMINAL_URL}")
        logger.debug(f"  SSH key path: {settings.SSH_KEY_PATH}")
        logger.debug(f"  Support-Tooling: {settings.SUPPORT_TOOLING_PATH}")
    yield


app = FastAPI(title="Lightning Training Lab", lifespan=lifespan)


# ──────────────────────────────────────────
# debug middleware -- logs every request with timing
# only active when DEBUG=true, zero overhead otherwise
# ──────────────────────────────────────────
if settings.DEBUG:
    @app.middleware("http")
    async def debug_request_logger(request: Request, call_next):
        start = time.time()
        logger.debug(f"→ {request.method} {request.url.path}")
        response = await call_next(request)
        elapsed = (time.time() - start) * 1000
        logger.debug(f"← {request.method} {request.url.path} [{response.status_code}] {elapsed:.1f}ms")
        return response


# templates and static files
_app_dir = Path(__file__).parent
templates = Jinja2Templates(directory=str(_app_dir / "templates"))
app.mount("/static", StaticFiles(directory=str(_app_dir / "static")), name="static")


# ──────────────────────────────────────────
# curriculum loader
# ──────────────────────────────────────────
def load_curriculum() -> dict:
    """walk the curriculum/ directory tree and build the module structure"""
    base = Path(settings.CURRICULUM_PATH)
    tracks = {}

    if not base.exists():
        logger.warning(f"Curriculum path not found: {base}")
        return tracks

    logger.debug(f"Loading curriculum from {base}")

    for track_dir in sorted(base.iterdir()):
        if not track_dir.is_dir() or track_dir.name.startswith("."):
            continue
        # reference/ is standalone content, not a track
        if track_dir.name == "reference":
            continue

        track_name = track_dir.name.replace("track-", "")
        display_names = {
            "baremetal": "Bare Metal H100",
            "lightning-plg": "Lightning Platform (PLG)",
            "k8s": "Kubernetes",
        }
        modules = []

        for module_dir in sorted(track_dir.iterdir()):
            if not module_dir.is_dir() or module_dir.name.startswith("."):
                continue

            module_id = module_dir.name
            lesson_file = module_dir / "lesson.md"
            scripts_file = module_dir / "scripts.yaml"

            # default title from directory name (01-some-name -> Some Name)
            parts = module_id.split("-", 1)
            module_num = parts[0] if parts[0].isdigit() else "0"
            lesson_title = parts[1].replace("-", " ").title() if len(parts) > 1 else module_id

            lesson_html = ""
            if lesson_file.exists():
                lesson_md = lesson_file.read_text()
                for line in lesson_md.split("\n"):
                    if line.startswith("# "):
                        lesson_title = line[2:].strip()
                        break
                lesson_html = markdown.markdown(
                    lesson_md,
                    extensions=["fenced_code", "tables", "toc"],
                )
                lesson_html = _process_safety_labels(lesson_html)
                logger.debug(f"  Loaded lesson: {module_id} ({len(lesson_md)} chars)")
            else:
                logger.debug(f"  No lesson.md for {module_id}")

            scripts = []
            if scripts_file.exists():
                scripts = yaml.safe_load(scripts_file.read_text()) or []
                logger.debug(f"  Scripts for {module_id}: {[s.get('name','?') for s in scripts]}")

            # quiz questions (multiple choice)
            quiz_file = module_dir / "quiz.yaml"
            quiz = []
            if quiz_file.exists():
                quiz = yaml.safe_load(quiz_file.read_text()) or []
                logger.debug(f"  Quiz for {module_id}: {len(quiz)} questions")

            scenarios = []
            scenarios_dir = module_dir / "scenarios"
            if scenarios_dir.exists():
                for sc_dir in sorted(scenarios_dir.iterdir()):
                    if not sc_dir.is_dir():
                        continue
                    sc_yaml = sc_dir / "scenario.yaml"
                    if sc_yaml.exists():
                        meta = yaml.safe_load(sc_yaml.read_text()) or {}
                        meta["id"] = sc_dir.name
                        meta["path"] = str(sc_dir)
                        # render example_output markdown to HTML
                        if meta.get("example_output"):
                            meta["example_output"] = markdown.markdown(
                                meta["example_output"],
                                extensions=["fenced_code", "codehilite", "tables"]
                            )
                        scenarios.append(meta)
                        logger.debug(f"  Scenario: {sc_dir.name} ({meta.get('title', '?')})")

            modules.append({
                "id": module_id,
                "number": module_num,
                "title": lesson_title,
                "lesson_html": lesson_html,
                "scripts": scripts,
                "quiz": quiz,
                "scenarios": scenarios,
                "path": str(module_dir),
            })

        tracks[track_name] = {
            "name": track_name,
            "display_name": display_names.get(track_name, track_name.title()),
            "modules": modules,
        }
        logger.debug(f"Track '{track_name}': {len(modules)} modules")

    return tracks


# ──────────────────────────────────────────
# page routes
# ──────────────────────────────────────────
@app.get("/health")
async def health():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    tracks = load_curriculum()
    if len(tracks) <= 1:
        # single track - redirect straight to it (or setup if not configured)
        if not settings.is_configured:
            return RedirectResponse(url="/setup")
        first = next(iter(tracks), "baremetal")
        return RedirectResponse(url=f"/track/{first}")
    # multiple tracks - show track selector
    return templates.TemplateResponse("tracks.html", {
        "request": request,
        "tracks": tracks,
        "settings": settings,
    })


@app.get("/track/{track_name}", response_class=HTMLResponse)
async def dashboard(request: Request, track_name: str):
    tracks = load_curriculum()
    if track_name not in tracks:
        raise HTTPException(404, f"Track '{track_name}' not found")

    track = tracks[track_name]
    progress_data = await get_progress(track_name)
    progress_map = {p["module"]: p for p in progress_data}

    # attach progress info to each module so templates can use it
    total_scenarios = 0
    completed_modules = 0
    for module in track["modules"]:
        prog = progress_map.get(module["id"], {})
        module["progress"] = prog
        total_scenarios += len(module["scenarios"])
        if prog.get("lesson_completed"):
            completed_modules += 1

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "track": track,
        "tracks": tracks,
        "settings": settings,
        "completed_modules": completed_modules,
        "total_scenarios": total_scenarios,
    })


@app.get("/track/{track_name}/module/{module_id}", response_class=HTMLResponse)
async def module_page(request: Request, track_name: str, module_id: str):
    tracks = load_curriculum()
    if track_name not in tracks:
        raise HTTPException(404, f"Track '{track_name}' not found")

    track = tracks[track_name]
    module = next((m for m in track["modules"] if m["id"] == module_id), None)
    if not module:
        raise HTTPException(404, f"Module '{module_id}' not found")

    # mark as started if not already
    await update_progress(track_name, module_id, lesson_completed=0)

    for scenario in module["scenarios"]:
        state = await get_scenario_state(scenario["id"])
        scenario["state"] = state or {"status": "ready"}

    # load quiz results if quiz exists
    quiz_result = None
    if module.get("quiz"):
        quiz_result = await get_quiz_result(track_name, module_id)

    return templates.TemplateResponse("module.html", {
        "request": request,
        "track": track,
        "tracks": tracks,
        "module": module,
        "quiz_result": quiz_result,
        "settings": settings,
    })


@app.get("/track/{track_name}/module/{module_id}/scenario/{scenario_id}", response_class=HTMLResponse)
async def scenario_page(request: Request, track_name: str, module_id: str, scenario_id: str):
    tracks = load_curriculum()
    if track_name not in tracks:
        raise HTTPException(404)

    track = tracks[track_name]
    module = next((m for m in track["modules"] if m["id"] == module_id), None)
    if not module:
        raise HTTPException(404)

    scenario = next((s for s in module["scenarios"] if s["id"] == scenario_id), None)
    if not scenario:
        raise HTTPException(404)

    state = await get_scenario_state(scenario_id)
    scenario["state"] = state or {"status": "ready"}

    return templates.TemplateResponse("scenario.html", {
        "request": request,
        "track": track,
        "module": module,
        "scenario": scenario,
        "settings": settings,
    })


@app.get("/terminal", response_class=HTMLResponse)
async def terminal_page(request: Request):
    # list recent session logs if any exist
    sessions_dir = Path(settings.DB_PATH).parent / "sessions"
    recent_sessions = []
    if sessions_dir.exists():
        for f in sorted(sessions_dir.glob("*.log"), reverse=True)[:10]:
            recent_sessions.append({
                "name": f.stem,
                "path": str(f),
                "size": f.stat().st_size,
                "modified": datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d %H:%M"),
            })
    tracks = load_curriculum()
    return templates.TemplateResponse("terminal.html", {
        "request": request,
        "settings": settings,
        "tracks": tracks,
        "sessions": recent_sessions,
    })


@app.get("/reference/{page_name}", response_class=HTMLResponse)
async def reference_page(request: Request, page_name: str):
    """render reference pages like cheat-sheet and symptom-map from markdown"""
    ref_dir = Path(settings.CURRICULUM_PATH) / "reference"
    md_file = ref_dir / f"{page_name}.md"
    if not md_file.exists():
        raise HTTPException(404, f"Reference page '{page_name}' not found")

    content = md_file.read_text()
    title = page_name.replace("-", " ").title()
    for line in content.split("\n"):
        if line.startswith("# "):
            title = line[2:].strip()
            break
    html = markdown.markdown(content, extensions=["fenced_code", "tables", "toc"])
    html = _process_safety_labels(html)

    tracks = load_curriculum()
    return templates.TemplateResponse("reference.html", {
        "request": request,
        "title": title,
        "content_html": html,
        "tracks": tracks,
        "settings": settings,
    })


@app.get("/api/search")
async def search_lessons(q: str = ""):
    """full-text search across all curriculum markdown files"""
    if not q or len(q) < 2:
        return {"results": []}

    import re
    base = Path(settings.CURRICULUM_PATH)
    results = []
    query = q.lower()

    for md_file in base.rglob("*.md"):
        content = md_file.read_text()
        if query not in content.lower():
            continue

        # figure out which module this belongs to
        rel = md_file.relative_to(base)
        parts = list(rel.parts)
        track_name = parts[0].replace("track-", "") if len(parts) > 0 else ""
        module_id = parts[1] if len(parts) > 1 else ""
        file_name = parts[-1]

        # grab title from first heading
        title = file_name
        for line in content.split("\n"):
            if line.startswith("# "):
                title = line[2:].strip()
                break

        # find matching lines with context
        matches = []
        for i, line in enumerate(content.split("\n")):
            if query in line.lower():
                snippet = line.strip()[:150]
                matches.append({"line": i + 1, "text": snippet})
                if len(matches) >= 3:
                    break

        url = f"/track/{track_name}/module/{module_id}" if track_name and module_id else f"/reference/{md_file.stem}"

        results.append({
            "title": title,
            "module": module_id,
            "track": track_name,
            "file": str(rel),
            "url": url,
            "matches": matches,
        })

    return {"query": q, "results": results, "count": len(results)}


@app.get("/setup", response_class=HTMLResponse)
async def setup_page(request: Request):
    return templates.TemplateResponse("setup.html", {
        "request": request,
        "settings": settings,
    })


# ──────────────────────────────────────────
# setup API (save config from the web UI)
# ──────────────────────────────────────────
class SetupRequest(BaseModel):
    host: str
    port: int = 4747
    user: str = "vpsupport"
    ssh_cmd: str = "sshv"


@app.post("/api/setup/install/{tool}")
async def install_tool(tool: str):
    """run install commands for missing tools - opens a terminal to do so"""
    import subprocess
    import shutil
    from pathlib import Path

    commands = {
        "homebrew": '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"',
        "bash": "brew install bash",
        "onepassword_cli": "brew install --cask 1password-cli",
        "support_tooling": "git clone git@github.com:VPJoeM/Support-Tooling.git ~/Github/Support-Tooling",
    }

    if tool not in commands:
        return {"status": "error", "message": f"Unknown tool: {tool}"}

    cmd = commands[tool]

    # open a terminal and run the command
    try:
        if shutil.which("osascript"):
            # macOS - open Terminal.app with the command
            apple_script = f'''
            tell application "Terminal"
                activate
                do script "{cmd}"
            end tell
            '''
            subprocess.Popen(["osascript", "-e", apple_script])
            return {"status": "ok", "message": f"Opened terminal to install {tool}"}
        else:
            return {"status": "error", "message": "Could not open terminal (non-macOS?)"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.get("/api/setup/check-prereqs")
async def check_prereqs():
    """scan the host system for required tools -- runs locally on the agent's laptop"""
    import subprocess
    import shutil

    def run_check(cmd: list[str]) -> tuple[bool, str]:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            return result.returncode == 0, result.stdout.strip()
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False, ""

    checks = {}

    # homebrew
    brew_ok, brew_out = run_check(["brew", "--version"])
    checks["homebrew"] = {
        "installed": brew_ok,
        "version": brew_out.split("\n")[0] if brew_ok else None,
        "install_cmd": '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"',
    }

    # bash version (need 5+ for modern features)
    bash_ok, bash_out = run_check(["bash", "--version"])
    bash_version = ""
    if bash_ok:
        # parse "GNU bash, version 5.2.37..."
        for part in bash_out.split():
            if part[0:1].isdigit():
                bash_version = part.rstrip(",")
                break
    bash_modern = bash_version.startswith(("5.", "6.", "7.")) if bash_version else False
    checks["bash"] = {
        "installed": bash_ok and bash_modern,
        "version": bash_version or None,
        "needs_upgrade": bash_ok and not bash_modern,
        "install_cmd": "brew install bash",
    }

    # 1password CLI
    op_ok, op_out = run_check(["op", "--version"])
    checks["onepassword_cli"] = {
        "installed": op_ok,
        "version": op_out.strip() if op_ok else None,
        "install_cmd": "brew install --cask 1password-cli",
    }

    # SSH agent -- check both the default agent and 1Password's agent
    ssh_ok, ssh_out = run_check(["ssh-add", "-l"])
    has_keys = ssh_ok and "no identities" not in ssh_out.lower() and "error" not in ssh_out.lower()
    key_count = len(ssh_out.strip().split("\n")) if has_keys else 0
    agent_source = "default"

    # if default agent has nothing, check the 1Password SSH agent socket directly
    op_sock = Path.home() / "Library" / "Group Containers" / "2BUA8C4S2C.com.1password" / "t" / "agent.sock"
    if not has_keys and op_sock.exists():
        env = dict(os.environ)
        env["SSH_AUTH_SOCK"] = str(op_sock)
        try:
            result = subprocess.run(
                ["ssh-add", "-l"], capture_output=True, text=True, timeout=5, env=env,
            )
            op_out = result.stdout.strip()
            if result.returncode == 0 and "no identities" not in op_out.lower():
                has_keys = True
                key_count = len(op_out.strip().split("\n"))
                ssh_out = op_out
                agent_source = "1password"
        except Exception:
            pass

    checks["ssh_agent"] = {
        "has_keys": has_keys,
        "key_count": key_count,
        "agent_source": agent_source,
        "op_socket_exists": op_sock.exists(),
        "output": ssh_out[:200] if ssh_out else None,
    }

    # support-tooling repo
    st_path = Path(settings.SUPPORT_TOOLING_PATH)
    # also check common locations if the configured path is inside a container
    local_paths = [
        st_path,
        Path.home() / "Github" / "Support-Tooling",
        Path(__file__).resolve().parent.parent.parent / "Support-Tooling",
    ]
    st_found = None
    for p in local_paths:
        if p.exists() and (p / "scripts").exists():
            st_found = str(p)
            break

    checks["support_tooling"] = {
        "found": st_found is not None,
        "path": st_found,
        "clone_cmd": "git clone git@github.com:VPJoeM/Support-Tooling.git ~/Github/Support-Tooling",
    }

    # sshv -- the SSH wrapper everything depends on
    sshv_ok, sshv_out = run_check(["which", "sshv"])
    checks["sshv"] = {
        "installed": sshv_ok,
        "path": sshv_out.strip() if sshv_ok else None,
        "install_url": "https://github.com/voltagepark/sshv/releases",
    }

    # tailscale -- VPN to reach internal infrastructure
    # check CLI first, then fall back to checking for the app bundle
    ts_ok, ts_out = run_check(["which", "tailscale"])
    ts_connected = False
    
    # if CLI not in PATH, check for the macOS app (which has CLI inside)
    ts_app_path = Path("/Applications/Tailscale.app")
    ts_cli_in_app = ts_app_path / "Contents" / "MacOS" / "Tailscale"
    if not ts_ok and ts_app_path.exists():
        ts_ok = True
        ts_out = str(ts_app_path)
    
    # check connection status - try the app's CLI location if needed
    if ts_ok:
        # try system CLI first, then app CLI
        for ts_cmd in ["tailscale", str(ts_cli_in_app)]:
            ts_status_ok, ts_status = run_check([ts_cmd, "status", "--json"])
            if ts_status_ok:
                try:
                    import json
                    ts_data = json.loads(ts_status)
                    ts_connected = ts_data.get("BackendState") == "Running"
                    break
                except:
                    pass
    
    checks["tailscale"] = {
        "installed": ts_ok,
        "connected": ts_connected,
        "install_cmd": "brew install --cask tailscale",
    }

    # github SSH access -- can we talk to github at all?
    gh_env = dict(os.environ)
    if op_sock.exists():
        gh_env["SSH_AUTH_SOCK"] = str(op_sock)
    try:
        gh_result = subprocess.run(
            ["ssh", "-T", "-o", "ConnectTimeout=5", "-o", "StrictHostKeyChecking=no", "git@github.com"],
            capture_output=True, text=True, timeout=10, env=gh_env,
        )
        # github returns exit code 1 but prints "Hi <user>!" on success
        gh_output = gh_result.stdout + gh_result.stderr
        gh_authed = "successfully authenticated" in gh_output.lower() or "hi " in gh_output.lower()
        gh_username = ""
        if gh_authed:
            for part in gh_output.split():
                if part.endswith("!"):
                    gh_username = part.rstrip("!")
                    break
    except Exception:
        gh_authed = False
        gh_output = ""
        gh_username = ""

    checks["github_ssh"] = {
        "authenticated": gh_authed,
        "username": gh_username,
        "output": gh_output.strip()[:200] if gh_output else None,
    }

    # overall readiness
    all_good = all([
        checks["homebrew"]["installed"],
        checks["bash"]["installed"],
        checks["onepassword_cli"]["installed"],
        checks["ssh_agent"]["has_keys"],
        checks["github_ssh"]["authenticated"],
        checks["support_tooling"]["found"],
        checks["sshv"]["installed"],
        checks["tailscale"]["installed"],
    ])
    checks["ready"] = all_good

    return checks


@app.post("/api/setup/test")
async def setup_test_connection(req: SetupRequest):
    """test SSH using the actual ssh/sshv command -- same auth chain the user has"""
    import subprocess
    import shutil

    ssh_cmd = req.ssh_cmd or "ssh"

    # make sure the command exists on this machine
    if not shutil.which(ssh_cmd):
        return {"connected": False, "message": f"'{ssh_cmd}' not found on this machine. Install it first."}

    # build the command the same way the user would type it
    cmd = [
        ssh_cmd,
        "-o", "ConnectTimeout=10",
        "-o", "StrictHostKeyChecking=no",
        "-o", "BatchMode=yes",
        "-p", str(req.port),
        f"{req.user}@{req.host}",
        "echo ok && hostname",
    ]

    logger.debug(f"Testing connection: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        if result.returncode == 0 and "ok" in result.stdout:
            hostname = result.stdout.strip().split("\n")[-1]
            return {"connected": True, "hostname": hostname}
        else:
            err = result.stderr.strip() or result.stdout.strip() or "Connection failed"
            logger.debug(f"SSH test failed: {err}")
            return {"connected": False, "message": err}
    except subprocess.TimeoutExpired:
        return {"connected": False, "message": "Connection timed out after 15s"}
    except Exception as e:
        logger.debug(f"SSH test error: {e}")
        return {"connected": False, "message": str(e)}


@app.post("/api/setup/save")
async def setup_save(req: SetupRequest):
    """write the target config to .env and reload settings"""
    import os

    logger.debug(f"Saving config: {req.host}:{req.port} user={req.user}")

    # read existing .env to preserve non-target settings (DEBUG, ports, etc.)
    existing_lines = []
    if ENV_FILE.exists():
        existing_lines = ENV_FILE.read_text().splitlines()

    # keys we're going to write -- strip old values of these
    target_keys = {"LAB_TARGET_HOST", "LAB_TARGET_PORT", "LAB_TARGET_USER", "LAB_SSH_CMD"}
    preserved = [
        line for line in existing_lines
        if not any(line.strip().startswith(f"{k}=") for k in target_keys)
    ]

    # append the new target config
    preserved.append("")
    preserved.append("# target server (configured via web UI)")
    preserved.append(f"LAB_TARGET_HOST={req.host}")
    preserved.append(f"LAB_TARGET_PORT={req.port}")
    preserved.append(f"LAB_TARGET_USER={req.user}")
    preserved.append(f"LAB_SSH_CMD={req.ssh_cmd}")

    # make sure we have DEBUG=true if it's not already in there
    if not any(line.strip().startswith("DEBUG=") for line in preserved):
        preserved.insert(0, "DEBUG=true")

    ENV_FILE.write_text("\n".join(preserved) + "\n")
    logger.info(f"Wrote .env: target={req.host}:{req.port} user={req.user}")

    # reload settings in memory so the app picks it up immediately
    settings.reload()

    # also update the scenario engine's connection info
    scenario_engine.host = settings.LAB_TARGET_HOST
    scenario_engine.port = settings.LAB_TARGET_PORT
    scenario_engine.user = settings.LAB_TARGET_USER

    return {"status": "ok", "message": f"Saved target: {req.host}:{req.port}"}


# ──────────────────────────────────────────
# API endpoints (HTMX + CLI wrapper hit these)
# ──────────────────────────────────────────
@app.post("/api/terminal/open")
async def open_terminal(scenario_id: str = None):
    """launch a real terminal window with sshv auto-connecting to the target
    
    If scenario_id is provided:
    - For 'laptop' scenarios: opens terminal with the script loaded (e.g. Node Toolkit)
    - For 'node' scenarios: SSHs to target and runs setup script
    """
    import subprocess
    import shutil
    import tempfile

    scenario = None
    if scenario_id:
        scenario = _find_scenario_by_id(scenario_id)

    # session log directory
    sessions_dir = Path(settings.DB_PATH).parent / "sessions"
    sessions_dir.mkdir(parents=True, exist_ok=True)
    session_file = sessions_dir / f"session_{int(datetime.now().timestamp())}.log"

    # detect which terminal app to use
    use_iterm = shutil.which("osascript") and subprocess.run(
        ["osascript", "-e", 'tell application "System Events" to get name of every process'],
        capture_output=True, text=True, timeout=5,
    ).stdout

    # handle laptop-based scenarios - run script locally, not via SSH
    if scenario and scenario.get("runs_on") == "laptop":
        # get the startup command from scenario
        startup_cmd = scenario.get("startup_command")
        
        if not startup_cmd:
            # default to Node Toolkit if this is a toolkit-based lab
            if "toolkit" in scenario_id.lower() or "toolkit" in scenario.get("title", "").lower():
                startup_cmd = "cd ~/Github/Support-Tooling && ./scripts/sshv/start-node-toolkit.sh"
        
        if startup_cmd:
            logged_command = f"script -q {session_file} bash -c '{startup_cmd}'"
            logger.debug(f"Launching laptop terminal: {logged_command}")
            
            try:
                if "iTerm" in (use_iterm or ""):
                    subprocess.Popen([
                        "osascript", "-e",
                        f'tell application "iTerm2" to create window with default profile command "{logged_command}"',
                    ])
                else:
                    subprocess.Popen([
                        "osascript", "-e",
                        f'tell application "Terminal" to do script "{logged_command}"',
                        "-e", 'tell application "Terminal" to activate',
                    ])
                return {"status": "ok", "message": f"Terminal opened with Node Toolkit", "session_log": str(session_file)}
            except Exception as e:
                logger.error(f"Failed to open terminal: {e}")
                return JSONResponse(500, {"status": "error", "message": str(e)})
        else:
            return JSONResponse(400, {"status": "error", "message": "No startup command defined for this lab"})

    # for node-based scenarios, need SSH config
    if not settings.is_configured:
        return JSONResponse(400, {"status": "error", "message": "No target configured. Complete setup first."})

    ssh_cmd = settings.LAB_SSH_CMD or "sshv"
    host = settings.LAB_TARGET_HOST
    port = settings.LAB_TARGET_PORT
    user = settings.LAB_TARGET_USER

    ssh_command = f"{ssh_cmd} -p {port} {user}@{host}"
    logged_command = f"script -q {session_file} {ssh_command}"

    logger.debug(f"Launching terminal: {logged_command}")

    # if we have a setup script, embed it directly in the SSH command
    # using base64 to avoid escaping issues
    if scenario and scenario.get("setup_script"):
        import base64
        wrapper_script = sessions_dir / f"lab_setup_{scenario_id}.sh"
        setup_b64 = base64.b64encode(scenario["setup_script"].encode()).decode()
        
        wrapper_content = f'''#!/bin/bash
{ssh_cmd} -p {port} {user}@{host} -t "echo '{setup_b64}' | base64 -d | bash; exec bash -l"
'''
        wrapper_script.write_text(wrapper_content)
        wrapper_script.chmod(0o755)
        logged_command = f"script -q {session_file} {wrapper_script}"

    try:
        if "iTerm" in (use_iterm or ""):
            # iTerm2
            subprocess.Popen([
                "osascript", "-e",
                f'tell application "iTerm2" to create window with default profile command "{logged_command}"',
            ])
        else:
            # Terminal.app fallback
            subprocess.Popen([
                "osascript", "-e",
                f'tell application "Terminal" to do script "{logged_command}"',
                "-e", 'tell application "Terminal" to activate',
            ])

        return {"status": "ok", "message": f"Terminal opened — connecting to {user}@{host}", "session_log": str(session_file)}
    except Exception as e:
        logger.error(f"Failed to open terminal: {e}")
        return JSONResponse(500, {"status": "error", "message": str(e)})


@app.get("/api/terminal/sessions")
async def list_sessions():
    """list recent session logs for review"""
    sessions_dir = Path(settings.DB_PATH).parent / "sessions"
    sessions = []
    if sessions_dir.exists():
        for f in sorted(sessions_dir.glob("*.log"), reverse=True)[:20]:
            sessions.append({
                "name": f.stem,
                "size": f.stat().st_size,
                "modified": datetime.fromtimestamp(f.stat().st_mtime).isoformat(),
            })
    return {"sessions": sessions}


@app.get("/api/terminal/session/{session_name}")
async def get_session_log(session_name: str):
    """read a session log -- lets us see what commands the trainee ran"""
    sessions_dir = Path(settings.DB_PATH).parent / "sessions"
    log_file = sessions_dir / f"{session_name}.log"
    if not log_file.exists():
        raise HTTPException(404, "Session not found")

    content = log_file.read_text(errors="replace")
    # strip ANSI escape codes for clean reading
    import re
    clean = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', content)
    return {"name": session_name, "content": clean[-10000:], "total_bytes": len(content)}


@app.post("/api/module/{track_name}/{module_id}/complete")
async def complete_lesson(track_name: str, module_id: str):
    await update_progress(
        track_name, module_id,
        lesson_completed=1,
        completed_at=datetime.now().isoformat(),
    )
    return HTMLResponse(
        '<span class="px-4 py-2 bg-lab-green/10 text-green-400 rounded-lg text-sm font-medium">'
        "Lesson marked complete</span>"
    )


@app.post("/api/scenario/{scenario_id}/start")
async def start_scenario(scenario_id: str):
    scenario = _find_scenario_by_id(scenario_id)
    if not scenario:
        raise HTTPException(404, "Scenario not found")

    runs_on = scenario.get("runs_on", "node")  # default to node/server
    logger.debug(f"Starting scenario: {scenario_id} (runs_on: {runs_on}, path: {scenario['path']})")
    
    # for laptop/web/docs labs, don't run setup via SSH - just show instructions inline
    if runs_on in ["laptop", "web", "docs"]:
        # read the setup script to get instructions (it just prints them)
        setup_script = scenario.get("setup_script", "")
        # extract the echo lines as instructions
        instructions = ""
        for line in setup_script.split("\n"):
            if 'echo "' in line or "echo '" in line:
                # extract content between quotes
                if 'echo "' in line:
                    start = line.find('echo "') + 6
                    end = line.rfind('"')
                elif "echo '" in line:
                    start = line.find("echo '") + 6
                    end = line.rfind("'")
                else:
                    continue
                if end > start:
                    instructions += line[start:end] + "\n"
        
        await update_scenario_state(
            scenario_id,
            track=scenario["_track"],
            module=scenario["_module"],
            status="active",
            started_at=datetime.now().isoformat(),
        )
        return {"status": "active", "runs_on": runs_on, "message": "Lab ready!", "instructions": instructions}
    
    # server/node labs - run setup via SSH
    success, output = scenario_engine.setup_scenario(scenario["path"])
    if success:
        await update_scenario_state(
            scenario_id,
            track=scenario["_track"],
            module=scenario["_module"],
            status="active",
            started_at=datetime.now().isoformat(),
        )
        logger.debug(f"Scenario {scenario_id} is now active")
        return {"status": "active", "runs_on": runs_on, "message": "Lab is ready -- go fix it!", "output": output}
    else:
        logger.debug(f"Scenario {scenario_id} setup FAILED: {output}")
        return JSONResponse(500, {"status": "error", "message": f"Setup failed: {output}"})


@app.post("/api/scenario/{scenario_id}/verify")
async def verify_scenario(scenario_id: str):
    scenario = _find_scenario_by_id(scenario_id)
    if not scenario:
        raise HTTPException(404, "Scenario not found")

    state = await get_scenario_state(scenario_id)
    attempts = (state["attempts"] + 1) if state else 1

    logger.debug(f"Verifying scenario: {scenario_id} (attempt {attempts})")
    success, output = scenario_engine.verify_scenario(scenario["path"])
    logger.debug(f"Verify result: {'PASS' if success else 'FAIL'} -- {output[:200] if output else '(empty)'}")

    if success:
        scenario_engine.teardown_scenario(scenario["path"])
        await update_scenario_state(
            scenario_id,
            status="passed",
            completed_at=datetime.now().isoformat(),
            attempts=attempts,
        )

        # update the module's scenario completion list
        track = scenario["_track"]
        module_id = scenario["_module"]
        progress = await get_progress(track)
        mp = next((p for p in progress if p["module"] == module_id), None)
        completed = json.loads(mp["scenarios_completed"]) if mp else []
        if scenario_id not in completed:
            completed.append(scenario_id)
        await update_progress(track, module_id, scenarios_completed=json.dumps(completed))

        return {"status": "passed", "message": "Nice work -- you nailed it.", "output": output}
    else:
        await update_scenario_state(scenario_id, attempts=attempts)
        hints = scenario.get("hints", [])
        return {
            "status": "failed",
            "message": "Not quite -- check the hints and try again.",
            "output": output,
            "attempts": attempts,
            "hints": hints[:min(attempts, len(hints))],
        }


@app.post("/api/scenario/{scenario_id}/force-complete")
async def force_complete_scenario(scenario_id: str):
    """Skip verification and mark scenario as complete -- for when verification is stuck or broken"""
    scenario = _find_scenario_by_id(scenario_id)
    if not scenario:
        raise HTTPException(404, "Scenario not found")

    logger.info(f"Force-completing scenario: {scenario_id} (verification skipped)")
    
    # run teardown if it exists
    try:
        scenario_engine.teardown_scenario(scenario["path"])
    except Exception as e:
        logger.warning(f"Teardown failed during force-complete: {e}")
    
    # mark as passed
    state = await get_scenario_state(scenario_id)
    attempts = (state["attempts"] + 1) if state else 1
    
    await update_scenario_state(
        scenario_id,
        status="passed",
        completed_at=datetime.now().isoformat(),
        attempts=attempts,
    )

    # update the module's scenario completion list
    track = scenario["_track"]
    module_id = scenario["_module"]
    progress = await get_progress(track)
    mp = next((p for p in progress if p["module"] == module_id), None)
    completed = json.loads(mp["scenarios_completed"]) if mp else []
    if scenario_id not in completed:
        completed.append(scenario_id)
    await update_progress(track, module_id, scenarios_completed=json.dumps(completed))

    return {"status": "ok", "message": "Marked complete (verification skipped)"}


class QuizSubmission(BaseModel):
    answers: dict  # {question_index: selected_option_index}


@app.post("/api/quiz/{track_name}/{module_id}/submit")
async def submit_quiz(track_name: str, module_id: str, submission: QuizSubmission):
    """Grade a quiz and store the results"""
    tracks = load_curriculum()
    if track_name not in tracks:
        raise HTTPException(404, "Track not found")

    module = next((m for m in tracks[track_name]["modules"] if m["id"] == module_id), None)
    if not module or not module.get("quiz"):
        raise HTTPException(404, "No quiz found for this module")

    quiz = module["quiz"]
    total = len(quiz)
    score = 0
    results = []

    for i, question in enumerate(quiz):
        selected = submission.answers.get(str(i))
        correct = question.get("correct", 0)
        is_correct = selected == correct
        if is_correct:
            score += 1
        results.append({
            "question": question["question"],
            "selected": selected,
            "correct": correct,
            "is_correct": is_correct,
            "explanation": question.get("explanation", ""),
        })

    await save_quiz_result(
        track_name, module_id, score, total,
        json.dumps(submission.answers),
    )

    passed = score >= (total * 0.7)  # 70% to pass
    if passed:
        await update_progress(
            track_name, module_id,
            lesson_completed=1,
            completed_at=datetime.now().isoformat(),
        )

    return {
        "score": score,
        "total": total,
        "percentage": round(score / total * 100) if total > 0 else 0,
        "passed": passed,
        "results": results,
    }


@app.post("/api/quiz/{track_name}/{module_id}/check")
async def check_quiz_answer(track_name: str, module_id: str, question: int = 0, answer: int = 0):
    """Check a single quiz answer — returns correct/incorrect + explanation"""
    tracks = load_curriculum()
    if track_name not in tracks:
        raise HTTPException(404, "Track not found")

    module = next((m for m in tracks[track_name]["modules"] if m["id"] == module_id), None)
    if not module or not module.get("quiz"):
        raise HTTPException(404, "No quiz found")

    quiz = module["quiz"]
    if question < 0 or question >= len(quiz):
        raise HTTPException(400, "Invalid question index")

    q = quiz[question]
    correct = q.get("correct", 0)
    is_correct = answer == correct

    return {
        "is_correct": is_correct,
        "correct_answer": correct,
        "explanation": q.get("explanation", ""),
    }


@app.post("/api/quiz/{track_name}/{module_id}/reset")
async def reset_quiz(track_name: str, module_id: str):
    """Clear quiz results so the user can retake it"""
    await save_quiz_result(track_name, module_id, 0, 0, "{}")
    return {"status": "ok", "message": "Quiz reset"}


@app.post("/api/scenario/{scenario_id}/reset")
async def reset_scenario(scenario_id: str):
    """Reset scenario state completely -- for when things get stuck"""
    scenario = _find_scenario_by_id(scenario_id)
    if not scenario:
        raise HTTPException(404, "Scenario not found")

    logger.info(f"Resetting scenario: {scenario_id}")
    
    # run teardown if it exists
    try:
        scenario_engine.teardown_scenario(scenario["path"])
    except Exception as e:
        logger.warning(f"Teardown failed during reset: {e}")
    
    # clear scenario state
    await update_scenario_state(
        scenario_id,
        status="pending",
        completed_at=None,
        attempts=0,
    )

    # remove from module's completed list
    track = scenario["_track"]
    module_id = scenario["_module"]
    progress = await get_progress(track)
    mp = next((p for p in progress if p["module"] == module_id), None)
    if mp:
        completed = json.loads(mp["scenarios_completed"]) if mp.get("scenarios_completed") else []
        if scenario_id in completed:
            completed.remove(scenario_id)
        await update_progress(track, module_id, scenarios_completed=json.dumps(completed))

    return {"status": "ok", "message": "Scenario reset"}


@app.post("/api/scenario/{scenario_id}/teardown")
async def teardown_single(scenario_id: str):
    scenario = _find_scenario_by_id(scenario_id)
    if not scenario:
        raise HTTPException(404, "Scenario not found")

    success, output = scenario_engine.teardown_scenario(scenario["path"])
    await update_scenario_state(scenario_id, status="ready")
    return {"status": "ok" if success else "error", "output": output}


@app.post("/api/scenarios/teardown-all")
async def teardown_all():
    """tear down every active scenario -- called by 'training-lab reset'"""
    active = await get_active_scenarios()
    results = []

    for state in active:
        scenario = _find_scenario_by_id(state["scenario_id"])
        if scenario:
            success, _ = scenario_engine.teardown_scenario(scenario["path"])
            await update_scenario_state(state["scenario_id"], status="ready")
            results.append({"id": state["scenario_id"], "success": success})

    return {"status": "ok", "teardowns": results}


@app.get("/api/progress")
async def api_progress():
    progress = await get_progress()
    return {"progress": progress}


@app.get("/api/connection-test")
async def connection_test():
    success, message = scenario_engine.test_connection()
    return {"connected": success, "message": message}


@app.get("/api/debug")
async def debug_info():
    """dump everything useful for troubleshooting -- only when DEBUG is on"""
    if not settings.DEBUG:
        return {"error": "Debug mode is off. Set DEBUG=true in .env"}

    import sys

    tracks = load_curriculum()
    progress = await get_progress()
    active = await get_active_scenarios()
    curriculum_path = Path(settings.CURRICULUM_PATH)

    module_files = {}
    if curriculum_path.exists():
        for track_dir in sorted(curriculum_path.iterdir()):
            if track_dir.is_dir():
                for mod_dir in sorted(track_dir.iterdir()):
                    if mod_dir.is_dir():
                        files = [f.name for f in mod_dir.rglob("*") if f.is_file()]
                        module_files[f"{track_dir.name}/{mod_dir.name}"] = files

    return {
        "debug": True,
        "python_version": sys.version,
        "config": {
            "LAB_TARGET_HOST": settings.LAB_TARGET_HOST,
            "LAB_TARGET_PORT": settings.LAB_TARGET_PORT,
            "LAB_TARGET_USER": settings.LAB_TARGET_USER,
            "LAB_SSH_CMD": settings.LAB_SSH_CMD,
            "WEB_PORT": settings.WEB_PORT,
            "TERMINAL_PORT": settings.TERMINAL_PORT,
            "TERMINAL_URL": settings.TERMINAL_URL,
            "DB_PATH": settings.DB_PATH,
            "CURRICULUM_PATH": settings.CURRICULUM_PATH,
            "SSH_KEY_PATH": settings.SSH_KEY_PATH,
            "SUPPORT_TOOLING_PATH": settings.SUPPORT_TOOLING_PATH,
        },
        "tracks": {
            name: {
                "modules": len(t["modules"]),
                "scenarios": sum(len(m["scenarios"]) for m in t["modules"]),
            }
            for name, t in tracks.items()
        },
        "curriculum_files": module_files,
        "db": {
            "path": settings.DB_PATH,
            "exists": os.path.exists(settings.DB_PATH),
            "size_bytes": os.path.getsize(settings.DB_PATH) if os.path.exists(settings.DB_PATH) else 0,
        },
        "progress_rows": len(progress),
        "active_scenarios": [s["scenario_id"] for s in active],
        "ssh_keys_dir": settings.SSH_KEY_PATH,
        "ssh_keys_found": os.listdir(settings.SSH_KEY_PATH) if os.path.isdir(settings.SSH_KEY_PATH) else "not mounted",
    }


# ──────────────────────────────────────────
# helpers
# ──────────────────────────────────────────
import re as _re

def _process_safety_labels(html: str) -> str:
    """convert [SAFE:type] markers to styled badges after code blocks"""
    labels = {
        "readonly": ("readonly", "read-only"),
        "state": ("state", "state-changing"),
        "disruptive": ("disruptive", "disruptive"),
        "approval": ("approval", "needs approval"),
    }
    for key, (css_class, display) in labels.items():
        pattern = rf'\[SAFE:{key}\]'
        replacement = f'<span class="cmd-safe {css_class}">{display}</span>'
        html = _re.sub(pattern, replacement, html, flags=_re.IGNORECASE)
    return html


def _find_scenario_by_id(scenario_id: str) -> dict | None:
    """dig through the curriculum to find a scenario by its directory name"""
    tracks = load_curriculum()
    for track_name, track in tracks.items():
        for module in track["modules"]:
            for scenario in module["scenarios"]:
                if scenario["id"] == scenario_id:
                    scenario["_track"] = track_name
                    scenario["_module"] = module["id"]
                    # load setup script content if it exists
                    setup_path = Path(scenario["path"]) / "setup.sh"
                    if setup_path.exists():
                        scenario["setup_script"] = setup_path.read_text()
                    return scenario
    return None
