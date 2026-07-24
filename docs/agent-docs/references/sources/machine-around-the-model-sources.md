# Source dossier — "The Machine Around the Model"

**Compiled 2026-07-18; updated through 2026-07-24.** Entries record their own checked dates;
none is cited from memory. Author lists, dates, and identifiers are as returned by the source
itself.

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

**[V] Model Context Protocol specification, version 2025-11-25. Checked 24 July 2026.**
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

**[V] MCP specification release candidate targeting 2026-07-28.**
<https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/>
→ Published **21 May 2026**; the date in the title and URL is the targeted specification
version, not the post's publication date. The RC is described as the largest revision since
launch, moving to a stateless core that runs on ordinary HTTP infrastructure, plus MCP Apps
(server-rendered UI) and a Tasks extension for long-running work. As checked on **24 July
2026**, `/specification/latest` still redirects to the stable 2025-11-25 specification; the
2026-07-28 release remains a draft candidate scheduled for 28 July. Act 9 therefore teaches
the stable 2025-11-25 architecture and does not present RC internals as current protocol.

### 1.6 Practitioner sources (vendor — label as such)

**[V] Anthropic (2024). "Building Effective Agents." Published 19 December 2024; checked
24 July 2026.**
<https://www.anthropic.com/engineering/building-effective-agents>
→ *Acts 4, 11.* Verified verbatim definitions, which the series can adopt:
- **Workflows:** "Systems where LLMs and tools are orchestrated through predefined code paths."
- **Agents:** "Systems where LLMs dynamically direct their own processes and tool usage,
  maintaining control over how they accomplish tasks."
Also the "augmented LLM" building block; five workflow patterns (prompt chaining, routing,
parallelization, orchestrator-workers, evaluator-optimizer); and the counterweight for Act 11:
"Optimizing single LLM calls with retrieval and in-context examples is usually enough."

**[V] Anthropic. "Effective Context Engineering for AI Agents." Checked 24 July 2026.**
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

**[V, restored to public exhibit 2026-07-24 by explicit author decision] Karpathy, A. (2023). "LLM OS" diagram, post on X, 11 November 2023.**
<https://x.com/karpathy/status/1723140519554105733>
→ Former source of Act 4, Figure 1. The block diagram places the LLM in the CPU position with the
context window drawn inside it as RAM, plus tools, disk, network and other models as attached
boxes. Post text supplied by the author 2026-07-21 and the URL confirmed by web search.

**Date verification.** x.com returns HTTP 402 to automated fetches, so the date could not be
read off the page. It is derived from the Twitter snowflake ID instead: `id >> 22` plus the
Twitter epoch `1288834974657` ms gives 2023-11-11T00:48Z. The method self-validates, because
applying it to the already-verified 28 September post above reproduces that date exactly.
Note the UTC boundary: in US time zones this post reads as 10 November.

**Why it earns a figure.** The specs quoted in the post (GPT-4 Turbo at 20 tok/s, 128K RAM,
Ada002 filesystem) are now all obsolete while the boxes and arrows are not. That contrast is
used in the act as evidence for the series' own date-stamping discipline, so the exhibit
argues the method as well as the metaphor.

**⚠️ RIGHTS — third-party exhibit.** The image is not the author's work and is not covered by
the site's CC BY 4.0 licence. It is reproduced for commentary and criticism with attribution in
the exhibit bar, caption, and reference 2. **If Karpathy or X objects, remove the image; the
act's argument survives without it, since the prose describes the diagram.** Do not add further
third-party images without the same treatment.

**[P] Ge, Y., et al. (2023). "LLM as OS, Agents as Apps."**
→ Search results credit this with the earliest systematic articulation. **Not yet verified —
I have not fetched it, and the author list and arXiv ID are unconfirmed.** Must be verified
before it appears anywhere in the series.

Your specific refinement — *the model is the CPU, the harness is the rest of the computer,
and the harness is what changed* — is a sharper and more useful framing than "LLM as OS",
because it locates the engineering where it actually happened. That framing can be presented
as yours, with these two as acknowledged predecessors.

### 1.8 AGENTS.md discovery and scope (Codex, product-specific)

**[V] OpenAI. "Custom instructions with AGENTS.md." Codex documentation. Checked 24 July
2026.** <https://learn.chatgpt.com/docs/agent-configuration/agents-md>
→ *Act 6.* Official current behaviour for Codex, verified through the current Codex manual:
- Codex builds the instruction chain once per run (once per launched TUI session).
- Global scope checks `AGENTS.override.md`, then `AGENTS.md`, in the Codex home directory.
- Project scope walks from the project root down to the current working directory and includes
  at most one applicable instruction file per directory.
- More local guidance appears later and takes precedence where instructions conflict.
- Empty files are skipped; combined project guidance stops at `project_doc_max_bytes`, whose
  default is 32 KiB.
- OpenAI describes `AGENTS.md` as persistent project guidance and explicitly recommends pairing
  it with enforcing infrastructure such as pre-commit hooks, linters, and type checkers.

⚠️ **Product/date boundary:** these are Codex discovery rules as checked on the date above,
not properties of language models and not a promise about every harness that recognises the
filename. The durable claim is only that a supporting harness finds ordinary text and adds it
to model context.

### 1.8a Codex project configuration (product-specific)

**[V] OpenAI. "Config basics" and "Advanced Configuration." Codex documentation. Checked
22 July 2026 through the current Codex manual.**
<https://learn.chatgpt.com/docs/config-file/config-basic>
<https://learn.chatgpt.com/docs/config-file/config-advanced>
→ *Workspace routing maps.* Codex loads project-scoped `.codex/config.toml` layers only in a
trusted project. It walks from the project root toward the current working directory; if the
same setting appears more than once, the closest file wins. Project settings take precedence
over profile, user, system, and built-in defaults, but command-line overrides take precedence
over project settings.

The configuration reference says `developer_instructions` are injected before `AGENTS.md`.
This workspace uses that setting to direct Codex to the same local control bootstrap named by
its `AGENTS.md`. It is therefore an automatic, Codex-specific start route for applicable runs,
not a skill selected later. It is still guidance supplied to the model: sandboxing, approvals,
and hooks are separate technical controls. A project config is not read for an untrusted
project, and it has no effect on Claude or another client that does not support this file.

The current command reference defines `codex resume` as continuing a previous interactive
session. It does not by itself establish a universal project-file rediscovery sequence for
every Codex surface. The stronger start-or-resume statement on the workspace map comes from
this workspace's own checked `.codex/config.toml` and `AGENTS.md`: both explicitly instruct an
agent to read `BOOTSTRAP.md` at task start or resume. The map therefore presents this as local
workspace policy. It distinguishes automatically supplied startup guidance from the subsequent
explicit file route: startup guidance → `BOOTSTRAP.md` → selected `SKILL.md`.

### 1.9 Agent Skills: open format and current harness behaviour

**[V] Agent Skills. "Specification." Checked 24 July 2026.**
<https://agentskills.io/specification>
→ *Act 7.* Primary specification for the portable file format. A skill is a directory whose
required entry point is `SKILL.md`, with required `name` and `description` frontmatter and a
Markdown instruction body. Optional `scripts/`, `references/`, and `assets/` directories carry
executable helpers, documentation, and static resources. The specification describes three
progressive-disclosure tiers: metadata at startup, the full `SKILL.md` after activation, and
supporting resources only as required. It recommends keeping the main file below 500 lines.

⚠️ **Protocol/product boundary:** this source specifies the shared format and intended loading
shape. Discovery paths, context budgets, invocation controls, and lifecycle details belong to
individual clients and must not be presented as universal properties of the format.

**[V] OpenAI. "Build skills." Codex documentation. Checked 24 July 2026 through the current
Codex manual.** <https://learn.chatgpt.com/docs/build-skills>
→ *Act 7.* Current Codex behaviour. The initial skills catalogue supplies each skill's name,
description, and file path; Codex reads the full `SKILL.md` when it selects the skill. A skill
can be selected explicitly or implicitly from a task matching its description. The initial
catalogue is limited to at most 2% of the model context, or 8,000 characters when the context
window is unknown; the full selected body is outside that catalogue budget. User skills are
discovered under `~/.agents/skills/`, with repository, administrator, and bundled system scopes
also documented. These details are product-specific and date-stamped.

**[V] Anthropic. "How Claude remembers your project." Claude Code documentation. Checked 22
July 2026.** <https://code.claude.com/docs/en/memory>
→ *Act 6, Act 7, and the workspace routing maps.* Claude Code reads `CLAUDE.md`, not
`AGENTS.md`; a repository that shares `AGENTS.md` with another agent can use a `CLAUDE.md`
import or symlink instead. This workspace instead uses an unscoped
`.claude/rules/website-control.md` symlink to the canonical `BOOTSTRAP.md`: rules without a
`paths` frontmatter field load at launch with the same priority as `.claude/CLAUDE.md`, and
symlinks in `.claude/rules/` are resolved and loaded normally. Rules with `paths` load only
when Claude reads a matching file.

The same source distinguishes rules from skills: task-specific skills load only when invoked or
when Claude judges them relevant to the prompt. The matching
`.claude/skills/website-control` symlink therefore exposes the canonical skill as an additional
discovery route, while the unscoped rule gives the mandatory start instruction. Treat all
discovery, invocation, persistence, and compaction details here as Claude Code product
behaviour, not as part of the open format.

### 1.10 Hooks, sandboxing, and approvals (Codex, product-specific)

**[V] OpenAI. "Hooks." Codex documentation. Checked 24 July 2026 through the current Codex
manual and live documentation.** <https://learn.chatgpt.com/docs/hooks>
→ *Act 8.* Current Codex hook lifecycle and wire format:
- Codex discovers hooks beside active configuration layers, including a trusted project's
  `.codex/hooks.json`; non-managed command hooks must be reviewed and trusted before running.
- A `PreToolUse` hook receives one JSON object on standard input. For Bash, the object reports
  `tool_name: "Bash"` and the command in `tool_input.command`.
- A supported call can be denied before execution by returning the documented
  `hookSpecificOutput` object with `hookEventName: "PreToolUse"`,
  `permissionDecision: "deny"`, and a reason. Exit status 2 plus a reason on standard error is
  also supported.
- As checked on this date, pre/post hooks cover Bash, unified exec, `apply_patch`, MCP calls,
  and most local function tools, but not hosted tools such as web search. Some specialised tool
  paths may opt out. OpenAI therefore describes tool hooks as a useful guardrail, not a complete
  enforcement boundary.
- Matching command hooks for the same event can run concurrently; one hook should not be
  described as a universal serial gateway for all other matching hooks.
- Unsupported blocking fields can make a hook run fail and allow the tool call to continue.
  Hook trust, event coverage, response validity, and the policy code itself all belong in the
  threat model.

**[V] OpenAI. "Sandbox." Codex documentation. Checked 24 July 2026.**
<https://learn.chatgpt.com/docs/sandboxing>
→ *Act 8.* The sandbox and approval policy are distinct controls. The sandbox defines enforced
technical boundaries, including filesystem and network access; the approval policy determines
when the agent must stop and ask before crossing those boundaries. Commands spawned by the
agent inherit the sandbox. This is the source for distinguishing a user-written hook from the
harness's built-in permission boundary.

### 1.10a Codex lifecycle-hook coverage for the Agent Ledger (product-specific)

**[V] OpenAI. "Hooks." Codex documentation. Checked 24 July 2026 through the current Codex
manual.** <https://learn.chatgpt.com/docs/hooks>
→ *Workspace explorer and Agent Ledger documentation.* The current manual says project-local
hooks load only for trusted project configuration and changed non-managed command hooks need
review/trust. Matching command hooks for the same event are launched concurrently. It lists
`UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `PreCompact`, `PostCompact`, `Stop`, and
`SessionEnd`; `Stop` is a turn-stage hook, while `SessionEnd` runs when the main thread ends.

The same checked documentation says local pre/post tool hooks cover shell commands, unified
exec, patches, MCP calls, and most local function tools, but not hosted tools such as web
search; specialised paths can opt out. The Agent Ledger's Codex adapter is therefore described
as **shadow-mode, partial local-hook evidence**, never a complete trace or an enforcement
boundary. Its code reduces the hook payload to a controlled event category, opaque phase token,
and optional coarse tool class; prompts, transcript paths, raw tool names, arguments, and
outputs are excluded by both adapter and schema.

⚠️ **Product/date boundary:** these are Codex behaviours as checked on the date above. Hooks
are features of a particular harness, not properties of language models or of the model API.

### 1.10a Git commit hooks (Git-specific)

**[V] Git. "githooks" documentation. Checked 22 July 2026.**
<https://git-scm.com/docs/githooks>
→ *Workspace routing maps.* Git hooks are executable programs which Git invokes at named
points in its own execution. Git normally looks in `$GIT_DIR/hooks`, or in the directory named
by `core.hooksPath`. The `commit-msg` hook receives the path to Git's proposed commit-message
file; a non-zero exit status aborts the commit, and `git commit --no-verify` can bypass it.

**Local workspace evidence, checked 22 July 2026.** This clone has
`core.hooksPath = .githooks`, and `.githooks/commit-msg` is executable. It therefore runs
automatically when this clone makes a local commit, regardless of whether the committer is a
person or an agent. The checked-in script only examines `feat`, `fix`, and `refactor` subjects;
it warns about a missing or absent `Plan:` target, then exits zero, so it is intentionally
warn-only. The setting is per clone, not a property of a model or an agent, and the public map
must not imply that it applies to GitHub web commits or every clone automatically.

### 1.10b Playwright MCP as an optional client ability (product-specific)

**[V] Microsoft. "Playwright MCP." Checked 22 July 2026.**
<https://github.com/microsoft/playwright-mcp>
→ *Workspace routing map.* The official project describes Playwright MCP as an MCP server for
browser automation. Its standard configuration starts `@playwright/mcp` through `npx`; the
server offers structured browser interaction to an MCP client. The source distinguishes MCP
from its separate CLI-and-skills approach and lists browser automation as the server's purpose.

**Local workspace boundary, checked 22 July 2026.** An enabled user-level client plugin makes
this ability available in compatible agent sessions, but no tracked workspace instruction,
skill, hook, plan, or control recipe requires it or decides when to choose it. The relationship
map must therefore show it as visible optional capability, not as an automatic workflow. The
ignored `.playwright-mcp/` folder contains disposable screenshots, page snapshots, and console
captures from prior browser checks; it is not loaded as agent memory or reused automatically.
The explorer's folder explanation links back to the relationship-map ability node so the output
folder is not mistaken for the capability that produced it.

### 1.11 Tool definitions as interface contracts

**[V] OpenAI. "Function calling." API documentation. Checked 24 July 2026.**
<https://developers.openai.com/api/docs/guides/function-calling>
→ *Act 9.* In the current OpenAI API, a function tool definition supplies a name, a
description of when and how to use the function, and parameters expressed as JSON Schema.
The documented best practices call for clear names, detailed parameter descriptions, explicit
purpose and output shape, and guidance about when the tool should and should not be used.
This supports the act's claim that a description participates in tool selection. Keep the
wire-format details scoped to this API and date; the broader, durable point is that the model
only sees the interface the harness places in context.

**[V] Model Context Protocol. "Tools," specification version 2025-11-25. Checked 24 July
2026.** <https://modelcontextprotocol.io/specification/2025-11-25/server/tools>
→ *Act 9.* A stable MCP tool definition includes a name, optional title and description,
an `inputSchema`, optional `outputSchema`, and optional annotations. Output schemas enable
clients to validate and type structured results. The specification warns that annotations are
hints, not enforcement, and should be treated as untrusted unless they come from a trusted
server. This is the contract shape used by the website-local teaching tool; that local tool is
not represented as a deployed MCP server.

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

**[V] Hooks and remaining harness-specific features (Act 8).**
Current Codex hook behaviour, sandboxing, and approvals are verified and dated in Section
1.10. Keep every claim scoped to Codex as checked on 24 July 2026; do not generalise the event
names, discovery paths, or response schema to every harness.

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

### Act 9 — Tools: website-local contract and recorded calls **[V, publishable; 2026-07-21]**

The principal exhibit is built and recorded entirely inside this public repository:
- `figure_generation/harness/tool_demo/inspect_site_page.py` is a real read-only handler for
  this static site. It accepts a repository-relative HTML path and returns the page title,
  meta description, heading outline, and local stylesheet/script references.
- `figure_generation/harness/tool_demo/tool.json` is the complete MCP-shaped interface
  contract. It has a precise selection description, JSON Schema input and output, and
  read-only/idempotent annotations. It is a teaching contract, not a claim that this repository
  runs an MCP server.
- `figure_generation/harness/record_tool_demo.py` invokes the exact handler in a subprocess
  for one allowed path and one traversal attempt. It writes the complete capture to
  `media/research/harness/tool-demo.json`.

The handler resolves the requested path before reading it, rejects anything outside the
repository, requires an existing `.html` file, and returns stable structured data instead of
raw page prose. The recorded traversal case is a real rejection from that code, not a drawn
or reconstructed outcome. The tool demonstrates three promotion pressures directly: gating,
rendering, and auditability. Parallelization is presented as a separate design heuristic, not
as something this single-page handler performs.

The closing MCP exhibit reuses the already-screened Act 4 trace in
`media/research/harness/toolloop.json`. Its first `iterating` request records the model asking
for `mcp__plugin_playwright_playwright__browser_take_screenshot` with
`ai-page-5.png`, followed by the harness's screenshot result. The page labels the namespace as
product-side naming visible in this trace, not as a naming rule imposed by the MCP protocol.
No private MCP configuration or private-workspace session is needed or published.

### Act 8 — Hooks: website-local policy and live denial **[V, publishable; 2026-07-21]**

The complete public exhibit lives in this repository:
- `figure_generation/harness/hook_demo/public_asset_guard.py` is a real Codex `PreToolUse`
  command hook. It protects `media/search-index.json`, allows the exact supported rebuild
  command, and denies any other Bash command containing that literal path.
- `figure_generation/harness/hook_demo/hooks.json` is the complete project hook wiring used
  for the capture. A temporary identical copy was placed at `.codex/hooks.json` for the live
  run, then removed after capture so this teaching policy does not silently become permanent
  workspace control.
- `figure_generation/harness/record_hook_demo.py` sends documented hook payloads to the exact
  process and records the results in `media/research/harness/hook-probes.json`. Candidate
  commands are classified, never executed.
- `media/research/harness/hook-live-denial.txt` is a screened extract from an ephemeral Codex
  run. Codex requested `rg -l title media/search-index.json`; the router reported that the
  `PreToolUse` hook blocked it before execution and surfaced the hook reason to the model.

The four recorded probes deliberately expose the threat model: the approved rebuild is
allowed; a direct deletion is denied; a harmless read is over-blocked; and a path assembled
from two strings evades the literal matcher. The latter two are a real false positive and a
demonstrated classifier gap. The gap command was never executed. Session/turn identifiers,
usage metadata, and startup warnings were omitted from the live extract; no denial text was
reconstructed. All published artifacts originate in this public website workspace and were
screened with the standing sensitive-string rules.

### Act 7 — Skills: progressive disclosure, measured **[V, screened teaching excerpts; 2026-07-24]**

The real local `website-control` skill is the Act 7 exhibit. Its exact frontmatter description
is **70 whitespace-delimited words**, its `SKILL.md` is **120 lines**, its bundled
`scripts/validate_control.py` is **487 lines**, and its bundled `scripts/controlctl.py` is
**281 lines**. Line counts were recounted on 24 July 2026 and are an inspectable measure of
file size, never token counts.

The skill directs the agent to compare live Git state with the control handoff and to run the
bundled standard-library entry command. On 24 July 2026, the public entry run returned:
`control receipt: validated`. That command invokes the validator and records only a redacted
local receipt. The result concerns structure and applicability only; it does not certify prose,
citations, visual rendering, or agent decision quality.

The panel's three stages are a sourced mechanism diagram, not a recorded model transcript. The
first stage is the catalogue description; the second is the selected `SKILL.md`; the third is
the command invocation and returned structural result. It illustrates that bundled scripts are
not automatically added to instructions merely because they exist: the skill body tells the
agent when and how to invoke the entry command or validator.

**Publication boundary and screen, 24 July 2026.** The skill and its control pack are normally
ignored local infrastructure. The user specifically authorized a public teaching example, so
the page contains only the exact frontmatter, safe workflow excerpts, selected validator
excerpts, and the one-line real entry result. It does not copy `CURRENT.md`, `HANDOFF.json`,
`CONTROL.json`, provider configuration, or any live state record. The selected excerpts were
screened for IPv4 addresses, API-key prefixes, private-key headers, and the standing private
machine identifier; no sensitive string appears in the public excerpts.

### Act 6 — AGENTS.md **[V, publishable as of 2026-07-24]**

The sole popup exhibit is the real `~/PhD/Adrian-Mag.github.io/AGENTS.md` from this website
workspace. It is 73 lines and shows the local-control bootstrap, no-build site, unified
agent-docs protocol, living-reference routing, cache busting, and search-index rebuild step.

The popup content was mechanically compared with the source after HTML entity decoding and
matched byte for byte apart from the source file's final newline, which is outside the `pre`
element. It was re-screened on 24 July 2026 for IPv4 addresses, emails, API-key/token patterns,
private keys, passwords, hostnames, and private material. No match required redaction. No
artifact or identifying detail from another workspace is included.

### Privacy screen result

Scanned all skills for IPs, emails, SSH keys, API keys, tokens, passwords. **All matches were
documentation *about* secrets, not secrets** — Slidev's `--password` CLI flag, an
all-interface wildcard bind address in docs, and `long-missions/SKILL.md:271`: "Keep status file contents free of
secrets (no keys, tokens, passwords)". The remote-office skill describes its target machine
abstractly with no hostname, IP, or username. **Nothing above requires redaction** — unlike the poster's
Exhibit 2, which needed an IP removed.
⚠️ Re-run this screen at drafting time; files change.

### Act 9 — MCP scope: **resolved and deliberately narrow**

No deployed public MCP server configuration is in scope for publication. Act 9 therefore
teaches tool design through the real website-local contract, handler, and recording documented
above. MCP is a short closing section sourced to the stable specification, with the screened
Playwright call from the Act 4 trace as its one concrete invocation. The page does not inspect,
describe, or depend on private user-level MCP configuration.

### Act 4 — tool-loop trace **[V, found 2026-07-18]**

**Sourced from the website repo's own session logs, deliberately** — that repo is public by
construction. Sessions from every other workspace are excluded.

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

### Act 4 panel — REAL, no mock **[V, extracted 2026-07-18]**

The only panel in Movement I–II running on genuine data. Two traces, extracted by
`figure_generation/harness/extract_toolloop.py` into
`media/research/harness/toolloop.json`:

- **minimal** (3 steps, session `5288737a…`, 2026-07-16): `Bash: pwd` → result → the model
  reading its own answer back. The entire mechanism with nothing in the way.
- **iterating** (15 steps, session `6f674b3c…`, 2026-07-18): scroll → screenshot → read
  image, cycling. Three round trips per screenful to do what a person does with one glance.

**Both drawn from the website repo's sessions deliberately** — that repo is public by
construction, and sessions from every other workspace are excluded. The extractor additionally
aborts if it finds an IP-shaped value or a known credential-prefix pattern in its own output.

Two extraction bugs found and fixed, worth recording because both would have produced a
quietly wrong exhibit:

1. **Wrong date** on the minimal trace's window (07-18 vs the real 07-16) — the trace simply
   did not extract, which at least failed loudly.
2. **7 of 15 steps extracted blank.** MCP tool inputs are not in `command`/`file_path`, and
   image results are not text, so both flattened to `""`. Blank rows read as *nothing
   happened* rather than *we looked in the wrong field* — worse than an elision, because it
   is invisible. Now: inputs fall back through a wider key list then to a key summary, and
   non-text results are labelled `[image content returned to the model]`.

Elision policy is enforced in the data, not just the prose: every truncation carries
`"elided": true` and the original length, and the panel renders it. Current extract has
**0 truncations** — everything fits under the 240-character limit.

**Bonus for Act 9:** the MCP namespacing is visible in the tool names
(`mcp__plugin_playwright_playwright__browser_take_screenshot`), and the panel renders the
server as a badge. A real MCP invocation is on the page even though the MCP deployment is
thin.

### Act 2 panels — illustrative, for two different reasons

Both carry an on-screen **ILLUSTRATIVE** badge and a closing note.

**Tokenizer** — illustrative *by decision* (R4). A hand-built vocabulary reproduces the
behaviours that matter (leading space belongs to the token, common words survive, technical
words fragment, digits split, case matters) without shipping a real BPE table. Verified:
`seismology` → `seism|ology` bare and `·seis|molo|gy` in a sentence; `the` vs `·The` differ;
no orphan space tokens. **Upgradeable** if a real vocabulary is ever wanted.

**Next-token distribution** — illustrative *by constraint*, which is different and worth
recording. This is a static site; obtaining real next-token probabilities would require a
model that returns per-token probabilities, which the page cannot call. Unlike the Act 3
recording, **there is no script that would make this real** — it would need an open-weights
model run locally. The panel's on-screen note states this plainly rather than implying the
numbers were measured.

⚠️ **Unverified claim to check before publication:** whether the Anthropic API exposes
per-token probabilities at all. The panel text avoids asserting anything about any specific
API — it says only that *this page* cannot obtain them, which is true regardless. Do not
strengthen that wording without checking.

### ⚠️ OUTSTANDING — Act 3 panel is running on an illustrative mock

`media/research/harness/statelessness.mock.json` is **hand-written placeholder data**, not a
recording. It exists so Act 3 reads end-to-end before the real transcript can be captured.

**This must be replaced before publication.** Guards currently in place:

1. The file carries `"_mock": true` and a `_comment` saying so in the first line.
2. The panel renders an **ILLUSTRATIVE** badge in its header and a closing note: *"These
   replies and token counts are written by hand to show the shape of the demonstration —
   they are not measured output."*
3. It lives at a **separate path** from the real file, so a recording can never silently
   overwrite-and-hide it, and the mock can never be mistaken for the real one on disk.
4. The panel **prefers** `statelessness.json` (the real file) and only falls back to the mock.

**To replace:** run `figure_generation/harness/record_statelessness.py` with an API key. The
panel picks up the real file automatically — no code change — and the badge disappears on its
own. Optionally delete the mock afterwards.

Mock token counts (29 → 74 → 145 stateful; 29 → 25 → 27 stateless) are plausible but invented.
**Do not quote these numbers anywhere in prose** — the act's text deliberately refers to the
counter climbing rather than to specific values, so no prose changes when the real data lands.

### Act 1 — arithmetic screenshot **[restored to public exhibit 2026-07-24 by explicit author decision]**

`media/ai-fail.png` (641×259). A ChatGPT screenshot supplied by the author. Prompt
`241 - (-241) + 1`; reply: *"…is equivalent to 241 + 241 + 1, which simplifies to 483 + 1.
So 241 - (-241) + 1 is equal to 484."* The correct answer is 483.

Why it formerly earned its place over a fabricated-citation example: the *algebra is right*. Subtracting
a negative is handled correctly and stated correctly. The failure is arithmetic, mid-sentence,
with no change in the register of the prose around it. It sets up Act 2 (fluency and
correctness come out of the same forward pass and neither audits the other) far better than a
made-up reference would, because nothing here is invented.

The two errors have one cause: `241 + 241` is rendered as 483, which is the true sum 482 with
the trailing `+ 1` already absorbed, and the `+ 1` is then applied a second time.

**Publication decision.** The page embeds this user-supplied product screenshot as a small,
explicitly undated illustration of a failure mode. It must retain the visible version caveat and
must not be used to support a claim about any current model.

### Still missing

- **A deployed public MCP server configuration** is not available. Act 9 deliberately does not
  require one: it exhibits a real local tool contract and handler, then uses the already
  screened Act 4 trace for one genuine MCP-mediated call.

### Acts 10–11, summary, and workspace maps **[V, public workspace artifacts; 2026-07-22]**

Acts 10 and 11 use this workspace's own control structure as their practical example. Act 10
shows only the roles of `AGENTS.md`, the selected skill, tracked plan/source dossier, source
files, and the checked handoff; it does not disclose live local control state. Its retrieval and
context claims use the verified RAG and long-context sources in Sections 1.3–1.4.

Act 11 and `agentic-structure-map.html` describe a single-agent workspace control graph, not a
deployed multi-agent service. The map exposes only public paths or safe role descriptions for
local-only nodes. Its outlined `docs/agent-docs/` area groups the private website-control routine
with the durable records it uses; the two are parts of one control system, not peer systems. The
page introduces those mechanics through a house-building robot analogy. The agent host and its
tools are the robot and its starting kit; higher-level instructions, sandboxes, and approvals are
separated into guidance and enforced limits; stable project instructions are the house manual;
checked current-state and handoff notes are the shift log; task-specific skills, plans, source
records, and pipeline guides are job manuals; scripts and MCP tools are specialist equipment;
and matching verification plus a refreshed handoff closes the shift. The analogy is an authored
teaching device, not an exhibit or recorded execution. It does not quote or claim to reproduce an
actual system prompt. The electrical-work passage is explicitly illustrative and names only the
general sequence of isolation, preventing accidental re-energising, verifying dead, working,
and testing afterward; it is not presented as electrical safety instruction.

The
primary graph deliberately includes only ongoing agentic roles. It is ordered by timing, not by
filesystem location: host rules, tools, and short skill descriptions can be supplied before a
prompt; a trusted Codex project additionally supplies its configuration and `AGENTS.md`, while
this Claude project supplies its unscoped rule. No workspace command runs merely because that
context exists. In this workspace, a task start or resume begins the single `website-control` routine, which
verifies the local continuity packet before selecting any task records. The map separately shows the ordinary host/session conversational loop: an agent response returns to prompt N+1 without rerunning bootstrap in the same continuous task; that loop is not a rule stored in the local control files. The local control instructions say that the start-or-resume route runs once per continuous task or resumed session, not once per message. During work, a material change in objective, scope, evidence, or phase triggers a smaller reassessment: continue focused small work, create or use a plan, or update the active plan before returning to the job. A meaningful close refreshes the handoff for the next start. A general conversation may then need no
further workspace material. Other tasks can select a relevant plan, dossier, living reference, or source file before reaching the conditional site-change checklist in
`AGENTS.md`, the optional Playwright MCP ability, the automatic Git commit hook, or explicitly
invoked search-index, figure-generation, and mobile-audit scripts. The site-change route names
the real conditional requirements: notes prose refreshes the search index; CSS or JavaScript
changes refresh cache query versions; navigation changes are copied to every HTML page; and
affected page or stylesheet work is checked in a browser. Ordinary website source files and the
Act 8–9 hook/tool teaching exhibits are intentionally omitted because they are not active
agentic machinery.
The revised `agentic-structure-map.html` is an original hardware-inspired illustrative board:
context injection, the next-token model, actions, persistent records, evidence checks, and the
private control route occupy distinct labelled regions. It retains pan/zoom and gives every
visible component a short plain-language popup without exposing private contents. Its complete
orange control route is based on the local `website-control` files: start/resume; `BOOTSTRAP.md`;
the canonical `SKILL.md`; principles plus provisional handoff; Git comparison; validator; a
pass/fail decision; redacted local incident recording and source/Git repair on failure; selected
current records and the four-way small/follow/revise/new-plan decision on success; work and
matching checks; phase landing, handoff refresh, and revalidation. A failure blocks ordinary
workspace work until the repaired packet passes again. The local incident records retain only
safe categories, the newest 100 detailed events, and durable totals; their contents are not
public artifacts. The blue outer loop remains explicitly host/session behaviour rather than a
control-file rule. The dashed grey node says that no permanent monitoring service exists in this
workspace. This is an illustrative relationship diagram built from real components, not a
recorded execution trace.

**Client context example, 22 July 2026.** A user-supplied screenshot of Claude&rsquo;s `/context`
view was reviewed for this map revision. It visibly separates system prompt, system tools,
custom agents, memory files, skills, prior messages, free space, and an MCP-tools category
marked &ldquo;loaded on-demand.&rdquo; The map now names the corresponding context categories: system
prompt, tool descriptions, project/memory files, skill catalogue, conversation so far, current
user prompt, and client-loaded-on-demand MCP tools. It intentionally does not reproduce the
screenshot&rsquo;s model name, token figures, private paths, or UI as a generic product contract.
The on-demand MCP statement is therefore labelled as a Claude client observation on that date,
not a claim about every agent host.

`workspace-explorer.html` is a second view of the same real workspace. Its curated tree was
checked against path names and symlink targets on 24 July 2026. It includes selected agent-
related entries under `.agents/`, `.claude/`, `.codex/`, `.githooks/`, `.playwright-mcp/`,
`docs/agent-docs/citation-audit/`, `docs/agent-docs/`, `figure_generation/harness/`, `js/`, `media/`, `pages/`,
and `tools/`, plus the root `AGENTS.md` and `.gitignore`. The static page embeds only selected
names, parent-child relationships, local/tracked/generated/shortcut labels, and authored
plain-language role descriptions. It does not read the filesystem at runtime or reproduce any
file content. The `.agents/` and `.claude/` skill shortcuts are shown as expandable shortcut
folders: their visible `SKILL.md`, `scripts/`, `controlctl.py`, and `validate_control.py`
descendants resolve to the same canonical files under
`docs/agent-docs/control/skills/website-control/`, not duplicate copies. The `.agents/` route
starts open so the bundled entry command and validator are not hidden several levels down. The
explorer is explicitly curated rather than a claim to show every path.

**Privacy screen.** No live `CURRENT.md`, `HANDOFF.json`, `CONTROL.json`, provider adapter, or
session log is copied into these pages. The public descriptions were screened under the standing
sensitive-string rules before publication.

## 4. Standing rules for this series

1. **No citation from memory.** Every reference is fetched and checked before it ships. This
   file is the record.
2. **Date every claim about a product or protocol.** MCP alone changed between my training
   data and today.
3. **Separate protocol from product, and peer-reviewed from vendor.** Mark each inline.
4. **Argue from necessity where internals are undocumented** rather than asserting them.
5. **No invented exhibits.** (D4.) If there is no artifact, there is no exhibit.
6. **Where the literature disagrees, say so** rather than picking the tidier side.
