## Control telemetry and observation — Phase 1 complete
**Completed:** 2026-07-23

Added the local telemetry contract, rolling 500-event JSONL ledger, aggregate
summary, current receipt state, `controlctl` lifecycle/report commands, and
validator checks for schema and privacy boundaries. The records are ignored and
the validator rejects raw-content fields.

**Evidence:** telemetry unit tests; control validator; `controlctl begin`,
explicit skill recording, route classification, and report smoke run.
