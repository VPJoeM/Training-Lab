#!/usr/bin/env bash
# GPU Support Training Lab - one command to start
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

# detect OS
is_mac() { [[ "$(uname)" == "Darwin" ]]; }
is_linux() { [[ "$(uname)" == "Linux" ]]; }

# install dependencies automatically
install_deps() {
    echo -e "${CYAN}Installing dependencies...${NC}"
    
    if is_mac; then
        # install Homebrew if missing
        if ! command -v brew &>/dev/null; then
            echo "Installing Homebrew..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            eval "$(/opt/homebrew/bin/brew shellenv 2>/dev/null || /usr/local/bin/brew shellenv)"
        fi
        
        # install Python 3 if missing
        if ! command -v python3 &>/dev/null; then
            echo "Installing Python 3..."
            brew install python@3.11
        fi
        
        # check Python version (need 3.10+)
        PY_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
        PY_MAJOR=$(echo "$PY_VERSION" | cut -d. -f1)
        PY_MINOR=$(echo "$PY_VERSION" | cut -d. -f2)
        if [[ "$PY_MAJOR" -lt 3 ]] || [[ "$PY_MAJOR" -eq 3 && "$PY_MINOR" -lt 10 ]]; then
            echo "Python 3.10+ required (found $PY_VERSION). Installing..."
            brew install python@3.11
        fi
        
    elif is_linux; then
        # Debian/Ubuntu
        if command -v apt-get &>/dev/null; then
            if ! command -v python3 &>/dev/null; then
                echo "Installing Python 3..."
                sudo apt-get update
                sudo apt-get install -y python3 python3-venv python3-pip
            fi
        # RHEL/CentOS/Fedora
        elif command -v dnf &>/dev/null; then
            if ! command -v python3 &>/dev/null; then
                echo "Installing Python 3..."
                sudo dnf install -y python3 python3-pip
            fi
        elif command -v yum &>/dev/null; then
            if ! command -v python3 &>/dev/null; then
                echo "Installing Python 3..."
                sudo yum install -y python3 python3-pip
            fi
        fi
    fi
    
    # final check
    if ! command -v python3 &>/dev/null; then
        echo -e "${RED}Could not install Python 3. Please install manually.${NC}"
        echo "  macOS: brew install python@3.11"
        echo "  Ubuntu: sudo apt install python3 python3-venv"
        exit 1
    fi
    
    echo -e "${GREEN}Dependencies installed.${NC}"
}

case "${1:-start}" in
    start|"")
        echo -e "${CYAN}${BOLD}GPU Support Training Lab${NC}"
        echo ""
        
        # auto-install Python if missing
        if ! command -v python3 &>/dev/null; then
            install_deps
        fi
        
        # check Python version
        PY_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
        PY_MAJOR=$(echo "$PY_VERSION" | cut -d. -f1)
        PY_MINOR=$(echo "$PY_VERSION" | cut -d. -f2)
        if [[ "$PY_MAJOR" -lt 3 ]] || [[ "$PY_MAJOR" -eq 3 && "$PY_MINOR" -lt 10 ]]; then
            echo -e "${YELLOW}Python 3.10+ required (found $PY_VERSION)${NC}"
            install_deps
        fi
        
        # create venv if needed
        if [ ! -d ".venv" ]; then
            echo "Creating virtual environment..."
            python3 -m venv .venv
        fi
        
        # activate and install deps
        source .venv/bin/activate
        
        if [ ! -f ".venv/.installed" ]; then
            echo "Installing Python packages..."
            pip install -q --upgrade pip
            pip install -q -r requirements.txt
            touch .venv/.installed
        fi
        
        # create data dir
        mkdir -p data
        
        # check if already running
        if curl -sf "http://localhost:${PORT}/health" &>/dev/null 2>&1; then
            echo -e "${GREEN}Already running at http://localhost:${PORT}${NC}"
            open "http://localhost:${PORT}" 2>/dev/null || xdg-open "http://localhost:${PORT}" 2>/dev/null || true
            exit 0
        fi
        
        # start server
        echo "Starting server on port ${PORT}..."
        uvicorn app.main:app --host 0.0.0.0 --port "$PORT" &
        SERVER_PID=$!
        echo $SERVER_PID > .server.pid
        
        # wait for startup
        for i in {1..30}; do
            if curl -sf "http://localhost:${PORT}/health" &>/dev/null; then
                break
            fi
            sleep 0.5
        done
        
        echo ""
        echo -e "${GREEN}${BOLD}Ready!${NC} http://localhost:${PORT}"
        echo ""
        echo "Stop with: ./start.sh stop"
        
        # open browser (macOS or Linux)
        open "http://localhost:${PORT}" 2>/dev/null || xdg-open "http://localhost:${PORT}" 2>/dev/null || true
        
        # keep running in foreground so ctrl-c works
        wait $SERVER_PID
        ;;
        
    stop)
        if [ -f ".server.pid" ]; then
            PID=$(cat .server.pid)
            if kill -0 "$PID" 2>/dev/null; then
                kill "$PID"
                echo "Stopped."
            fi
            rm -f .server.pid
        else
            # try to find and kill uvicorn
            pkill -f "uvicorn app.main:app" 2>/dev/null || true
            echo "Stopped."
        fi
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
