# PLG Support — Quick Reference

Condensed quick-reference for PLG (Lightning AI Studio) support. PLG tickets arrive via **Plain** (support@lightning.ai). Canned replies are **snippets**: in Plain, type `[` in the reply box to autocomplete. Snippet names have **no `!` prefix** and are namespaced as `PLG - <Category> - <name>`.

## Start here — every ticket

1. **Look the user up in ToolJet first** — check ban status, account, credits, multiple accounts. [Open ToolJet](https://tooljet.lightning.ai/applications/7b6a09f5-f91a-44a2-9e28-803a13eb8bf0)
2. **If banned, that's the cause** of whatever they're reporting — regardless of what the ticket says. Ban status is always step 1.
3. **Read the first line** of the ticket — the real question is usually right there.
4. **Prioritise paid users** over free users.

## Support codes

| Code | Meaning | Action |
|---|---|---|
| 09332104 | Phone verification (system message) | Verify phone on ToolJet |
| 03920104 | Can't log in / create app = shadowbanned | ToolJet → User Management → check ban reason |

## Tools at a glance

| Tool | Use for | Access |
|---|---|---|
| **Plain** | PLG ticket management (email lands here) | Support team |
| **ToolJet** | User lookup, phone verify, credits, bans, deletion | Support + admins (Natalie Rand) |
| **Stripe** | Billing, subscriptions, refunds, invoices | Natalie Rand + finance |
| **Slack** `#customer-support-plg` | Engineering escalation for PLG | Support + eng |

## Phone verification (most common ticket)

1. ToolJet → **Phone Verification** tab → enter email.
2. Enter number — **digits only**, no spaces/symbols.
3. **Lookup** tab → check the number isn't on too many accounts.
4. Click **Verify Phone** → refresh to confirm.
5. Resolve immediately — don't wait for the user.

**Red flags:** US (+1) numbers that fail → Google them (likely fake). Non-US user sending a +1 → temp number, ask for their real local one. Same number on many accounts → free credits only go to one account per number (often intentional abuse).

## Bans

### Soft bans (often reversible — verify identity, then unban)

| Ban reason | What to do |
|---|---|
| "manually banned before verification" | Ask for LinkedIn / Scholar / Student ID. If legit, unban. |
| Temp / flagged email domain | Ask for a real email or verify identity. |
| Attempted too many phone numbers | **NOT fraud by default** — usually a legit user retrying their real number. Verify account, then verify phone. `attempting-multiple-phones` |
| Completed quests too fast (<2 min) | Verify identity, unban if legit. |
| Soft-blocked country | Verify identity, then unban. |

### Hard bans (do NOT reverse)

| Ban reason | Action |
|---|---|
| Crypto mining / torrenting / inappropriate content | `suspicious-activity`. Offer data deletion only. |
| Sanctioned country (hard block) | Cannot unban. Use the `hard-ban` snippet. |
| Complex AWS GuardDuty errors | Don't interpret yourself — send the full error to `#customer-support-plg`. |

### Country lists

**Hard block** (cannot unban — legal): Belarus +375, Cuba +53, Iran +98, North Korea +850, Russia +7, Syria +963, Venezuela +58, Ukraine Crimea/Donbas +380 (regions only), Bangladesh +880, Sri Lanka +94, Oman +968, Indonesia +62. (Sri Lanka, Oman, Indonesia = crypto-abuse hard blocks.)

**Soft block** (verify identity, then unban): Vietnam +84, Philippines +63, India +91, Singapore +65, South Korea +82, Egypt +20, Pakistan +92.

> High volume of Russia phone-verification requests right now — use the `hard-ban` response for all of them. University students can be verified **unless** they're in a hard-blocked country (legal restriction, no exceptions).

## Credits

**The #1 rule:** free credits only replenish what was **used**, and they **don't roll over**. Use 4 → get 4 back. Use 0 → get 0 back. Free tier = 15 credits/month (≈ 80 GPU hours), refresh on the 1st (or ~30 days from signup for some accounts). Credits ≠ tokens (tokens = inference API).

**Common scenarios**
- **"Where are my credits?"** → Check for multiple accounts and the wrong teamspace. Credits are per-teamspace; one account per phone number gets free credits.
- **"Draining too fast"** → Usually real spend (an H200 burns tens of credits in hours) or idle studios left running. Pull usage (read-only impersonation → usage CSV) to show where it went. Never mention impersonation/CSV/ToolJet to the customer.
- **"Studio slept but I have credits"** → Credits are in a different teamspace/wallet than the studio. Move them, or open the studio from the funded teamspace. Auto-sleep preserves the studio — no work lost.
- **"Credits didn't refresh" + nothing in ToolJet** → Missing top-up. **Add 15 manually** (`credits-added`), no escalation.
- **Transfer caught it** → If credits were transferred to another teamspace and spent by someone else, the owner's credits correctly **don't refresh**. Don't grant — explain with `how-do-credits-work`.

**Grant decision (Monthly Free Credits row)**

| What you see | Action |
|---|---|
| Balance near 15 + "previous period not used" | **Don't grant** — working as intended. |
| Balance near 0 + "not used" | Contradiction → investigate (single account + spent here?) then usually **grant 15**. |
| Blank / no data | Failed top-up → **grant 15**. |
| Transferred-in + spent by another account | **Don't grant** — explain the transfer rule. |

## Subscriptions & billing (Stripe)

**Refunds: escalate all to Natalie Rand.** Refunds are proportional to **unused** credits (not the flat price), and you must remove the remaining credits from ToolJet when issuing one.

- **Receipt:** Stripe → Payments → search email → Receipt History → Send Receipt.
- **Invoice:** More → Invoices → create → set status to **paid**.
- **Cancel:** self-serve cancels at end of period; we cancel immediately or on payment failure (Stripe → Subscriptions → search → Cancel).
- **Update card:** get details on a call, set new method as **default** on the subscription.
- **Billing email:** Stripe → Customers → search → Details → edit.

## Common platform issues

- **Studio stuck/won't start** → Ask: one studio or all? studio name? machine type? cloud? Free studio with 300GB+ → switch to a data-prep machine. H100s can be slow at peak. Stuck a long time → escalate with email, teamspace, studio name, duration, free/paid.
- **Credit depletion confusion** → idle studios, autosleep off (only Pro/Teams can disable; free can't), credits auto-reload on, machine switching, storage >10GB ($0.10/GB/mo), cross-cloud transfers.
- **Data loss / recovery** → engineering only. Post `#customer-support-plg` with username, free/paid, teamspace/studio. Don't run recovery yourself.
- **Impersonation** → restricted. Read-only usage viewing is fine for diagnosis; account access/actions → escalate to Natalie Rand.
- **Storage not updating after deletion** → escalate; eng forces a recalculation.

**Storage limits:** Free 50 GB · Pro 200 GB · Teams 2 TB · Enterprise unlimited (all get 10 GB free). After 10 GB: **$0.10/GB/month** (billed daily). External data connections (S3/GCS) aren't billed.

## Plain workflow & escalation

- Tickets split into **Paid** and **Free** inboxes. Prioritise paid.
- **Verification tickets:** resolve immediately. **Duplicates:** internal note "duplicate" → Resolve.
- **Escalating to eng:** post to `#customer-support-plg` with: 1) Paid/Free, 2) username/email, 3) studio name, 4) the full message. **No escalation on weekends.**
- Missing a snippet for a recurring issue? Create one so we can track it.

## ToolJet cheat sheet

All sections live in **one app** → [Open ToolJet](https://tooljet.lightning.ai/applications/7b6a09f5-f91a-44a2-9e28-803a13eb8bf0), then pick the tab.

| Section (tab) | Does |
|---|---|
| User Management | Status, ban reason, auth_provider, multiple accounts, activity |
| Phone Verification | Verify number + Lookup for abuse |
| Credit Management | Check / add / subtract per teamspace; Monthly Free Credits Check |
| Account Deletion | Permanently delete (irreversible — confirm first) |

## Tiers

| Tier | Cost | Key |
|---|---|---|
| Free | $0 | 15 credits/mo, 1 studio |
| Pro | $9.99/mo | Priority GPU, more storage (Academic $9.99 annual via Magic Link + .edu) |
| Teams | $49.99/mo | Multi-member, shared teamspace, admin |
| Enterprise | Custom | SLAs, dedicated support, BYOC |

## Most-used snippets (type `[` in Plain to insert; names have no prefix)

- **Phone Verification:** `phone-verified` · `need-phone-number`
- **Account / Identity:** `account-verified` · `need-to-verify-identity` · `attempting-multiple-phones` · `incorrect-email`
- **Credits:** `credits-added` · `how-do-credits-work` · `free-credits-check` · `multiple-accounts`
- **Bans:** `suspicious-activity` · `hard-ban`
- **Studio:** `studio-stuck` · `studio-name`
- **Account Deletion:** `delete-account`

Plain shows the full path as `PLG - <Category> - <name>`.

## Who owns what

| Need | Go to |
|---|---|
| Refunds, Stripe, tricky ban calls, impersonation | **Natalie Rand** |
| Platform bugs, stuck studios, data recovery, L2 | **`#customer-support-plg`** (no escalation on weekends) |
| Enterprise customers | Dedicated Slack channels (separate workflow) |
