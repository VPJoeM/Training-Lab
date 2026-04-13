# Credit Management

## How Credits Work

Credits are the currency of the Lightning AI platform. Here's what you need to know:

### Credit Basics

- **Free tier**: 15 credits per month (~22 GPU hours)
- **Refresh cycle**: Every 30 days from the user's sign-up date (not calendar month)
- **Billing granularity**: Compute charged by the second
- **Hidden cost**: Running a GPU studio also spins up a monitoring CPU machine at ~$0.43/hr

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

## Common Credit Scenarios

### "Where are my credits?"

1. Check if they have **multiple accounts** — credits may be in a different one
2. Check which **teamspace** the credits were allocated to — users often look in the wrong one
3. Verify the phone number isn't shared across accounts (credits only go to one)

### "I should have more credits"

1. Explain the refresh rule (only replenishes what was used)
2. Check if someone else spent their credits (transfer scenario above)
3. Point them to the [billing FAQ](https://lightning.ai/docs/overview/faq/billing)

### "My credits are draining too fast"

1. Ask what machine type they're running — GPU machines cost more
2. Check if they have **idle studios running** — compute charges even when they're not actively coding
3. Remind them about the monitoring CPU machine (~$0.43/hr on top of GPU costs)
4. Help them understand [compute costs](https://lightning.ai/pricing#compute)

## When Users Want Credits Back

If a user claims they were incorrectly charged or want a goodwill credit:

- Small amounts (under 5 credits): Use your judgment, add them via ToolJet
- Larger amounts: Check with Natalie Rand or the team lead before adding
- Refunds for paid plans: That's a Stripe operation (see Module 06)
