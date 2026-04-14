# ToolJet Guide

## What is ToolJet?

ToolJet is our internal admin tool for managing Lightning AI user accounts. It's similar to Retool if you've used that before. Think of it as the control panel for everything user-related that Crisp tickets require action on.

**ToolJet URL:** [tooljet.lightning.ai](https://tooljet.lightning.ai/applications/7b6a09f5-f91a-44a2-9e28-803a13eb8bf0)

**Key operations on ToolJet:**

- Phone number verification
- Account verification / unbanning
- Credit management (check, add, subtract)
- User lookup (ban status, auth provider, account details)
- Account deletion
- Monthly free credits check

## Getting Access

ToolJet lives at [tooljet.lightning.ai](https://tooljet.lightning.ai/applications/7b6a09f5-f91a-44a2-9e28-803a13eb8bf0). Access is managed by Natalie Rand — she's an admin and can add team members. If you can't log in, reach out to her directly.

## Main Tabs / Sections

### 1. User Management

This is your primary lookup tool. Enter a user's email to see:

- **Account status** — active, banned, waitlisted
- **Ban reason** — why they were banned (if applicable)
- **Auth provider** — GitHub, Google, or Magic Link
- **GA enabled** — essentially means "verified"
- **Multiple accounts** — users sometimes create several with different emails
- **API key** — used internally (impersonation is restricted to Natalie Rand)
- **Activity log** — recent actions on the account

### 2. Phone Verification

The most-used section. Steps:

1. Enter the user's email
2. Enter phone number (no spaces or symbols, just digits)
3. Use the **Lookup** tab to check if the number has been used on too many accounts
4. Click **"Verify Phone"**
5. Refresh to confirm it went through

> **Always** Google the phone number first to check for temp/VoIP numbers.

### 3. Credit Management

Two main operations:

**Check balance:**

- Enter username or email
- See all teamspaces with their credit amounts

**Modify credits:**

- Click on the specific teamspace
- Scroll down to add/subtract controls
- Enter amount and confirm

**Monthly free credits check:**

- Scroll to the "Monthly Free Credits Check" section
- Enter email
- See `refresh_date` and `free_credits_enabled`

### 4. Account Deletion

- Search for the user
- Click **"Permanently delete user"** in the top right
- **This is irreversible** — confirm with the user first

## Loom Resources

Natalie Rand has recorded walkthroughs for most ToolJet operations. Reference these when you need a visual guide:

| Operation | Loom Link |
|----------|-----------|
| Phone verification | [Watch](https://www.loom.com/share/60cdbe172584497daa111a60ab8ab317) |
| Verify identity (ban reason) | [Watch](https://www.loom.com/share/bf66503cb7904768a0ef0f3ab65154ce) |
| Account with wrong email | [Watch](https://www.loom.com/share/e118b455a7dc4317b407b072f43b980f) |
| Multiple accounts / credits | [Watch](https://www.loom.com/share/618e3941f79c4a61880e68de57a8f648) |
| Delete an account | [Watch](https://www.loom.com/share/55ebe432315648c2beb72a191e5f732d) |
| Suspicious activity review | [Watch](https://www.loom.com/share/53097c3de0684a0da81d8dd6c7566c57) |
| Credit management | [Watch](https://www.loom.com/share/6a237b2cd1b24f8685b581f97438df61) |

## ToolJet vs Other Tools

| Task | Tool |
|------|------|
| User lookup, verification, credits, bans | **ToolJet** |
| Ticket management, customer communication | **Crisp** |
| Subscriptions, refunds, invoices, billing | **Stripe** |
| Engineering escalation | **Slack** (#customer-support-plg) |
| Enterprise customer support | **Slack** (dedicated channels) |

## Tips

- **Always look up the user in ToolJet before responding** in Crisp. Context is everything.
- **Check for multiple accounts.** Users create them and forget. Credits often end up in an account they're not looking at.
- **The Lookup tab is your friend.** Use it to spot phone numbers linked to too many accounts (abuse pattern).
- **When in doubt, check the Loom.** Natalie Rand's walkthroughs cover edge cases that text can't.
