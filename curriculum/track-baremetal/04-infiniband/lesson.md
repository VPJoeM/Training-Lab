# InfiniBand Troubleshooting

InfiniBand is how GPU nodes talk to each other for distributed training. When IB is down or degraded, training jobs either fail or crawl. This module teaches you to diagnose it.

## IB Fundamentals

Each server has InfiniBand HCAs (Host Channel Adapters) -- usually Mellanox/NVIDIA ConnectX-7. Each HCA has one or more ports. The ports connect to IB switches via fiber cables.

Key terms:
- **HCA**: The InfiniBand network card
- **Port**: Physical connection point on the HCA
- **Link Layer**: InfiniBand (not Ethernet)
- **Rate**: HDR = 200 Gb/s, NDR = 400 Gb/s
- **Port State**: Active (good), Down (bad), Init (coming up)
- **Physical State**: LinkUp, Polling, Disabled

## Reading ibstat

```bash
sudo ibstat
```

This shows you every IB port on the system. What to look for:

```
CA 'mlx5_0'
    Port 1:
        State: Active          ← this is what you want
        Physical state: LinkUp
        Rate: 400              ← NDR speed
```

If State is **Down** or Rate is lower than expected, something's wrong -- could be a bad cable, switch port, or HCA.

## Our IB Scripts

```bash
# interactive toolkit -- ibstat, error counters, mlxlink, cable checks
./scripts/infiniband/start-ib-toolkit.sh

# clean formatted ibstat summary for the current node
./scripts/infiniband/get-ib-stat-summary.sh
```

For fleet-wide IB checks across multiple nodes, use `start-node-toolkit.sh` from the sshv scripts -- it can target multiple hosts and run any of these on them in parallel.

## Manual IB Diagnostics

The scripts wrap these, but you should know the raw commands.

```bash
# list all IB devices on the system
sudo ibstat -l

# full status of all ports
sudo ibstat

# check a specific device
sudo ibstat mlx5_0

# show IB link status (alternative view)
sudo ibstatus

# check what's connected to the IB fabric
sudo ibhosts          # list hosts on the subnet
sudo ibswitches       # list switches
sudo iblinkinfo       # full link map

# check for errors on a specific port
sudo perfquery -x mlx5_0 1

# reset error counters (after investigating)
sudo perfquery -R mlx5_0 1

# check PCIe link width manually (should be x16)
sudo lspci -vv -s $(lspci | grep Mellanox | head -1 | awk '{print $1}') | grep -i "lnk"
```

## MLX Diagnostics

For deeper cable/transceiver diagnostics:

```bash
sudo mlxlink -d mlx5_0 -p 1       # link status for port 1
sudo mlxlink -d mlx5_0 -p 1 -m    # optical module info (power levels, temp)
sudo mlxlink -d mlx5_0 -p 1 -e    # error counters
```

**Optical power** is crucial -- if TX/RX power is out of spec, the cable or transceiver is bad. Compare values against the module's datasheet thresholds.

## What's Next

Labs: find a down IB port, diagnose degraded link speed, check PCIe width for HCAs.
