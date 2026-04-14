# Crisp Workflow & Ticket Management

## How Tickets Arrive

Users email **support@lightning.ai** and their tickets automatically populate into [Crisp](https://crisp.chat). Tickets route into one of two inboxes:

1. **Paid Sub Users** — Pro tier or Teams tier subscribers. Subscription info shows in the bottom-right corner of the Crisp console when you open the ticket.
2. **Free Users** — Users on the free tier.

> **Always prioritize paid users over free users.** We don't have the bandwidth to immediately address every free-tier request — that's just reality. Paid users are paying us and deserve faster responses.

## Escalation Flow

### The #customer-support-plg Slack Channel

You should already be added to **#customer-support-plg** on Slack — this is where Natalie Rand escalates PLG tickets that need an engineer to take a look. Now that our team is covering PLG support, we use this channel too.

This is **the** channel for anything that can't be solved with ToolJet, Crisp shortcuts, or Stripe alone. If you need an engineer to investigate a studio issue, a weird ban, or a platform bug — post it here.

### What to Include When Escalating

Before posting, add the **"eng help" segment** to the conversation in Crisp — this is how we track how many tickets require engineering. Then include these four things in your Slack post:

1. **Paid user OR Free user** — so engineers know the priority
2. **Username OR user email**
3. **Studio name** (or deployment name if applicable)
4. **Screenshot of the full message**

If the user doesn't initially provide a studio name, ask for it. This saves everyone time.

## Ticket Hygiene

### Resolving Tickets

- **Phone verification / account verification** tickets: Resolve immediately after verifying. Don't wait for the user to respond.
- **Duplicate tickets**: Leave an **internal note** on the duplicate conversation, write **"duplicate"** in the note, then click **Resolve**.

### Creating Shortcuts
If you encounter an issue that doesn't have an existing shortcut (canned response), create one so we can track it.

## Most Used Message Shortcuts

These are the pre-built responses in Crisp. Use them — they're consistent and save time.

| Shortcut | When to Use |
|----------|------------|
| `#phone-verified` | After verifying someone's phone number on ToolJet |
| `#account-verified` | After verifying/unbanning an account |
| `#need-to-verify-identity` | Ban reason says "manually banned before verification" — ask for LinkedIn/Scholar/student ID |
| `#studio-name` | User reports an issue but didn't tell us which studio |
| `#studio-stuck` | Studio is stuck loading or unresponsive |
| `#need-phone-number` | User says they can't verify but didn't give us the number |
| `#need-account-email` | User's email doesn't match what's in ToolJet |
| `#multiple-accounts` | User has multiple accounts — credits are in a different one |
| `#how-do-credits-work` | User confused about credit replenishment rules |
| `#delete-account` | After permanently deleting an account on ToolJet |
| `#suspicious-activity` | Account banned for mining, porn, torrenting |
| `#product-question` | General product questions that don't fit other categories |

## Practical Tips

- **Read the first line.** People write novels but the core question is usually in the opening sentence. Don't waste time reading everything before acting.
- **Check [ToolJet](https://tooljet.lightning.ai/applications/7b6a09f5-f91a-44a2-9e28-803a13eb8bf0) first.** Before responding, look up the user. If they're banned, that's the cause of whatever issue they're reporting — regardless of what the ticket says. First step for any and all problems is checking ban status. Then check account info, credits, multiple accounts.
- **Use shortcuts consistently.** They help us track issue volume and types over time, which feeds back into product improvements.
- **Don't ghost free users forever.** We deprioritize them, sure, but try to get back to them within a couple days. Even a "we're looking into this" is better than silence.
