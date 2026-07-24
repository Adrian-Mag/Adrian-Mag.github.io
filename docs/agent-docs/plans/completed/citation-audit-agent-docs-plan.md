# Plan: Integrate the Citation Audit library into agent docs

**Status:** complete
**Created:** 2026-07-24

## Goal

Move the private citation-audit evidence library under `docs/agent-docs/`, add
a tracked protocol that routes citation verification to the local
`pdf-source-reading` skill, and make that durable research infrastructure
discoverable from agent entry, reference selection, and the public filesystem
map without exposing its contents.

## Design decisions

- `docs/agent-docs/citation-audit/PROTOCOL.md` is tracked, canonical guidance.
  The moved evidence library lives beneath its ignored `library/` subtree.
- Local PDFs, extracted text, Zotero matches, summaries, and verification
  working records stay private, untracked, and unserved. The protocol names
  their roles but does not copy their content into tracked docs.
- Citation work starts with the smallest relevant source dossier or living
  reference; use the audit library when local paper evidence is needed.
- Opening or extracting a library PDF requires the local-only
  `pdf-source-reading` skill. It must not upload source content. The skill
  provides page-specific evidence; the audit record records the verdict.
- This phase changes no public scholarly claim or citation verdict. It moves
  infrastructure and routes future work.

## Phases

1. **Establish ownership and privacy boundary.** Create the protocol, move the
   existing private library, and update ignore rules.
2. **Wire agent routing.** Update AGENTS, cross-protocol/reference documents,
   and living maps so citation evidence reaches the PDF-reading skill.
3. **Update the public structural view.** Move the explorer representation to
   `agent-docs` and retain descriptions only; update the Act 6 snapshot.
4. **Verify and settle.** Check ignored boundaries and paths, static pages,
   search index, and completion records.

## Open questions

- Should a later citation-audit skill package the protocol and repeatable
  cross-page claim checks, rather than relying on AGENTS routing alone?
