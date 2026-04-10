# Log Collection & Diagnosis

The first thing you do on any GPU issue is collect logs. Before you theorize, before you restart anything -- get the logs. They're your evidence.

## nvidia-bug-report.sh

NVIDIA ships a built-in log collector. This is often the first thing NVIDIA support asks for, and it's packed with useful diagnostic data.

```bash
sudo nvidia-bug-report.sh
```

This produces `nvidia-bug-report.log.gz` in the current directory -- a compressed dump of everything NVIDIA-related.

**What's in it:**
- Driver version and loaded kernel modules
- Full `nvidia-smi -q` output for all GPUs
- dmesg excerpts (especially XID errors)
- PCIe topology and link status
- ECC error counts and retired pages
- Temperature and power history
- NVLink status and errors
- Fabric Manager logs (if running)

**How to read it:**

```bash
# decompress it
gunzip nvidia-bug-report.log.gz

# search for common issues
grep -i "xid" nvidia-bug-report.log
grep -i "fallen off" nvidia-bug-report.log
grep -i "ecc" nvidia-bug-report.log
grep -i "RmInitAdapter" nvidia-bug-report.log    # driver init failures

# or open it and scroll -- the summary is near the top
less nvidia-bug-report.log
```

**When to use it:**
- NVIDIA support asks for it
- You need a comprehensive snapshot of GPU state
- Something weird is happening and you want everything in one file
- Before and after a driver change (for comparison)

**Pro tip:** The report is huge (often 10MB+). Don't try to read it all -- search for keywords related to your issue.

## Node Toolkit Log Collection

For day-to-day work in the lab, **`start-node-toolkit.sh` is the main log collection path** -- it talks to nodes over **sshv**, you can aim it at a **hostname** or lean on **discovery** when you do not want to type IPs by hand, and it keeps the messy SSH details out of your way.

From the main menu, **option 14** drops you into the **log collection** submenu. That is where you pull the usual evidence without reinventing the shell one-liners each time. Rough map of what matters:

| Option | What it grabs |
|--------|----------------|
| **1** | **dmesg** -- kernel ring buffer, XIDs, PCIe noise |
| **2** | **journalctl** -- systemd / service story around the incident |
| **3** | **nvidia-smi** (detailed **`-q`** style output) -- driver, clocks, thermals, etc. |
| **4** | **ECC** check -- memory error counters you actually care about |
| **5** | **IB diagnostics** -- InfiniBand side of the house |
| **6** | **nvidia-bug-report** -- NVIDIA’s own bundle (same idea as the section below) |
| **7** | **Dell TSR** -- hardware vendor support bundle when the box is Dell |
| **9** | **Collect All** -- runs **1 through 5 in parallel** so you get the core OS + GPU + IB slice in one shot |

There is more in that menu (SOS reports, DCGMI diagnostics, NCCL benchmark, and friends) when you need a deeper cut -- poke around when you have time.

Stuff lands under **`~/Reports/`**, **organized by hostname**, so you are not hunting for a random tarball in `/tmp` at 2am.

## Manual Commands (What the Toolkit Runs)

Know the raw commands. The toolkit wraps these, but you should be able to run them yourself when needed.

```bash
# dmesg -- kernel ring buffer (toolkit option 1)
sudo dmesg

# journalctl -- systemd logs (toolkit option 2)
sudo journalctl --no-pager

# nvidia-smi detailed output (toolkit option 3)
nvidia-smi -q

# ECC error check (toolkit option 4)
nvidia-smi --query-gpu=index,name,ecc.errors.corrected.volatile.total,ecc.errors.uncorrected.volatile.total --format=csv

# nvidia-bug-report -- NVIDIA's full diagnostic bundle (toolkit option 6)
sudo nvidia-bug-report.sh
# produces nvidia-bug-report.log.gz

# InfiniBand diagnostics (toolkit option 5)
sudo ibstat
sudo ibstatus
sudo mlxlink -d mlx5_0 -p 1 -e    # error counters per port

# Dell TSR -- Tech Support Report (toolkit option 7)
sudo racadm supportassist collect -t Debug
sudo racadm jobqueue view     # monitor the job

# SOS report (toolkit option 10)
sudo sos report --batch

# PSB check (toolkit option 8)
sudo lspci -vv | grep -A 20 "3D controller"
```

## Downloading Logs to Your Laptop

Once you've collected logs on the server, you need to get them back to your laptop for analysis or to share with others.

**Using Node Toolkit (recommended):**

The toolkit's **option 15** (File Transfer menu) handles downloads via sshv:

```bash
./scripts/sshv/start-node-toolkit.sh
# → Main Menu → option 15 (Download files from nodes)
```

It can pull specific files, entire directories, or common log bundles -- and it handles the sshv authentication for you.

**Manual download with scp/rsync via sshv:**

```bash
# download a single file
sshv -p 4747 vpsupport@<server-ip>:/path/to/nvidia-bug-report.log.gz ~/Downloads/

# download a directory
sshv -p 4747 vpsupport@<server-ip>:/tmp/logs/ ~/Downloads/server-logs/ -r

# using rsync for large transfers (better for big files, can resume)
rsync -avz -e "sshv -p 4747" vpsupport@<server-ip>:/path/to/logs/ ~/Downloads/logs/
```

**Common files you'll download:**

| File | Where it lives | What it is |
|------|---------------|------------|
| `nvidia-bug-report.log.gz` | Current dir where you ran it | NVIDIA's full diagnostic bundle |
| TSR `.zip` | `/tmp/` or iDRAC specifies location | Dell Tech Support Report |
| `sosreport-*.tar.xz` | `/var/tmp/` | Red Hat/Ubuntu system report |
| dmesg output | Save it yourself: `sudo dmesg > /tmp/dmesg.log` | Kernel ring buffer |
| DCGM results | `~/Reports/<hostname>/` if using toolkit | GPU stress test results |

**Pro tip:** When collecting evidence for an RMA or escalation, grab everything into one directory on the server first, then download that whole directory. Makes it easier to keep track of what you have.

```bash
# on the server -- bundle everything
mkdir -p /tmp/case-12345
sudo dmesg > /tmp/case-12345/dmesg.log
sudo nvidia-bug-report.sh
mv nvidia-bug-report.log.gz /tmp/case-12345/
nvidia-smi -q > /tmp/case-12345/nvidia-smi.log

# on your laptop -- download the bundle
sshv -p 4747 vpsupport@<server-ip>:/tmp/case-12345/ ~/Downloads/case-12345/ -r
```

---

## Reading dmesg for GPU Errors

GPU problems show up in the kernel ring buffer. The most important patterns:

```bash
# look for GPU XID errors
sudo dmesg | grep -i xid

# look for PCIe errors (GPUs falling off the bus)
sudo dmesg | grep -i "AER\|pci.*error\|fallen off"

# look for anything NVIDIA
sudo dmesg | grep -i nvidia
```

### XID Error Reference

| XID | Meaning | Typical Action |
|-----|---------|---------------|
| 13 | Graphics engine exception | Usually a software bug, but check thermals |
| 31 | GPU memory page fault | Check ECC errors, might need RMA |
| 48 | Double-bit ECC error | Likely needs RMA |
| 63 | ECC page retirement | Row remapping exhausted, RMA |
| 79 | GPU fallen off the bus | PCIe issue, reseat or RMA |
| 94 | Contained ECC error | Monitor, reset ECC counters, RMA if recurring |

## What's Next

Two labs to get you comfortable with log collection:

1. **XID 79 Diagnosis** - Find a GPU error using manual dmesg commands
2. **Log Collection via Node Toolkit** - The preferred workflow you'll use day-to-day

Always prefer Node Toolkit when possible -- it organizes logs by hostname and handles multiple collection types in parallel.
