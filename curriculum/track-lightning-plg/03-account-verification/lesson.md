# Account Verification & Login Issues

## The Verification Process

When a user signs up for Lightning AI, their account goes through an automatic verification process that typically takes **2-3 days**. Some users get verified faster if they use a work or `.edu` email address.

Users reach out about verification issues through multiple channels:

- support@lightning.ai (Crisp)
- Discord
- Twitter / X
- LinkedIn
- [Reddit /r/lightningAI](https://www.reddit.com/r/lightningAI/)

## Phone Verification

This is the **single most common ticket type** we deal with. Here's the process:

### Step by Step on ToolJet

Open [ToolJet](https://tooljet.lightning.ai/applications/7b6a09f5-f91a-44a2-9e28-803a13eb8bf0) and:

1. Navigate to the **Phone Verification** tab
2. Enter the user's email address
3. Enter the phone number — **no spaces or symbols**, just digits
4. Switch to the **Lookup** tab to verify the number hasn't been used for an excessive number of accounts
5. Click **"Verify phone"**
6. Refresh to confirm the verification went through

### Red Flags to Watch For

- **US numbers (+1) that fail verification** — this is when you should Google the number. People using US numbers that fail during phone verification often indicates a fake number. For non-US numbers, you don't need to Google every single one — there are too many of these queries to get hung up on it.
- **Non-US user sending a +1 number?** Almost certainly a temp number. Ask for their real local number.
- **Same number on multiple accounts?** Free credits only go to one account per phone number. This is often intentional abuse.

> **Support code for phone verification: 09332104** — you'll see this in certain system messages.

## Login Issues

### Common Causes

**Support code 03920104** — This means the user has been **shadowbanned**. Steps:

1. Open [ToolJet](https://tooljet.lightning.ai/applications/7b6a09f5-f91a-44a2-9e28-803a13eb8bf0) → **User Management** tab
2. Enter the user's email
3. Check the **ban status** and **ban reason** columns
4. Check for **multiple accounts/IDs** — sometimes a previously-banned account is the issue
5. Check the **auth_provider** field — if they signed up with GitHub, they can't use Google/Magic Link even with the same email

### Ban Reasons You'll See in ToolJet

| Ban Reason | What It Means | Action |
|-----------|--------------|--------|
| "manually banned before verification" | Domain or username flagged in scans | Ask for identity verification (LinkedIn/Scholar/ID), then unban if legit |
| Temp email domain | They used a disposable email | Ask for a real email, or verify identity |
| Completed multiple quests in < 2 min | Automated behavior detection | Verify identity first, then unban if legit |
| Crypto mining / torrenting / inappropriate content | Nefarious activity | **Do not unban.** Use `#suspicious-activity` shortcut |
| Country ban | Sanctioned or high-risk country | See Module 05 for the country lists |
| Complex GuardDuty errors | AWS-level detection of suspicious DNS/activity | Escalate to engineering with the full error |

### University Email Domains

Some university domains don't follow the standard `.edu` format (e.g., `.ac.uk`, `.edu.au`). Our ban rules flag these automatically. **It's completely fine to verify students from any legitimate university** — just Google the domain to confirm it's real.

## Account Deletion

When a user wants their account deleted:

1. **Confirm which account** — they may have multiple
2. **Confirm they want permanent deletion**, not just subscription cancellation
3. **Ask for feedback** — "Is there anything we could improve?"
4. On ToolJet, click **"Permanently delete user"** (top right corner)

> **This is completely irreversible.** Double-check before clicking.
