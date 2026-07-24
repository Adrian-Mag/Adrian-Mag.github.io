## Plan: "The Machine Around the Model" — a series on agentic AI usage
**Status:** active   **Created:** 2026-07-18
**Drafting progress:** Acts 1–11 and the summary complete; final series review and accessibility checks remain.

> Companion: `docs/agent-docs/references/sources/machine-around-the-model-sources.md` — the verified source dossier and artifact
> inventory. No citation enters the series without an entry there.

### Goal

A long-form series that takes a reader who has only used ChatGPT and shows them the
engineering layer that has grown around large language models: what the model actually is,
what the harness around it does, and what parts of that harness a user can build or change.
The arc runs from the chat box everyone knows, through the LLM-as-CPU / harness-as-computer
framing, to the concrete levers — AGENTS.md, skills, hooks, tools/MCP, retrieval, memory,
orchestration.

Aimed at people who have used AI "a little" and concluded it is unimpressive. The central claim is
that their experience was accurate but was a measurement of the *harness*, not the *model*.

---

### Locked decisions (proposed — revise freely)

**D1. Concepts first, real setup as evidence.**
The spine is vendor-neutral concepts; Adrian's actual setup appears as worked examples and
screenshots, the way the AI-usage poster uses exhibits. Rationale: concepts stay true as
tools churn; a pure tour of one setup ages badly and reads as a flex. This also lets the
text say "I am learning this too" honestly — the series can show a real, imperfect, evolving
system rather than a finished product. **This was the open fork before the crash; recorded
here as a decision so it can be overturned deliberately.**

**D2. Not filed under "Notes on Inverse Theory & Inference."**
This series does not belong in the maths group — different audience, different subject.
Proposal: its own homepage section and its own nav grouping next to *AI-Assisted Research*.
See Open Questions Q1.

**D3. Date-stamped and decay-aware.**
The field moves monthly. Each act carries a "current as of" date; version-specific detail
(model names, exact API parameters, product feature names) is confined to clearly marked
call-out boxes so it can be updated or allowed to age visibly without rotting the prose.
Durable mechanics (statelessness, the tool loop, context economy) carry the argument.

**D4. Every mechanism claim must be demonstrable.**
Same standard as the poster: if the text says a hook blocks a command, there is a real
transcript. No invented examples presented as real.

**D5. Directory and naming.**
`pages/research/overview/harness/` with landing `the-machine-around-the-model.html`,
`act-1.html` … `act-N.html`, `summary.html`, `ai-companion.txt` — matching the existing
series layout exactly. CSS at `css/harness.css`.

---

### The arc

Three movements. The two load-bearing reveals are **statelessness** (Act 3) and **the tool
loop** (Act 4) — everything after them is elaboration, so they land early and hard.

#### Movement I — What you are actually talking to

**Act 1 — The Box Everyone Knows.**
Start where the reader is. The naive model: text in, text out, magic in between. Name the
common experience honestly — asked it something, got confident nonsense, concluded the
technology is oversold. Promise: that experience was real, and it was a measurement of the
scaffolding, not the intelligence.

**Act 2 — Inside the Kernel.**
What an LLM actually is: a function from a token sequence to a distribution over next
tokens. Transformer layers, attention, why "layer" here means something entirely different
from the "layers" of the next act. **This ambiguity is the single biggest source of public
confusion and clearing it is the act's job.** The model has no memory, no filesystem, no
clock, no ability to act. It is a pure function. Also: how a raw predictor becomes
chat-shaped (instruction tuning, RLHF).

**Act 3 — Even the Chat Box Is a Harness.**
The hinge of the series. A consumer chat product is already several systems around the
model: a system prompt the user never sees, conversation replay, memory retrieval, tool
access, safety filtering. The reveal: **the API is stateless — the entire conversation is
re-sent on every single turn.** The model does not remember your last message; software
re-reads it to the model each time. "Memory" is an illusion assembled by code. Once this
lands, the rest of the series is inevitable.

#### Movement II — The harness

**Act 4 — The CPU and the Computer.**
The metaphor, formalized. The LLM is a CPU: fast, general, stateless, no I/O of its own. The
harness is everything that makes a CPU useful — memory hierarchy (context window, files,
retrieval), I/O (tools), a clock (the agent loop), an OS (permissions, policy).
Then the mechanism that does the real work: **the model never executes anything.** It emits
a request to use a tool; the harness executes it and appends the result; the loop repeats
until the model stops asking. That loop *is* what "agent" means. Everything else in the
series is a variation on it.

**Act 5 — Anatomy of a Coding Agent.**
Concrete inventory of a large harness: read/write/edit/bash/grep/glob/search tools, a
permission system, context management (compaction, clearing stale tool results), subagents
with their own context windows, session persistence. Small harness vs. large harness, side
by side, same kernel. Why the capability gap is an engineering gap.

#### Movement III — What you can change (ordered by increasing effort and power)

**Act 6 — Steering by Text: AGENTS.md.**
The cheapest lever. A file the harness reads and injects into context. **Not enforced** —
guidance, not law. Why that is simultaneously its weakness (it can be ignored or drowned
out) and its strength (costless to write, instantly changeable). What distinguishes a useful
one from decoration.

**Act 7 — Packaging Expertise: Skills.**
Progressive disclosure: a short description sits in the initial catalogue, and the full body
loads only when relevant. Why this beats one enormous system prompt: context is finite, and
everything loaded competes with everything else.

**Act 8 — Mechanism, Not Trust: Hooks and Permissions.**
Where text stops being enough. Deterministic interception that runs whether or not the model
cooperates for the events the harness exposes. Code moves the decision outside the model, but
the hook is only as strong as its event coverage, matcher, response, trust, and threat model.
The exhibit must be created or captured inside this public website workspace. Do not use
artifacts or session logs from private workspaces.

**Act 9 — New Senses: How a Capability Becomes Available.** *(narrowed — see Resolved, 2nd pass)*
Tool design. Tool definitions as an interface contract; why descriptions are load-bearing —
they are how the model decides *when* to reach for something, not just what it does. The
promote-to-a-dedicated-tool heuristic: start general, promote when you need to gate, render,
audit, or parallelize. Closes with a **short** MCP section: host/client/server, the protocol's
purpose, and the one real invocation on record from the Act 4 trace.

**Act 10 — What It Knows: Context, Retrieval, and Memory.**
Context as the budget everything competes for. RAG as *context assembly*, not magic:
chunking, embedding, retrieval, and the failure modes. Memory as files on disk. Compaction
and why long sessions degrade. Prompt caching and why prefix stability is worth designing
for.

**Act 11 — Orchestration: Loops, Graphs, and Many Agents.**
When one loop is not enough: graph frameworks, subagent delegation, the split between who
supplies the harness and who supplies the deployment. Includes the honest counterweight —
most tasks do not need this, and reaching for orchestration early is the most common
expensive mistake.

**Summary — The Instrument.**
Ties back to the poster's central claim: what all this machinery is *for*. Verification, audit,
honest limits, and a frank section on where it is still bad.

> **11 acts is one or two more than any existing series on the site.** Merge candidates, if
> you want it tighter: Act 4 + Act 5 (concept and inventory), or Act 10 + Act 11. My
> recommendation is to keep 4 and 5 separate — the metaphor and the parts list do different
> jobs — and merge 10 into 11 only if the series feels long in drafting.

---

### Factual guardrails

The series makes claims about how real systems work, to an audience that cannot check them.
Non-negotiables:

- **Distinguish the two "layers"** (transformer layers vs. harness layers) explicitly and
  early. Conflating them would be the series' worst possible error, and it is the exact
  conflation the source voice memo makes — worth naming as a feature of the explanation.
- **Do not overclaim about closed products.** What a specific consumer product does
  internally is largely undocumented. Write about *what a chat product must do* given
  statelessness, and label the general case as general.
- **Separate protocol from product.** Statelessness and the tool loop are properties of the
  API. Hooks, skills, and AGENTS.md are features of *particular harnesses*. Mark which is
  which, every time.
- **Mark version-specific claims** with a date and confine them to call-outs (D3).
- **Verify every citation** before it ships, per the site's existing citation rule —
  genuine, clickable, checked.

Candidate references (all to be verified, none to be cited from memory): Vaswani et al.
2017 (attention); Ouyang et al. 2022 (instruction tuning / RLHF); Lewis et al. 2020 (RAG);
Yao et al. 2022 (ReAct); Schick et al. 2023 (Toolformer); the MCP specification; current
vendor documentation for tool use, context management, and agent architecture.

---

### Files and components

| Path | Purpose |
|---|---|
| `pages/research/overview/harness/the-machine-around-the-model.html` | Landing: hero, act nav, overview, sources |
| `pages/research/overview/harness/act-1.html` … `act-11.html` | The acts |
| `pages/research/overview/harness/summary.html` | Summary + the closing argument |
| `pages/research/overview/harness/agentic-structure-map.html` | House-building robot analogy plus an original hardware-inspired interactive board: context, next-token model, action tools, persistent records, evidence checks, the full prompt-triggered control/recovery loop, optional abilities, and an explicit monitoring gap |
| `pages/research/overview/harness/workspace-explorer.html` | VS Code-style recursive explorer of selected real agent-related paths, showing explanations but never file contents |
| `pages/research/overview/ai-in-practice.html` | Landing for the series, its two interactive maps, and AI-assisted-research material |
| Both workspace maps | Per-file routing explanations: how a Codex or Claude session reaches a file, including their distinct pre-prompt project-context routes; when a skill loads, when a script is actually run, Git's automatic local commit-message check, and Playwright MCP as an optional visible browser ability rather than a workflow. The relationship page uses the same house-building robot analogy, then shows the literal workspace mechanics on a hardware-inspired board. Its control region keeps the whole route visible: bootstrap, skill, provisional continuity note, Git comparison, validator, pass/fail, redacted incident plus repair/revalidate, selected records, four-way plan decision, work, phase landing, refreshed handoff, and revalidation. The blue host/session loop remains separate from the orange workspace routine, and the board marks the absence of permanent monitoring. A workspace task may lead to conditional site maintenance (notes prose/search, CSS or JavaScript/cache, navigation/manual copies, browser validation), a figure or audit script, an optional browser ability, or an independent Git event. It deliberately omits ordinary source files plus the Act 8–9 teaching exhibits. The explorer's `.playwright-mcp/` selection links directly to that ability and labels its contents as scratch output |
| `pages/research/overview/harness/ai-companion.txt` | Reading-companion brief (narrative arc, guardrails) |
| `css/harness.css` | Series stylesheet, following `think-first-discretize-later.css` |
| `index.html` | New homepage section (see Q1) |
| every `*.html` with a nav | Nav dropdown entry — site-wide edit, per AGENTS.md |
| `media/search-index.json` | Rebuilt via `python3 tools/build_search_index.py` |

Diagrams: several acts want figures (the loop, the harness anatomy, context budget). Options
are inline SVG (hand-authored, no build step, theme-aware) or the existing
`figure_generation/` Python pipeline. **Recommendation: inline SVG** — these are conceptual
diagrams, not computed results, and the Python pipeline exists for data figures.

---

### Phases

Each is independently committable.

- **Phase 0 — Approve structure.** Lock the act list, the title, the placement decision
  (Q1), and the concepts-vs-setup call (D1). No files written.
- **Phase 1 — Skeleton.** Directory, `css/harness.css`, landing page, empty acts with
  headings and act nav, site-wide nav update, cache-bust bump. Verifiable in a browser.
- **Phase 2 — Movement I** (Acts 1–3). Includes the statelessness demonstration, which is
  the piece most worth getting right.
- **Phase 3 — Movement II** (Acts 4–5) + the loop and anatomy diagrams.
- **Phase 4 — Movement III, part one** (Acts 6–8). The hooks exhibit must come from this
  public website workspace.
- **Phase 5 — Movement III, part two** (Acts 9–11).
- **Phase 6 — Summary, companion file, citation verification pass, search index rebuild,
  accessibility check** (the site is at Lighthouse 100 on other pages; hold that bar).

### Companion-map review (2026-07-24)

The relationship map and curated explorer were checked against the live workspace and reviewed
with Playwright at desktop and narrow widths. The map now visibly records its review date,
routes all non-terminal arrows around cards, has no node overlap, and returns to Act 11, where
the map is introduced. Every map popup opens with a non-empty explanation; pan, zoom, reset,
and the return link were exercised. The explorer now records its review date, labels its two
active plans and two companion pages honestly as untracked worktree drafts, resolves all 126
curated paths against the workspace, opens every detail pane with route information, and scrolls
when fully expanded. The remaining Phase 6 work is series-wide review, accessibility checks,
and replacing Act 3's labelled mock with a real recording.

### Map layout follow-up (2026-07-24)

The board's Persist/SSD region was moved below Action so their boundaries no longer overlap;
the Observe region now clears the model; the Control frame shifted left; and the downstream
control steps moved down to make the new/resumed-task entry legible. Connectors were rerouted
to the new destinations. A Playwright render confirmed zero node overlaps and no horizontal
overflow at a 390px viewport.

The next routing pass widened Action, left a visible Control-to-Persist gap, and made the
blue host-session return a short top-of-model loop to Conversation so it does not cross the
current-prompt input. The two yellow skill links now terminate at their distinct durable
records: Citation Audit and the Legacy continuity bridge.

The AI material now has a dedicated `ai-in-practice.html` landing beside the research
overview. It gathers the series, its two maps, and AI-assisted-research material; the
homepage and the global dropdown both link to it. The Act 4 map link carries an explicit
source marker, so the map swaps its default Act 11 return button for an Act 4 return.

Drafting note: I write a technically-grounded draft, you revise for voice and for what you
actually believe. Where I am uncertain, the draft will say so inline rather than bluffing —
that uncertainty is data about what you still want to learn.

---

### Resolved (2026-07-18)

**Q1 — Placement: RESOLVED.** New page/section **"Notes on AI in Practice"**, separate from
the inverse-theory notes. Own homepage section, own nav grouping.

**Q2 — Own setup: RESOLVED.** Exhibits appear **only where a real artifact exists**. No
illustrative-but-invented examples anywhere. Where no artifact exists, the act carries the
mechanism in prose and diagram instead. This means the exhibit density is uneven across acts
by design — Acts 6–9 will be artifact-rich, Acts 1–4 largely artifact-free.

**Q3 — Interactivity: RESOLVED — maximise.** Interactive panels are a first-class goal, not
an add-on. Candidate panels are listed per act in the interaction inventory below.

**Q4 — Poster cross-link: RESOLVED.** No relink. The series stands alone.

**Q5 — Name: RESOLVED.** "The Machine Around the Model".

### Interaction inventory (Q3 — maximise)

| Act | Panel | What the reader does | Why it teaches |
|---|---|---|---|
| 2 | Next-token predictor | Type a prefix, see a distribution over next tokens; temperature slider | Makes "it predicts distributions, it does not retrieve answers" visceral |
| 2 | Tokenizer *(illustrative — labelled)* | Type text, watch it split into sub-word units | Kills the "it reads words like I do" intuition. Hand-built vocabulary, **not** a real BPE table; carries a visible label saying so (R4) |
| 3 | Statelessness demo | Toggle "resend history" on/off, watch the model lose the thread | **The series' central reveal, made tactile** |
| 4 | Tool-loop stepper | Step through model → tool request → harness executes → result appended → repeat | Shows the model never acts; the harness does |
| 5 | Small vs large harness | Same prompt, two harnesses, diff the outcome | The capability gap is engineering, not intelligence |
| 6 | Context inspector | Toggle an AGENTS.md on/off, see exactly what enters the context window | Guidance is text injection, not law |
| 7 | Progressive disclosure | Watch a skill's description sit in context, body load on demand | Context economy, visualised |
| 8 | Hook interceptor | Attempt a blocked command, watch the hook deny it deterministically | Mechanism vs. trust |
| 10 | Context budget | Fill a window, watch compaction fire and detail get lost | Context as scarce, paid resource |

All panels: vanilla JS + inline SVG/canvas, no build step, theme-aware, no external calls
(pre-recorded traces, not live API calls — the site is static). Panels degrade to a static
figure where JS is off.

### Resolved (2026-07-18, second pass)

**Q6 — Act 2 depth: RESOLVED — stay shallow.** No excursion into encoder/decoder internals.
Act 2 establishes only the working model — *context in, distribution over next tokens out* —
which is all any later argument needs. The inner "layers" (transformer layers) are **named and
explicitly distinguished** from the outer "layers" (harness scaffolding), and then left alone.
Consequence: the request for a transformer textbook reference (R1) is **withdrawn** — the
original transformer paper suffices for the one architectural mention, with its
machine-translation caveat respected.

**Q7 — Contested claims: RESOLVED — skip entirely.** No "emergent abilities", no scaling-law
extrapolation, no capability forecasting. The series argues from mechanism, which is not in
dispute. Anything requiring "researchers disagree about whether…" is out of scope.

**R4 — Tokenizer panel: RESOLVED — illustrative, and labelled as such.** No real BPE
vocabulary ships. The panel demonstrates *that* text is split into sub-word units and that the
split is unintuitive, using a hand-built illustrative vocabulary. It carries a visible label
saying so. Rationale: the pedagogical point (text is not processed as words) does not require
a real vocabulary, and an unlabelled fake would breach D4.

**Act 9 — Scope: RESOLVED — narrowed to tool design.** Retitled *"New Senses: How a Capability
Becomes Available."* The act is now carried by material that genuinely exists: tool definitions
as interface contracts, why descriptions are load-bearing (they are how the model decides
*when* to reach for something), and the promote-to-a-dedicated-tool heuristic — gate, render,
audit, parallelize. MCP becomes a **shorter closing section** rather than the act's spine:
the protocol's host/client/server roles, and the one real invocation on record — the
`mcp__plugin_playwright_playwright__browser_take_screenshot` calls in the Act 4 trace, where
MCP's namespacing is visible in the tool name itself. Honest scope: "here is the shape of the
standard, and here is the one place I actually use it."

### Open questions (remaining)

**Q8 — Act count.** Still 11, which is one or two more than any shipped series on the site.
Merge candidates remain Act 4 + Act 5, or Act 10 + Act 11. Deferred until drafting reveals
whether the length is real.

### Implementation note (2026-07-21) — Act 6 artifacts

Act 6 uses accessible text popups, reusing the existing `concept-popup.js` modal, rather than
an image of an instruction file. The sole exhibit is a verbatim snapshot of this website's own
`AGENTS.md`. It includes the no-build setup, living-reference routing, cache busting, search-
index rebuild, and local-control bootstrap without exposing unrelated workspaces. The settings/
guidance distinction remains in prose and leads into the mechanisms of Act 8. The interactive
context inspector is explicitly labelled as a mechanism diagram, not a recorded transcript.

### Implementation note (2026-07-24) — Act 7 artifacts

Act 7 uses the open Agent Skills specification as the vendor-neutral spine and dated Codex
documentation for current client behaviour. Its progressive-disclosure panel is a mechanism
diagram built from the real local `website-control` skill: a 70-word description routes to a
120-line `SKILL.md`, whose workflow can invoke a bundled 281-line entry command and 487-line
validator. The page uses screened excerpts rather than complete private control files and
records one real `controlctl.py --repo . begin` result. Live handoff, state, and configuration
records remain local-only. The source dossier
records the publication boundary, exact measures, product boundaries, and verification date.

### Implementation note (2026-07-21) — Act 8 artifacts

Act 8 uses a website-local Codex `PreToolUse` policy protecting the generated search index.
The interactive panel replays four outputs measured by invoking the exact hook process with
documented JSON payloads: one allowed rebuild, one denied deletion, a denied read-only false
positive, and an allowed string-construction gap. Candidate commands were classified and not
executed. A separate ephemeral Codex run produced the live denial extract for the harmless
read, proving that the configuration was wired into the real lifecycle rather than only
tested as a standalone script. Accessible popups expose the complete policy, complete
`hooks.json`, and complete screened live extract. The prose keeps hooks, sandboxing, and
approvals distinct and dates current Codex hook and sandbox behaviour to 24 July 2026.
