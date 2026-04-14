# GPU Support Training Lab

Interactive training for GPU infrastructure support. Hands-on labs with real scenarios.

## Quick Start

One line — works on a fresh macOS or Linux laptop:

```bash
git clone https://github.com/VPJoeM/Training-Lab.git && cd Training-Lab && ./start.sh
```

Opens at http://localhost:8080 → Setup wizard guides you through configuration.

> **Fresh Mac?** The script handles everything: Xcode CLI tools, Homebrew, Python, virtual environment, and pip packages. Just run the one-liner and follow any prompts. You might need to click "Install" on an Xcode dialog and enter your password for Homebrew.

## Prerequisites

### Auto-Installed
The start script automatically installs these if missing:
- **Xcode Command Line Tools** (macOS — needed for git and compilers)
- **Python 3.10+** via Homebrew (macOS) or apt/dnf (Linux)
- **Homebrew** (macOS only, if needed for Python)

### Required
- **Target server** - an H100 node you can SSH into for server-based labs

### For Full Functionality
- **Support-Tooling repo** - clone to `~/Github/Support-Tooling`
- **sshv configured** - run `connect-to-sshv-portal.sh` to set up your token
- **Tailscale connected** - required for internal tools (VOLT, Redfish, etc.)
- **1Password CLI** - for VOLT API key storage (Node Toolkit uses this)

## Setup Flow

1. Run `./start.sh` - installs dependencies, starts server
2. Browser opens to setup wizard
3. Enter your target server details:
   - **Host**: IP or hostname of an H100 node (e.g., `10.0.1.50`)
   - **Port**: SSH port (usually `4747` for sshv)
   - **User**: SSH username (usually `vpsupport`)
4. Test connection
5. Start training!

## Lab Types

| Type | What Happens |
|------|--------------|
| **Node labs** | SSH to target server, run commands there |
| **Laptop labs** | Run scripts locally (Node Toolkit, Redfish) |
| **Web labs** | Browser-based (VOLT, Metabase) |

## What's Included

| Module | Labs |
|--------|------|
| Environment Overview | Explore VOLT |
| Log Collection | XID 79 Diagnosis, Node Toolkit |
| GPU Diagnostics | Manual DCGM, DCGM via Toolkit |
| InfiniBand | Down Port, Degraded Speed, PCIe Width |
| Driver Management | Version Mismatch, Fabric Manager |
| iDRAC & Redfish | Health Check, Collect TSR |
| Thermal Diagnostics | Read CSV, Identify Hot GPU |
| VPOD Admin | Lookup Customer, Check Balance |

## Commands

```bash
./start.sh          # Start the lab
./start.sh stop     # Stop the lab
./start.sh reset    # Wipe progress and restart
./start.sh status   # Check if running
```

## Troubleshooting

**"Connection failed" on setup**
- Check you can SSH manually: `sshv -p 22 vpsupport@<host>`
- Make sure Tailscale is connected
- Verify your sshv token is set up

**Labs not working**
- Server-based labs need a working SSH connection
- Laptop-based labs need Support-Tooling cloned locally
- Web-based labs just need browser access to internal tools

**Reset everything**
```bash
./start.sh reset
```

## For Developers

```bash
# run with auto-reload
source .venv/bin/activate
uvicorn app.main:app --reload --port 8080

# run tests
./run_tests.sh
```
