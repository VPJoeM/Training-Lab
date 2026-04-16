# Subscription & Billing Management

## Pricing Overview

Direct users to the [pricing page](https://lightning.ai/pricing) and [compute costs](https://lightning.ai/pricing#compute) when they have questions.

### Quick Reference

| Tier | Monthly Cost | Key Features |
|------|-------------|-------------|
| Free | $0 | 15 credits, 1 studio, basic machines |
| Pro | $9.99 | Priority GPU, more storage, faster startup |
| Teams | $49.99 | Multi-member, shared teamspace, admin controls |
| Enterprise | Custom | Dedicated support, SLAs, custom infra |

### Compute Billing Details

- Billed **by the second** — no minimum
- CPU machines have a base cost
- GPU machines vary by type (check compute costs page)
- **Running a job on any GPU machine also spins up a monitoring CPU at ~$0.43/hr**
- Studios running = credits depleting, even if you're not actively using them

## Stripe Operations

> **Who can issue refunds on Stripe?** Only Natalie Rand and select finance team members. If you don't have Stripe access yet, route refund requests through Natalie Rand.

### Sending a Receipt

1. Open Stripe → **Payments** tab
2. Search by customer email
3. Scroll to **"Receipt History"**
4. Click **"Send Receipt"** on the right

https://www.loom.com/share/a36b9f42e3954f6f98cd4677950761d2

### Creating a Custom Invoice

Users automatically receive receipts, but some request a formal invoice for their records.

1. Stripe → **"More"** sidebar → **Invoices**
2. Create the invoice
3. **Important:** Change the invoice status to "paid" after creating it

https://www.loom.com/share/14792dfa491e49c6b98c1767009beb9f

https://www.loom.com/share/f2fafb58e88f403dac675d3387ae7533

### Processing a Refund

**Escalate all refund requests to Natalie Rand.**

Refunds are based on how many credits the user has consumed, not the flat subscription price:

> Example: A user bought a $50 monthly Pro sub (40 credits per month). They're not satisfied and want to cancel and get a refund. They've used 30 credits and only have 10 left. We can only offer a **partial refund of $10** — proportional to the unused credits. **We also need to remove the remaining 10 credits from their account on ToolJet when we issue the refund.**

### Cancelling a Subscription

**Self-serve:** Users can cancel their own subscription, but it only cancels at the **end of the current billing period** — they keep access until then.

https://www.loom.com/share/30258dc9bd3f47d8bbfb12c7f4e2f7fd

**When we need to step in:**

- **User wants immediate cancellation** — self-serve only does end-of-period. Cancel it for them on Stripe.
- **Payment failure** — if their payment has failed, they can't cancel self-serve. We have to do it on Stripe.

Manual cancellation:

1. Stripe → **Subscriptions** sidebar
2. Search by customer email
3. Click **"Cancel Subscription"**

### Updating Billing Email

1. Stripe → **Customers** tab → search user email
2. Click **Details** tab → edit icon in the corner
3. Update the email

### Updating Credit Card

1. Get on a call with the customer
2. Get their new card details over the phone
3. Set the new payment method as **"default"**
4. Go to their subscription → Payment Method → select the default card → save

https://www.loom.com/share/ab792169cf8940b2867777d819226fa3

## Managing Subscriptions (Self-Serve)

Users can manage their own subscription in their Lightning account. Share this Loom if they need guidance:

https://www.loom.com/share/6934d653f0fd47dfb4ab729fe7c891ef
