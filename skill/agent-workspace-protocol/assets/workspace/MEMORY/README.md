---
type: reference
status: active
authority: derived
scope: workspace
source: agent-workspace-protocol template
updated: {{DATE}}
verified: pending-user-review
---

# Permanent Memory Index

This is the durable memory index and reading map. The canonical protocol is
[01-rules/workspace-protocol.md](01-rules/workspace-protocol.md).

## Index

| ID | Topic | File | Scope |
| --- | --- | --- | --- |
| AWP-000 | Agent Workspace Protocol | [01-rules/workspace-protocol.md](01-rules/workspace-protocol.md) | Workspace |

Add new durable entries here. Do not use this index as a second copy of their
contents.

## Navigation

- Current state: [05-state/current.md](05-state/current.md)
- Decisions: [06-decisions/README.md](06-decisions/README.md)
- Sessions: [03-sessions/README.md](03-sessions/README.md)
- Structure: [02-structure/directory-layout.md](02-structure/directory-layout.md)

## Write Checklist

1. Check for an existing canonical file.
2. Add status, authority, source, and update date.
3. Store it in the correct memory or workspace category.
4. Register durable entries in this index.
5. Distill current conclusions into `05-state/current.md`.
6. Record a material rule or structure change in `06-decisions/`.
