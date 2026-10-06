---
id: AWP-002
type: reference
status: active
authority: authoritative
scope: workspace
source: agent-workspace-protocol template
updated: {{DATE}}
verified: pending-user-review
---

# Directory Layout

| Path | Purpose |
| --- | --- |
| `MEMORY/` | Durable rules, state, decisions, glossary, sessions |
| `10-docs/` | Requirements, design, manuals, meeting records |
| `20-projects/` | Project knowledge, plans, code maps, local tools |
| `30-data/` | Raw data, processed data, data dictionaries |
| `40-deliverables/` | Final outputs and generated artifacts |
| `50-assets/` | Images, fonts, styles, static templates |
| `60-research/` | External research and references |
| `90-temp/` | Temporary work |
| `99-archive/` | Superseded history |

Root-level files are limited to navigation, agent adapters, `.gitignore`, and
the category directories.

## Change Process

If the existing categories cannot contain a new artifact type:

1. Describe why an existing category is unsuitable.
2. Record the decision.
3. Update this file and the canonical protocol.
4. Update indexes and adapters.
5. Create the directory and a README.
