# Infra Ticket Triage

Built from **750+ real Plain tickets**. This module teaches you the CX workflow for each ticket type — what you own, what you diagnose first, and when to escalate.

## The CX Role: You're Not Just Routing

CX doesn't just forward tickets. For most infra tickets, you're the one who:

- **Contacts the customer** to confirm maintenance windows
- **Opens Jira tickets** for DC Ops once the window is confirmed
- **Diagnoses first** using tools like `sshv` before escalating
- **Closes spam** with a note

## Ticket Volume Breakdown

Here's what the queue actually looks like:

| Category | % of Tickets | CX Action |
|----------|-------------|-----------|
| **Automated Alerts (GPU temp)** | ~60% | Contact customer, confirm maintenance window, open Jira for DC Ops |
| **GPU Thermal Throttle (TT)** | ~15% | Contact customer, confirm maintenance window, open Jira for DC Ops |
| **Software/Image Issues** | ~8% | Diagnose first (sshv, check drivers), escalate to infra-ops if needed |
| **Downtime/Maintenance** | ~5% | Coordinate with customer, open Jira for DC Ops |
| **Node Unreachable** | ~4% | Contact customer, coordinate, open Jira for DC Ops |
| **User Management** | ~3% | Handle directly (sshv, key additions) |
| **Billing/Onboarding** | ~3% | Handle directly |
| **Network/IB** | ~2% | Diagnose, escalate with context |

## Workflow by Ticket Type

### GPU Temperature Alerts & Thermal Throttle

These are the bulk of your queue. When you see:

```
ALERT: [idrac-6vb0fz3] [sensor] [System Board GPU22] A GPU is over 81°.
```

or

```
DFW1 - gpu040360 - Northstar AI - GPU26 - TT
```

**Your workflow:**

1. Contact the customer
2. Confirm a maintenance window that works for them
3. Once confirmed, open a Jira ticket for DC Ops with the maintenance window details
4. Update the Plain ticket with the Jira link
5. After GPU replacement: run DCGMI r3+ via node-toolkit to validate the new hardware before returning the node

**Option A — Node Toolkit (preferred):**

```bash
./scripts/sshv/start-node-toolkit.sh
# → Main Menu option 14 (Log Collection) → option 11 (Run DCGMI Diagnostics)
# → Select level 3 or above for post-replacement validation
```

**Option B — One-liner snippet (run directly on the node):**

This installs DCGM if needed, kills GPU processes, stops conflicting services, and runs L4 in a screen session:

```bash
if ! dpkg -l | grep -q cuda-keyring; then echo "NVIDIA keyring not found, installing..." && wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu$(lsb_release -rs | tr -d '.')/x86_64/cuda-keyring_1.1-1_all.deb && sudo dpkg -i cuda-keyring_1.1-1_all.deb && sudo apt-get update && echo "NVIDIA keyring installed"; else echo "NVIDIA keyring already installed"; fi && CUDA_VERSION=$(nvidia-smi | sed -E -n 's/.*CUDA Version: ([0-9]+)[.].*/\1/p') && sudo apt-get install -y --install-recommends screen datacenter-gpu-manager-4-cuda${CUDA_VERSION} && echo "Checking for running processes using GPUs..." && RUNNING_PROCESSES=$(nvidia-smi --query-compute-apps=pid,process_name,used_memory --format=csv,noheader) && if [ -n "$RUNNING_PROCESSES" ]; then echo "Found running GPU processes:" && echo "$RUNNING_PROCESSES" && read -p "Do you want to kill these processes? (y/n) (Answering 'n' will exit the script): " KILL_CHOICE && if [ "$KILL_CHOICE" = "y" ]; then echo "Killing GPU processes..." && nvidia-smi --query-compute-apps=pid --format=csv,noheader | xargs -r kill -9 && echo "GPU processes terminated."; else echo "You chose not to kill GPU processes. Exiting for safety." && exit 1; fi; else echo "No GPU processes found."; fi && echo "Checking service status..." && RUNNING_SERVICES=() && echo "Checking for GPU services..." && for SVC in $(systemctl list-units --type=service --all | grep -E 'gpu' | awk '{print $1}' | sed 's/\.service$//'); do if [[ "$SVC" != fake-* ]]; then if systemctl is-active --quiet $SVC; then echo "$SVC service is running" && RUNNING_SERVICES+=("$SVC"); fi; fi; done && echo "Checking for Kubernetes services..." && for SVC in $(systemctl list-units --type=service --all | grep -E 'kube|containerd|docker' | awk '{print $1}' | sed 's/\.service$//'); do if [[ "$SVC" != fake-* ]]; then if systemctl is-active --quiet $SVC; then echo "$SVC service is running" && RUNNING_SERVICES+=("$SVC"); fi; fi; done && if [ ${#RUNNING_SERVICES[@]} -gt 0 ]; then read -p "Do you want to stop these services? (y/n) (Answering 'n' will exit the script): " STOP_SERVICES && if [ "$STOP_SERVICES" = "y" ]; then for SERVICE in "${RUNNING_SERVICES[@]}"; do echo "Stopping $SERVICE..." && sudo systemctl stop $SERVICE && echo "$SERVICE stopped"; done; else echo "You chose not to stop running services. Exiting for safety." && exit 1; fi; else echo "No relevant services are running."; fi && screen -dmS dcgm_stress_test bash -c 'dcgmi diag -r 4 --verbose | tee dcgm_stress.log; echo -e "\nTest complete. Output saved to dcgm_stress.log. Shell will remain open."; exec bash' && echo "Started DCGM stress test in screen session 'dcgm_stress_test'"
```

The snippet handles everything: DCGM install, CUDA version detection, GPU process cleanup, service stops, and runs L4 in a detached screen session. Results go to `dcgm_stress.log`. Reattach with `screen -r dcgm_stress_test`.

See the [Bare Metal GPU Diagnostics module](../track-baremetal/03-gpu-diagnostics/lesson.md) for the full breakdown of DCGM levels.

This is bread-and-butter CX work. You're the bridge between the customer and DC Ops.

### User Management (SSH Keys, Access, Passwords)

Real examples:

- `Add new SSH public key`
- `SSH Access Suddenly Failing with "Permission Denied (Publickey)"`
- `Node 11 asking password`
- `Add user to cluster`

**Your workflow:**

1. For key additions: add the key using `sshv`
2. For access issues: login with `sshv` to verify the problem first
3. For password issues: check LDAP status
4. Handle directly — no escalation needed

### Software & Driver Issues

Real examples:

- `nvidia-smi fails under srun`
- `NVIDIA runtime not injecting GPUs`
- `NVRM API mismatch`

**Your workflow:**

1. Login with `sshv` to check the node
2. Check drivers (`nvidia-smi`, driver versions)
3. Look for obvious issues you can fix
4. If no issue found on your end, **then** escalate to infra-ops with what you checked

Don't just forward these blind — diagnose first.

### Billing & Onboarding

Real examples:

- `Request for Refund Due to Lack of Available Resources`
- `Change bank details`
- `Invoices`
- `Inquiry About Academic GPU Credits`
- `Need to expand storage`

**Your workflow:** Handle directly. Refund requests, invoice questions, payment method changes, capacity inquiries, storage expansion requests.

### Spam & Solicitations

Real examples:

- `Quick SEO Review for Your Website`
- `85 MW Available for GPU Deployment in Kenya`
- `I Want to post on your website please tell me price`

**Your workflow:** Close with a note. Don't waste time on these.

### Security Reports

Real examples:

- `Critical Security Vulnerabilities Found`
- `Cluster security questions`

**Your workflow:**

1. Take it seriously
2. Don't share internal infrastructure details
3. Escalate immediately to the security team
4. Confirm to the customer that it's been received

### Downtime & Maintenance Coordination

Real examples:

- `Coordinate SEA1 node downtime`
- `Schedule node downtime`
- `Node g0726 ready for maintenance`

**Your workflow:**

1. For customer-requested downtime: confirm details and window
2. For "ready for maintenance" tickets: open Jira for DC Ops
3. Track completion and update the customer

### Node Down / Unreachable

Real examples:

- `VP DGX-52 unreachable`
- `Orion Corp - Five nodes repeatedly down`

**Your workflow:**

1. Contact the customer to let them know you're aware
2. Coordinate with DC Ops
3. Open Jira with node details
4. Keep the customer updated on progress

## Reading Ticket Titles

Most infra tickets follow this format:

```
SITE - HOSTNAME - CUSTOMER - IP - ISSUE
```

Example: `DFW1 - gpu040190 - Acme Labs - 10.0.41.63 - GPU26 - TT`

- **DFW1** — Dallas datacenter, cluster 1
- **gpu040190** — Node hostname
- **Acme Labs** — Customer name
- **10.0.41.63** — Node IP
- **GPU26** — Specific GPU affected
- **TT** — Thermal Throttle

Sites:

| Code | Location |
|------|----------|
| **DFW1** | Dallas, TX (cluster 1) |
| **DFW2** | Dallas, TX (cluster 2) |
| **SEA1** | Seattle, WA |
| **IAD1** | Ashburn, VA |

## Shift Handovers

You'll see tickets like `EMEA->US Handover` and `US->APAC Handover`. The region label just tells you which shift left it — pick up any handover ticket and continue the work regardless of region.

## The Escalation Checklist

When you do escalate, include:

1. **Node** — hostname, IP, site
2. **Timeframe** — when did it start, is it ongoing
3. **Error messages** — exact output, not paraphrased
4. **What you already checked** — sshv login, driver status, etc.
5. **Related tickets** — any other Plain or Jira tickets on the same node
6. **Customer maintenance window** — if already confirmed

The difference between a good CX engineer and a great one is how much useful context you attach when you escalate.
