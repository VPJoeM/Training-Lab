# Infrastructure Fundamentals

This module covers the physical hardware, networking, and software stack that powers everything. Understanding this helps you make sense of the tickets you'll see and the tools you'll use.

## GPU Servers — What's Inside a Node

Our primary server is the **Dell PowerEdge XE9680** — a 4U box that draws 10-14 kW. Here's what's in each one:

| Component | Spec | What It Does |
|-----------|------|-------------|
| **8x H100 SXM5 GPUs** | 80GB HBM3 each, 700W TDP, 989 TFLOPS (BF16) | The AI accelerators doing all the work |
| **NVSwitch** | 900 GB/s bidirectional per GPU | Connects all 8 GPUs via NVLink — they behave as one unit with 640GB shared memory |
| **2x Intel Xeon CPUs** | Host processors | Manage data loading, networking, storage I/O |
| **1-2 TB system RAM** | Server main memory (separate from GPU memory) | Staging data before it hits the GPUs |
| **2x InfiniBand HCAs** | ConnectX-7, 400 Gb/s each | Connect this node to other nodes in the cluster |
| **4-8x NVMe SSDs** | Fast local storage | Temp files, checkpoint staging, data buffers |

Newer builds use the **Dell PowerEdge XE9780** with **8x B200 SXM GPUs**.

**Why NVLink matters:** During training, 8 GPUs constantly share gradient updates. If this went through the CPU (PCIe), it'd be a bottleneck. NVLink bypasses the CPU entirely — 900 GB/s direct GPU-to-GPU. That's why we use SXM form factor instead of cheaper PCIe cards.

**Why this matters for CX:** When a single GPU thermal throttles, it slows down all 8 because NVLink keeps them in sync. One bad GPU = one bad node = customer's training job degrades or crashes.

## Rack Layout

A standard rack is **42U tall** (1U = 1.75 inches). A typical GPU rack:

- 1U management switch
- 1U InfiniBand leaf switch
- 8x 4U GPU nodes = 32U
- 2U for PDUs

Total: ~37U used, 5U for cable management. One rack = **64 GPUs**, **5.12 TB GPU memory**, drawing **80-100 kW**.

For comparison, a normal office server rack draws 5-10 kW. Our racks draw 10-20x more from the same physical footprint. This power density drives every other design decision.

## Power & Cooling

Every watt a chip consumes becomes heat. An H100 at 700W = 700W of heat, constantly. Eight per server = 5,600W of heat from one box.

**Power path:** Grid (115 kV) → Substation (steps down to 480V) → UPS (battery backup, switches in <1ms if grid flickers) → PDUs (rack-level distribution with A-feed and B-feed redundancy)

**UPS (Uninterruptible Power Supply):** A large battery system between the grid and the servers. If power flickers for even 50 milliseconds, GPUs mid-training would crash. The UPS switches to battery in under 1 millisecond — servers never notice. It provides 10-15 minutes of runtime while diesel generators start.

**PDU redundancy:** Each rack has two PDUs (A-feed and B-feed) from separate power circuits. Each server has two power supplies — one per feed. If an entire circuit fails, every server stays up on the other feed. When you see "PSU issues" in tickets, this is why the node usually stays running.

**Cooling:** Most of our facilities use **liquid cooling** — cold plates sitting directly on GPU chips with chilled water flowing through. Water conducts heat ~25x better than air. A CDU (Cooling Distribution Unit) per rack manages flow rate and temperature.

**PUE** (Power Usage Effectiveness) = total facility power / IT equipment power. Perfect = 1.0 (impossible). Every tenth of a point saves millions per year.

**Why this matters for CX:** TT (thermal throttle) tickets are the most common in your queue. They happen when cooling can't keep up — failed fan, blocked airflow, thermal paste degradation, or ambient DC temperature.

## Networking — InfiniBand vs Ethernet

Regular Ethernet (10-25 Gb/s) was designed for web traffic. When 1,024 GPUs need to synchronize gradients thousands of times per second, it's too slow and the software overhead (TCP/IP stack) adds too much latency.

**InfiniBand NDR** runs at **400 Gb/s per port** (50 GB/s per cable). More importantly, it supports **RDMA** (Remote Direct Memory Access) — one GPU can read/write another GPU's memory directly without any CPU involvement. Latency drops from ~100 microseconds (Ethernet/TCP) to **~1-2 microseconds**.

**Network topology — Fat-tree:**

We use a fat-tree — leaf switches (one per rack), aggregation switches, and spine switches at the top. Fat-tree means **non-blocking** — every path between any two servers has equal bandwidth. No single point of congestion.

Any server reaches any other in at most 4 hops: server → leaf → spine → leaf → server.

**NCCL** (NVIDIA Collective Communications Library) handles gradient synchronization during distributed training. It automatically uses NVLink within a node (900 GB/s) and InfiniBand RDMA between nodes (400 Gb/s). When customers report "NCCL errors" — it's usually an InfiniBand or NVLink issue underneath.

**Why this matters for CX:** IB port down tickets, BER (Bit Error Rate) alerts, and NCCL errors in customer jobs all trace back to this layer. When a spine switch has issues, it affects the entire cluster — that's why "cluster-wide IB outage" is a high-severity ticket.

## Storage

**VAST** and **WekaFS** — parallel filesystems accessible from all nodes simultaneously. VAST is the primary shared NFS storage; WekaFS is used at some sites. Training datasets live here.

**Checkpoints:** During training, code periodically saves the entire model state to storage — a checkpoint. For a 70B parameter model, a checkpoint is ~140GB, written every 30 minutes across all nodes. This is massive storage throughput demand.

**Why this matters for CX:** "Slowdown accessing /data/" tickets are storage issues. They can be VAST capacity, network congestion to the storage cluster, or NFS mount configuration problems.

## Data Centers

| Code | Location | Colo Provider |
|------|----------|---------------|
| **SEA1** | Puyallup, WA | Centeris |
| **SEA2** | Quincy, WA | H5 Data Centers |
| **IAD1** | Sterling, VA | CyrusOne |
| **DFW1** | Allen, TX | CenterSquare |
| **DFW2** | Fort Worth, TX | CenterSquare |
| **SLC1/SLC2** | Bluffdale, UT | Lambda/DataBank |
| **ORD1** | Lisle, IL | CenterSquare |

## Software Stack

From bottom to top — each layer builds on the one below:

| Layer | What | Details |
|-------|------|---------|
| **BMC/iDRAC** | Out-of-band management | Tiny computer on the motherboard, always on. Remote power cycle, console, temp monitoring — even when the server is dead |
| **OS** | Ubuntu Linux | Tuned for GPU workloads — huge pages, RDMA kernel modules |
| **NVIDIA Driver** | GPU translator | Without it, the OS sees GPUs as generic PCIe devices. Driver version must match cluster-wide — mismatches cause failures |
| **CUDA Toolkit** | GPU programming platform | cuBLAS (matrix math), cuDNN (neural net ops), NCCL (collective comms) |
| **Containers** | Docker + NVIDIA Container Toolkit | Isolated customer environments — they run in containers, not on bare OS. Containers access GPUs via the toolkit |
| **Slurm** | Job scheduler | Customers submit jobs: "give me 64 nodes for 48 hours." Slurm queues, allocates, runs, reclaims |
| **DCGM** | GPU monitoring | Temps, utilization, XID errors, NVLink health → Prometheus → Grafana dashboards → alerts to on-call |
| **Observium** | Host/device monitoring | Network and server health |
| **MaaS** | Bare-metal provisioning | PXE boot, DHCP, OS deployment (Canonical) |
| **UFM** | InfiniBand fabric management | Manages the entire IB network topology |
| **Rootly** | Incident management | Paging and incident lifecycle |
| **Asset Panda** | Hardware inventory | Track every server, GPU, cable |
| **Metabase** | Usage analytics | Reporting and dashboards |

**Key things CX needs to know from this stack:**

- **iDRAC** — when you see iDRAC alerts in tickets, that's the BMC reporting a hardware problem
- **Driver mismatches** — if nvidia-smi fails, first thing to check is driver version
- **DCGM** — this is what you run via node-toolkit to validate GPUs after replacement
- **XID errors** — NVIDIA fault codes reported by DCGM. XID 79 = GPU fell off bus (hardware). XID 48 = double-bit ECC error (RMA)
- **Slurm** — enterprise customers interact with their allocation through Slurm. "All 16 workers drained" means Slurm removed the node from scheduling
