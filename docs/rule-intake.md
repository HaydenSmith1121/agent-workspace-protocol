# Rule Intake and Automatic Placement

Installing the skill or bootstrapping a workspace does not create a background
watcher. It gives agents a deterministic convention to follow when they create
or revise rules.

## What Is Automatic

When an agent has read the workspace entry file and canonical protocol:

- a durable workspace rule is classified before it is written;
- the canonical file is updated instead of creating a duplicate;
- the memory index and current state are updated when required;
- a decision record is added when the change affects structure, authority, or
  a durable tradeoff;
- temporary material is moved out of `90-temp/inbox/` before task completion.

The agent performs this classification. The skill cannot enforce filesystem
watchers or intercept manual edits outside an agent session.

## Placement Table

| New content | Default location | Authority | Required update |
| --- | --- | --- | --- |
| Durable workspace rule | `MEMORY/01-rules/<topic>.md` | Authoritative | `MEMORY/README.md` |
| Directory, naming, or classification rule | `MEMORY/02-structure/` | Authoritative | Structure document and index |
| Current fact or conclusion | `MEMORY/05-state/current.md` | Derived summary | Link to canonical source |
| Durable decision and rationale | `MEMORY/06-decisions/NNNN-<topic>.md` | Authoritative | Decision index |
| Task history | `MEMORY/03-sessions/YYYY-MM-DD-<topic>.md` | Non-authoritative | Register when useful |
| Requirement, design, specification, or contract | `10-docs/` | Authoritative after approval | Relevant index |
| Final report, export, or presentation | `40-deliverables/` | Derived output | Source and status |
| Unclassified temporary material | `90-temp/inbox/` | Non-authoritative | Classify or remove |

## Why This Is Not Fully Automatic

Files can be created by many tools:

- an IDE;
- a shell script;
- a sync tool;
- a human;
- an agent that has not loaded the workspace instructions.

Only the last case can follow the protocol directly. The other cases require
an explicit migration or an agent-mediated review.

## How to Make It More Reliable

1. Commit the workspace adapters and canonical protocol.
2. Start agent tasks by requiring the nearest adapter and canonical protocol.
3. Add a periodic link, secret, and root-file audit.
4. Keep one canonical rule file instead of creating duplicate rule summaries.
5. Ask the agent to update the index and state whenever a durable rule changes.

For the complete protocol, see the canonical
[workspace protocol](../skill/agent-workspace-protocol/references/workspace-protocol.md).
