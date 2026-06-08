# Compute Dashboard (Lightning Cloud Nodes)

The compute dashboard is the CX view into every node connected to the global Lightning cluster. When a node has a problem, this is where you take it out of rotation so no new work lands on it — and, once it's clear, hand it off for maintenance.

> **Heads up:** right now CX accounts have **admin** permissions on this dashboard and **nothing is gated**. That means you *can* disrupt live customer work. Act carefully — only touch a node you're actually working a ticket on. Permissions will be tightened later.

## Getting Access

You need a Lightning account on the platform:

1. Create an account on **lightning.ai** with your **@lightning.ai** email address.
2. During the onboarding flow, **join the `lightning-ai` org**.
3. If you already have an account but no org access, ask to be invited to `lightning-ai` (check your email for the invite).

Once you're in, the dashboard lives under **Cloud Accounts → Lightning Cloud → Nodes**.

## Reading the Dashboard

The top of the page summarises the fleet in three buckets:

- **Usage** — nodes currently in use, plus CPU / GPU / RAM utilisation across the cluster
- **Cordoned** — nodes that have scheduling disabled (won't take new work)
- **Unreachable** — nodes the control plane can't reach

Below that is the node list. Each row shows the node name (e.g. `gXXX`), status (running), public IP, hardware (e.g. `8 x H100`), and affinity. We don't have a huge fleet — roughly 36 nodes at the moment.

Click a node to open the **Node details** panel on the right. It shows:

- **Summary** — Node ID, name, hostname, status, public + private IP, hardware, purpose, order, affinity
- Tabs for **GPU Health**, **Memory**, **Storage**, **Servers**, **Warnings**, and **System**

The side panel is still a work in progress, so some of it looks unfinished — that's expected.

## The Node Actions Menu (the hidden 3 dots)

This is the part everyone misses. Node actions live behind a **three-dot menu** that only appears when you **hover over the node's row** — not the node name.

> **Known UI quirk:** the 3 dots only show up when your cursor is over the spot where they should be, on the row itself. If you hover the name, you won't see them. This is a known issue and will be added to the side panel later. For now, hover the row.

## What To Do When a Node Has an Issue

If you find a node with a terminal issue — or any problem reported from your side — the flow is:

1. **Open the 3-dot menu** on that node's row.
2. **Disable scheduling** (cordon it). The node is now marked so **no new resources get scheduled onto it**. Do this **as soon as you get in** on a problem node.
3. **Mark "Require Maintenance"** (when ready). This flags **every resource running on that machine** as requiring maintenance, and that status is **displayed across the entire system** so everyone can see it.
4. **Re-enable scheduling** once the node is healthy again, to return it to the pool.

### Is anything running on it?

Whether you can go straight to maintenance depends on what's on the node:

- **Nothing running** → after disabling scheduling, you can **mark it for maintenance right away** — there's nothing to wait on.
- **Servers/workloads running** → the node has to **wait for those to be flushed out / migrated** before maintenance can proceed. Disable scheduling first so nothing new lands, then let the running work clear.

You can see what's on a node in the **Servers** tab of the node details panel.

> The "Require Maintenance" reporting flow is still being finished. For now, the reliable action is: **disable scheduling on a problem node as soon as you spot it.** More of the maintenance flow is landing over the next few days.

## Baremetal ↔ VM Mode

There's a switch coming to toggle a node between **Baremetal** and **VM** mode directly from the UI. This is **required to run node validation** — you'll flip a node to the right mode before validating it. When it lands, use it as part of the post-maintenance validation step (pair it with DCGMI diagnostics from the triage module before returning a node to a customer).

## Quick Reference

| Situation | Action |
|-----------|--------|
| Node has any issue you've found | Open 3-dot menu → **Disable scheduling** immediately |
| Node cordoned, nothing running | **Mark Require Maintenance** right away |
| Node cordoned, workloads running | Wait for them to flush out, then maintenance |
| Node healthy again | **Re-enable scheduling** |
| Need to validate a node | Switch Baremetal/VM mode (when available) + run DCGMI r3+ |
| Can't find node actions | Hover the **row**, not the name — 3 dots are hidden |
