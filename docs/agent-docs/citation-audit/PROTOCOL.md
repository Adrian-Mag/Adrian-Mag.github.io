# Citation Audit Library Protocol

This is the private, long-term evidence library for checking whether website
citations and research claims are supported by their sources. It is part of the
workspace's agentic research infrastructure: it gives an agent durable local
material to consult instead of reconstructing prior paper checks from memory.

## Layout and privacy

```text
docs/agent-docs/citation-audit/
  PROTOCOL.md     tracked routing and privacy rules
  library/        ignored local PDFs, extracts, summaries, and working records
```

`library/` is never staged, served, copied into public page content, or sent to
an external service. It currently contains the prior audit report, local paper
copies, page-text extracts, summaries, and matching records. Its material is
evidence, not automatic model context.

## When to use it

Use this protocol when a task needs to verify or revise a citation, assess
whether a public claim is supported, or revisit a paper-based finding. Start
with `references/INDEX.md`: a source dossier or living reference may already
answer the task. Use this private library when the needed evidence is a local
paper or a previous audit record.

## Reading a local paper

Before reading, extracting, or rendering a PDF in `library/`, use the
local-only `pdf-source-reading` skill. Its procedure keeps source content on
this machine and produces page-specific evidence. Do not upload a PDF, its
text, page image, or long quotation to web search, a cloud OCR service, or any
other external tool.

Record the resulting verdict in the local audit record with the source, page,
and any relevant numbered result. Keep the public source dossier focused on
claims that actually appear on the website; do not copy whole local papers or
working extracts into it.

## Boundaries

- This library supports citation and claim verification; it does not replace
  the references protocol, a source dossier, a plan, or the Agent Ledger.
- A local summary is a navigation aid. The PDF or authoritative publisher
  record remains the evidence when one is available.
- Do not treat the library's presence as proof that every website citation has
  been checked recently. Read the relevant audit verdict and current source.
