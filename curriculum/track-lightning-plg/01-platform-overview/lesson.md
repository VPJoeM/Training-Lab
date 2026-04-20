# Lightning AI Platform Overview

## What is Lightning AI?

Lightning AI is a cloud platform for building, training, and deploying AI/ML models. Users access GPU-powered development environments called **Studios** — think VS Code in the cloud with access to real hardware.

The platform supports everything from free-tier researchers doing experiments to enterprise customers running production inference at scale.

## Key Concepts

### Account Hierarchy

Understanding how Lightning accounts are structured is critical for support:

```
Organization (Org)
  └── Team Space
       └── Studios
       └── Deployments
       └── Drive (shared storage)
       └── Budget / Credits
```

- **Organization** — Top-level entity. Enterprise customers get their own org. PLG users share the default org.
- **Team Space** — Where work happens. Each team space has its own credit balance, budget settings, and member permissions. A user can belong to multiple team spaces.
- **Studio** — A cloud dev environment. Can run on CPU (free) or GPU (paid). Includes VS Code, terminal, file system, and pre-installed ML frameworks.
- **Drive** — Persistent storage attached to a team space. Data lives here between studio sessions.
- **Deployments** — Production endpoints for serving models.

### Subscription Tiers

| Tier | Cost | What They Get |
|------|------|--------------|
| **Free** | $0 | 15 credits/month (~22 GPU hours), 1 studio at a time |
| **Pro (Monthly)** | Standard pricing | Priority GPU access, more storage, faster startup |
| **Pro (Annual)** | Standard pricing (annual) | Same as Pro Monthly, billed annually |
| **Pro (Academic)** | $9.99/month (annual) | Must use Magic Link auth with university/academic email for this discount |
| **Teams** | $49.99/month (also annual) | Multiple members, shared team space, admin controls |
| **Enterprise** | Custom | Dedicated support, SLAs, custom configs |

See [lightning.ai/pricing](https://lightning.ai/pricing) for current pricing.

**Watch: How to enable academic pricing for a domain** *(this uses ToolJet — covered in detail in [Module 8: ToolJet Guide](/track/lightning-plg/module/08-tooljet-guide))*

https://www.loom.com/share/46855740168c447eb017008efcc7cac8

> **Important:** Credits do not roll over. If a user only uses 4 of their 15 free credits, they'll get 4 back next cycle — not 15. Credits refresh on the 1st of each month.

### How Credits Work

- 1 credit ≈ 1.5 GPU hours (varies by machine type)
- Compute is billed **by the second**
- Running a GPU studio also spins up a monitoring CPU machine at ~$0.43/hr
- Free credits only replenish for the account that spent them — transferring credits to another user's teamspace and having them spend it won't trigger a refill

### Login Methods

Users can sign in via:

- **GitHub** — OAuth
- **Google** — OAuth
- **Magic Link** — Email-based passwordless login

> **Note:** Users can sign in with any method (GitHub, Google, Magic Link) — these no longer block each other. The `auth_provider` field in ToolJet shows which method they originally signed up with.

## Platform Tour

Natalie Rand is preparing a video walkthrough of the Lightning platform. Once available, it will be embedded here.

**In the meantime, go explore:** [lightning.ai](https://lightning.ai)

When you log in, pay attention to:

- Where you land (dashboard vs studio list)
- How to find your **team space** and switch between them
- Where **credits** and **billing** info lives
- How to create a **new studio** and pick a machine type
- The **Drive** — where persistent files are stored

## Support Tools Overview

| Tool | What It Does | Who Has Access |
|------|-------------|---------------|
| **Crisp** | PLG ticket management — emails come in here | Support team |
| **[ToolJet](https://tooljet.lightning.ai/applications/7b6a09f5-f91a-44a2-9e28-803a13eb8bf0)** | User management, phone verification, credit ops, ban management | Support team + admins |
| **Stripe** | Billing, subscriptions, refunds, invoices | Limited (Natalie Rand + finance) |
| **Slack** (`#customer-support-plg`) | Engineering escalation for PLG tickets — you should already be added here | Support + engineering |

## PLG vs Enterprise

This is an important distinction:

- **PLG (Product-Led Growth)** — Self-serve customers. Free tier, Pro, and Teams. Support comes through Crisp (email). This is what we're covering in this track.
- **Enterprise** — Annual contract customers. Support happens on dedicated Slack channels with an on-call engineer rotation. Separate workflow entirely.

We're starting with PLG because that's tier 2 and below — the volume is high and it's a great way to learn the platform.
