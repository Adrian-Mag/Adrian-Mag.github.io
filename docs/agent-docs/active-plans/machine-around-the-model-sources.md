# Source dossier — "The Machine Around the Model"

**Compiled 2026-07-18.** Every entry below was fetched and checked today; none is cited from
memory. Author lists, dates, and identifiers are as returned by the source itself.

Status key: **[V]** verified against primary source today · **[P]** pending verification ·
**[G]** gap — no adequate source yet.

---

## 1. Verified sources

### 1.1 The model itself

**[V] Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, L.,
& Polosukhin, I. (2017). "Attention Is All You Need." arXiv:1706.03762.** Submitted 12 Jun 2017.
<https://arxiv.org/abs/1706.03762>
→ *Act 2.* The transformer architecture.
⚠️ **Caveat that must be respected in the prose:** this paper introduces an encoder–decoder
transformer for **machine translation**. It is not a description of a modern decoder-only
chat LLM. Cite it for the architecture's origin, never as "how ChatGPT works." Getting this
wrong is a common popular-science error and the series should visibly not make it.

**[V] Ouyang, L., Wu, J., Jiang, X., Almeida, D., Wainwright, C. L., Mishkin, P., Zhang, C.,
Agarwal, S., Slama, K., Ray, A., Schulman, J., Hilton, J., Kelton, F., Miller, L., Simens, M.,
Askell, A., Welinder, P., Christiano, P., Leike, J., & Lowe, R. (2022). "Training language
models to follow instructions with human feedback." arXiv:2203.02155.** Submitted 4 Mar 2022.
<https://arxiv.org/abs/2203.02155>
→ *Act 2.* How a next-token predictor becomes chat-shaped (supervised fine-tuning + RLHF).
Verified quotable finding: the 1.3B InstructGPT model's outputs were preferred to those of
the 175B GPT-3, "despite having 100x fewer parameters" — a clean, citable illustration that
capability is not only scale.

### 1.2 Acting and tool use

**[V] Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., & Cao, Y. (2022).
"ReAct: Synergizing Reasoning and Acting in Language Models." arXiv:2210.03629. Published
ICLR 2023.** <https://arxiv.org/abs/2210.03629>
→ *Act 4.* The interleaved reason-then-act loop — the closest thing to a canonical citation
for the agent loop. Verified detail: on HotpotQA and Fever, ReAct interacts with "a simple
Wikipedia API"; reports +34% and +10% absolute success on ALFWorld and WebShop respectively.

### 1.3 Retrieval

**[V] Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., Küttler, H.,
Lewis, M., Yih, W., Rocktäschel, T., Riedel, S., & Kiela, D. (2020). "Retrieval-Augmented
Generation for Knowledge-Intensive NLP Tasks." arXiv:2005.11401. Published NeurIPS 2020.**
<https://arxiv.org/abs/2005.11401>
→ *Act 10.* The origin of "RAG" as a term, and the parametric / non-parametric memory split.
⚠️ **Caveat:** the paper's RAG is a *trained* seq2seq architecture with a dense retriever.
What the industry now calls "RAG" — embed, chunk, retrieve, stuff into a prompt — is a
descendant, not the thing described. The series should say so; the drift is itself a good
teaching point about how vocabulary moves faster than meaning.

### 1.4 Context as a scarce resource — the empirical backbone of Act 10

**[V] Liu, N. F., Lin, K., Hewitt, J., Paranjape, A., Bevilacqua, M., Petroni, F., & Liang, P.
(2023). "Lost in the Middle: How Language Models Use Long Contexts." arXiv:2307.03172.
Published in *Transactions of the ACL* (TACL), 2023.** <https://arxiv.org/abs/2307.03172>
→ Verified verbatim finding: "performance is often highest when relevant information occurs
at the beginning or end of the input context, and significantly degrades when models must
access relevant information in the middle of long contexts." Peer-reviewed — the strongest
citation available for this claim.

**[V] Hong, K., Troynikov, A., & Huber, J. (2025). "Context Rot: How Increasing Input Tokens
Impacts LLM Performance." Chroma technical report, 14 July 2025.**
<https://www.trychroma.com/research/context-rot>
→ 18 models across Anthropic, OpenAI, Google, and Alibaba. Verified verbatim claim: "Large
Language Models (LLMs) are typically presumed to process context uniformly—that is, the model
should handle the 10,000th token just as reliably as the 100th. However, in practice, this
assumption does not hold."
⚠️ **Industry technical report, not peer-reviewed.** Label it as such. Pair it with Liu et al.
(peer-reviewed) so the claim does not rest on vendor-adjacent research alone.

### 1.5 The protocol layer

**[V] Model Context Protocol specification, version 2025-11-25.**
<https://modelcontextprotocol.io/specification/2025-11-25>
→ *Act 9.* Verified architecture, in the spec's own terms:
- **Hosts** — "LLM applications that initiate connections"
- **Clients** — "Connectors within the host application"
- **Servers** — "Services that provide context and capabilities"
- Base protocol: JSON-RPC 2.0, **stateful connections**, capability negotiation
- Server→client features: **Resources**, **Prompts**, **Tools**
- Client→server features: **Sampling**, **Roots**, **Elicitation**
- Explicitly inspired by the Language Server Protocol — a genuinely useful analogy for a
  technical reader, and one the spec itself makes.
- Spec's own security note, worth quoting in Act 8/9: tool descriptions and annotations
  "should be considered untrusted, unless obtained from a trusted server."

**[V] MCP specification release candidate 2026-07-28.**
<https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/>
→ ⚠️ **This is why we searched.** The RC is described as the largest revision since launch,
moving to *a stateless core* that runs on ordinary HTTP infrastructure, plus MCP Apps
(server-rendered UI) and a Tasks extension for long-running work. **My training data predates
this.** Any claim about MCP being stateful must be dated and scoped to 2025-11-25.

### 1.6 Practitioner sources (vendor — label as such)

**[V] Anthropic (2024). "Building Effective Agents." Published 19 December 2024.**
<https://www.anthropic.com/engineering/building-effective-agents>
→ *Acts 4, 11.* Verified verbatim definitions, which the series can adopt:
- **Workflows:** "Systems where LLMs and tools are orchestrated through predefined code paths."
- **Agents:** "Systems where LLMs dynamically direct their own processes and tool usage,
  maintaining control over how they accomplish tasks."
Also the "augmented LLM" building block; five workflow patterns (prompt chaining, routing,
parallelization, orchestrator-workers, evaluator-optimizer); and the counterweight for Act 11:
"Optimizing single LLM calls with retrieval and in-context examples is usually enough."

**[V] Anthropic. "Effective Context Engineering for AI Agents."**
<https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents>
→ *Act 10.* Context engineering as "the natural progression of prompt engineering"; context
framed as "a critical but finite resource."

### 1.7 The CPU / operating-system metaphor — **attribution required**

Your central metaphor is not novel, which is good news: it is a well-established framing with
real provenance, so it should be *cited* rather than presented as your own coinage.

**[V] Karpathy, A. (2023). Post on X, 28 September 2023.**
<https://x.com/karpathy/status/1707437820045062561>
→ Describes LLMs "not as a chatbot, but the kernel process of a new Operating System."
Popularised the framing. ⚠️ A social-media post is a weak citation — cite it as the
popularisation, not as the source of record.

**[P] Ge, Y., et al. (2023). "LLM as OS, Agents as Apps."**
→ Search results credit this with the earliest systematic articulation. **Not yet verified —
I have not fetched it, and the author list and arXiv ID are unconfirmed.** Must be verified
before it appears anywhere in the series.

Your specific refinement — *the model is the CPU, the harness is the rest of the computer,
and the harness is what changed* — is a sharper and more useful framing than "LLM as OS",
because it locates the engineering where it actually happened. That framing can be presented
as yours, with these two as acknowledged predecessors.

---

## 2. Gaps — claims I cannot currently source to your standard

**[G] How ChatGPT actually works internally (Act 3).**
This is the single biggest exposure in the series. The internals of a closed consumer product
are not publicly documented; most online accounts are inference or reverse-engineering.
**Mitigation, which I recommend adopting as a rule:** Act 3 argues from *necessity*, not from
insider knowledge — given a stateless model API, any chat product **must** re-send
conversation state, **must** inject a system prompt, and **must** assemble context somehow.
That argument is airtight and needs no leaked details. Where a specific product's behaviour is
described, cite that vendor's own published documentation and date it.

**[G] A citable reference for decoder-only LLM mechanics (Act 2).**
"Attention Is All You Need" does not cover it (see caveat above). I need a canonical,
citable, preferably peer-reviewed or textbook treatment of how a modern decoder-only LLM
actually processes context. See request R1 below.

**[G] Tokenization (Act 2 interactive panel).**
The panel needs a real tokenizer to be honest. Options: ship a small real BPE vocabulary,
or clearly label the panel as illustrative. **A fake tokenizer presented as real would violate
D4** — so this must be decided explicitly, not fudged.

**[P] Schick, T., et al. (2023). "Toolformer: Language Models Can Teach Themselves to Use
Tools." arXiv:2302.04761.** → Not yet verified. Minor citation; verify or drop.

**[G] Claude Code / harness-specific features (Acts 6–8).**
Hooks, skills, and AGENTS.md are features of particular harnesses and are moving targets. They
must be cited to current vendor documentation with an access date, and confined to the
version-marked call-outs described in D3 of the plan. My internal reference material for the
Claude API is current to 2026-06-24 and is authoritative for API-level facts (statelessness,
the tool-use loop, context management, prompt caching) — but *not* for harness features, which
I will fetch and date at drafting time.

---

## 3. What I'd like from you

You offered to supply papers. These are the places where having the actual PDF would move me
from "confident" to "certain":

**R1 — A canonical reference for modern LLM mechanics (highest value).**
For Act 2 I want something citable and durable rather than a blog post. Best candidates:
- Jurafsky & Martin, *Speech and Language Processing*, 3rd edition — the transformer and
  large-language-model chapters. Free online, updated, widely cited, textbook-grade.
- Bishop & Bishop, *Deep Learning: Foundations and Concepts* (2024) — transformer chapter.
- Elhage et al., "A Mathematical Framework for Transformer Circuits" (Anthropic, 2021) — much
  deeper; only worth it if Q6 resolves toward real depth.

If you have any of these as PDFs in your `references/`, point me at them and I'll read them
properly with the pdf-source-reading skill rather than working from recollection.

**R2 — Your own artifacts (blocking for Acts 6–9).**
Per D2, exhibits only exist where an artifact exists. To plan those acts concretely I need to
know what you actually have: hook denial transcripts, a representative AGENTS.md, a skill
definition, an MCP server config, session logs showing a tool loop. The poster used several of
these already. **Tell me what exists and I'll design the acts around the real material rather
than around what would be convenient.**

**R3 — A decision on Q6 and Q7** (Act 2 depth; whether to touch contested claims).

**R4 — Optional, if you want the tokenizer panel to be real:** confirm whether shipping a
real BPE vocabulary in the repo is acceptable, or whether the panel should be labelled
illustrative.

---

## 3b. Artifact inventory (surveyed 2026-07-18)

Located on the local machine. **Privacy screened** for IPs, emails, keys, tokens, and
hostnames — see the note at the end of this section.

### Act 8 — Hooks: `privacy_guard.py` **[V, publishable as-is]**

`~/PhD/{PLI_paper,BGP_Paper,thesis}/.claude/hooks/privacy_guard.py` — 112 lines, plus the
16-line `settings.json` that wires it as a `PreToolUse` hook matching `Bash|WebFetch|WebSearch`.
Identical in PLI_paper and BGP_Paper; the thesis copy differs (worth diffing for the act —
divergence across workspaces is itself a point about maintaining policy).

Why it is a strong exhibit: the whole mechanism is legible in one screen. Wiring
(`matcher` → `command`), decision protocol (JSON `permissionDecision: deny|allow`), pattern
table, and — lines 98–102 — **a documented carve-out with a comment explaining why europa is
exempt.** The audited exception the poster claims is visible in the source.

⚠️ **Honesty requirement — this is a blocklist, and blocklists have gaps.**
The patterns catch `curl`, `wget`, `ssh`, `scp`, `rsync`, `git push`, `gh`, package managers.
They do **not** catch, for example, `python3 -c "import urllib.request; ..."` or any script
that performs network I/O internally. The guard is genuine defence against *accidental* egress
and against an agent casually reaching for a network tool — which is the real threat model.
It is **not** a sandbox and would not stop a determined adversary.

The poster's "0 bytes of unpublished work ever transmitted; blocked mechanically" is stronger
than the mechanism strictly supports. **Recommendation: Act 8 states the limitation
explicitly.** A security-literate reader spots the gap in seconds; pre-empting it is far more
credible than being caught by it, and "here is my guard, here is precisely what it does not
cover" is a better argument for the engineering-over-trust thesis than an absolute claim.
This also makes Act 8 the natural home for the general lesson: *mechanisms have threat models,
and a mechanism without a stated threat model is marketing.*

### Act 7 — Skills: progressive disclosure, measured **[V, publishable]**

Six user-scope skills at `~/.claude/skills/`: `europa`, `long-missions`, `paper`,
`pdf-source-reading`, `plan-docs`, `slidev`.

**`slidev` is the ideal exhibit — three tiers, real numbers:**

| Tier | Content | Size | When loaded |
|---|---|---|---|
| 1 | `description:` frontmatter | **34 words** | Always in context |
| 2 | `SKILL.md` body | **190 lines** | On trigger |
| 3 | `references/` | **3,721 lines across 53 files** | On demand |

A ~34-word permanent footprint gates roughly 3,900 lines of material. That ratio *is* the
lesson of Act 7, and it is measured from a real skill rather than asserted.

`paper` shows the same shape with mode-specific references (`mode-audit.md` 319 lines,
`mode-proofread.md` 151, `mode-verify.md` 131) plus executable `scripts/`
(`crossref_lookup.py` 272 lines, `zotero_lookup.py` 187) — a good second exhibit showing a
skill can carry code, not just prose.

**A demonstration worth using in the act:** the skill *descriptions* are visible in the
agent's context at all times, while the bodies are not — the agent must read the file. The
series can show this directly rather than describing it, since the drafting agent's own
context is the demonstration.

### Act 6 — AGENTS.md **[V, publishable]**

`~/PhD/Adrian-Mag.github.io/AGENTS.md` (42 lines) — a real, working example with commit
convention, cache-busting rule, and the search-index rebuild step. Good because it is
*mundane*: it shows guidance is ordinary text about ordinary constraints, not incantation.
Pairs well with `~/.claude/settings.json` (26 lines) to show the settings/guidance split.

### Privacy screen result

Scanned all skills for IPs, emails, SSH keys, API keys, tokens, passwords. **All matches were
documentation *about* secrets, not secrets** — Slidev's `--password` CLI flag, a `0.0.0.0`
bind address in docs, and `long-missions/SKILL.md:271`: "Keep status file contents free of
secrets (no keys, tokens, passwords)". `europa/SKILL.md` describes the machine abstractly with
no hostname, IP, or username. **Nothing above requires redaction** — unlike the poster's
Exhibit 2, which needed an IP removed.
⚠️ Re-run this screen at drafting time; files change.

### Act 8 — live denial events **[V, found 2026-07-18 — redaction required]**

Source: `~/.claude/projects/-home-adrian-PhD-BGP-Paper/3bb23525-….jsonl` — **6 genuine live
denials**. Extracted by joining `tool_result` records containing the guard's reason strings to
the parent assistant `tool_use` on `tool_use_id`, so only the denial events were read, not
surrounding conversation.

**The single best exhibit in the whole series:**

```
$ grep -nc 'sigma' BGP/BGP_draft.tex
✗ DENIED: "Network socket and transfer commands are blocked in this paper workspace."
```

The guard blocks a **read-only `grep`** because the pattern `\b(nc|netcat|telnet|ftp|lftp)\b`
matches the `-nc` in `grep -nc` — a hyphen is a word boundary, so the netcat rule fires on a
grep flag. Completely benign command, confidently blocked, for a reason that is obvious once
seen and invisible beforehand.

This is a better teaching example than the poster's "curl in a commit message" because the
reader can *derive* the bug from the regex printed two paragraphs earlier. It demonstrates in
one line: blocklists over-block; the over-blocking is not random but mechanical; and a rule
you can read is a rule you can debug. Two occurrences (2026-07-13T12:14:56Z, 12:15:05Z).

Other genuine denials, all usable:

| Command | Reason given | Character |
|---|---|---|
| `curl --version` | Network download/upload blocked | Harmless version check, blocked |
| `... npx slidev --port 3030 … curl -s …` | Network download/upload blocked | **Localhost-only** call, blocked |
| `ssh-add -l; ls ~/.ssh/ …` | Remote shell/file transfer blocked | Arguably a correct block |
| `echo "SSH_AUTH_SOCK=…"` | Remote shell/file transfer blocked | Env inspection, blocked |

⚠️ **REDACTION REQUIRED — europa's real IP address appears in the thesis session log**
(2026-07-10T11:37Z), inside a recovered record of the `ssh … && europa release PLI_PAPER`
attempt. This is precisely what the poster redacted in Exhibit 2. **Any exhibit drawn from
these logs must be screened for it.** Treat the IP as never-publish.

⚠️ **Do not overcount the thesis log.** A naive text search reports 10 "denials" in
`-home-adrian-PhD-thesis/1974e3cb-….jsonl`, but most are false matches: the agent was
*diffing or reading `privacy_guard.py` itself*, so the guard's reason strings appear as file
content rather than as denial events. Only ~1 is genuine. **The honest count is ~6 live
denials in BGP_Paper**, and the series should use that number rather than the naive one —
a small thing, but the series' entire claim is that its numbers are checked.

### Act 9 — MCP: **thin, and this constrains the act**

`~/.claude.json` declares exactly **one** MCP server (`slidev`), at top level plus BGP_Paper
scope. There is no rich MCP deployment to exhibit.

Under D2 (artifacts only), Act 9 therefore **cannot** carry MCP on your own setup. Options:
(a) teach MCP conceptually from the specification, with the single real server as the one
concrete instance; (b) build something real first and exhibit it; (c) shrink Act 9 to tool
*design* — where the `privacy_guard` matcher and the skills provide real material — and treat
MCP as a shorter closing section. **Recommendation: (a) or (c).** Flagging because it is the
one act where the artifacts-only rule genuinely bites.

### Act 4 — tool-loop trace **[V, found 2026-07-18]**

**Sourced from the website repo's own session logs, deliberately** — that repo is public by
construction, so unlike the paper workspaces there is no confidential content to screen.

**Exhibit 4a — the minimal loop** (`5288737a-….jsonl`, 2026-07-18T16:44Z). Three lines, the
entire mechanism:

```
model ASKS       →  Bash: pwd
harness RETURNS  ←  /home/adrian/PhD/Adrian-Mag.github.io
model says          "Same workspace as before: … on the main branch, under WSL2."
```

The model did not run `pwd`. It *asked*. The harness ran it and appended the answer. Use this
before anything more complex — it is the whole of Act 4 in three lines.

**Exhibit 4b — the loop iterating** (`6f674b3c-….jsonl`, 2026-07-18T12:18–12:19Z). A real
repeating cycle from the session that drafted this series, while inspecting the author's own
poster page:

```
model ASKS  → browser_run_code_unsafe   (scroll the page)
harness ←     "ok"
model ASKS  → browser_take_screenshot
harness ←     [Screenshot of viewport] → ai-page-5.png
model ASKS  → Read: ai-page-5.png
…cycle repeats for ai-page-6.png, ai-page-7.png…
```

Why it teaches well: the model cannot *see* a web page. To look at one it must ask for a
scroll, ask for a screenshot, then ask to read the resulting file — three round trips for one
human glance. The asymmetry between "look at the page" and what that actually costs is the
most vivid available argument that the harness, not the model, does the work.

**Bonus — this partly rescues Act 9.** The tool names in the trace are literally
`mcp__plugin_playwright_playwright__browser_take_screenshot`. The MCP namespacing is visible
in the tool name itself: an MCP server's tools arrive prefixed and namespaced. So a *real* MCP
invocation is on record even though the MCP deployment is thin — Act 9 can show MCP being used
rather than only described.

**Self-referential framing available:** these traces come from the session that built the
series, inspecting the site the series lives on. Worth considering as a deliberate device — it
makes the exhibits unfalsifiable-by-construction (the reader is looking at the machinery that
produced the page they are reading) and costs nothing.

⚠️ **Extraction caveat — must be fixed before shipping.** The trace above was produced with a
filter skipping log lines >200 KB (base64 screenshot payloads). **Some tool results are
therefore missing from the printed sequence** — e.g. no `RES` appears after each
`Read: ai-page-N.png`. Publishing it as-is would show a loop with silently dropped steps,
which violates D4. Regenerate without the size filter, or mark the elisions explicitly the way
the poster marks them.

### Still missing

- **Session transcripts showing a live hook denial.** The poster's Exhibit 2 used real session
  logs; the code alone shows the mechanism but not the *event*. The Act 8 interactive panel
  wants a real denial trace. Source: `~/.claude/history.jsonl` or `projects/` session logs —
  **not yet examined, and it needs care: session logs may contain unpublished paper content.**
- **MCP server configuration** for Act 9 — user-scope MCP is configured per memory, but I have
  not located and screened the config.
- **A tool-loop trace** for the Act 4 stepper — needs a real transcript of
  model → tool request → result → repeat.

## 4. Standing rules for this series

1. **No citation from memory.** Every reference is fetched and checked before it ships. This
   file is the record.
2. **Date every claim about a product or protocol.** MCP alone changed between my training
   data and today.
3. **Separate protocol from product, and peer-reviewed from vendor.** Mark each inline.
4. **Argue from necessity where internals are undocumented** rather than asserting them.
5. **No invented exhibits.** (D4.) If there is no artifact, there is no exhibit.
6. **Where the literature disagrees, say so** rather than picking the tidier side.
