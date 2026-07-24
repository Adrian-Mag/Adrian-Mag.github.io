## Plan: Observable workspace harness architecture
**Status:** active   **Created:** 2026-07-23

### Goal

Design, before further implementation, a provider-neutral workspace harness
that lets a coding agent safely move between temporary context and durable
workspace knowledge. The harness must make its operational path observable,
support continuity across sessions, and distinguish soft instructions from
mechanical enforcement without claiming access to private model reasoning.

### Confirmed design principles

- Treat context as temporary working memory and workspace documents as durable
  storage. The agent must select the smallest relevant durable record rather
  than load every plan, reference, dossier, or transcript.
- The small automatic entry layer is `.codex/config.toml`, `AGENTS.md`, the
  short skill catalogue, and the current user prompt. It should contain only
  stable workspace identity, routing instructions, and pointers; it cannot be
  the complete workspace manual.
- `AGENTS.md` must tell an agent that durable agent documents exist and where
  their dispatcher lives. It steers an agent toward the system but cannot by
  itself mechanically enforce it.
- Control is a workflow/contract with several surfaces, not merely a skill.
  `website-control` may package its detailed recipe and scripts, but it cannot
  be the sole entry point because skill selection is conditional.
- Telemetry records externally observable lifecycle decisions, route changes,
  tool/check events, and receipt outcomes. It never stores prompts, commands,
  raw paths, file contents, transcripts, tool output, or claims that a model
  understood a file.
- The present Codex telemetry layer is observation-only. A human reviews real
  evidence before any later blocking mutation, commit, or publication gate.
- Public maps explain observed reality only; they must not be revised merely to
  advertise a desired future architecture.
- Agent documents are organised as self-contained protocols, not one flat
  catch-all directory. The plans protocol is the first: it owns plan rules,
  active plans, completed plans, and phase-completion records under
  `docs/agent-docs/plans/`.
- References own current architecture and source evidence; plans link to those
  records rather than absorbing dossiers or reference details.
- The references protocol now owns `references/PROTOCOL.md`, a compact
  `references/INDEX.md`, living subsystem maps, and source dossiers. The
  agent-document architecture has its own living reference; no private live
  state is copied into it.
- The **Agent Ledger** is now a tracked protocol with a canonical local writer,
  compact state, event stream, and conservative report. It records
  agent-declared events now and has a thin trusted-Codex shadow adapter for
  supported local-hook observations. Coverage is partial; it has no automatic
  enforcement gate or strong anti-tamper boundary.
- The **Citation Audit Library** is now agent-docs infrastructure: a tracked
  protocol routes citation and claim checks to an ignored local evidence
  library. Local PDFs must be opened through `pdf-source-reading`; the library
  is durable SSD material but not automatic context or public content.
- The former catch-all `control` concept is not a target subsystem. The current
  ignored `control/` overlay remains a live legacy bridge until its continuity,
  planning, reference, and observation responsibilities can be migrated safely.

### Target layers

1. **Automatic entry:** minimal Codex config and `AGENTS.md` supply workspace
   identity, authority boundaries, and the instruction to classify
   consequential work.
2. **Prompt router:** each prompt enters a reversible operational route. The
   initial taxonomy is conversation, research, workspace inspection, planning,
   small workspace change, planned workspace change, external/high-impact, and
   uncertain. A route is a declared operational state, not hidden reasoning.
3. **Document dispatcher:** a compact, tracked need-to-record index maps a
   route to the first relevant durable record: current orientation, handoff,
   active plan, protocol, living reference, source dossier, verification
   profile, or Git/source evidence.
4. **Workspace-memory protocols:** plans, references, and later other
   self-contained agent-document protocols own their respective durable state
   and rules. A compact dispatcher selects the relevant record rather than
   treating one generic control folder as the source of all state.
5. **Capabilities:** tools, specialist skills, MCP abilities, and bounded
   subagents are selected inside a route. They are not automatic memory and
   are not themselves the main router.
6. **Agent Ledger:** agent-declared routes and procedures are recorded beside
   independently host-observed lifecycle, tool, Git, and check events. Later
   gates may deny an action that lacks a permitted route/receipt; the ledger
   remains the diagnostic record.

### Route and authority model

- A route may be reclassified when evidence changes. Record a short reason
  category such as `scope_expanded`, `evidence_changed`, or `user_superseded`.
  Reclassification must happen before the first consequential action under the
  new route.
- Route and authority are separate. Discovering that an edit would help does
  not grant permission to edit when the user asked only for explanation or
  inspection. If modification was already authorised, the agent may escalate
  from inspection to change after entering the appropriate work route.
- In early observation mode, missing/reclassified routes are reported, not
  blocked. A later hook gate should cover only consequential actions such as
  patch/write, commit/push, destructive commands, and external writes—not
  every read or ordinary conversation turn.

### Document roles to preserve

| Record | Role |
|---|---|
| `AGENTS.md` | Small permanent entry card: workspace identity, durable-document existence, routing instruction, critical boundaries. |
| `BOOTSTRAP.md` | Minimal doorway from automatic context into the canonical control workflow. |
| `SKILL.md` | Detailed operational recipe plus scripts; loaded only after the relevant workflow is selected. |
| `CURRENT.md` | Compact stable orientation, not a running diary. |
| `HANDOFF.json` | Replaceable last-shift snapshot for a new/resumed agent. |
| Active plan | Live goal, phase, open questions, and remaining decisions for substantial work. |
| Completed plan | Settled decisions and verification evidence. |
| Living reference | Current architecture of a subsystem. |
| Source dossier | Provenance and claim/artifact evidence, not operational state. |
| Git/source | Authoritative durable workspace reality when records disagree. |
| Telemetry | Observed path and gaps; evidence for refining the design. |

### Subagent rule

The parent agent owns routing, central workspace state, plan/current/handoff
updates, and commits. A subagent receives a bounded brief and relevant document
slice, then returns evidence or findings; it does not independently rewrite
central continuity records unless a later, explicit workflow grants that role.

### Phases

1. **Architecture discovery and vocabulary.** Refine the layer model, route
   taxonomy, document roles, authority model, and desired telemetry questions.
   No workflow redesign is implemented in this phase.
2. **Routing and document-dispatch contract.** Specify the tracked route policy
   and compact need-to-record registry, then test it against real workspace
   tasks before adopting it.
3. **Observation integration.** Extend telemetry to record prompt routes,
   route transitions, capability selection, and route/action mismatches in
   shadow mode.
4. **Control workflow revision.** Refactor Bootstrap, skill, local state, and
   task/verification profiles to match the approved router/dispatcher model.
5. **Measured enforcement and public explanation.** Review real telemetry;
   separately approve any gates, Git/CI attestation, Claude adapter, and
   evidence-backed website-map revision.

### Open questions

- Which routes should be explicit versus inferred when a turn uses no tools?
- What is the smallest document registry that reliably finds the right record
  without becoming a second giant `AGENTS.md`?
- Which website verification profiles belong in the dispatcher versus a
  specialist website skill?
- What observable event should constitute a route declaration in Codex: a
  `controlctl` command first, or eventually a dedicated structured tool?
- What baseline telemetry and human review threshold justify the first narrow
  action gate?
