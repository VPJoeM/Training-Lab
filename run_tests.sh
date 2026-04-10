#!/usr/bin/env bash
# run the full test suite -- one command, everything gets tested
# usage: ./run_tests.sh [--quick] [--verbose] [--json]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${SCRIPT_DIR}/.venv"
VERBOSE=""
QUICK=false
JSON_OUTPUT=false
EXIT_CODE=0

for arg in "$@"; do
    case "$arg" in
        --verbose|-v) VERBOSE="-v" ;;
        --quick|-q)   QUICK=true ;;
        --json)       JSON_OUTPUT=true ;;
        --help|-h)
            echo "Usage: ./run_tests.sh [--quick] [--verbose] [--json]"
            echo ""
            echo "Flags:"
            echo "  --quick, -q     Skip slow tests"
            echo "  --verbose, -v   Verbose pytest output"
            echo "  --json          Output results as JSON (for agent consumption)"
            echo "  --help, -h      This help"
            exit 0
            ;;
    esac
done

# activate venv if it exists
if [[ -d "${VENV_DIR}" ]]; then
    source "${VENV_DIR}/bin/activate"
fi

# make sure dev deps are installed
if ! python -c "import pytest" &>/dev/null 2>&1; then
    echo "Installing test dependencies..."
    pip install -q -r "${SCRIPT_DIR}/requirements-dev.txt"
fi

echo ""
echo "═══════════════════════════════════════"
echo "  GPU Support Training Lab - Test Suite"
echo "═══════════════════════════════════════"
echo ""

# ── python tests ──
echo "▸ Running Python tests..."
cd "${SCRIPT_DIR}"

if [[ "$JSON_OUTPUT" == true ]]; then
    python -m pytest tests/ ${VERBOSE} --tb=short -q --no-header 2>&1 || EXIT_CODE=1
else
    python -m pytest tests/ ${VERBOSE} --tb=short 2>&1 || EXIT_CODE=1
fi

echo ""

# ── CLI tests ──
if [[ "$QUICK" != true ]]; then
    echo "▸ Running CLI tests..."
    bash tests/test_cli.sh || EXIT_CODE=1
    echo ""
fi

# ── static checks ──
echo "▸ Running static checks..."

# check all python files parse
PARSE_FAIL=0
for pyfile in app/*.py; do
    if ! python -c "import ast; ast.parse(open('${pyfile}').read())" &>/dev/null 2>&1; then
        echo "  FAIL: ${pyfile} has syntax errors"
        PARSE_FAIL=1
    fi
done
if [[ $PARSE_FAIL -eq 0 ]]; then
    echo "  All Python files parse OK"
fi

# check bash scripts parse
for shfile in setup.sh training-lab.sh; do
    if bash -n "${shfile}" &>/dev/null 2>&1; then
        echo "  ${shfile} syntax OK"
    else
        echo "  FAIL: ${shfile} has syntax errors"
        EXIT_CODE=1
    fi
done

# check required files exist
echo ""
echo "▸ Checking project structure..."
REQUIRED_FILES=(
    "Dockerfile"
    "Dockerfile.terminal"
    "docker-compose.yml"
    "requirements.txt"
    ".env.example"
    ".gitignore"
    "app/main.py"
    "app/config.py"
    "app/models.py"
    "app/scenario_engine.py"
    "app/templates/base.html"
    "app/templates/dashboard.html"
    "app/templates/module.html"
    "app/templates/scenario.html"
    "app/templates/terminal.html"
)

MISSING=0
for f in "${REQUIRED_FILES[@]}"; do
    if [[ ! -f "${SCRIPT_DIR}/${f}" ]]; then
        echo "  MISSING: ${f}"
        MISSING=1
    fi
done
if [[ $MISSING -eq 0 ]]; then
    echo "  All required files present"
fi

# check curriculum has content
MODULE_COUNT=$(find "${SCRIPT_DIR}/curriculum" -name "lesson.md" 2>/dev/null | wc -l | tr -d ' ')
echo "  Curriculum modules with lessons: ${MODULE_COUNT}"

echo ""
echo "═══════════════════════════════════════"
if [[ $EXIT_CODE -eq 0 ]]; then
    echo "  All tests passed"
else
    echo "  Some tests failed (exit code: ${EXIT_CODE})"
fi
echo "═══════════════════════════════════════"

exit $EXIT_CODE
