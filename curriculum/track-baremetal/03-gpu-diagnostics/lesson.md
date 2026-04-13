# GPU Diagnostics

Now we get into the meat of it. When someone says "my GPUs aren't working," this module teaches you how to figure out why.

## nvidia-smi Deep Dive

`nvidia-smi` is your best friend. Learn to read it fast:

```bash
nvidia-smi                    # overview of all GPUs
nvidia-smi -q                 # detailed query (verbose)
nvidia-smi -q -d ECC          # just ECC error info
nvidia-smi -q -d TEMPERATURE  # thermal info
nvidia-smi topo -m            # GPU topology (NVLink connections)
nvidia-smi nvlink -s          # NVLink status
```

Key things to check on every `nvidia-smi` output:

1. **Driver version** -- does it match what we expect?
2. **GPU count** -- are all 8 GPUs showing up?
3. **Temperature** -- anything above 85°C under load is concerning
4. **ECC errors** -- any non-zero counts need investigation
5. **Power** -- are GPUs getting full power draw?

## ECC Errors

ECC (Error-Correcting Code) memory tracks bit-flip errors:

- **Single-bit (correctable)**: Hardware fixed it, but it's a warning sign
- **Double-bit (uncorrectable)**: Data corruption, GPU is unreliable

```bash
# our script for checking ECC across all GPUs
./scripts/gpu/check-ecc.sh
```

**Manual ECC commands (what check-ecc.sh runs under the hood):**

```bash
# quick ECC summary -- all GPUs, one line each
nvidia-smi --query-gpu=index,name,ecc.errors.corrected.volatile.total,ecc.errors.uncorrected.volatile.total --format=csv

# detailed ECC per GPU
nvidia-smi -q -d ECC

# check retired pages (row remapping)
nvidia-smi -q -d RETIRED_PAGES

# reset ECC volatile counters (after investigating)
sudo nvidia-smi -i 0 --reset-ecc-errors 0     # reset volatile for GPU 0
sudo nvidia-smi --reset-ecc-errors 0            # reset volatile for ALL GPUs

# check persistence mode (should be enabled)
nvidia-smi -q -d PERFORMANCE | grep "Persistence Mode"
```

**When to reset vs replace**:

- Small number of single-bit errors → reset counters, monitor
- Recurring single-bit on same GPU → start an RMA conversation
- Any double-bit error → RMA

## DCGM (Data Center GPU Manager)

DCGM is NVIDIA's diagnostic and monitoring suite. Way more thorough than nvidia-smi for real diagnostics:

```bash
# run the diagnostic suite
sudo dcgmi diag -r 3              # level 3 = full diagnostic (takes ~15 min)
```

DCGM levels:

- Level 1: Quick health check (~1 min)
- Level 2: Hardware diagnostics (~2 min)
- Level 3: Full stress test (~12 min)
- Level 4: Extended stress test (~30+ min)

## GPU Stress Testing

When you need to stress-test GPUs, use **DCGM diagnostics** -- either through the node toolkit or directly.

**Preferred method -- Node Toolkit (handles everything):**

```bash
./scripts/sshv/start-node-toolkit.sh
# → Main Menu option 14 (Log Collection) → option 11 (Run DCGMI Diagnostics)
```

The toolkit installs DCGM if missing, kills GPU processes, stops conflicting services, runs the test in a screen session (so you can disconnect), and collects the results. The toolkit stops GPU-related services (like kubernetes, containerd, docker, and any gpu-operator services) before running DCGM, and restarts them after. Results are saved to the current directory as dcgm_stress.log. Supports L1 through L4:

| Level | Time | What It Does |
|-------|------|-------------|
| L1 | ~1 min | Quick health check |
| L2 | ~2 min | Hardware diagnostics |
| L3 | ~12 min | Full stress test |
| L4 | ~30+ min | Extended stress test |

**Manual method (if you're already on the node):**

Know the raw commands so you understand what the toolkit is doing under the hood.

**Step 1 -- Install DCGM if it's not there:**

```bash
# check if dcgmi is available
which dcgmi

# if not, install it (needs NVIDIA keyring + CUDA version detection)
if ! dpkg -l | grep -q cuda-keyring; then
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu$(lsb_release -rs | tr -d '.')/x86_64/cuda-keyring_1.1-1_all.deb
    sudo dpkg -i cuda-keyring_1.1-1_all.deb
    sudo apt-get update
fi

CUDA_VERSION=$(nvidia-smi | sed -E -n 's/.*CUDA Version: ([0-9]+)[.].*/\1/p')
sudo apt-get install -y --allow-change-held-packages datacenter-gpu-manager-4-cuda${CUDA_VERSION}
```

**Step 2 -- Clear GPU processes (DCGM needs exclusive access):**

```bash
# check what's running on the GPUs
nvidia-smi --query-compute-apps=pid,process_name,used_memory --format=csv,noheader

# kill them if needed (careful on customer nodes!)
nvidia-smi --query-compute-apps=pid --format=csv,noheader | xargs -r sudo kill -9
```

**Step 3 -- Run the diagnostic:**

```bash
# quick health check
sudo dcgmi diag -r 1

# full stress test (use screen so you can disconnect)
screen -S dcgm_test
sudo dcgmi diag -r 3 --verbose | tee dcgm_results.log
# Ctrl+A then D to detach, screen -r dcgm_test to reattach
```

**For Dell thermal validation** (full workflow with temp monitoring + TSR), use the thermal diagnostics script instead -- see Module 7.

## What's Next

Two labs to get you comfortable with DCGM:

1. **Manual DCGM Install & L1 Test** - Learn the raw commands for when Node Toolkit isn't available
2. **DCGM via Node Toolkit** - The preferred workflow you'll use day-to-day

Always prefer Node Toolkit when possible -- it handles the install, process cleanup, and result collection automatically.
