# Agent Ledger event schema

This schema defines safe metadata for the local Agent Ledger runtime. It deliberately
does not define a transcript format.

## Common fields

| Field | Meaning | Limits |
| --- | --- | --- |
| `schema_version` | Event-format version | Integer. |
| `at` | Event time | UTC timestamp. |
| `kind` | Event category | One value from the vocabulary below. |
| `work_phase` | Opaque work-phase correlation token | Never a raw path, prompt, or transcript. |
| `route` | Agent-declared operational route, when applicable | Short controlled vocabulary. |
| `source` | `agent`, `host`, `git`, or `derived` | Says who supplied the evidence. |
| `outcome` | Safe result category, when applicable | `observed`, `passed`, `failed`, or `missing`. |
| `record_type` | Durable record category, for a selected record | `plan`, `reference`, `source`, or `other`; never a path. |
| `step` | Declared procedure step | `work`, `plan-updated`, or `reference-updated`. |
| `tool_class` | Coarse local-hook tool category | `shell`, `patch`, `mcp`, `local_function`, or `other`; never a tool argument. |

The schema excludes prompt, command, path, content, output, transcript,
credential, and secret fields. A future implementation rejects them rather than
redacting them after writing.

## Event vocabulary

### Agent-declared

- `agent.route_declared`
- `agent.route_reclassified`
- `agent.record_selected`
- `agent.procedure_step_declared`
- `agent.check_declared`
- `agent.work_closed`

### Independently observed

- `host.session_started`
- `host.turn_submitted`
- `host.tool_requested`
- `host.tool_completed`
- `host.context_pre_compact`
- `host.context_post_compact`
- `host.turn_stopped`
- `host.session_ended`
- `git.commit_attempted`
- `git.commit_completed`

### Derived by the reporter

- `ledger.expected_evidence_missing`
- `ledger.route_action_mismatch`
- `ledger.work_phase_unclosed`

## Route vocabulary

The initial controlled vocabulary is `conversation`, `research`, `inspect`,
`plan`, `change-small`, `change-planned`, `external`, and `uncertain`. It is a
declared operational label, not a claim about private reasoning or a permission
to take an action.

## Runtime files

The canonical `scripts/ledgerctl.py` writes only these ignored local files:

- `runtime/events.jsonl`: one validated declaration or host/Git observation per
  line. It is append-only in normal use, but is not tamper-proof.
- `runtime/state.json`: compact current or most-recent work-phase state.
- `runtime/report.json`: derived diagnostic findings; it is regenerated rather
  than treated as independent evidence.

`work_phase` is an opaque generated token of the form `wp-` plus 24 lowercase
hexadecimal characters. It is intentionally not a task name, path, prompt, or
session transcript.

## Pending host phases

The Codex shadow adapter makes a pending phase on `UserPromptSubmit` and adds
only `host.turn_submitted`. A later agent `begin` command claims the same token
and adds its route declaration. If a local tool hook occurs before that route,
it is still associated with the pending phase. A prompt with no observed local
work is not a finding merely because it created a pending phase.
