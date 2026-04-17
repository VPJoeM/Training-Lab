# Lightning Support Training Lab

Interactive training platform for Lightning AI support. Lessons, video walkthroughs, and knowledge-check quizzes.

## First Time Setup

One line — works on a fresh macOS or Linux laptop:

```bash
git clone git@github.com:VPJoeM/Training-Lab.git && cd Training-Lab && ./start.sh
```

The script handles everything automatically: Xcode CLI tools, Homebrew, Python, 1Password CLI, and all dependencies. Just follow any prompts that pop up.

Opens at http://localhost:8080 — pick **Lightning Platform (PLG)** to start.

> **Fresh Mac?** You might need to click "Install" on an Xcode dialog and enter your password for Homebrew. That's it.

## Beta Testers

### Getting Updates

Every time you start the lab, it automatically pulls the latest changes. Just run:

```bash
cd Training-Lab && ./start.sh
```

Or if the lab is already running, `Ctrl+C` to stop it first, then run the above.

### Quick Alias (Recommended)

Set up a shortcut so you can just type `lab` from anywhere:

```bash
cd Training-Lab && ./start.sh alias lab
```

Then open a new terminal (or run `source ~/.zshrc`) and just type:

```bash
lab
```

That's it — kills any old instance, pulls the latest, and starts fresh with a browser window.

### Resetting Progress

Want to start the quizzes from scratch?

```bash
cd Training-Lab && ./start.sh reset
```

## What's Included

### Lightning Platform (PLG) — Active

| Module | Content |
|--------|---------|
| Platform Overview | Account hierarchy, tiers, credits, login methods |
| Crisp Workflow | Ticket routing, shortcuts, escalation process |
| Account Verification | Phone verification, login issues, ban reasons |
| Credit Management | How credits work, ToolJet operations |
| Banned Users | Ban types, country lists, when to unban |
| Subscription & Billing | Stripe ops, refunds, cancellations |
| Common Issues | Studios stuck, credit drain, data recovery |
| ToolJet Guide | Full ToolJet walkthrough with embedded video demos |

Each module has a lesson, embedded Loom video walkthroughs, and a 5-question knowledge check quiz (one question at a time, 3 tries per question, instant feedback).

### Bare Metal H100 — Coming Soon

Infrastructure training with hands-on labs. Currently in development.

## Commands

```bash
./start.sh          # Start the lab (auto-updates first)
./start.sh stop     # Stop the lab
./start.sh reset    # Wipe progress and restart
./start.sh status   # Check if running
./start.sh alias    # Create a shell alias (e.g. ./start.sh alias lab)
```

## Prerequisites

### Auto-Installed

The start script automatically installs these if missing:

- Xcode Command Line Tools (macOS)
- Homebrew (macOS)
- Python 3.10+
- Bash 5+
- 1Password CLI
- jq

### For Full Functionality (Bare Metal track only)

- Target H100 server with SSH access
- Support-Tooling repo cloned locally
- sshv configured
- Tailscale connected

## Troubleshooting

**Script fails on first run**
- Make sure you have internet access
- On macOS: click "Install" if an Xcode dialog pops up
- Enter your password when Homebrew asks for it

**Port already in use**
- The script will ask if you want to use a different port or kill the existing process

**Reset everything**
```bash
cd Training-Lab && rm -rf .venv && ./start.sh
```

**Wrong Python version**
- The script auto-detects and uses Homebrew Python over the system one
- If it's still wrong: `rm -rf .venv && ./start.sh`
