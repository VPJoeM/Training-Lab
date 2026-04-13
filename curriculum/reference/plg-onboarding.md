# Lightning Platform (PLG) Support Onboarding

**Author:** Joe Mannix (CX Team Lead, EU)
**Last Updated:** April 2026
**Status:** Active

---

## 1. Introduction

This document covers everything a new CX engineer needs to support **PLG (Product-Led Growth) customers** on the Lightning AI platform. PLG customers are self-serve users — Free, Pro, and Teams tier — as opposed to Enterprise customers who are on annual contracts with dedicated Slack channels.

We're taking over tier 2 and below support from Natalie Rand, who has been handling PLG solo. The goal is to reduce her workload, speed up response times, and build team-wide familiarity with the Lightning platform.

> **Important:** Enterprise support is a separate workflow handled through dedicated Slack channels. This document covers PLG only.

---

## 2. Required Access

Before you can handle PLG tickets, you need access to the following tools. Request any missing access through Natalie Rand or your CX lead.

### 2.1 Crisp

- **What:** Ticket management system for PLG customers
- **URL:** [crisp.chat](https://crisp.chat) (ask Natalie Rand for an invite)
- **How tickets arrive:** Users email `support@lightning.ai` → auto-routed into Crisp
- **Two inboxes:**
  - **Paid Sub Users** — Pro or Teams tier (subscription info shows in bottom-right of the console)
  - **Free Users** — Free tier

### 2.2 ToolJet

- **What:** Internal admin tool for user management, verification, credits, and bans
- **URL:** [tooljet.lightning.ai](https://tooljet.lightning.ai/applications/7b6a09f5-f91a-44a2-9e28-803a13eb8bf0)
- **Access:** Natalie Rand is an admin and can add you
- **Similar to:** Retool (if you've used that before)

### 2.3 Stripe (Read-Only Initially)

- **What:** Billing, subscriptions, refunds, and invoices
- **Access:** Limited — Natalie Rand and finance can issue refunds
- **You may need:** Read access to verify transactions and subscription status
- **Login:** Google SSO

### 2.4 Slack Channels

You must be added to:

| Channel | Purpose |
|---------|---------|
| **#customer-support-plg** | Engineering escalation for PLG tickets. This is where you post when a ticket needs an engineer to look at it. |

### 2.5 Lightning AI Account

- **URL:** [lightning.ai](https://lightning.ai)
- Sign up or log in with your Lightning/Voltage Park Google account
- Explore the platform — you should know what users see when they log in

### Access Verification Checklist

- [ ] Crisp account created and can view both inboxes (Paid / Free)
- [ ] ToolJet access granted — can log in at [tooljet.lightning.ai](https://tooljet.lightning.ai/applications/7b6a09f5-f91a-44a2-9e28-803a13eb8bf0)
- [ ] Stripe access confirmed (at minimum read-only)
- [ ] Added to **#customer-support-plg** on Slack
- [ ] Lightning AI account active — can log in and see the dashboard

---

## 3. Platform Overview

### 3.1 Account Hierarchy

Understanding this structure is critical — it comes up in nearly every ticket:

```
Organization (Org)
  └── Team Space
       ├── Studios (cloud dev environments)
       ├── Deployments (production endpoints)
       ├── Drive (persistent storage)
       └── Budget / Credits
```

- **Organization** — Top-level entity. Enterprise gets their own; PLG users share the default.
- **Team Space** — Where work happens. Has its own credit balance and members. Users can belong to multiple team spaces.
- **Studio** — A cloud dev environment (VS Code + terminal + GPU). Can run on CPU (free) or GPU (paid).
- **Drive** — Persistent file storage attached to a team space.

### 3.2 Subscription Tiers

| Tier | Cost | Key Details |
|------|------|------------|
| **Free** | $0 | 15 credits/month (~22 GPU hours), 1 studio at a time |
| **Pro** | $9.99/month | Priority GPU access, more storage, faster startup |
| **Teams** | $49.99/month | Multiple members, shared team space, admin controls |
| **Enterprise** | Custom | Dedicated support, SLAs — handled separately, not in scope here |

### 3.3 How Credits Work

This is the **most common source of confusion** for users. Memorize these rules:

1. Free tier gets **up to 15 credits** per month
2. Credits refresh **every 30 days** from sign-up date (not calendar month)
3. **Only consumed credits are replenished** — use 4, get 4 back (not 15)
4. Credits **do not roll over** or accumulate
5. Compute is billed **by the second**
6. Running a GPU studio also starts a monitoring CPU at **~$0.43/hr**
7. Free credits go to **one account per phone number** only
8. If Account A gives credits to Account B and B spends them, **A's credits won't refresh**

### 3.4 Login Methods

| Method | Notes |
|--------|-------|
| GitHub OAuth | Most common |
| Google OAuth | Second most common |
| Magic Link | Email-based, passwordless |

> **Critical gotcha:** If a user signs up with GitHub, they **cannot** log in with Google or Magic Link — even if the email is the same. The `auth_provider` field in ToolJet tells you which method they used.

### Platform Verification Checklist

- [ ] Can explain the account hierarchy (Org → Team Space → Studio)
- [ ] Knows all four tiers and their costs
- [ ] Can explain the credit refresh rule correctly
- [ ] Understands the login method lock-in

---

## 4. Crisp Workflow

### 4.1 Ticket Priority

**Always prioritize paid users over free users.** Paid users are in the "Paid Sub Users" inbox; free users are in the "Free Users" inbox.

Free user tickets can wait — we don't have the bandwidth to answer every one immediately. But try not to leave them hanging for more than a couple of days.

### 4.2 Responding to Tickets

1. **Look up the user in ToolJet first.** Check ban status, account info, credits. Context shapes your response.
2. **Use the correct shortcut (canned response).** These are pre-built in Crisp under Settings → Inbox Settings → Message Shortcuts.
3. **If no shortcut exists for the issue, create one.** This helps us track issue types over time.

### 4.3 Most Used Shortcuts

| Shortcut | When to Use |
|----------|------------|
| `#phone-verified` | After verifying phone number on ToolJet |
| `#account-verified` | After verifying/unbanning an account |
| `#need-to-verify-identity` | Ban says "manually banned before verification" — ask for LinkedIn/Scholar/student ID |
| `#studio-name` | User reports issue but didn't say which studio |
| `#studio-stuck` | Studio is stuck loading |
| `#need-phone-number` | User says phone verification failed but didn't provide the number |
| `#need-account-email` | User's email doesn't match ToolJet records |
| `#multiple-accounts` | Credits are in a different account |
| `#how-do-credits-work` | User confused about credit refresh rules |
| `#delete-account` | After permanently deleting on ToolJet |
| `#suspicious-activity` | Banned for mining/porn/torrenting — do not unban |
| `#product-question` | General product questions |

### 4.4 Escalation to Engineering

Post to **#customer-support-plg** on Slack with:

1. **Paid user OR Free user**
2. **Username OR email**
3. **Studio name** (or deployment name)
4. **Screenshot of the full message**

### 4.5 Duplicate Tickets

Users often submit multiple tickets about the same issue. Consolidate and close duplicates.

### Crisp Verification Checklist

- [ ] Can navigate both Crisp inboxes
- [ ] Knows where to find message shortcuts
- [ ] Can apply the correct shortcut for a given scenario
- [ ] Knows what to include in an engineering escalation

---

## 5. ToolJet Operations

ToolJet is the admin control panel. You will use it daily.

### 5.1 User Management (Lookup)

Enter a user's email to see:

- Account status (active / banned / waitlisted)
- Ban reason (if applicable)
- Auth provider (GitHub / Google / Magic Link)
- GA enabled (= verified)
- Multiple accounts
- API key (needed for impersonation)

### 5.2 Phone Verification

**This is the #1 most common operation.** Steps:

1. Enter user's email
2. Enter phone number — **digits only, no spaces or symbols**
3. Switch to **Lookup** tab — check the number isn't on too many accounts
4. Click **"Verify Phone"**
5. Refresh to confirm

> **Always Google the phone number first.** If it's a VoIP/temp number, ask for a real one. Non-US users sending +1 numbers are almost certainly using fake numbers.

**Loom:** [Phone verification walkthrough](https://www.loom.com/share/60cdbe172584497daa111a60ab8ab317)

### 5.3 Credit Management

**Check balance:**

- Enter username/email → see teamspaces with credit amounts

**Add/subtract credits:**

- Click on the specific teamspace → scroll down → enter amount

**Check free credits status:**

- Scroll to "Monthly Free Credits Check" → enter email → see `refresh_date` and `free_credits_enabled`

**Loom:** [Credit management walkthrough](https://www.loom.com/share/6a237b2cd1b24f8685b581f97438df61)

### 5.4 Account Deletion

1. Confirm **which** account (they may have multiple)
2. Confirm they want **permanent deletion**, not just subscription cancellation
3. Ask for feedback
4. Click **"Permanently delete user"** (top right)

> **This is irreversible.** Double-check before clicking.

**Loom:** [Account deletion walkthrough](https://www.loom.com/share/55ebe432315648c2beb72a191e5f732d)

### ToolJet Verification Checklist

- [ ] Can look up a user by email and read their account status
- [ ] Can perform phone verification end-to-end
- [ ] Can check and modify credit balances
- [ ] Knows where the Lookup tab is and why it matters
- [ ] Understands account deletion is irreversible

---

## 6. Handling Banned Users

### 6.1 Soft Bans (Can Be Reversed)

| Ban Reason | Action |
|-----------|--------|
| "manually banned before verification" | Ask for LinkedIn/Scholar/Student ID → if legit, unban |
| Temp email domain | Ask for real email or verify identity |
| Completed quests too fast (< 2 min) | Verify identity → unban if legit |
| Soft-blocked country | Verify identity → unban |

### 6.2 Hard Bans (Do NOT Reverse)

| Ban Reason | Action |
|-----------|--------|
| Crypto mining | `#suspicious-activity` — offer data deletion only |
| Pornography | `#suspicious-activity` — no unban |
| Torrenting | `#suspicious-activity` — no unban |
| Sanctioned country (hard block) | Cannot unban — legal restriction |

### 6.3 Country Restrictions

**Hard Block (cannot unban):**
Belarus, Cuba, Iran, North Korea, Russia, Syria, Venezuela, Crimea & Donbas regions, Bangladesh, Sri Lanka, Oman, Indonesia

**Soft Block (verify identity then allow):**
Vietnam, Philippines, India, Singapore, Korea, Egypt, Pakistan

### 6.4 False Positive Waves

If you notice a cluster of bans for the same reason in a short period, flag it in #customer-support-plg. It may be an automation error. Natalie Rand has seen this happen — engineering fixed it and mass-unbanned affected users.

### 6.5 Complex GuardDuty Errors

If the ban reason contains AWS GuardDuty output (DNS requests, detector IDs, etc.), **do not interpret it yourself.** Escalate the full error to engineering.

### Ban Handling Verification Checklist

- [ ] Can distinguish soft bans from hard bans
- [ ] Knows which countries are hard-blocked vs soft-blocked
- [ ] Knows never to unban crypto miners / torrenting / inappropriate content
- [ ] Knows to escalate complex GuardDuty errors

---

## 7. Billing & Subscriptions (Stripe)

### 7.1 Common Operations

| Operation | Steps |
|----------|-------|
| **Send receipt** | Stripe → Payments → search by email → Receipt History → Send Receipt |
| **Create invoice** | Stripe → More → Invoices → create → **mark as "paid" after** |
| **Refund** | User must have 50 credits in teamspace. Stripe refund + ToolJet credit subtraction |
| **Cancel subscription** | Stripe → Subscriptions → search → Cancel Subscription |
| **Update billing email** | Stripe → Customers → Details → edit. **Also update in HubSpot** |
| **Update credit card** | Phone call with customer → set new card as default → update subscription payment method |

### 7.2 Self-Serve Subscription Management

Users can manage their own subscription. Share this Loom if they need help:
[How to manage your subscription](https://www.loom.com/share/6934d653f0fd47dfb4ab729fe7c891ef)

### 7.3 Who Can Issue Refunds?

Only Natalie Rand and select finance team members. Route refund requests through her until you have full Stripe access.

---

## 8. Common L1 Issues & Responses

### 8.1 Studios Not Starting / Stuck

- Ask: one studio or all? What's the studio name? What machine type?
- **Free studio with 300GB+ data** → switch to data prep machine
- **Random error** → escalate to engineering (flag Neil / Ethan)

### 8.2 Credits Draining Fast

- Check for **idle studios still running**
- Check the **monitoring CPU** cost (~$0.43/hr)
- Check **machine type** — GPU costs vary significantly
- Point to [compute costs](https://lightning.ai/pricing#compute)

### 8.3 "Where Are My Credits?"

- Check for **multiple accounts** — credits may be in another one
- Check **which teamspace** has the credits — users often look in the wrong one
- Check phone number isn't shared across accounts

### 8.4 CUDA Installation Issues

Docs: [Environments — Lightning AI](https://lightning.ai/docs/overview/studios/environments#drivers-and-cuda-versions)

```bash
# general install
sudo apt-get -y install cudnn

# specific version
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt-get update
sudo apt-get install libcudnn8=8.9.7.29-1+cuda11.8
```

### 8.5 Account Impersonation

When you need to see what a user sees, use the impersonation tool in Support-Tooling:

```bash
# interactive menu
~/Github/Support-Tooling/scripts/plg/lightning-impersonate.sh

# CLI mode — generate snippet, copy to clipboard, open browser
~/Github/Support-Tooling/scripts/plg/lightning-impersonate.sh --user <username> --key <api_key> --copy --open
```

You'll need the username and API key from [ToolJet](https://tooljet.lightning.ai/applications/7b6a09f5-f91a-44a2-9e28-803a13eb8bf0) → User Management. Enter them into the tool and it generates the JavaScript, copies it to your clipboard, and opens lightning.ai.

> **Set up the alias:** Run the script, choose option 6, and you can just type `impersonate` from anywhere.

**Manual method:** If you prefer, paste this into the browser console on lightning.ai:

```javascript
localStorage.setItem("gridUserId", "<username>");
localStorage.setItem("gridUserKey", "<api_key from ToolJet>");
localStorage.setItem("gridUserToken", "<token>");
```

Then open lightning.ai in a new tab. **All changes are real.** Sign out when done.

**Loom:** [Impersonation demo](https://www.loom.com/share/87a32198121a4a149110e50bf1d5173b)

### 8.6 Whitelisted IPs

Lightning **does not provide static IPs.** Each studio gets a new IP on every start. Users can check their current IP with `curl https://ipinfo.io/ip` but it will change on restart.

### 8.7 Killing High-Memory Processes

```bash
ps aux --sort=-%mem
sudo kill <PID>
```

### 8.8 Data Recovery (L2 — Needs Engineering)

Only pursue if the user has paid at least $100 (check Stripe). Otherwise, guide them to create a new account and duplicate studios.

**Loom:** [Data recovery walkthrough](https://www.loom.com/share/74641ae78d324ae1968c1ebb44e2e999)

---

## 9. Loom Reference Library

Natalie Rand has recorded walkthroughs for most operations. Bookmark these:

| Operation | Link |
|----------|------|
| Phone verification | [Watch](https://www.loom.com/share/60cdbe172584497daa111a60ab8ab317) |
| Identity verification (ban review) | [Watch](https://www.loom.com/share/bf66503cb7904768a0ef0f3ab65154ce) |
| Email not found in ToolJet | [Watch](https://www.loom.com/share/e118b455a7dc4317b407b072f43b980f) |
| Multiple accounts / credits | [Watch](https://www.loom.com/share/618e3941f79c4a61880e68de57a8f648) |
| Account deletion | [Watch](https://www.loom.com/share/55ebe432315648c2beb72a191e5f732d) |
| Suspicious activity review | [Watch](https://www.loom.com/share/53097c3de0684a0da81d8dd6c7566c57) |
| Credit management | [Watch](https://www.loom.com/share/6a237b2cd1b24f8685b581f97438df61) |
| Crisp shortcut creation | [Watch](https://www.loom.com/share/1907c8ae2ed4467f93cf66808295962d) |
| Duplicate tickets handling | [Watch](https://www.loom.com/share/3703e62c697a42399dac44ce2176906e) |
| Subscription management | [Watch](https://www.loom.com/share/6934d653f0fd47dfb4ab729fe7c891ef) |
| Self-serve cancellation | [Watch](https://www.loom.com/share/30258dc9bd3f47d8bbfb12c7f4e2f7fd) |
| Send receipt (Stripe) | [Watch](https://www.loom.com/share/a36b9f42e3954f6f98cd4677950761d2) |
| Create invoice (Stripe) | [Watch](https://www.loom.com/share/14792dfa491e49c6b98c1767009beb9f) |
| Mark invoice paid (Stripe) | [Watch](https://www.loom.com/share/f2fafb58e88f403dac675d3387ae7533) |
| Update credit card (Stripe) | [Watch](https://www.loom.com/share/ab792169cf8940b2867777d819226fa3) |
| Data recovery (L2) | [Watch](https://www.loom.com/share/74641ae78d324ae1968c1ebb44e2e999) |
| Impersonate account | [Watch](https://www.loom.com/share/87a32198121a4a149110e50bf1d5173b) |
| Custom domain setup | [Watch](https://www.loom.com/share/890e614759d24bdd8c566572cf2d3578) |
| Marimo in Studio | [Watch](https://www.loom.com/share/3a827fbc026149708660ee12f3f71a8e) |

---

## 10. Interactive Training Lab

In addition to this document, there is an interactive training module covering PLG support with hands-on quizzes. Run the Training Lab locally:

```bash
git clone git@github.com:voltagepark/Training-Lab.git
cd Training-Lab && ./start.sh
```

Navigate to **Lightning Platform (PLG)** from the track selector. The 8 modules cover everything in this document with multiple-choice knowledge checks.

---

## 11. Key Contacts

| Person | Role | When to Contact |
|--------|------|----------------|
| **Natalie Rand** | PLG Support Lead | ToolJet/Crisp access, Stripe refunds, tricky ban decisions |
| **Neil** | Engineering Lead | L2 escalations, platform bugs, policy questions |
| **Ethan** | Engineering | Studio issues, ban automation, platform bugs |
| **Joe Mannix** | CX Team Lead (EU) | Training questions, process, tooling |

---

## 12. PLG Onboarding Verification Checklist

Before handling live PLG tickets, confirm all of the following:

### Access & Tools

- [ ] Crisp account active — can view Paid and Free inboxes
- [ ] ToolJet access — can log in to [tooljet.lightning.ai](https://tooljet.lightning.ai/applications/7b6a09f5-f91a-44a2-9e28-803a13eb8bf0) and look up users
- [ ] Stripe access (at minimum read-only)
- [ ] Added to #customer-support-plg on Slack
- [ ] Lightning AI account — can log in to the platform

### Platform Knowledge

- [ ] Can explain the account hierarchy (Org → Team Space → Studio → Drive)
- [ ] Knows all four subscription tiers and costs
- [ ] Can explain the credit refresh rules accurately
- [ ] Understands the login method lock-in (GitHub ≠ Google)

### Ticket Handling

- [ ] Can navigate Crisp and apply shortcuts
- [ ] Can perform phone verification on ToolJet
- [ ] Can check and modify credit balances
- [ ] Can identify soft bans vs hard bans
- [ ] Knows the hard-blocked and soft-blocked country lists
- [ ] Knows how to escalate to engineering with the correct info

### Completed Training

- [ ] Read this document end-to-end
- [ ] Completed the PLG track in the Training Lab (all quizzes passed)
- [ ] Watched at least the phone verification, credit management, and impersonation Looms
- [ ] Shadowed a live Crisp session (if available)

### Manager Sign-Off

| Item | Verified By | Date |
|------|------------|------|
| Tool Access | | |
| Platform Knowledge | | |
| Ticket Handling | | |
| Training Completed | | |
