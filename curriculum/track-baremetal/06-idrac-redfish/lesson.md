# iDRAC & Redfish

iDRAC (Integrated Dell Remote Access Controller) is the out-of-band management controller on Dell servers. It lets you manage the server even when the OS is down -- check health, pull logs, update firmware, reset the BMC, all via a web UI or REST API.

## In-Band vs Out-of-Band

- **In-band**: You're logged into the OS via SSH. If the OS hangs, you're stuck.
- **Out-of-band**: iDRAC has its own network interface, its own IP, its own mini-OS. It works even when the main OS is dead.

When a server is completely unresponsive, iDRAC is how you diagnose and recover.

## Finding Node Info

Your first stop is always [VOLT](https://volt.lightning.ai). Search the hostname and you'll see the datacenter, cluster, customer, public IP, private IP, and iDRAC IP all in one row.

You don't need to look up iDRAC IPs separately -- the Redfish script builds the iDRAC address for you.

## Redfish API

Redfish is the REST API that iDRAC exposes. Our script wraps all the common operations into an interactive menu:

```bash
./scripts/api/connect-idrac-via-redfish.sh
```

**How it works:** When you run the script, it asks you to pick a datacenter (SEA1, DFW1, IAD1, etc.) and enter hostnames. It automatically constructs the iDRAC FQDN using the pattern `{hostname}-i.{dc}.voltagepark.net` -- so you never need to manually look up or type iDRAC IPs. Just know the hostname from VOLT and which DC it's in.

You can also enter full IPs or hostnames manually if needed.

**What you can do via the Redfish menu:**

| Option | What It Does |
|--------|-------------|
| **BIOS** | Read/modify BIOS settings, check hyperthreading, boot order |
| **Fan Control** | Check fan profiles, set fan speed overrides |
| **PSU** | Power supply status and redundancy info |
| **Power Controls** | Graceful shutdown, hard reset, power cycle, force off |
| **vBIOS Update** | Check and schedule GPU firmware updates |
| **GPU Tools** | GPU inventory, PCIe slot mapping, firmware versions |
| **System Info & Health** | Overall health, memory, CPU, storage, NIC details |
| **Job Management** | View/clear iDRAC jobs (firmware updates, BIOS changes) |
| **Custom Redfish** | Run raw Redfish API calls for anything the menu doesn't cover |
| **CSV Export** | Bulk export system info across multiple hosts |

## Manual Redfish Calls (curl)

The script wraps these, but understanding the raw API helps when you need something custom.

```bash
# set your iDRAC address and credentials
IDRAC="gpu020001-i.sea1.voltagepark.net"
CREDS="user:password"

# system health overview
curl -sk -u $CREDS https://$IDRAC/redfish/v1/Systems/System.Embedded.1 | python3 -m json.tool

# check power state
curl -sk -u $CREDS https://$IDRAC/redfish/v1/Systems/System.Embedded.1 | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['PowerState'])"

# list all GPUs
curl -sk -u $CREDS https://$IDRAC/redfish/v1/Systems/System.Embedded.1/Processors | python3 -m json.tool

# get BIOS attributes
curl -sk -u $CREDS https://$IDRAC/redfish/v1/Systems/System.Embedded.1/Bios | python3 -m json.tool

# power cycle the server
curl -sk -u $CREDS -X POST https://$IDRAC/redfish/v1/Systems/System.Embedded.1/Actions/ComputerSystem.Reset \
  -H "Content-Type: application/json" \
  -d '{"ResetType": "ForceRestart"}'

# check fan sensors
curl -sk -u $CREDS https://$IDRAC/redfish/v1/Chassis/System.Embedded.1/Sensors | python3 -m json.tool
```

## racadm (In-Band)

When you're already SSH'd into the server, `racadm` talks to iDRAC locally:

```bash
sudo racadm getsysinfo               # system overview
sudo racadm get BIOS.SysInformation   # BIOS info
sudo racadm get iDRAC.Info.Name       # iDRAC hostname
sudo racadm getconfig -g cfgLanNetworking  # iDRAC network config
sudo racadm hwinventory               # full hardware inventory
sudo racadm supportassist collect -t Debug  # trigger a TSR
sudo racadm jobqueue view             # check running jobs
sudo racadm jobqueue delete -i JID_CLEARALL  # clear completed jobs
sudo racadm set iDRAC.Reset.Force 1   # reset the BMC itself
```

## TSR (Tech Support Report)

When Dell support asks for diagnostic data, this is what they want. A TSR is a massive zip file with hardware logs, sensor data, firmware versions, event logs -- everything Dell needs to diagnose hardware issues.

**How to collect a TSR:**

The easiest way is through the **node toolkit** (`start-node-toolkit.sh`). From the main menu, option **14** opens the Log Collection submenu, then option **7** handles the full TSR flow -- triggers via racadm, monitors the iDRAC job, downloads the zip via sshv, and appends a GPU slot report automatically.

```bash
# via the node toolkit (recommended -- handles everything)
./scripts/sshv/start-node-toolkit.sh
# → Main Menu option 14 (Log Collection) → option 7 (Collect Dell TSR Report)
```

The **thermal diagnostics script** also collects a TSR as part of its workflow (Module 7).

If you're already on the node and just need a quick manual trigger:

```bash
sudo racadm supportassist collect -t Debug
sudo racadm jobqueue view   # monitor the job
```

## What's Next

Labs: pull system health via Redfish, check GPU firmware versions, collect a TSR.
