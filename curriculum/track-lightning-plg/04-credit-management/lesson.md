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

## How Credit Consumption Works

Lightning follows a specific order when consuming credits:

1. **Free credits are used first**
2. Once free credits are gone, **purchased credits** are used
3. Subscription-included credits (Pro/Teams) act like purchased credits and stack with free credits

When a user runs out of all credits, Lightning will **gracefully shut down all running Studios and jobs** to prevent overuse. Users get warnings before this happens.

## How to Transfer Credits (Self-Service)

Users can move credits between teamspaces themselves:

1. Click on their credits
2. Hit **"Add Credits"**
3. Then **"Transfer Credits"**
4. Pick the destination teamspace from the dropdown

> **"My credits disappeared after transfer"** — They almost certainly landed in a different teamspace than expected. Check ToolJet and look at ALL teamspaces for that user. The credits are there, just not where they're looking.

## Common Credit Scenarios

### "Where are my credits?"

1. Check if they have **multiple accounts** — credits may be in a different one
2. Check which **teamspace** the credits were allocated to — users often look in the wrong one
3. Verify the phone number isn't shared across accounts (credits only go to one)
4. If they recently transferred credits, check ALL teamspaces — transfers sometimes land in "general" or a different teamspace than intended

### "I should have more credits"

1. Explain the refresh rule (only replenishes what was used)
2. Check if someone else spent their credits (transfer scenario above)
3. Point them to the [billing FAQ](https://lightning.ai/docs/overview/faq/billing)

### "My credits are draining too fast"

1. Ask what machine type they're running — GPU machines cost more
2. Check if they have **idle studios running** — compute charges even when they're not actively coding
3. Help them understand [compute costs](https://lightning.ai/pricing#compute) — prices are shown in the machine selection menu

### "My credits didn't refresh"

If a user's monthly top-up didn't happen and there's no data showing why — i.e. you look them up in ToolJet and **nothing comes back / the balance and refresh fields are blank**, and there's no usage anomaly or multi-account issue to explain it:

- **Add 15 credits manually via ToolJet** — this is standard practice for a missing monthly top-up
- The "no data shown" case is the tell: if the platform has no record of the top-up happening, just grant the 15 and move on
- No need to escalate for this, just add them and let the user know (canned reply: `!credits-added`)

**Watch for the "not granted" message in ToolJet:** The Monthly Free Credits Check section will show `"not granted, free credits for previous billing period were not used"` — this means the system didn't top up because they didn't use enough last month. If the user has <1 credit left and genuinely can't use it (below minimum to start any studio), they're in a **deadlock** — just add 15 credits and move on.

### Credit Deadlock

This happens when a user has a tiny balance (like 0.88 credits) that's too small to run anything, so they can never consume it, so the system never refreshes their 15 credits. They're stuck.

**Signs:** User has <1 credit, can't start any studio, credits won't refresh because "previous period credits weren't used."

**Fix:** Don't send them the `!free-credits-balance` canned response — that just explains the refresh rule they already understand. **Add 15 credits directly.** They're stuck, not confused.

### When Users Want Credits Back

If a user claims they were incorrectly charged or want a goodwill credit:

- Small amounts (under 5 credits): Use your judgment, add them via ToolJet
- Larger amounts: Check with Natalie Rand or the team lead before adding
- Missing monthly top-up with no clear cause: Add 15 credits — it's a known edge case
- Refunds for paid plans: That's a Stripe operation (see Module 06)

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
