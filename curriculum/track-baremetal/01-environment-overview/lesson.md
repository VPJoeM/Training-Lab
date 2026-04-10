# Environment Overview

Welcome to GPU support. Before you touch anything, you need to understand what you're looking at.

## What We Support

Our bare metal GPU servers typically look like this:

- **8x NVIDIA H100 SXM GPUs** connected via NVLink/NVSwitch
- **InfiniBand HCAs** (usually ConnectX-7) for inter-node networking
- **Dell PowerEdge** chassis with iDRAC for out-of-band management
- **Ubuntu 22.04** with NVIDIA drivers, CUDA toolkit, Fabric Manager, NCCL

The GPU interconnect topology matters. NVLink connects GPUs within a node (crazy fast), InfiniBand connects nodes to each other (also fast, but not NVLink fast). When customers complain about "slow training," understanding this topology is step one.

## Server Anatomy

```
┌─────────────────────────────────────────────────────┐
│  Dell PowerEdge (iDRAC for remote management)       │
│                                                     │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐  │
│  │ H100 #0 │ │ H100 #1 │ │ H100 #2 │ │ H100 #3 │  │
│  └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘  │
│       └──────┬─────┴──────┬────┘           │       │
│              │ NVSwitch    │               │       │
│       ┌──────┴─────┬──────┴────┐           │       │
│  ┌────┴────┐ ┌─────┴───┐ ┌────┴────┐ ┌────┴────┐  │
│  │ H100 #4 │ │ H100 #5 │ │ H100 #6 │ │ H100 #7 │  │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘  │
│                                                     │
│  ┌──────────────┐  ┌──────────────┐                │
│  │ IB HCA (mlx5)│  │ IB HCA (mlx5)│   ← ConnectX-7│
│  └──────────────┘  └──────────────┘                │
└─────────────────────────────────────────────────────┘
```

## Finding Node Information -- VOLT

When a ticket comes in, your first stop is [VOLT](https://volt.lightning.ai) -- the infrastructure dashboard. This is the single source of truth for everything about our fleet.

**What you'll find on a node's row in VOLT:**

| Field | What It Tells You |
|-------|-------------------|
| **DC** | Which datacenter the server lives in (SEA1, DFW1, IAD1, etc.) |
| **Cluster** | The cluster group it belongs to (C1, C2, etc.) -- nodes in the same cluster work together |
| **Hostname** | The server's hostname (e.g., `gpu020001`) -- this is usually what shows up in tickets |
| **Customer** | Who's using this node -- tells you if it's customer-facing or internal |
| **End Date** | When the customer contract expires -- important for planning maintenance windows |
| **GPU** | GPU type and count -- confirms what hardware you're working with |
| **Public IP** | The public-facing IP address -- what you'll SSH into |
| **Private IP** | The internal network IP -- used for inter-node communication and IB traffic |
| **iDRAC** | The out-of-band management IP -- this is how you reach the server when the OS is down |

**Pro tip:** Bookmark VOLT. You'll have it open constantly. When someone says "gpu020042 is having issues," you open VOLT, search the hostname, and immediately know the DC, cluster, customer, and IPs.

For iDRAC/Redfish work, you don't even need the iDRAC IP -- our Redfish script builds the iDRAC address automatically from the hostname and datacenter (e.g., `gpu020042-i.sea1.voltagepark.net`). You just need to know the hostname and which DC it's in, both of which are right there in VOLT.

## How We Connect

**SSH access** goes through `sshv` -- our SSH wrapper that handles Vault authentication and key management. You'll use it constantly:

```bash
sshv -p 4747 vpsupport@<server-ip>
```

The `<server-ip>` comes from VOLT's Public IP column. Your SSH keys live in 1Password and get served through the SSH agent -- you set this up during the Training Lab setup wizard.

## The Support-Tooling Repo

Everything we build and maintain lives in the `Support-Tooling` repo. The scripts are organized by domain:

```
scripts/
├── api/          # iDRAC/Redfish API scripts
├── basic/        # Utility scripts (LVM setup, alias creation)
├── gpu/          # GPU diagnostics, drivers, thermal, DCGM
├── infiniband/   # IB health checks, toolkit, PCIe
├── reports/      # TSR collection, SOS reports, refund calculator
└── sshv/         # SSH portal, node toolkit
```

You'll learn each directory's scripts as we go through the modules. The key thing now: **these scripts are your primary tools**. Learn them, trust them, improve them.

## Key Concepts

| Term | What It Means |
|------|---------------|
| XID Error | GPU error code from NVIDIA driver -- shows up in dmesg/syslog |
| ECC | Error-Correcting Code memory -- tracks single-bit and double-bit errors |
| DCGM | NVIDIA Data Center GPU Manager -- diagnostics and monitoring |
| Fabric Manager | Manages NVLink/NVSwitch topology |
| iDRAC | Dell's out-of-band management controller (like IPMI on steroids) |
| Redfish | REST API for server management (iDRAC speaks it) |
| TSR | Tech Support Report -- Dell's diagnostic bundle from iDRAC |
| HCA | Host Channel Adapter -- the InfiniBand network card |

## What's Next

The rest of this track walks you through each piece of the stack with real hands-on labs. You'll collect logs, diagnose GPU errors, troubleshoot InfiniBand, manage drivers, talk to iDRAC, and run thermal diagnostics -- all on real hardware.

Let's go.
