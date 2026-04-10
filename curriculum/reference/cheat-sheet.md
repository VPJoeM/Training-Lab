# Quick Reference Cheat Sheet

Your go-to commands organized by situation. Bookmark this page.

**Safety Labels:** [SAFE:readonly] Safe to run anytime. [SAFE:state] Changes system state. [SAFE:disruptive] Can interrupt workloads. [SAFE:approval] May need customer approval.

---

## Node Unresponsive / Can't SSH

| Step | Command | What You're Checking |
|------|---------|---------------------|
| 1 | Check [VOLT](https://volt.lightning.ai) [SAFE:readonly] | Is the node showing as available? What DC? Who's on it? |
| 2 | `./scripts/api/connect-idrac-via-redfish.sh` [SAFE:readonly] | Use Redfish to check system health and power state via iDRAC |
| 3 | Power cycle via Redfish → Power Controls menu [SAFE:disruptive] | If OS is hung, hard reset through iDRAC |
| 4 | Check iDRAC event log via System Info menu [SAFE:readonly] | Look for hardware errors, PSU failures, thermal events |

---

## GPU Issues / "GPUs Not Working"

| Step | Command | What You're Checking |
|------|---------|---------------------|
| 1 | `nvidia-smi` [SAFE:readonly] | Are all 8 GPUs showing? Driver loaded? Temps normal? |
| 2 | `nvidia-smi -q -d ECC` [SAFE:readonly] | Any ECC errors? Correctable vs uncorrectable? |
| 3 | `dmesg \| grep -i xid` [SAFE:readonly] | XID errors in the kernel log? Check timestamps! |
| 4 | `nvidia-smi -q -d TEMPERATURE` [SAFE:readonly] | Thermal throttling? Anything above 85°C? |
| 5 | `nvidia-smi topo -m` [SAFE:readonly] | NVLink topology intact? Any X's where there should be NV links? |
| 6 | `systemctl status nvidia-fabricmanager` [SAFE:readonly] | Fabric Manager running? Version match the driver? |

---

## Training Job Slow / Performance Issues

| Step | Command | What You're Checking |
|------|---------|---------------------|
| 1 | `nvidia-smi` | GPU utilization near 100%? Power draw near TDP (700W for H100)? |
| 2 | `ibstat` | All IB ports Active? Expected rate (NDR = 400)? |
| 3 | `nvidia-smi nvlink -s` | NVLink errors? Any replays or recovery counts? |
| 4 | `dmesg \| grep -i "AER\|pci.*error"` | PCIe errors could mean degraded GPU/IB bandwidth |
| 5 | Node Toolkit → NCCL Benchmark (option 14 → 12) | Run an actual inter-node bandwidth test |

---

## InfiniBand Issues

| Step | Command | What You're Checking |
|------|---------|---------------------|
| 1 | `ibstat` | Port states: Active = good, Down = bad. Check rate too |
| 2 | `mlxlink -d mlx5_0 -p 1` | Link status for specific port |
| 3 | `mlxlink -d mlx5_0 -p 1 -m` | Optical power levels -- out of spec = bad cable/transceiver |
| 4 | `mlxlink -d mlx5_0 -p 1 -e` | Error counters on the link |
| 5 | `lspci -vv -s $(lspci \| grep Mellanox \| head -1 \| awk '{print $1}') \| grep -i lnk` | PCIe width: should be x16 |

---

## ECC Errors

| Step | Command | What You're Checking |
|------|---------|---------------------|
| 1 | `./scripts/gpu/check-ecc.sh` [SAFE:readonly] | Quick ECC scan across all GPUs |
| 2 | `nvidia-smi -q -d ECC` [SAFE:readonly] | Detailed per-GPU ECC counts |
| 3 | Check if correctable or uncorrectable [SAFE:readonly] | Correctable = monitor. Uncorrectable = likely RMA |
| 4 | `nvidia-smi -q -d RETIRED_PAGES` [SAFE:readonly] | Row remapping status -- exhausted = RMA |

**Decision:** Small number of correctable → reset counters, monitor. Recurring on same GPU → start RMA conversation. Any uncorrectable → RMA.

---

## Driver Issues

| Step | Command | What You're Checking |
|------|---------|---------------------|
| 1 | `nvidia-smi` | Shows driver version + CUDA version at the top |
| 2 | `modinfo nvidia \| grep ^version` | Kernel module version -- should match nvidia-smi |
| 3 | `systemctl status nvidia-fabricmanager` | Fabric Manager version -- must match driver major version |
| 4 | `dpkg -l \| grep -i nvidia` | All installed NVIDIA packages and versions |
| 5 | `cat /usr/local/cuda/version.txt` | CUDA toolkit version |

**Common failure:** Driver upgraded but Fabric Manager wasn't (or vice versa). Multi-GPU jobs fail, single-GPU works fine.

---

## GPU Stress Testing / Thermal Validation

**DCGM via Node Toolkit (default for post-RMA, GPU replacement, stress testing):**

| Step | Command | What You're Checking |
|------|---------|---------------------|
| 1 | Node Toolkit → option 14 → option 11 | Handles DCGM install, process cleanup, runs in screen |
| 2 | Pick Level 3 (~12 min) or Level 4 (~30 min) | L3 for quick post-replacement, L4 for thorough |
| 3 | Check results in `~/Reports/` | Pass/fail per GPU, any errors |

**Or directly on the node:** [SAFE:state]

```bash
sudo dcgmi diag -r 3 --verbose    # L3 stress test
sudo dcgmi diag -r 4 --verbose    # L4 extended (use screen for long runs)
```


---

## Collecting Logs

**Via Node Toolkit (recommended -- fleet-capable, organized output):**

```bash
./scripts/sshv/start-node-toolkit.sh
# → Main Menu → option 14 (Log Collection)
```

| Option | What It Collects | Speed |
|--------|-----------------|-------|
| 1 | dmesg | Fast, parallel |
| 2 | journalctl | Fast, parallel |
| 3 | nvidia-smi -q | ~10s per node |
| 4 | ECC check report | ~15s per node |
| 5 | InfiniBand diagnostics | ~30s per node |
| 6 | NVIDIA bug report | ~5 min per node |
| 7 | Dell TSR | ~10 min, serial |
| 9 | **Collect All (1-5)** | Parallel, recommended |
| 11 | DCGMI diagnostics | L1: ~1min, L3: ~12min, L4: ~30min |
| 12 | NCCL benchmark | ~10-20 min first run |

Logs saved to `~/Reports/` organized by hostname.

**Manual commands (when you're already on the node):**

```bash
sudo dmesg                              # kernel ring buffer
sudo journalctl --no-pager              # systemd logs
nvidia-smi -q                           # full GPU details
nvidia-smi -q -d ECC                    # ECC errors only
sudo nvidia-bug-report.sh               # NVIDIA's full bundle
sudo ibstat                              # IB port status
sudo racadm supportassist collect -t Debug  # Dell TSR
sudo sos report --batch                  # SOS report
sudo dcgmi diag -r 3 --verbose               # DCGM stress test
```

---

## XID Error Quick Reference

| XID | Meaning | Action |
|-----|---------|--------|
| 13 | Graphics engine exception | Check thermals, usually software bug |
| 31 | GPU memory page fault | Check ECC, might need RMA |
| 48 | Double-bit ECC error | RMA |
| 63 | ECC page retirement exhausted | RMA |
| 79 | GPU fallen off the bus | PCIe issue -- reseat or RMA |
| 94 | Contained ECC error | Monitor, reset counters, RMA if recurring |

---

## Key Tools

| Tool | What For | Where |
|------|----------|-------|
| **VOLT** | Node lookups (hostname, IPs, DC, customer) | [volt.lightning.ai](https://volt.lightning.ai) |
| **Node Toolkit** | Fleet ops, log collection, diagnostics | `scripts/sshv/start-node-toolkit.sh` |
| **Redfish Script** | iDRAC operations (BIOS, power, fans, firmware) | `scripts/api/connect-idrac-via-redfish.sh` |
| **sshv** | SSH to nodes (handles Vault auth) | `sshv -p 4747 vpsupport@<ip>` |
