# Build on Lightning — Capstone

## TL;DR

Pick a problem you actually want to solve. Write it up using the **[Value Framework](https://www.notion.so/lightningai/Value-framework-HOW-to-2ff28e47620980c188e9d5516c9ef636)** (Lightning's standard format for describing problems and solutions from the user's POV) and the **[1:3:1 Decision-Making Process](https://www.notion.so/lightningai/1-3-1-Decision-Making-Process-2df28e476209805384fad87009e35955)** (one problem → up to three options → one recommendation). Then **build it on Lightning AI** — Studio, agent, web app, CLI tool, automation, anything that runs on the platform. Present it to the team in a 15-minute slot.

The discipline (frameworks) is the muscle being trained. The project itself is the substrate — pick whatever you find interesting enough to ship.

---

## Why this exists

Two reasons:

1. **Grow the muscle on the platform.** You spend most of your day talking to customers about Lightning. The fastest way to talk credibly about it is to actually build something on it. After this module you'll have shipped a working artifact end-to-end — created a Studio, picked a machine type, deployed something, hit the API — and that practical experience is what separates support engineers customers trust from ones they don't.

2. **Practice the company's two operating frameworks.** Every brief written at Lightning uses the [Value Framework](https://www.notion.so/lightningai/Value-framework-HOW-to-2ff28e47620980c188e9d5516c9ef636). Every non-trivial decision uses [1:3:1](https://www.notion.so/lightningai/1-3-1-Decision-Making-Process-2df28e476209805384fad87009e35955). By the end of this module you'll have produced both, which is the same shape of doc you'll write the rest of your time at the company.

---

## The brief

Build something on Lightning AI and present it. Two written deliverables, one demo, one presentation:

1. **[Value Framework](https://www.notion.so/lightningai/Value-framework-HOW-to-2ff28e47620980c188e9d5516c9ef636) write-up** — describing the problem and outcome from the user's point of view (the "user" can be you, your team, your customers, or anyone — pick one and stay consistent)
2. **[1:3:1](https://www.notion.so/lightningai/1-3-1-Decision-Making-Process-2df28e476209805384fad87009e35955) doc** — define the problem, list up to three options (one of which must be "Do Nothing"), recommend one with rationale and concrete next steps
3. **Working build** — running on Lightning. Studio template, agent, web app on a Studio, model API integration, CLI tool, automation script, internal team tool, hobby project. Open scope.
4. **15-minute presentation** — walk us through the framework, the decision, and a live demo

You'll be evaluated on the **discipline** of how you used the frameworks, not the ambition of the project. A small, tightly-framed thing beats a sprawling, vaguely-framed one.

---

## Step 1 — Pick the problem

### Picking criteria

A good capstone problem has three traits:

1. **You actually care about it.** If you're forcing yourself to be interested, the framework write-up will read flat. Pick something that bothers you, intrigues you, or that you'd genuinely want to use.
2. **It's small enough to ship.** If you can describe the build in one sentence, it's the right size. If you need a paragraph, cut something.
3. **You can name a user.** Even if the user is "me, six months ago" or "ML engineers like me who keep hitting X". The Value Framework is unusable without a specific person whose lived reality you're describing.

### Examples (just to get you thinking — pick your own)

- "I keep losing track of which Studio is running on which GPU. Build a CLI dashboard that lists them with cost-per-hour."
- "When teaching ML to friends, I always rebuild the same boilerplate. Build a Studio template that lands them in a working PyTorch + dataset environment in one click."
- "I want to fine-tune a small model for a hobby project but the workflow is intimidating. Build a step-by-step interactive notebook that takes someone from zero to a deployed endpoint."
- "Our team gets asked the same five questions over and over. Build a small agent that answers them from a Notion doc."
- "I want to run a personal LLM evaluation harness on different machines without hand-managing it."

Don't copy any of these — they're warm-ups for your own picking.

### What NOT to pick

- A project that's mostly an excuse to use a specific tool ("I want to learn Rust" → that's a means, not a problem)
- A project that requires shipping infrastructure changes to Lightning itself
- A project so ambitious you'd need a quarter to ship it

---

## Step 2 — Apply the Value Framework

The Value Framework is Lightning's standard for describing problems from the **user's** point of view. It deliberately ignores internal execution, technical details, and project status. **If a sentence wouldn't make sense to the user without insider context, it doesn't belong in this section.**

The four canonical sections are:

- **Current State** — what the user is experiencing today if nothing changes. Their reality in production: what's broken, missing, slow, risky, unreliable, or manual *from their point of view*. Not the project status. Not the team's experience. Not the technical root cause.
- **Negative Implications** — the direct consequences to the user if the current state continues. Risk, delay, cost, lost trust, degraded performance, operational burden, exposure. *How does this hurt the user if nothing changes?*
- **Future State** — what the user's experience looks like once this is fully resolved and stable. The world they operate in after the problem no longer exists. Not "MVP", not phases, not partial solutions — describe the **finished** reality.
- **Positive Outcomes** — the value the user gains and the business captures once the future state exists. Concrete benefits, not feature names. *Why does this materially matter?*

The team-extended format adds two sections at the top — a one-sentence positioning and a description of who this is for:

```
# 1-liner Value Prop
<one sentence — what is this and who's it for?>

# ICP (Ideal Customer Profile)
<who is the user — be specific. "ML engineers who use VS Code" beats "developers".>

# Current State
<what the user is experiencing today if nothing changes — broken, missing,
slow, risky, manual, frustrating from THEIR point of view. Numbered list
of 3–5 specific things.>

# Negative Implications
<the direct consequences to the user if the current state continues. Risk,
delay, cost, lost trust, operational burden, business exposure. Bullets.>

# Future State
<what the user's experience looks like once this is fully resolved.
NOT phases or partial solutions. NOT "MVP". Describe the finished reality.>

# Positive Outcomes
<the value the user gains when the future state exists. Concrete benefits,
not feature names.>

# Open Questions
<a written list of what you don't know yet going into the build phase.
Trains you to distinguish "I know" from "I'm guessing".>
```

### Worked example: good vs bad

From the Value Framework canonical doc — the food/oven example shows the trap most people fall into.

**Good** (user POV):
> **Current State:** The user is hungry and does not have food available to eat. They are distracted, frustrated, and unable to focus on what they need to do next.
>
> **Future State:** The user has a warm, satisfying meal ready without effort or uncertainty.

**Bad** (operator POV — the trap):
> **Current State:** The oven is not preheated and the cooking process hasn't started.
>
> **Future State:** The oven is preheated, ingredients are chopped, and the recipe is ready to execute.

The bad version describes the *cook's* problem, not the *user's*. Same trap shows up in support engineering: it's tempting to write "ToolJet doesn't have a button for X" when the actual user-side reality is "I keep doing this five-minute thing manually and it's annoying".

### Worked example: a fabricated brief

Here's a fabricated example showing the team-extended format in action. Imagine the project is a one-click Studio template for someone fine-tuning their first model:

> **1-liner Value Prop**
> A one-click Studio template that takes someone from "I want to fine-tune a small model" to a working training run in under 10 minutes, with sensible defaults already wired up.
>
> **ICP**
> Engineers and researchers new to model fine-tuning who already know Python and ML basics but haven't stitched together GPU + dataset + framework + checkpoint setup before. They want to learn by experimenting, not by configuring.
>
> **Current State**
> 1. New fine-tuners spend 1–2 hours stitching together environment setup (CUDA versions, framework installs, dataset download, base-model download) before they can run anything.
> 2. Most "getting started" guides assume the reader already knows which framework and which base model to use; choosing both is itself a decision they're not equipped to make.
> 3. When something fails (OOM, dataset format mismatch, tokenizer issue), the error message rarely points at the actual fix.
>
> **Negative Implications**
> - Many users abandon fine-tuning before their first successful run; the platform never gets to demonstrate its value.
> - Time spent debugging setup is time not spent learning the actual ML concepts.
> - Users form a "fine-tuning is hard" mental model that blocks them from using the platform's strongest capabilities later.
>
> **Future State**
> A new user opens the template, runs one command, and sees their first fine-tuned model produce a sensible output within 10 minutes. The template's README walks them through each piece of the pipeline so they understand what just happened.
>
> **Positive Outcomes**
> - First-time fine-tuners reach a working result in their first session, building confidence to keep going.
> - Time-to-value drops from "I'll come back to this when I have an afternoon" to "let me try one more thing right now".
> - Users build accurate mental models of fine-tuning rather than learning to fear it.
>
> **Open Questions**
> - Which base model strikes the best balance of "small enough to run quickly" and "interesting enough to produce good output"?
> - Should the template include evaluation, or is that a separate template?
> - How much hand-holding is too much?

Read what's there carefully:

- **Current State items are concrete** — specific time costs, specific cognitive blockers, specific failure modes. Not "the experience could be better".
- **Each Negative Implication is one specific consequence to the user**, not internal frustration ("our docs are unclear" is not a Negative Implication; "users finish their first session without a working model and don't return" is).
- **The 1-liner names the thing AND the user in one sentence.** Not "we built a template" — "takes someone from X to Y in under 10 minutes". You can feel the audience in the sentence.
- **Open Questions are honest unknowns** — not rhetorical. The author genuinely doesn't know the answers yet, and writing them down means they'll surface in the build phase rather than ambushing them mid-implementation.

---

## Step 3 — Apply the 1:3:1 Decision-Making Process

After the Value Framework, you write a 1:3:1 to decide *which* solution to actually build.

The format is:

- **1: The Problem** — clearly state what you're deciding. Numbered sub-points if multiple things need solving.
- **3: Options** — up to three viable approaches, with explicit Pros / Cons.
- **1: Recommendation** — the one you're going with, with the reasoning and concrete next steps.

The framework's principles:

- **Single decision maker.** One person owns the final call, not a committee.
- **Bias to action.** Default to moving forward rather than waiting for perfect information.
- **No blockers.** The team must be empowered to proceed; don't let indecision stall progress.
- **Clarity over complexity.** Present information in a format that can be reviewed in minutes.

### Hard rule: one of your three options must be "Do Nothing"

This is non-optional. "Do Nothing" forces you to articulate the cost of inaction — what stays broken, what stays expensive, what stays risky. If you can't make "Do Nothing" sound clearly worse than your recommended option, your problem framing is weak and you should re-do Step 2.

Don't make Do Nothing a strawman ("Cons: doesn't solve the problem"). Treat it like a real option:

- **Pros:** no work required, no new dependencies, no maintenance burden, no risk of regression
- **Cons:** the specific bad things from your Negative Implications section continue to happen

### Worked example: a fabricated 1:3:1

Continuing the fabricated fine-tuning template scenario from Step 2 — here's the kind of design decision you'd write up before starting the build.

> **1: The Problem**
>
> The fine-tuning Studio template needs to decide whether to bundle a quick evaluation step at the end of training, or ship as training-only and leave evaluation to a separate template later. The decision touches four things:
>
> 1. **Time-to-first-result.** A bundled evaluation step adds 5–10 minutes to the first run. Users who came expecting "show me a fine-tune" might bail before the eval finishes.
> 2. **Pedagogical loop.** Without evaluation in the same flow, users finish the training run with no signal that the model "learned anything" — which is the satisfying moment that makes them come back.
> 3. **Maintenance surface.** A bundled template has more moving parts and more failure modes than a training-only one.
> 4. **Discovery cost.** Two separate templates means users have to find both. Many won't bother with the second.
>
> **3: Options**
>
> **Option 1: Bundle a small evaluation step into the same template (Recommended)**
>
> > *Pros:* one click takes the user end-to-end; users feel the full loop on first run; the pedagogical "did it work?" moment is built in; no extra discovery step required.
> >
> > *Cons:* longer first-run time (5–10 extra minutes); more code in one template means a single failure can break the whole flow; one more thing to maintain.
>
> **Option 2: Two separate templates — one for training, one for evaluation**
>
> > *Pros:* simpler to maintain each; failures isolated; users opt in to evaluation rather than waiting through it.
> >
> > *Cons:* users have to find and run two things; many won't; the satisfying loop is broken (training ends with no "did it work?" answer); two READMEs to keep in sync.
>
> **Option 3: Do Nothing — ship training-only, no evaluation anywhere**
>
> > *Pros:* no work; we can ship today; no maintenance overhead beyond the training piece.
> >
> > *Cons:* users finish the first run with no idea whether the fine-tune worked; a non-trivial fraction will conclude "fine-tuning is mysterious" and not come back; we miss the chance to teach the full mental model on first contact; the Negative Implication "users form a 'fine-tuning is hard' mental model" from the Value Framework continues to be true.
>
> **1: Recommendation**
>
> Bundle a small evaluation step into the same template. The pedagogical loop matters more than the maintenance overhead — users who feel the model "learned" on their first run come back; users who don't, often don't. The longer first-run time is a real concern, but we mitigate it by using a tiny held-out set (under 60 seconds of evaluation) rather than full benchmarking. The maintenance overhead is acceptable while there's one template; if we add three more later, we'll re-evaluate the bundling choice then.
>
> **Next steps if approved:**
> 1. Pick a small held-out eval set (≤200 examples) appropriate for the chosen base model
> 2. Wire training output into a quick eval script that runs after the training job finishes
> 3. Update the README so eval output is the explicit "you finished" moment, not an afterthought
> 4. Test the bundled run end-to-end on a clean Studio with no cached state

What to take away from the shape:

- **The Problem is broken into numbered sub-points** — each is a discrete consequence, not a generic "things are bad"
- **Three options including a real Do Nothing** — the Cons of Do Nothing reuse the specifics from the Negative Implications section above. That's the forcing function: if Do Nothing's costs don't echo the framework's pain points, one of them is wrong
- **Pros and Cons are plain bullets** — no jargon, no hedging
- **The Recommendation is a paragraph, not a vote** — the reader finishes it knowing *why* this option won, not just which one
- **It ends with concrete next steps** — actionable, not analytical

That's the shape yours should take.

---

## Step 4 — Build it

Open scope. Anything that runs on Lightning AI counts:

- **[Studio](https://lightning.ai/docs/overview/studios) template** — a published Studio with a working environment and example notebooks
- **[Agent](https://lightning.ai/docs/overview/build-agents)** — built on the platform's agent tooling, deployed and callable
- **Web app on a Studio** — anything you can `streamlit run` / `uvicorn` / `next dev` on a Studio
- **[Model API](https://lightning.ai/docs/overview/model-apis) integration** — using Lightning's hosted models from your tool
- **CLI tool** — written in any language, running on a Studio or your laptop, hitting Lightning APIs
- **Automation** — a script that runs on a schedule, does a useful thing, leaves a useful trace
- **Internal team tool** — for support, ops, sales, anyone

Use any model, any framework, any cloud option Lightning offers. The only requirement is that it actually runs end-to-end on the platform — not a slide deck describing a thing.

If you've never spun up a Studio before, that's the first thing to do. Start there ([Studio quickstart](https://lightning.ai/docs/overview/studios/quickstart)), get one running, then layer the project on top.

---

## Step 5 — Present

You get a 15-minute slot with the team. Roughly:

- **5 min — User reality.** Read the Current State + Negative Implications from your Value Framework. Make us feel the user's pain. Cite specific moments, not abstractions.
- **5 min — Demo + recommendation.** Show the build running. Walk through your 1:3:1 — what the problem was, what the three options were, why this one. Be honest about Do Nothing.
- **5 min — Future state + Q&A.** What does the world look like for the user when this is in their hands? Then take questions.

We're not grading whether your tool is production-grade. We're grading whether you used the frameworks honestly to think about the problem, and whether you actually shipped something on the platform.

---

## Evaluation rubric

Three axes, equal weight:

### 1. Frameworks used honestly

- Is the **1-liner Value Prop** sharp? If you can't compress it into one sentence, the framework hasn't done its job — the problem isn't crisp enough yet.
- Is the **Current State** in the user's voice, not yours? Would a non-engineer reading it understand what's broken?
- Did you **honestly consider Do Nothing**? Is the cost of inaction named with specifics (not just "the problem continues")?
- Is the **Recommendation defended**, not just stated? Two paragraphs of reasoning, not a one-line vote?
- Did you write **Open Questions**? A blank or generic Open Questions section means you haven't actually thought about what you don't know yet.

### 2. You shipped something on the platform

- It runs on Lightning. End to end.
- We can see it work in the demo.
- The build matches the recommendation in your 1:3:1 (no scope creep mid-project that the framework didn't account for).

### 3. Communication is clear

- Presentation hits the 15-minute window.
- The user's pain comes across in the first 5 minutes — we feel it, not just hear it described.
- The recommendation is defensible — when we ask "why not option 2?", you have a concrete answer.

---

## How long should this take?

Plan for **one to two weeks** end-to-end:

- Day 1: pick the problem, draft Value Framework v1, sit with it
- Day 2–3: revise Value Framework, write 1:3:1, get feedback before you start building
- Day 4–8: build
- Day 9: prepare the presentation, dry-run it once
- Day 10: present

If the build is taking longer than five days, your scope is too big — go back to the 1:3:1 and pick a smaller option.

---

## Resources & links

**Frameworks — canonical guides:**

- [Value Framework HOW to](https://www.notion.so/lightningai/Value-framework-HOW-to-2ff28e47620980c188e9d5516c9ef636)
- [1:3:1 Decision-Making Process](https://www.notion.so/lightningai/1-3-1-Decision-Making-Process-2df28e476209805384fad87009e35955)

**Adjacent reading (optional but useful):**

- [Lightning Engineer Manifesto](https://www.notion.so/lightningai/Lightning-Engineer-Manifesto-1d928e47620980859270f65a19cdf822) — the company's view on what good engineering looks like; the customer-credibility section is especially relevant when picking a project
- [Lightning Platform Fullstack](https://www.notion.so/lightningai/Lightning-Platform-Fullstack-d1ae9aed8d60402db03338207f715cc4) — the T-shape skillset framing; useful context for why "build something on the platform" is part of every onboarding path
- [Value Framework extractor for customer conversations](https://www.notion.so/lightningai/Value-Framework-extractor-for-customer-conversations-1d928e47620980ba8479e7d67cbbcdb9) — examples of value frameworks built from real customer conversations

**Lightning platform docs (for the build):**

- [Lightning Studios](https://lightning.ai/docs/overview/studios) — the core compute environment; almost any build starts here
- [Studio quickstart](https://lightning.ai/docs/overview/studios/quickstart) — get one running in a few minutes
- [Build Agents](https://lightning.ai/docs/overview/build-agents) — agent tooling on the platform
- [Model APIs](https://lightning.ai/docs/overview/model-apis) — Lightning-hosted LLM endpoints
- [Lightning AI Studio gallery](https://lightning.ai/studios) — flip through to see what people have built; good way to gauge scope and find inspiration

---

## One more thing

The frameworks feel like overhead the first time you use them. They feel like alignment after the third. They feel like clarity after the tenth. Trust the process — write the Value Framework even when the project feels obvious, write the 1:3:1 even when "Do Nothing" feels silly. The point of this module isn't the artifact; it's the muscle.
