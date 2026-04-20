# Healthy vs Broken Sample Outputs

Know what "normal" looks like so you can spot abnormal instantly. These are real outputs from H100 nodes.

---

## nvidia-smi

### Healthy Output

```
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 560.35.03              Driver Version: 560.35.03      CUDA Version: 12.6     |
|-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|=========================================+========================+======================|
|   0  NVIDIA H100 80GB HBM3          On | 00000000:18:00.0   Off |                    0 |
| N/A   31C    P0              72W / 700W |       0MiB / 81559MiB |      0%      Default |
+-----------------------------------------+------------------------+----------------------+
|   1  NVIDIA H100 80GB HBM3          On | 00000000:2A:00.0   Off |                    0 |
| N/A   29C    P0              71W / 700W |       0MiB / 81559MiB |      0%      Default |
+-----------------------------------------+------------------------+----------------------+
|   2  NVIDIA H100 80GB HBM3          On | 00000000:3A:00.0   Off |                    0 |
| N/A   30C    P0              70W / 700W |       0MiB / 81559MiB |      0%      Default |
+-----------------------------------------+------------------------+----------------------+
|   3  NVIDIA H100 80GB HBM3          On | 00000000:5D:00.0   Off |                    0 |
| N/A   30C    P0              72W / 700W |       0MiB / 81559MiB |      0%      Default |
+-----------------------------------------+------------------------+----------------------+
|   4  NVIDIA H100 80GB HBM3          On | 00000000:9A:00.0   Off |                    0 |
| N/A   32C    P0              71W / 700W |       0MiB / 81559MiB |      0%      Default |
+-----------------------------------------+------------------------+----------------------+
|   5  NVIDIA H100 80GB HBM3          On | 00000000:AB:00.0   Off |                    0 |
| N/A   31C    P0              73W / 700W |       0MiB / 81559MiB |      0%      Default |
+-----------------------------------------+------------------------+----------------------+
|   6  NVIDIA H100 80GB HBM3          On | 00000000:BA:00.0   Off |                    0 |
| N/A   29C    P0              70W / 700W |       0MiB / 81559MiB |      0%      Default |
+-----------------------------------------+------------------------+----------------------+
|   7  NVIDIA H100 80GB HBM3          On | 00000000:DB:00.0   Off |                    0 |
| N/A   30C    P0              71W / 700W |       0MiB / 81559MiB |      0%      Default |
+-----------------------------------------+------------------------+----------------------+

+-----------------------------------------------------------------------------------------+
| Processes:                                                                              |
|  GPU   GI   CI        PID   Type   Process name                              GPU Memory |
|        ID   ID                                                               Usage      |
|=========================================================================================|
|  No running processes found                                                             |
+-----------------------------------------------------------------------------------------+
```

**What to look for:**
- All 8 GPUs present (indices 0-7)
- Persistence Mode: **On**
- Volatile Uncorr. ECC: **0**
- Temps under 50C at idle
- Power usage ~70W at idle

---

### Broken: Missing GPUs

```
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 560.35.03              Driver Version: 560.35.03      CUDA Version: 12.6     |
|-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|=========================================+========================+======================|
|   0  NVIDIA H100 80GB HBM3          On | 00000000:18:00.0   Off |                    0 |
| N/A   31C    P0              72W / 700W |       0MiB / 81559MiB |      0%      Default |
+-----------------------------------------+------------------------+----------------------+
```

**What's wrong:** Only 1 GPU visible when there should be 8. Check dmesg for XID 79 ("fallen off the bus") or PCIe errors.

**Next steps:**
1. `sudo dmesg | grep -i "xid\|fallen\|pci.*error"`
2. Check if nvidia driver loaded: `lsmod | grep nvidia`
3. May need power cycle via iDRAC

---

### Broken: ECC Errors

```
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 560.35.03              Driver Version: 560.35.03      CUDA Version: 12.6     |
|-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
|=========================================+========================+======================|
|   0  NVIDIA H100 80GB HBM3          On | 00000000:18:00.0   Off |                   47 |
| N/A   34C    P0              73W / 700W |       0MiB / 81559MiB |      0%      Default |
+-----------------------------------------+------------------------+----------------------+
```

**What's wrong:** `Volatile Uncorr. ECC: 47` -- that's 47 **uncorrectable** memory errors. This GPU likely needs RMA.

**Next steps:**
1. Get full ECC details: `nvidia-smi --query-gpu=index,ecc.errors.corrected.volatile.total,ecc.errors.uncorrected.volatile.total --format=csv`
2. Check row remapping status: `nvidia-smi --query-remapped-rows=gpu_uuid,remapped_rows.correctable,remapped_rows.uncorrectable,remapped_rows.pending,remapped_rows.failure --format=csv`
3. If `remapped_rows.failure` is non-zero → RMA

---

### Broken: Driver Not Loaded

```
NVIDIA-SMI has failed because it couldn't communicate with the NVIDIA driver. Make sure that the latest NVIDIA driver is installed and running.
```

**What's wrong:** Driver crashed or was never loaded.

**Next steps:**
1. Check if driver module exists: `lsmod | grep nvidia`
2. Check dmesg for driver errors: `sudo dmesg | grep -i nvidia | tail -30`
3. May need `sudo modprobe nvidia` or full driver reinstall

---

## dmesg - XID Errors

### Healthy Output (No XIDs)

```
[    0.000000] Linux version 6.5.0-44-generic ...
[    2.345678] nvidia: loading out-of-tree module taints kernel.
[    2.456789] nvidia-nvlink: Nvlink Core is being initialized
[    2.567890] nvidia 0000:18:00.0: enabling device (0000 -> 0003)
[    2.678901] nvidia 0000:2a:00.0: enabling device (0000 -> 0003)
...
[    4.123456] NVRM: loading NVIDIA UNIX x86_64 Kernel Module  560.35.03
```

**What to look for:** GPU devices initializing cleanly with no XID or error messages.

---

### Broken: XID 79 (GPU Fallen Off Bus)

```
[12345.678901] NVRM: Xid (PCI:0000:18:00): 79, pid=1234, GPU has fallen off the bus.
[12345.678902] NVRM: GPU at PCI:0000:18:00.0 has fallen off the bus.
[12345.678903] NVRM: A GPU crash dump has been created.
```

**What's wrong:** XID 79 = GPU lost PCIe communication. Hardware problem.

**Next steps:**
1. Check timestamp -- is this recent or old?
2. Look for PCIe AER errors: `dmesg | grep -i AER`
3. Power cycle the node via iDRAC
4. If recurring after power cycle → check seating, possibly RMA

---

### Broken: XID 48 (Double-bit ECC Error)

```
[67890.123456] NVRM: Xid (PCI:0000:2a:00): 48, pid=5678, name=python
```

**What's wrong:** XID 48 = uncorrectable ECC error. Memory fault.

**Next steps:**
1. Check ECC counters: `nvidia-smi --query-gpu=index,ecc.errors.uncorrected.volatile.total --format=csv`
2. Check row remapping: `nvidia-smi --query-remapped-rows=... --format=csv`
3. Likely RMA candidate

---

## ibstat

### Healthy Output

```
CA 'mlx5_0'
        CA type: MT4129
        Number of ports: 1
        Firmware version: 28.42.1000
        Hardware version: 0
        Node GUID: 0x946dae0300a8xxxx
        System image GUID: 0x946dae0300a8xxxx
        Port 1:
                State: Active
                Physical state: LinkUp
                Rate: 400
                Base lid: 0
                LMC: 0
                SM lid: 0
                Capability mask: 0x00010000
                Port GUID: 0x966dae03ffa8xxxx
                Link layer: InfiniBand
```

**What to look for:**
- State: **Active**
- Physical state: **LinkUp**
- Rate: **400** (for 400Gb NDR IB)

---

### Broken: Port Down

```
CA 'mlx5_0'
        CA type: MT4129
        Number of ports: 1
        Firmware version: 28.42.1000
        Port 1:
                State: Down
                Physical state: Disabled
                Rate: 10
```

**What's wrong:** Port is down. Could be cable, switch, or HCA issue.

**Next steps:**
1. Check link physically: is the cable connected?
2. Check mlxlink for errors: `sudo mlxlink -d mlx5_0 -p 1 -e`
3. Check switch port status
4. Try `sudo ibportstate -D 0 1 reset` (caution: disruptive)

---

### Broken: Link Errors

```
$ sudo mlxlink -d mlx5_0 -p 1 -e

Operational Info
----------------
State                           : Active
Physical state                  : LinkUp
Speed                           : NDR (100 Gb/s)
Width                           : 4x

Error Counters
--------------
Symbol Errors                   : 847293
Link Down Events                : 12
Link Error Recovery             : 45
Phy Receive Errors              : 1847
```

**What's wrong:** High symbol errors (847293) and link recovery events indicate a flaky connection.

**Next steps:**
1. Check/reseat cable at both ends
2. Try different switch port
3. If errors persist → replace cable or HCA

---

## DCGM Diagnostics

### Healthy Output (Level 2)

```
+---------------------------+------------------------------------------------+
| Diagnostic                | Result                                         |
+===========================+================================================+
| Software Deployment       | Pass                                           |
| GPU Memory                | Pass                                           |
| Integration               | Pass                                           |
| Stress                    | Pass                                           |
| Memory Bandwidth          | Pass                                           |
| SM Stress                 | Pass                                           |
| Target FP64 Stress        | Pass                                           |
| PCIe Bandwidth            | Pass                                           |
+---------------------------+------------------------------------------------+

Overall Result: Pass
```

---

### Broken: DCGM Failure

```
+---------------------------+------------------------------------------------+
| Diagnostic                | Result                                         |
+===========================+================================================+
| Software Deployment       | Pass                                           |
| GPU Memory                | FAIL - GPU 3: HBM memory test failed           |
| Integration               | Pass                                           |
| Stress                    | FAIL - GPU 3: Target stress not achieved       |
+---------------------------+------------------------------------------------+

Overall Result: Fail

Warnings/Errors:
- GPU 3 (UUID: GPU-abc123...): Memory diagnostic failed
- GPU 3: Unable to reach target stress level
```

**What's wrong:** GPU 3 is failing memory and stress tests.

**Next steps:**
1. Check ECC errors on GPU 3: `nvidia-smi -i 3 --query-gpu=ecc.errors.uncorrected.volatile.total --format=csv`
2. Check row remapping status
3. This GPU is likely an RMA candidate

---

## Quick Reference: Error → Action

| Signal | Likely Cause | First Command |
|--------|-------------|---------------|
| Missing GPUs | Driver crash, PCIe issue | `sudo dmesg \| grep -i "xid\|fallen"` |
| ECC errors > 0 | Bad GPU memory | `nvidia-smi --query-remapped-rows=...` |
| XID 79 | GPU off bus | Power cycle via iDRAC |
| XID 48/63 | Memory corruption | Check ECC, likely RMA |
| IB port Down | Cable/switch/HCA | `sudo mlxlink -d mlx5_0 -p 1 -e` |
| High symbol errors | Bad cable | Reseat/replace cable |
| DCGM fail | Hardware issue | Check specific GPU's ECC |
