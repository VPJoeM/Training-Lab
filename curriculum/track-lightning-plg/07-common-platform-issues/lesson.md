# Common Platform Issues

## Studios Not Starting / Stuck Loading

This is a frequent complaint. Here's your troubleshooting flow:

### Questions to Ask

1. Is it specific to **one studio** or are **none** of their studios working?
2. What's the **name** of the stuck studio?
3. How long has it been stuck?
4. What **machine type** were they trying to use?

### Common Causes

- **Free studio with 300GB+ of data** — The fix is to switch to a data prep machine
- **GPU availability** — Sometimes H100s take a while to provision. This is normal during peak times.
- **Random platform error** — Needs engineering escalation (flag Neil and Ethan)

### For Stuck Studios

If a studio is stuck saving or loading for an extended period, escalate to engineering with the studio name and user email.

## Credit Depletion Confusion

Users frequently don't understand why their credits are disappearing:

- **Idle studios still running** — Compute charges even when they're not coding
- **Machine switching** — Switching from CPU to GPU or between GPU types can trigger unexpected charges
- **The monitoring CPU** — ~$0.43/hr runs alongside every GPU job
- **Transferring to another cloud** — Costs credits that users didn't expect

**Always check:** What machines are running, how long they've been running, and which teamspace is being charged.

## CUDA Installation Issues

Users sometimes need specific CUDA versions for their ML frameworks.

**Docs link:** [Environments — Lightning AI](https://lightning.ai/docs/overview/studios/environments#drivers-and-cuda-versions)

### Quick Install

```bash
sudo apt-get -y install cudnn
```

### Specific Version Install

```bash
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt-get update
sudo apt-get install libcudnn8=8.9.7.29-1+cuda11.8
```

## Data Loss in Studios

When a user loses data:

### Understand the Drive

- The **Drive** is persistent storage attached to a teamspace
- Data in the studio's working directory may or may not persist depending on the setup
- Switching machine types can sometimes cause data loss if files weren't saved to the Drive
- [Drive documentation](https://lightning.ai/docs/overview/drive)

### Data Recovery (L2 — Engineering Required)

If a user has genuinely lost data and it needs recovery:

1. Confirm their AWS CLI setup: `aws sts get-caller-identity`
2. Get deletion markers from S3
3. Create recovery batches
4. Execute the recovery

> This is an L2 operation. Only escalate if the user has paid us at least $100 (check Stripe). Otherwise, guide them to create a new account and duplicate studios to transfer work.

[Loom: Data recovery walkthrough](https://www.loom.com/share/74641ae78d324ae1968c1ebb44e2e999)

## Impersonating a User Account

Sometimes you need to see what the user sees. We have a dedicated tool for this in Support-Tooling:

### Using the Impersonation Tool (Recommended)

```bash
# interactive menu
~/Github/Support-Tooling/scripts/plg/lightning-impersonate.sh

# or CLI mode — generates snippet, copies to clipboard, opens browser
~/Github/Support-Tooling/scripts/plg/lightning-impersonate.sh --user <username> --key <api_key> --copy --open
```

You'll need the username and API key from [ToolJet](https://tooljet.lightning.ai/applications/7b6a09f5-f91a-44a2-9e28-803a13eb8bf0) → User Management. The tool takes those values, generates the JavaScript snippet, and optionally copies it to your clipboard and opens lightning.ai.

> **Tip:** Run the script and choose option 6 to create a shell alias — then just type `impersonate` from anywhere.

### Manual Method

If you prefer to do it by hand:

1. Go to [lightning.ai](https://lightning.ai) and sign in to your own account
2. Open the browser developer console (Right-click → Inspect → Console)
3. Run this JavaScript (replacing username and API key from ToolJet):

```javascript
localStorage.setItem("gridUserId", "<username>");
localStorage.setItem("gridUserKey", "<user API key>");
localStorage.setItem("gridUserToken", "<token>");
```

4. Navigate to [lightning.ai](https://lightning.ai) in a different tab — you're now impersonating
5. **Be careful!** All changes are real. Sign out to end impersonation.

[Loom: Impersonation demo](https://www.loom.com/share/87a32198121a4a149110e50bf1d5173b)

## Kill High-Memory Process

If a user's studio is slow or hanging:

```bash
ps aux --sort=-%mem
```

Find the process eating memory and kill it:

```bash
sudo kill <PID>
```

Or for Python processes specifically:

```bash
pgrep -f python
```

## Clearing CUDA Memory

Users often have leftover GPU processes blocking their work:

1. Find what's using the GPU: `ps aux` or `pgrep -f python`
2. Kill the process: `sudo kill <PID>`

## Working with GitHub in Studios

Some users want to connect their GitHub repos to their studio. Point them to the [Discord guide](https://discord.com/channels/1077906959069626439/1267308626398412830/1267471909856088112).

## Whitelisted IPs

Lightning **does not have static IPs**. Each studio gets a new IP. Users can check their current IP with:

```bash
curl https://ipinfo.io/ip
```

But it will change when the studio restarts. If they need a static IP for firewall rules, this is a limitation of the platform.

## Setting Up a Custom Domain

[Loom: Custom domain setup](https://www.loom.com/share/890e614759d24bdd8c566572cf2d3578)

## Detect Machine Type

Users can check what they're running on:

```bash
nvidia-smi
```

Or programmatically:

```python
from lightning_sdk import Studio
print(Studio().machine)  # outputs Machine.L4_X_4
```

## Installing Third-Party Programs

All machines have `apt-get`, so check for a package first:

```bash
sudo apt-get install <package-name>
```

For programs not in apt, download and install manually:

```bash
wget https://example.com/path/to/file.zip
sudo apt-get install unzip
unzip file.zip
```

## Using Marimo in Studio

[Loom: Marimo setup](https://www.loom.com/share/3a827fbc026149708660ee12f3f71a8e)
