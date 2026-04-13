# VPOD Admin Interface

The VPOD Admin Interface is your command center for customer account management. When a customer has billing questions, needs a refund, or you need to look up their rental info, this is where you go.

## What is VPOD?

**VPOD = Voltage Park On Demand** — our self-service GPU rental product. Customers use VPOD to:

- Deploy bare metal NVIDIA HGX H100 servers on demand
- Pay-as-you-go with no long-term commitment
- Scale up or down in as little as 15 minutes
- Access their instances via the [customer portal](https://www.voltagepark.com) and [Help Center](https://support.voltagepark.com)

The **VPOD Admin Interface** is the internal tool we use to manage VPOD customer accounts. It's built on the `vpadmin-cli` tool (by Mark Wagner) and gives you access to:

- **User accounts** — look up customers by email, manage roles, verify emails
- **Organizations** — check balances, view transactions, see rental history
- **Transactions** — add credits, process refunds, track billing
- **Baremetal rentals** — see what servers a customer is renting, get IPs/hostnames
- **VM rentals** — virtual machine management

The `start-vpod-admin-interface.sh` script wraps the `vpadmin-cli` tool with a friendly menu interface.

## Customer Perspective

Before diving into the admin tools, understand what customers see:

| Customer Resource | What It Is |
|-------------------|------------|
| [voltagepark.com](https://www.voltagepark.com) | Main site — sign up, deploy GPUs, manage instances |
| [Help Center](https://support.voltagepark.com) | Documentation — Getting Started, Deploy GPUs, Billing, FAQs |
| [Status Page](https://status.voltagepark.com) | Public incident and maintenance status |

**On Demand Features** (what customers expect):

- **No minimums** — rent for as little as you need
- **Fast deployment** — 15 minutes to spin up
- **Bare metal access** — no virtualization, full hardware access
- **Clear pricing** — no hidden egress/ingress fees

When a customer contacts support, they've likely already checked the Help Center. Knowing what's there helps you avoid repeating info they've already read.

## Prerequisites

Before you can use VPOD Admin:

1. **API Access from Mark Wagner** — you need a token, contact Mark to request one
2. **1Password** — credentials are stored in your Employee vault
3. **VPN/Tailscale** — must be connected to reach `vpadmin-api.voltagepark.com`

## First Time Setup

Run the interface script — it will auto-install everything:

```bash
~/Github/Support-Tooling/scripts/api/start-vpod-admin-interface.sh
```

On first run, the script will:

1. Install Go, Git, jq if missing
2. Clone and build `vpadmin-cli` from source
3. Install 1Password CLI if needed
4. Guide you through storing your API token in 1Password

### Manual Setup (Fallback)

If the auto-installer fails, you can build vpadmin-cli manually:

```bash
# install Go if missing
brew install go  # macOS
# or: sudo apt install golang-go  # Linux

# clone and build
git clone git@github.com:voltagepark/vpadmin-api.git ~/Github/vpadmin-api
cd ~/Github/vpadmin-api
go build -o vpadmin-cli .
sudo mv vpadmin-cli /usr/local/bin/

# verify
vpadmin-cli --help
```

### 1Password Credential Setup

Store your credentials in 1Password:

- **Vault**: `Employee`
- **Item Title**: `VPAdminCLI`
- **Fields**:
  - `api_key`: Your API token from Mark
  - `base_url`: `https://vpadmin-api.voltagepark.com`

### Create an Alias

For quick access from anywhere:

```bash
~/Github/Support-Tooling/scripts/api/start-vpod-admin-interface.sh
# Go to: Configuration (2) → Create Shell Alias (8)
# Choose alias name like 'vpod' or 'vpodadmin'
```

Then you can just type `vpod` from any terminal.

## Common Support Tasks

### Looking Up a Customer

When a ticket comes in, you usually have an email address. Here's how to find everything about them:

1. **Get User by Email** — `Admin API → Users → Get User by Email`
   - Enter their email
   - Get their user UUID and org UUID

2. **Get Organization Details** — `Admin API → Organizations → Get Organization by ID`
   - Enter the org UUID from step 1
   - See company name, settings, etc.

3. **Check Balance** — `Admin API → Organizations → Get Balance by Org ID`
   - Shows current credit balance

### Checking a Customer's Servers

1. **Baremetal Rentals** — `Admin API → Organizations → Baremetal Rentals by Org ID`
   - Filter by: All / Active only / Terminated only
   - Shows rental IDs, server details, status

2. **Quick Node Access** — `Admin API → Organizations → Baremetal Nodes by Org ID`
   - Just the IPs and hostnames for quick SSH access
   - Example output:
   ```json
   [
     {"public_ip": "147.185.40.145", "private_ip": "10.15.42.1", "hostname": "g398"}
   ]
   ```

### Processing a Refund / Adding Credit

1. **Create Transaction** — `Admin API → Transactions → Create Transaction`
2. Enter the organization UUID
3. Choose transaction type:
   - **Add Credit** — for refunds, credits, promotional balances
   - **Remove Credit** — for billing corrections
4. Enter the amount (no $ symbol needed)
5. Enter a note (required) — explain why, include ticket number
6. Type `confirm` to execute

Example:
```
Organization UUID: 4f39bb3c-6f32-4bda-9547-a6fa17469934
Transaction Type: 1 (Add Credit)
Amount: 500
Note: Refund for downtime incident INC-12345
Type 'confirm' to proceed: confirm
```

### Finding Organization by Email

New shortcut: `Admin API → Organizations → Get Organization by Email`

- Enter any user's email
- Returns the organization UUID directly

### Terminating a Rental (Emergency Only)

**⚠️ DESTRUCTIVE — Use with caution**

`Admin API → Baremetal → Terminate Rental`

- Requires typing `TERMINATE` exactly
- Server stops immediately
- Data loss risk — no graceful shutdown
- Only use when authorized

## Menu Structure Quick Reference

```
Main Menu
├── Admin API
│   ├── Users — lookup, roles, verification
│   ├── Organizations — balance, rentals, pricing
│   ├── Transactions — credits/debits
│   ├── Locations — datacenters
│   ├── Baremetal — rentals, rates, termination
│   ├── Virtual Machines — VM management
│   ├── SQL Queries — read-only database access
│   └── Run Custom Command — advanced CLI
├── Configuration
│   ├── Run Auto Setup
│   ├── Change 1Password Settings
│   ├── Test Connection
│   ├── Check for Updates
│   └── Create Shell Alias
└── Show Status
```

## Safety Features

All destructive operations require typing `confirm`:

- Creating transactions
- Updating pricing
- Terminating rentals
- Modifying organization data

The interface validates UUIDs and shows warnings before dangerous actions.

## Troubleshooting

### "vpadmin-cli not found"

- Use Configuration → Manual Install/Repair → Install/Update vpadmin-cli
- Restart your terminal to pick up PATH changes

### "403 Forbidden: Insufficient permissions"

- Contact Mark Wagner for elevated access

### Connection timeout

- Check you're connected to Tailscale/VPN
- Use Configuration → Endpoint Health Check

### 1Password CLI issues

- Run `op account add` manually first
- Restart 1Password desktop app if TouchID keeps prompting

## Who to Contact

- **API Access/Permissions**: Mark Wagner
- **Tool Issues**: Joe Mannix
- **Feature Requests**: Mark Wagner (for API), Joe Mannix (for menu interface)

## What's Next

In the hands-on lab, you'll practice:

- Looking up a customer by email
- Checking their balance and rentals
- Creating a test transaction (on a sandbox org if available)
