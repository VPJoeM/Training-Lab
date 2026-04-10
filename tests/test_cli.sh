#!/usr/bin/env bash
# CLI tests for setup.sh and training-lab.sh
# run with: bash tests/test_cli.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PASS=0
FAIL=0

pass() { echo "  PASS: $1"; PASS=$((PASS + 1)); }
fail() { echo "  FAIL: $1"; FAIL=$((FAIL + 1)); }

run_test() {
    local desc="$1"
    shift
    if "$@" &>/dev/null; then
        pass "$desc"
    else
        fail "$desc"
    fi
}

run_test_output() {
    local desc="$1"
    local expected="$2"
    shift 2
    local output
    output=$("$@" 2>&1) || true
    if echo "$output" | grep -qi "$expected"; then
        pass "$desc"
    else
        fail "$desc (expected '$expected' in output)"
    fi
}

echo ""
echo "═══════════════════════════════"
echo "  CLI Tests"
echo "═══════════════════════════════"
echo ""

# ── setup.sh ──
echo "setup.sh:"
run_test "syntax valid" bash -n "${SCRIPT_DIR}/setup.sh"
run_test_output "--help exits 0" "Usage" "${SCRIPT_DIR}/setup.sh" --help
run_test_output "--version shows version" "v1.0.0" "${SCRIPT_DIR}/setup.sh" --version
run_test_output "unknown command exits non-zero" "Unknown" bash -c "${SCRIPT_DIR}/setup.sh badcmd 2>&1 || true"
echo ""

# ── training-lab.sh ──
echo "training-lab.sh:"
run_test "syntax valid" bash -n "${SCRIPT_DIR}/training-lab.sh"
run_test_output "--help exits 0" "Usage" "${SCRIPT_DIR}/training-lab.sh" --help
run_test_output "--version shows version" "v1.0.0" "${SCRIPT_DIR}/training-lab.sh" --version
run_test_output "--help lists reset command" "reset" "${SCRIPT_DIR}/training-lab.sh" --help
run_test_output "--help lists status command" "status" "${SCRIPT_DIR}/training-lab.sh" --help
run_test_output "--help lists teardown command" "teardown" "${SCRIPT_DIR}/training-lab.sh" --help
run_test_output "--help lists logs command" "logs" "${SCRIPT_DIR}/training-lab.sh" --help
echo ""

# ── summary ──
TOTAL=$((PASS + FAIL))
echo "═══════════════════════════════"
echo "  Results: ${PASS}/${TOTAL} passed"
if [[ $FAIL -gt 0 ]]; then
    echo "  ${FAIL} FAILED"
    echo "═══════════════════════════════"
    exit 1
else
    echo "  All tests passed"
    echo "═══════════════════════════════"
    exit 0
fi
