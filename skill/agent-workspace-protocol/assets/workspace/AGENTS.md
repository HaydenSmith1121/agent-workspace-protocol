# AGENTS.md

This file is a map, not the rule book.

- Canonical protocol: `MEMORY/01-rules/workspace-protocol.md`
- Memory index: `MEMORY/README.md`
- Current state: `MEMORY/05-state/current.md`

## Start

1. Read the memory index.
2. Read only task-relevant active rules.
3. Read current state.
4. Read the relevant category index before specific files.
5. Read code only when behavior must be understood, and record the revision.

## Authority

User instruction > active workspace rules > confirmed specifications >
code/tests > derived outputs > history.

If the order does not resolve a conflict, stop the affected write and ask.

## Do Not Treat As Input By Default

- `40-deliverables/`
- `90-temp/`
- `99-archive/`
- `MEMORY/03-sessions/`
- anything marked `draft`, `deprecated`, `superseded`, or `archived`

## Red Lines

- Do not let generated output become a requirement implicitly.
- Do not copy a canonical rule into adapters or summaries.
- Do not put secrets in reports, logs, examples, or summaries.
- Do not write outside this workspace unless the task explicitly authorizes it.
- Do not silently overwrite durable content.

## Finish

Place outputs in the correct category, update indexes and current state, mark
replaced content, clean temporary work, and report verification evidence.
