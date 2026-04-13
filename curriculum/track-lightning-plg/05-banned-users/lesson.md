# Banned Users & Country Restrictions

## Understanding Bans

Lightning AI has automated systems that detect and ban suspicious activity. As support, you'll deal with ban appeals daily. The key is knowing **when to unban** and **when to hold firm**.

## Ban Reasons (What You'll See in ToolJet)

Navigate to [ToolJet](https://tooljet.lightning.ai/applications/7b6a09f5-f91a-44a2-9e28-803a13eb8bf0) → User Management → enter the user's email → scroll right to see the **ban reason** column.

### Soft Bans (Can Often Be Reversed)

| Ban Reason | What Happened | What To Do |
|-----------|--------------|-----------|
| "manually banned before verification" | Domain or username flagged | Ask for identity (LinkedIn/Scholar/Student ID). If legit, unban. |
| Domain name flagged | Used a temp email or unusual domain | Ask for a real email or verify identity |
| Completed quests too fast | Auto-detected as potential bot (old threshold was 5 min, now 2 min) | Verify identity, then unban if legit |
| Soft-blocked country | User is in a high-crypto-abuse country | Verify identity, then unban |

### Hard Bans (Do NOT Reverse)

| Ban Reason | What To Do |
|-----------|-----------|
| Crypto mining detected | Use `#suspicious-activity`. Offer data deletion only. |
| Pornography / inappropriate content | Same — `#suspicious-activity`, no unban. |
| Torrenting | Same — `#suspicious-activity`, no unban. |
| Sanctioned country (hard block) | Cannot unban. Explain it's a legal restriction. |

### Complex Bans

Sometimes you'll see AWS GuardDuty errors that look like this:

```
{ServiceName:guardduty DetectorID:44c09ccce... Action:{ActionType:DNS_REQUEST 
DNSRequestAction:{Domain:thekuhlodyssey.com Protocol:UDP Blocked:false...}
```

**Don't try to interpret these yourself.** Send the full error to an engineer in #customer-support-plg and let them determine if it's nefarious.

## Country Restrictions

### Hard Block — Sanctioned Countries

These users **cannot** be unbanned. It's a legal/investor requirement:

- Belarus
- Cuba
- Iran
- North Korea
- Russia
- Syria
- Venezuela
- Crimea & Donbas regions (Ukraine)
- Bangladesh

Additional countries blocked for crypto abuse:

- Sri Lanka
- Oman
- Indonesia

### Soft Block — Verify Then Allow

Users from these countries **can** be manually verified and unbanned. Ask for LinkedIn, Google Scholar, Student ID, or government-issued ID:

- Vietnam
- Philippines
- India
- Singapore
- Korea
- Egypt
- Pakistan

> **When in doubt, verify identity.** It only takes a minute to Google someone's LinkedIn or university, and it prevents us from unfairly locking out legitimate researchers.

## Handling Ban Appeal Tickets

### The Process

1. **Look up the user in ToolJet** — check ban reason and status
2. **Determine ban type** — soft ban or hard ban?
3. **For soft bans**: Ask for identity verification, then unban
4. **For hard bans**: Send `#suspicious-activity` shortcut. Offer data deletion.
5. **For country bans**: Check if it's hard or soft blocked

### False Positive Trends

Sometimes we see waves of false-positive bans. If you notice a bunch of users being banned for the same reason in a short period, flag it in #customer-support-plg. Example: Natalie Rand recently noticed a mass ban for a flag that engineering had added but didn't actually need — they removed it and unbanned everyone.

Always trust your gut if something looks like a false positive at scale.
