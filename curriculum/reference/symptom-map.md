# Symptom-to-Entrypoint Map

Got a ticket and don't know where to start? Find the symptom below.

---

## "GPUs disappeared" / nvidia-smi shows fewer GPUs

**Start here:** [Module 5 - Driver Management](/track/baremetal/module/05-driver-management)

**First moves:**

1. `nvidia-smi` -- how many GPUs show? Any error messages?
2. `sudo lspci | grep -i nvidia` -- does the kernel see the GPUs on the PCIe bus?
3. `sudo dmesg | grep -i "fallen off\|xid 79\|AER"` -- did a GPU fall off the bus?
4. `modinfo nvidia | grep ^version` -- is the driver loaded?
5. `systemctl status nvidia-fabricmanager` -- Fabric Manager running?

**If all 8 show in lspci but not nvidia-smi:** driver issue. Check version mismatch.
**If missing from lspci too:** hardware/PCIe issue. Check iDRAC event log via Redfish.

---

## "Training is slow" / customer complains about performance

**Start here:** [Module 4 - InfiniBand](/track/baremetal/module/04-infiniband) (IB is the most common cause)

**First moves:**

1. `sudo ibstat` -- are all ports Active at expected rate (NDR 400)?
2. `nvidia-smi` -- GPU utilization near 100%? Power draw near 700W?
3. `nvidia-smi nvlink -s` -- any NVLink errors/replays?
4. `sudo dmesg | grep -i "AER\|pci.*error"` -- PCIe degradation?
5. Node Toolkit → NCCL Benchmark -- actual inter-node bandwidth numbers

**If IB ports are down or degraded:** cable or switch issue. Check mlxlink optical power.
**If GPUs show low utilization:** probably a job/framework issue, not hardware.

---

## "XID errors in logs"

**Start here:** [Module 2 - Log Collection](/track/baremetal/module/02-log-collection) (XID reference table)

**First moves:**

1. `sudo dmesg | grep -i xid` -- what XID number? **Check the timestamp!**
2. Is it fresh or stale? Compare timestamp to current time and last boot (`uptime`)
3. Look up the XID in the reference table (Module 2)
4. `nvidia-smi -q -d ECC` -- ECC-related XIDs need error counts
5. `nvidia-smi -q -d RETIRED_PAGES` -- row remapping exhausted?

**Common trap:** Old XIDs from before the last reboot. Always check timestamps first.

---

## "ECC errors on a GPU"

**Start here:** [Module 3 - GPU Diagnostics](/track/baremetal/module/03-gpu-diagnostics)

**First moves:**

1. `./scripts/gpu/check-ecc.sh` -- quick scan across all GPUs
2. `nvidia-smi -q -d ECC` -- correctable vs uncorrectable, which GPU?
3. Is it correctable-only with a small count? Reset and monitor
4. Uncorrectable or recurring correctable on same GPU? Start RMA process
5. `nvidia-smi -q -d RETIRED_PAGES` -- check row remapping

---

## "Node won't boot" / "Can't SSH to server"

**Start here:** [Module 6 - iDRAC & Redfish](/track/baremetal/module/06-idrac-redfish)

**First moves:**

1. Check [VOLT](https://volt.lightning.ai) -- is the node supposed to be up? What DC?
2. `./scripts/api/connect-idrac-via-redfish.sh` -- reach it via iDRAC
3. System Info → check overall health status
4. Power Controls → check power state, try power cycle
5. Check iDRAC event log for hardware failures

**If iDRAC is also unreachable:** physical issue (power, network). Needs datacenter hands.

---

## "InfiniBand port down"

**Start here:** [Module 4 - InfiniBand](/track/baremetal/module/04-infiniband)

**First moves:**

1. `sudo ibstat` -- which port, which HCA?
2. `sudo mlxlink -d mlx5_X -p 1` -- link status details
3. `sudo mlxlink -d mlx5_X -p 1 -m` -- optical module info (power levels, temp)
4. `sudo lspci -vv | grep -i lnk` -- PCIe width degraded (should be x16)?
5. Check if it's just this node or multiple (switch issue vs cable/HCA)

**If optical power is out of spec:** bad cable or transceiver.
**If PCIe width is x8 instead of x16:** reseat the HCA or check the slot.

---

## "Need to run thermal diagnostics" / Dell validation

**Start here:** [Module 7 - Thermal Diagnostics](/track/baremetal/module/07-thermal-diagnostics)

**First moves:**

1. `./scripts/gpu/thermal-diagnostics-2.6.2-vp.sh` -- full Dell thermal validation
2. Or Node Toolkit → option 14 → 11 for quick DCGM stress test
3. Check `thermal_results.*.csv` in results -- all GPUs below 83°C?
4. Compare power draw across GPUs -- outliers indicate issues

---

## "Customer asking for firmware versions"

**Start here:** [Module 6 - iDRAC & Redfish](/track/baremetal/module/06-idrac-redfish)

**First moves:**

1. `./scripts/api/connect-idrac-via-redfish.sh` → GPU Tools menu
2. vBIOS version, GPU firmware inventory
3. System Info → component firmware versions
4. `nvidia-smi -q | grep "VBIOS\|Image"` -- GPU VBIOS from the OS side
