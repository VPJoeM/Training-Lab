# Lightning Support Training Lab

Interactive training platform for Lightning AI support. Lessons, video walkthroughs, and knowledge-check quizzes.

## First Time Setup

Same flow for both repos: clone (or skip if the folder already exists), pull latest, run `start.sh`. Works on a fresh macOS or Linux laptop.

### Public repo (JM-LAI) — beta / HTTPS

Folder name: `raining-Lab`

```bash
git clone https://github.com/JM-LAI/raining-Lab.git 2>/dev/null; cd raining-Lab && git pull && ./start.sh
```

### Internal repo (VPJoeM) — SSH

Folder name: `Training-Lab`

```bash
git clone git@github.com:VPJoeM/Training-Lab.git 2>/dev/null; cd Training-Lab && git pull && ./start.sh
```

> **Folder already exists?** The `2>/dev/null` on clone hides the "already exists" noise; `cd` + `git pull` still runs. Same one-liner works on repeat.

The script handles everything automatically: Xcode CLI tools, Python, and all dependencies. Just follow any prompts that pop up.

Opens at http://localhost:8080 — pick **Lightning Platform (PLG)** to start.

> **Fresh Mac?** You might see an Xcode dialog — click "Install". On macOS the lab does **not** need Homebrew or sudo; optional tools only install if Homebrew is available.

## Beta Testers

Use the **public** clone above (`raining-Lab`). From that folder:

### Getting Updates

Every time you start the lab, it automatically pulls the latest changes. Just run:

```bash
cd raining-Lab && ./start.sh
```

Or if the lab is already running, `Ctrl+C` to stop it first, then run the above.

### Quick Alias (Recommended)

Set up a shortcut so you can just type `lab` from anywhere:

```bash
cd raining-Lab && ./start.sh alias lab
```

Then open a new terminal (or run `source ~/.zshrc`) and just type:

```bash
lab
```

That's it — kills any old instance, pulls the latest, and starts fresh with a browser window.

### Resetting Progress

Want to start the quizzes from scratch?

```bash
cd raining-Lab && ./start.sh reset
```

(If you use the VPJoeM clone, use `cd Training-Lab` instead.)

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

### Build on Lightning — Capstone

Final project that closes any track. Pick a problem, write it up using the Value Framework + 1:3:1 Decision-Making Process, build it on the platform, and present a 15-minute walkthrough to the team. Project-based — no quiz. Discipline of the frameworks is what's being trained, not the ambition of the build.

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
- Python 3.9+ (ships with macOS Xcode tools)

If you have admin rights, it'll also install (optional, not required):
- Homebrew (macOS)
- Bash 5+
- 1Password CLI
- jq

### For Full Functionality (Bare Metal track only)

- Target H100 server with SSH access
- Support-Tooling repo cloned locally
- sshv configured
- Tailscale connected

## Troubleshooting

**"destination path already exists"**
- That's fine — the one-liner handles it. It'll skip the clone and update instead.

**Script fails on first run**
- Make sure you have internet access
- On macOS: click "Install" if an Xcode dialog pops up

**"Need sudo access" / Homebrew install fails**
- This is not a blocker. The lab works with the system Python that comes with Xcode tools.
- Homebrew is only used for optional extras (bash 5+, 1Password CLI, jq).
- If you don't have admin rights on your Mac, the script skips those automatically.

**Port already in use**
- The script will ask if you want to use a different port or kill the existing process

**Reset everything**

```bash
cd raining-Lab && rm -rf .venv && ./start.sh
```

(Replace `raining-Lab` with `Training-Lab` if you cloned VPJoeM.)

**Wrong Python version**
- The script auto-detects and uses the best Python available
- If it's still wrong: `rm -rf .venv && ./start.sh`
