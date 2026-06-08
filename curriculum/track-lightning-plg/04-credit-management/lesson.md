# Credit Management

## How Credits Work

Credits are the currency of the Lightning AI platform. Here's what you need to know:

### Credit Basics

- **Free tier**: 15 credits per month (~80 GPU hours)
- **Refresh cycle**: On the **1st of each month**
- **Billing granularity**: Compute charged by the second; storage billed by the second once you exceed 10GB ([billing FAQ](https://lightning.ai/docs/overview/faq/billing))

> **Common confusion:** The landing page says "80 GPU hours" and some users think that means 80 credits. It's actually 15 credits = ~80 GPU hours. If a user says "where are my 80 credits?" — explain the difference.

### The Credit Refresh Rule (This Comes Up Constantly)

This is the single most confusing thing for users. Here's how it actually works:

> You get **up to** 15 free credits a month. If you only use 4, we only top up 4. If you use all 15, you get 15 back.

Credits **do not** accumulate. There's no rollover.

### Multi-Account Credit Rules

- Free credits are allocated to **one account per phone number**
- If a user creates 3 accounts with 3 different phone numbers, each gets credits
- **Critical rule**: If Account A transfers credits to Account B's teamspace and Account B spends them, Account A's credits **will not refresh** next cycle (because Account A didn't spend them)

## Checking Credits on ToolJet

### Finding a User's Balance

1. Open [ToolJet](https://tooljet.lightning.ai/applications/7b6a09f5-f91a-44a2-9e28-803a13eb8bf0) → Credit Management section
2. Enter the user's username or email
3. You'll see their **team spaces** listed with credit balances

### Adding or Subtracting Credits

1. Enter username/email
2. Click on the **specific teamspace** you want to modify
3. Scroll down to find the add/subtract controls
4. Enter the amount and confirm

### Checking Monthly Free Credits Status

Scroll down to the **"Monthly Free Credits Check"** section:

- Enter the user's email
- Look at the `refresh_date` and `free_credits_enabled` columns
- This tells you when their next refresh happens and if auto-refresh is active

### Watch: Credit Balances in ToolJet

https://www.loom.com/share/831ab84107f04ac29d5c5f8f2db4d3c3

### Watch: User Wallet vs Teamspace vs Org

https://www.loom.com/share/d8f0e28efaa04b1c97fd641998a9d3cf

### Watch: Multiple Accounts / Which Has Credits

https://www.loom.com/share/618e3941f79c4a61880e68de57a8f648

## Common Credit Scenarios

### "Where are my credits?"

1. Check if they have **multiple accounts** — credits may be in a different one
2. Check which **teamspace** the credits were allocated to — users often look in the wrong one
3. Verify the phone number isn't shared across accounts (credits only go to one)

### "I should have more credits"

1. Explain the refresh rule (only replenishes what was used)
2. Check if someone else spent their credits (transfer scenario above)
3. Point them to the [billing FAQ](https://lightning.ai/docs/overview/faq/billing)

### "My credits are draining too fast" (or "I'm out of credits but I have a Pro sub")

Often this isn't a bug — they've spent the cycle's credits on expensive compute. The top-tier GPUs (e.g. **H200**) burn credits fast: a single H200 running a few hours can eat **tens** of credits.

1. **Pull their actual usage — this is the fastest way to settle it.** Impersonate the account and **download the usage CSV**. It breaks spend down per studio/agent run: machine type, duration, and credit cost. That shows you (and them) exactly where the credits went (e.g. "minor-peach ran ~8h on a 1×H200 ≈ 54 credits").
2. Ask/confirm the **machine type** — GPU machines cost more, H200/top-tier most of all.
3. Check for **idle studios left running** — compute charges even when they're not actively coding, so a GPU left on overnight drains credits.
4. Help them understand [compute costs](https://lightning.ai/pricing#compute) — prices are shown in the machine selection menu.
5. **Tips to make credits last:** use a smaller machine when a full GPU isn't needed, and **stop the studio when idle**.

> **Note on impersonation:** read-only impersonation to *view usage and download the usage CSV* is fine for diagnosis. Impersonation for account access or taking actions on someone's account is restricted — escalate that to Natalie Rand.

> **Customer-facing hygiene:** never mention impersonation, the usage CSV, or ToolJet in the reply. Tell the customer *what* used the credits (e.g. an H200 studio running for hours) and *what to do* (add credits / stop idle studios / smaller machine), not *how* you looked it up.

### "My studio stopped / went to sleep but I have credits"

Credits are **per-teamspace**, and a studio only draws from the teamspace it runs in. So when a user says their studio paused/slept for lack of credits but insists they *have* credits, the credits are almost always in a **different teamspace** — or sitting in their **user wallet / org** — not the teamspace the studio lives in.

- In ToolJet, check the **Teamspace / Org / User** tabs: find where the credits actually are vs which teamspace the studio runs in. A near-zero balance on the studio's teamspace (even though the account has credits elsewhere) is the tell.
- **Fix:** move the credits into the studio's teamspace, or have them open the studio from the teamspace that already holds the credits, then restart it.
- **Reassure them:** a credit pause / auto-sleep **preserves the studio** — no work is lost, it resumes once the teamspace is funded.
- **Pro-plan note:** the $50/mo Pro plan includes 40 credits/month (a subscription) — that's different from buying 50 credits directly, and is a common point of confusion on these tickets.

### "My credits didn't refresh"

If a user's monthly top-up didn't happen and there's no data showing why — i.e. you look them up in ToolJet and **nothing comes back / the balance and refresh fields are blank**, and there's no usage anomaly or multi-account issue to explain it:

- **Add 15 credits manually via ToolJet** — this is standard practice for a missing monthly top-up
- The "no data shown" case is the tell: if the platform has no record of the top-up happening, just grant the 15 and move on
- No need to escalate for this, just add them and let the user know (canned reply: `!credits-added`)

### When Users Want Credits Back

If a user claims they were incorrectly charged or want a goodwill credit:

- Small amounts (under 5 credits): Use your judgment, add them via ToolJet
- Larger amounts: Check with Natalie Rand or the team lead before adding
- Missing monthly top-up with no clear cause: Add 15 credits — it's a known edge case
- Refunds for paid plans: That's a Stripe operation (see Module 06)

## Reading ToolJet Credit Data (grant or not?)

When you look a user up in ToolJet's Credit Management / "Monthly Free Credits Check" you get back a row of raw fields. Here's how to read them and decide whether a manual grant is warranted.

### The fields you'll see

A pasted row usually looks like:

```
glencarlosventura516@gmail.com          ← account email
glencarlosventura516                    ← username
random-forest-development-project       ← teamspace
0.987887099999975324724                 ← current credit balance
2026-03-27T05:37:37.967Z                ← timestamp(s): created / last refresh / refresh_date
not granted, free credits for previous billing period were not used   ← grant status + reason
```

- **balance** — how many credits are left right now. Near **15** = barely used; near **0** = used almost everything.
- **timestamps** — account created, last refresh, and/or next `refresh_date`. Free credits refresh every ~30 days from signup (not the 1st for these accounts). If the most recent refresh is **>30 days ago**, they're overdue.
- **grant status / reason** — the system's explanation for the last top-up. Common one: *"not granted, free credits for previous billing period were not used."*
- **free_credits_enabled** — if present and false, auto-refresh is off for this account.

### The core rule (don't forget it)

Free credits **only replenish what was actually used**, and they **don't roll over**. Use 4 → get 4 back. Use 0 → get 0 back. So "topped up nothing" is *correct* when they genuinely didn't use last period's credits.

### Decision guide

Read the **balance** against the **"not used" reason** — that's where the real signal is:

| What you see | Read | Action |
|---|---|---|
| Balance near 15 + "previous period not used" | They genuinely didn't use them — nothing to replenish | **Don't grant.** Working as intended. Explain with `!how-do-credits-work` / `!free-credits-balance` |
| **Balance near 0** + "previous period not used" | **Contradiction** — a near-empty balance means they DID burn through ~15. The "not used" flag is suspect | **Investigate, then usually grant.** Confirm single account + spend happened on THIS account → it's a missed top-up, add 15 (`!credits-added`) |
| Blank / no data comes back | Failed top-up, no record | **Grant 15** — the no-data edge case (`!credits-added`) |
| Last refresh > 30 days ago, balance low | Overdue refresh | Lean toward granting 15 once you've ruled out a transfer |
| Credits were transferred in + spent by another account | Replenishment correctly stops for the owner | **Don't grant.** Explain the transfer rule (`!how-do-credits-work`) |

### Before granting on a "contradiction" row

Rule out the legitimate reasons replenishment stops:

1. **Multiple accounts** — same person, credits sitting/spent on a different account (only one account per phone number gets credits).
2. **Transfer** — credits were moved to this teamspace and spent by someone who isn't the owner; the owner's credits then won't refresh.

If it's a single account and the user spent their own credits down to ~0, a balance-near-zero + "not used" row is a missed top-up — **grant 15 and move on**. If a transfer/multi-account explains it, don't grant; explain why.

<!-- crisp-shortcuts:start (auto-generated, do not edit) -->

## Crisp shortcuts (canned replies)

Common shortcuts that apply to this module. Type the `!bang` in
Crisp to insert the full message. The complete library lives in
Crisp under **Settings → Inbox Settings → Message Shortcuts**.

### !15-credits-not-in-pro

_Crisp group: Credit questions_

Thanks for reaching out. The 15 free monthly credits are reserved for the free tier only. You won't receive the 15 free credits on the Pro tier.

### !academic-100-credits

_Crisp group: Credit questions_

Thanks for reaching out. On the annual Pro plan with the academic discount, you will receive 100 credits for the entire year. You won't receive the additional 40 credits monthly. The 40 monthly credits are included in the standard Pro monthly offering.   Let us know if you have any other questions.

### !credits-added

_Crisp group: Credit questions_

Thanks for reaching out. I've added the credits to your account, you should be all set now.

### !credits-explained

_Crisp group: Credit questions_

Thanks for reaching out. Yes, on the free tier, you will receive 15 credits every 30 days. A few things to keep in mind regarding the credits:      You must be the user that uses the free credits in order for them to replenish.      You can transfer the credits to another teamspace, but if another user utilizes your free credits, this will reduce the number that you receive in following months permanently.      Looks like your credits were last refreshed on February 21, so the next refresh will be 30 days after that. Please let us know if you have any further questions.

### !free-credits-balance

_Crisp group: Credit questions_

Seems like everything is in order, you're just not using all 15 free credits monthly.   With Lightning, you get up to 15 free credits a month, but if you only use 4, we'll only top up 4. If you use all 15, we'll grant you 15 free credits.   Here is a guide with more info, let us know if you have any other questions: https://lightning.ai/docs/overview/billing

### !free-credits-check

_Crisp group: Credit questions_

Thanks for reaching out. Seems like everything is in order, Your 15 credits are sitting in your "vision-model" teamspace. Please confirm you can see them there.

### !free-credits-fixed

_Crisp group: Credit questions_

We've resolved the issue with your free credits not appearing. A few things to keep in mind:   1. You must be the user that uses the free credits in order for them to replenish.   2. You can transfer the credits to another teamspace, but if another user utilizes your free credits, this will reduce the number that you receive in following months permanently.   As a one time courtesy, we've reset your credits so that your account receives them going forward. Please let us know if you have any further questions.

### !how-do-credits-work

_Crisp group: Credit questions_

Thanks for reaching out. Happy to help. A few things to note about how the free credits work:   With Lightning, you get up to 15 free credits a month, but if you only use 4, we'll only top up 4. If you use all 15, we'll grant you 15 free credits. The credits don't build-up/accumulate. Here is a guide with more info: https://lightning.ai/docs/overview/faq/billing   You must be the user that uses the free credits in order for them to replenish.  * User A can transfer the credits to User B's teamspace, but if User B utilizes User A's free credits, then this will reduce the number that User A receives in following months permanently.  If your current balance still seems off to you, let me know. Happy to look into it further.

### !january-credits-bug

_Crisp group: Credit questions_

Thanks for reaching out. Our team is aware of a bug where most users didn't get the free credits this month (or got fewer than they should). We are working on a remediation, and this should be automatically resolved in the next couple hours. Thanks for your patience!

### !many-account-no-credits

_Crisp group: Credit questions_

Thanks for reaching out. Looks like you have X accounts, which is the problem. Which account would you like the credits to go to?

### !missing-phone-number

_Crisp group: Credit questions_

Happy to help - can you please provide your phone number? Looks like you don't have a phone number verified with your account which is the issue.

### !multiple-accounts

_Crisp group: Credit questions_

Thanks for reaching out. Looks like you have multiple accounts. Your 15 free credits are currently sitting in the account associated with email address [INSERT EMAIL ADDRESS]. Please confirm you can see your credits there.

### !refresh-date

_Crisp group: Credit questions_

Thanks for reaching out. Credits refresh every 30 days based on the day the account was created, not the first of each month. Please navigate to Teamspace > Settings > Activity > Transactions to check your renewal date. See more on how the free credits work here: https://lightning.ai/docs/overview/studios/lightning-credits.

### !user-wallet

_Crisp group: Credit questions_

Thanks for reaching out.

<!-- crisp-shortcuts:end -->
