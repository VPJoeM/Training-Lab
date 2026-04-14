# Common Platform Issues

## Studios Not Starting / Stuck Loading

This is a frequent complaint. Here's your troubleshooting flow:

### Questions to Ask

1. Is it specific to **one studio** or are **none** of their studios working?
2. What's the **name** of the stuck studio?
3. How long has it been stuck?
4. What **machine type** were they trying to use?
5. What **cloud provider** were they using?

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

> **Restricted access.** Account impersonation is a sensitive operation. Natalie Rand is confirming with Neil who should have access. Only use this if you've been explicitly authorized.

If authorized, use the impersonation tool in Support-Tooling:

```bash
~/Github/Support-Tooling/scripts/plg/lightning-impersonate.sh
```

[Loom: Impersonation demo](https://www.loom.com/share/87a32198121a4a149110e50bf1d5173b)

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
