#!/usr/bin/env bash
# GPU Support Training Lab - one command to start
# designed to work on a completely fresh macOS or Linux laptop
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

PORT="${PORT:-8080}"
MIN_PY_MINOR=10  # minimum python 3.10

is_mac() { [[ "$(uname)" == "Darwin" ]]; }
is_linux() { [[ "$(uname)" == "Linux" ]]; }

# get the python minor version from a given binary, returns 0 if broken
py_minor() {
    "$1" -c 'import sys; print(sys.version_info.minor)' 2>/dev/null || echo "0"
}

# find the best python3 binary (3.10+), preferring Homebrew on macOS
find_python() {
    local candidates=()
    
    if is_mac; then
        # Homebrew paths first (Apple Silicon then Intel)
        candidates+=(/opt/homebrew/bin/python3.12 /opt/homebrew/bin/python3.11 /opt/homebrew/bin/python3)
        candidates+=(/usr/local/bin/python3.12 /usr/local/bin/python3.11 /usr/local/bin/python3)
    fi
    candidates+=(python3.12 python3.11 python3)
    
    for p in "${candidates[@]}"; do
        if command -v "$p" &>/dev/null || [ -x "$p" ]; then
            local minor
            minor=$(py_minor "$p")
            if [ "$minor" -ge "$MIN_PY_MINOR" ] 2>/dev/null; then
                echo "$p"
                return 0
            fi
        fi
    done
    return 1
}

# fresh macOS needs Xcode CLI tools for git, python, etc.
ensure_xcode_tools() {
    if is_mac && ! xcode-select -p &>/dev/null; then
        echo -e "${YELLOW}Installing Xcode Command Line Tools...${NC}"
        echo -e "${YELLOW}A dialog may pop up — click 'Install' and wait for it to finish.${NC}"
        xcode-select --install 2>/dev/null || true
        until xcode-select -p &>/dev/null; do
            sleep 5
        done
        echo -e "${GREEN}Xcode tools installed.${NC}"
    fi
}

# make sure Homebrew is available and in PATH
ensure_brew() {
    if ! command -v brew &>/dev/null; then
        echo -e "${CYAN}Installing Homebrew...${NC}"
        NONINTERACTIVE=1 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    # make sure brew is in PATH for this session (Apple Silicon vs Intel)
    if [ -x /opt/homebrew/bin/brew ]; then
        eval "$(/opt/homebrew/bin/brew shellenv)"
    elif [ -x /usr/local/bin/brew ]; then
        eval "$(/usr/local/bin/brew shellenv)"
    fi
}

# install Python 3.10+ if we can't find one
install_python() {
    echo -e "${CYAN}Installing Python 3.11...${NC}"
    
    if is_mac; then
        ensure_xcode_tools
        ensure_brew
        brew install python@3.11
        # Homebrew doesn't always symlink — add to PATH explicitly
        export PATH="/opt/homebrew/opt/python@3.11/bin:/usr/local/opt/python@3.11/bin:$PATH"
    elif is_linux; then
        if command -v apt-get &>/dev/null; then
            sudo apt-get update -qq
            sudo apt-get install -y -qq python3 python3-venv python3-pip
        elif command -v dnf &>/dev/null; then
            sudo dnf install -y -q python3 python3-pip
        elif command -v yum &>/dev/null; then
            sudo yum install -y -q python3 python3-pip
        fi
    fi
}

# install 1Password CLI if missing (needed for credential storage in toolkit scripts)
ensure_onepassword_cli() {
    if ! command -v op &>/dev/null; then
        echo -e "${CYAN}Installing 1Password CLI...${NC}"
        if is_mac; then
            ensure_brew
            brew install --cask 1password-cli
        elif is_linux; then
            if command -v apt-get &>/dev/null; then
                curl -sS https://downloads.1password.com/linux/keys/1password.asc | sudo gpg --dearmor --output /usr/share/keyrings/1password-archive-keyring.gpg 2>/dev/null
                echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/1password-archive-keyring.gpg] https://downloads.1password.com/linux/debian/$(dpkg --print-architecture) stable main" | sudo tee /etc/apt/sources.list.d/1password.list >/dev/null
                sudo apt-get update -qq && sudo apt-get install -y -qq 1password-cli
            fi
        fi
        if command -v op &>/dev/null; then
            echo -e "${GREEN}1Password CLI installed.${NC}"
        else
            echo -e "${YELLOW}Could not install 1Password CLI automatically. Install manually: brew install --cask 1password-cli${NC}"
        fi
    fi
}

# kill anything on our port so we don't get "address in use"
kill_port() {
    if command -v lsof &>/dev/null; then
        lsof -ti :"$PORT" 2>/dev/null | xargs kill -9 2>/dev/null || true
    fi
}

case "${1:-start}" in
    start|"")
        echo -e "${CYAN}${BOLD}GPU Support Training Lab${NC}"
        echo ""
        
        # step 1: find a usable python, install if needed
        PYTHON=$(find_python) || true
        if [ -z "$PYTHON" ]; then
            echo -e "${YELLOW}Python 3.${MIN_PY_MINOR}+ not found — installing...${NC}"
            install_python
            PYTHON=$(find_python) || true
        fi
        
        if [ -z "$PYTHON" ]; then
            echo -e "${RED}Could not find or install Python 3.${MIN_PY_MINOR}+.${NC}"
            echo "  macOS: brew install python@3.11"
            echo "  Ubuntu: sudo apt install python3 python3-venv python3-pip"
            exit 1
        fi
        
        FOUND_VER=$("$PYTHON" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
        echo -e "${GREEN}Using Python ${FOUND_VER}${NC} (${PYTHON})"
        
        # install 1Password CLI if missing
        ensure_onepassword_cli
        
        # step 2: create or fix the venv
        if [ -d ".venv" ]; then
            VENV_MINOR=$(py_minor .venv/bin/python3)
            if [ "$VENV_MINOR" -lt "$MIN_PY_MINOR" ] 2>/dev/null; then
                echo -e "${YELLOW}Existing venv uses Python 3.${VENV_MINOR} — recreating with ${FOUND_VER}...${NC}"
                rm -rf .venv
            fi
        fi
        
        if [ ! -d ".venv" ]; then
            echo "Creating virtual environment..."
            "$PYTHON" -m venv .venv || {
                # venv module might be missing on some Linux distros
                echo -e "${YELLOW}venv module missing — installing...${NC}"
                if command -v apt-get &>/dev/null; then
                    sudo apt-get install -y -qq python3-venv
                fi
                "$PYTHON" -m venv .venv
            }
        fi
        
        # step 3: activate and install packages
        source .venv/bin/activate
        
        if [ ! -f ".venv/.installed" ]; then
            echo "Installing Python packages..."
            pip install -q --upgrade pip 2>/dev/null
            pip install -q -r requirements.txt
            touch .venv/.installed
        fi
        
        # step 4: prep data directory
        mkdir -p data
        
        # step 5: kill stale processes on our port
        kill_port
        
        # step 6: check if somehow already running after kill
        if curl -sf "http://localhost:${PORT}/health" &>/dev/null 2>&1; then
            echo -e "${GREEN}Already running at http://localhost:${PORT}${NC}"
            open "http://localhost:${PORT}" 2>/dev/null || xdg-open "http://localhost:${PORT}" 2>/dev/null || true
            exit 0
        fi
        
        # step 7: start server
        echo "Starting server on port ${PORT}..."
        uvicorn app.main:app --host 0.0.0.0 --port "$PORT" &
        SERVER_PID=$!
        echo $SERVER_PID > .server.pid
        
        # step 8: wait for startup
        for i in {1..30}; do
            if curl -sf "http://localhost:${PORT}/health" &>/dev/null; then
                break
            fi
            sleep 0.5
        done
        
        echo ""
        echo -e "${GREEN}${BOLD}Ready!${NC} http://localhost:${PORT}"
        echo ""
        echo "Stop with: Ctrl+C or ./start.sh stop"
        
        # step 9: open browser
        open "http://localhost:${PORT}" 2>/dev/null || xdg-open "http://localhost:${PORT}" 2>/dev/null || true
        
        # keep running in foreground so ctrl-c works
        wait $SERVER_PID
        ;;
        
    stop)
        kill_port
        if [ -f ".server.pid" ]; then
            PID=$(cat .server.pid)
            kill "$PID" 2>/dev/null || true
            rm -f .server.pid
        fi
        pkill -f "uvicorn app.main:app" 2>/dev/null || true
        echo "Stopped."
        ;;
        
    reset)
        echo "Resetting progress..."
        rm -f data/progress.db .venv/.installed
        $0 stop 2>/dev/null || true
        sleep 1
        $0 start
        ;;
        
    status)
        if curl -sf "http://localhost:${PORT}/health" &>/dev/null; then
            echo -e "${GREEN}Running${NC} at http://localhost:${PORT}"
        else
            echo -e "${RED}Not running${NC}"
        fi
        ;;
        
    *)
        echo "Usage: ./start.sh [start|stop|reset|status]"
        exit 1
        ;;
esac
