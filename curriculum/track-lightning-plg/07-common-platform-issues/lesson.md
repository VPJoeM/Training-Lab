# Common Platform Issues

## Studios Not Starting / Stuck Loading

This is a frequent complaint. Here's your troubleshooting flow:

### Questions to Ask

1. Is it specific to **one studio** or are **none** of their studios working?
2. What's the **name** of the stuck studio?
3. How long has it been stuck?
4. What **machine type** were they trying to use?
5. What **cloud provider** were they using?

### Common Causes

- **Free studio with 300GB+ of data** — The fix is to switch to a data prep machine
- **GPU availability** — Sometimes H100s take a while to provision. This is normal during peak times.
- **Random platform error** — Needs engineering escalation (flag Neil and Ethan)

### For Stuck Studios

If a studio is stuck saving or loading for an extended period, escalate to engineering with the studio name and user email.

## Credit Depletion Confusion

Users frequently don't understand why their credits are disappearing:

- **Idle studios still running** — Compute charges even when they're not coding
- **Autosleep disabled** — Only Pro and Teams users can disable autosleep. Free tier users have autosleep on by default and **cannot** turn it off. If a Pro/Teams user has autosleep off, their studios never stop running — check if it's enabled. [Autosleep docs](https://lightning.ai/docs/overview/ai-studio/auto-sleep)
- **Credits auto-reload enabled** — Many users don't know they have this enabled in their teamspace or org and get surprised by charges. Show them how to toggle it off:

https://www.loom.com/share/61f5acb5abdf4bd589705f023e8e8ab2

- **Machine switching** — Switching from CPU to GPU or between GPU types can trigger unexpected charges
- **Machine costs** — Prices are as shown in the CPU/GPU machine selection menu (see [pricing](https://lightning.ai/pricing))
- **Storage over 10GB** — Once you exceed 10GB, storage is billed by the second (same for all tiers). [Billing FAQ](https://lightning.ai/docs/overview/faq/billing)
- **Transferring to another cloud** — Costs credits that users didn't expect

**Always check:** What machines are running, how long they've been running, and which teamspace is being charged.

## Data Loss in Studios

When a user loses data:

### Understand the Drive

- The **Drive** is persistent storage attached to a teamspace
- Data in the studio's working directory may or may not persist depending on the setup
- Switching machine types can sometimes cause data loss if files weren't saved to the Drive
- [Drive documentation](https://lightning.ai/docs/overview/drive)

### Data Recovery (Engineering Required)

If a user says they lost data and needs recovery, **post to `#customer-support-plg`** and tag the **@oncall** group with:

- Username
- Free user or paid user (if paid, check their total spend on their Stripe customer profile)
- Teamspace or studio name they lost

Don't try to run recovery commands yourself — engineering handles this.

[Loom: Data recovery walkthrough](https://www.loom.com/share/74641ae78d324ae1968c1ebb44e2e999)

## Account Impersonation

If you need to see the platform as a specific user, **escalate to Natalie Rand**. Account impersonation is restricted and not available to the wider team.

Common reasons someone might need impersonation:

- User doesn't understand why they're being charged for storage — Natalie logs in as them to check storage costs and transaction page
- User says they can't find a specific studio — often they're looking in the wrong teamspace or org

If you think peeking into an account would solve the issue, let Natalie know and she'll take a look.

## Working with GitHub in Studios

Some users want to connect their GitHub repos to their studio. Point them to the [Discord guide](https://discord.com/channels/1077906959069626439/1267308626398412830/1267471909856088112).

## Whitelisted IPs

Lightning **does not have static IPs**. Each studio gets a new IP. Users can check their current IP with:

```bash
curl https://ipinfo.io/ip
```

But it will change when the studio restarts. If they need a static IP for firewall rules, this is a limitation of the platform.

## Setting Up a Custom Domain

[Loom: Custom domain setup](https://www.loom.com/share/890e614759d24bdd8c566572cf2d3578)

## Detect Machine Type

Users can check what they're running on:

```bash
nvidia-smi
```

Or programmatically:

```python
from lightning_sdk import Studio
print(Studio().machine)  # outputs Machine.L4_X_4
```

## Installing Third-Party Programs

All machines have `apt-get`, so check for a package first:

```bash
sudo apt-get install <package-name>
```

For programs not in apt, download and install manually:

```bash
wget https://example.com/path/to/file.zip
sudo apt-get install unzip
unzip file.zip
```

## Using Marimo in Studio

[Loom: Marimo setup](https://www.loom.com/share/3a827fbc026149708660ee12f3f71a8e)

<!-- crisp-shortcuts:start (auto-generated, do not edit) -->

## Crisp shortcuts (canned replies)

Common shortcuts that apply to this module. Type the `!bang` in
Crisp to insert the full message. The complete library lives in
Crisp under **Settings → Inbox Settings → Message Shortcuts**.

### !a100-voltage-park

_Crisp group: Trends / Product Gaps_

Thanks for reaching out.

### !a10g

_Crisp group: Trends / Product Gaps_

Thanks for reaching out. Lightning no longer supports A10Gs, but I suggest using L40S or L4 instead.

### !academic-pricing

_Crisp group: Trends / Product Gaps_

Thanks for reaching out. In order to access the academic tier, you must be logged into Lightning with your .edu email address.

### !accessing-files-in-studios

_Crisp group: Trends / Product Gaps_

Thanks for reaching out.

### !ai-repo-access

_Crisp group: Trends / Product Gaps_

Thanks for reaching out.

### !bug-bounty

_Crisp group: Trends / Product Gaps_

Thanks for reaching out. Feel free to report the information you have and we will assess the severity internally. Payout is possible depending on the level of severity we determine.

### !code-error-gpu-memory

_Crisp group: Trends / Product Gaps_

The error suggests you have some processes running that are using memory, you'll need to clean those up before running again. To do this, find processes with ps aux and kill them with kill <process id> - or alternatively you can try killing all python processes with pgrep -f python | xargs kill -9

### !comfy-ui-broken

_Crisp group: Trends / Product Gaps_

Thanks for reaching out. Please provide the name of the studio and we'll look into this asap.

### !data-deletion-drive

_Crisp group: Trends / Product Gaps_

You can delete data directly from the drive. Please see more information here: https://lightning.ai/docs/overview/ai-studio/add-data#delete-files

### !data-loss

_Crisp group: Trends / Product Gaps_

Thanks for reaching out and apologies for the scare. Please provide the name of the studio(s) and teamspace(s) that are missing, and we'll look into it asap.

### !download-data

_Crisp group: Trends / Product Gaps_

Thanks for reaching out. Please note that you can download your data directly from the Teamspace drive. Please see more details on how to do that here: https://lightning.ai/docs/overview/drive

### !drive-v1

_Crisp group: Trends / Product Gaps_

Thanks for reaching out and apologies for the inconvenience. We are aware of this issue and are releasing the fix for it. Would you be interested in jumping on a quick call with our product team? We'd love to hear any/all feedback you have on the drive. Happy to offer 25 credits for your time. If you're interested, let us know when you're available and we will set up a time.

### !drive-v2

_Crisp group: Trends / Product Gaps_

Thanks for reaching out and apologies for the inconvenience. We are aware of these issues and working on a fix.   Would you be interested in jumping on a quick call with our product team? We'd love to hear any/all feedback you have on the drive. Happy to offer 25 credits for your time. If you're interested, you can book a time slot using this link: https://calendar.google.com/appointments/schedules/AcZssZ3b-ySuPlpWQ0QH2T8a0pdEVO1hoL5g6OgCdhG7jExKL_WAFMm7TZVFts4eGpNy4ztOcT-E8Wqh

### !free-cpu-studio

_Crisp group: Trends / Product Gaps_

Thanks for reaching out. The free studio depends on the machine type. Our platform gives you free continuous uptime for any studio running on a 4-cpu machine. it's not a single slot that you can assign to any studio. So, if your other studio is also on a 4-cpu machine, it should also run without charge. If it's on a gpu or a larger cpu machine, then it will incur costs.

### !gcp-bucket

_Crisp group: Trends / Product Gaps_

Thanks for reaching out. If your data lives in GCP buckets, you should be able to connect to GCP buckets with the Add Data button in the Drive.

### !inactive-account

_Crisp group: Trends / Product Gaps_

Thanks for reaching out.

### !instance-not-shutting-down

_Crisp group: Trends / Product Gaps_

Thanks for reaching out.

### !machine-failure

_Crisp group: Trends / Product Gaps_

Thanks for reaching out and apologies for the inconvenience. Can you please share the name of the studio and let me know which cloud provider you used to request the machine?

### !manage-data

_Crisp group: Trends / Product Gaps_

Hi there,   You can manage your data on a more granular level by using the teamspace Drive. This guide will give you some more info: https://lightning.ai/docs/overview/organize-data/drive  Let us know if you have any further questions!

### !model-api

_Crisp group: Trends / Product Gaps_

Thanks for reaching out. The cost associated with each model type is listed here: https://lightning.ai/lightning-ai/models?section=allmodels&view=org

### !python-env

_Crisp group: Trends / Product Gaps_

Thank you for reaching out. Please see the documentation on modifying python environments here: https://lightning.ai/docs/overview/ai-studio/modify-environment#python-versions. Let us know if you have any further questions.

### !rate-limits

_Crisp group: Trends / Product Gaps_

Thanks for reaching out. Please find more info on the rate limits per tier here: https://lightning.ai/docs/overview/model-apis

### !s3-bucket

_Crisp group: Trends / Product Gaps_

Thanks for reaching out.

### !storage-amount-inaccurate

_Crisp group: Trends / Product Gaps_

Thank you for reaching out and apologies for the inconvenience. This was a bug on our end. We have released a fix today and the storage numbers will be accurate starting tomorrow. You do indeed only have [X} GB, so you are all set and there's no action needed from your end.

### !storage-limit

_Crisp group: Trends / Product Gaps_

Thanks for reaching out and apologies for the inconvenience. We have temporarily disabled the storage limits and you should be able to use the platform normally upon refresh. The limits are valid. However, we will ensure that users have the right deletion tools available before enabling these. You can expect proper tooling to delete your old data from the drive to be available on Monday. Thanks again for helping identify this issue quickly.

### !stuck-studio-resolved

_Crisp group: Trends / Product Gaps_

Thank you for letting us know and apologies for the inconvenience. We had an issue over the weekend with over-provisioned CPUs not working. This has now been resolved. Please let us know if you're still experiencing this issue with your studio. And let us know how many credits you lost here, happy to reimburse you for those.

### !studio-hangs

_Crisp group: Trends / Product Gaps_

Thanks for reaching out. Please provide the name of the studio and we will look into this asap.

### !studio-name

_Crisp group: Trends / Product Gaps_

Thanks for reaching out. Can you please provide the studio name? We will have an engineer look into this asap.

### !studio-stuck

_Crisp group: Trends / Product Gaps_

Thanks for reaching out and apologies for the inconvenience. Are you still experiencing this issue? If so, can you please provide the name of the studio?

### !teamspace-management

_Crisp group: Trends / Product Gaps_

Thanks for reaching out.

### !teamspace-topup

_Crisp group: Trends / Product Gaps_

Thanks for reaching out.

### !trends-/-product-gaps

_Crisp group: Trends / Product Gaps_

Thanks for reaching out.

### !upload-data

_Crisp group: Trends / Product Gaps_

Thanks for reaching out. This is likely because you uploaded to one cloud provider (e.g. AWS) and your studio is on a different one (GCP).   Where did you select to upload to when you originally uploaded the data? The default would be AWS. If you start an AWS studio, then you should be able to see the data inside the studio.

### !vulnerability-report

_Crisp group: Trends / Product Gaps_

Thanks for reaching out. You may report your findings here and our security team will assess. Thank you!

<!-- crisp-shortcuts:end -->
