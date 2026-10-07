---
name: agent-workspace-protocol
description: Bootstrap, audit, migrate, or document a cross-agent workspace so rules, inputs, outputs, code, memory, and history are distinguishable and safe to load. Supports English and Simplified Chinese templates. Use when designing workspace organization, installing agent entry files, or improving how multiple models share a repository.
metadata:
  short-description: "Make AI workspaces legible, safe, and reusable"
---

# Agent Workspace Protocol

Use this skill to make a workspace understandable to a new agent without
requiring it to read everything. The protocol is intentionally portable; adapt
it to the existing repository instead of replacing established, sensible rules.

## First Inspect

Before writing:

1. Read the nearest `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, Cursor rules, and
   Copilot instructions that exist.
2. Check for an existing canonical protocol such as
   `MEMORY/01-rules/workspace-protocol.md`.
3. Inspect the top-level directories and repository status.
4. Identify secrets, private data, generated outputs, and external code paths.
5. Determine whether the user's workspace language or documentation language
   requires the English or `zh-CN` templates.
6. Ask only if the authority model or intended scope is genuinely ambiguous.

Preserve good local rules. This skill supplies a structure and decision model,
not permission to rewrite a project's history or discard its conventions.

## Choose a Mode

- **Bootstrap:** initialize a workspace that has no protocol. Copy the
  workspace templates, then review them.
- **Audit:** keep the existing layout and report missing authority, status,
  provenance, input/output separation, or adapter drift.
- **Migrate:** move files incrementally, preserve links, and record why the
  structure changed.
- **Explain:** answer how to install the skill and where workspace rules live.

## Installation Boundary

Keep these separate:

- **Agent scope:** the reusable skill installed into an agent runtime. Codex
  commonly uses `$CODEX_HOME/skills/agent-workspace-protocol`, falling back to
  `~/.codex/skills/agent-workspace-protocol`.
- **Workspace scope:** `AGENTS.md`, adapters, `MEMORY/`, and the workspace's
  canonical protocol. These belong to the project and may be committed.

Never put project credentials, project history, or project decisions in the
global skill.

When explaining installation, lead with the agent-driven prompt published in
the repository README, and offer the manual commands second.

## Bootstrap

Run:

```sh
python scripts/bootstrap_workspace.py --workspace /path/to/workspace \
  --agents all --dry-run
python scripts/bootstrap_workspace.py --workspace /path/to/workspace \
  --agents all
```

For a Simplified Chinese workspace, add `--language zh-CN`.

The script refuses conflicts by default. `--force` overwrites; add `--backup`
to preserve conflicting files. Use `--skip-existing` when adopting the
protocol in a workspace that already has its own `AGENTS.md` or `README.md`;
it adds only the missing files and leaves local files untouched. The script
never writes outside the target workspace.

Afterward:

1. Replace placeholders and project description.
2. Review `MEMORY/01-rules/workspace-protocol.md`.
3. Confirm the adapters point to it.
4. Add sensitive paths to `.gitignore`.
5. Check links and remove unused template categories.

If modifying an existing workspace manually, use the files under
`assets/workspace/` and the canonical protocol in
`references/workspace-protocol.md`.

## Core Rules

Apply these invariants:

1. One canonical source per durable fact.
2. Authority is ordered: user instruction > active rules > confirmed specs >
   code/tests > derived outputs > history.
3. Generated outputs are not inputs until explicitly promoted.
4. Code and knowledge have separate lifecycles; store code maps and commit
   anchors rather than copying source into the knowledge workspace.
5. Current state, decisions, and session history have separate homes.
6. Entry files are maps, not manuals.
7. Formal content carries status, authority, source, and update metadata.
8. Conflicts are surfaced, not silently guessed away.

## Rule Intake and Placement

Installing the skill does not create a filesystem watcher. When adding or
changing a rule during an agent session:

1. Search for an existing canonical file before creating a new one.
2. Classify the content by durability, authority, and lifecycle.
3. Put durable workspace rules in `MEMORY/01-rules/`.
4. Put directory and classification rules in `MEMORY/02-structure/`.
5. Put current conclusions in `MEMORY/05-state/current.md`.
6. Put durable choices and rationale in `MEMORY/06-decisions/`.
7. Put task history in `MEMORY/03-sessions/`.
8. Update indexes, state, or decision records when required.
9. Classify or remove `90-temp/inbox/` items before task completion.

Do not claim that manual edits outside an agent session will be moved
automatically. State that placement is agent-mediated and depends on the
workspace entry file and canonical protocol being read.

## Read and Write Behavior

- Read the map, then the index, then only relevant files.
- Do not treat `40-deliverables/`, `90-temp/`, history, or unstatused files as
  requirements.
- Before writing, decide its category, canonical location, authority, and
  lifecycle status.
- Update the index when a durable entry changes.
- Do not duplicate a canonical rule into adapters or summaries.
- Never place credentials in reports, logs, session summaries, examples, or
  adapter files.

## Verification

Check:

- root-level files are intentional;
- every adapter points to the same canonical protocol;
- no real project path or credential leaked into public templates;
- generated files are marked as derived where the workspace requires it;
- temporary files are cleaned or explicitly retained;
- links resolve on a case-sensitive filesystem;
- installer dry runs do not write.

## References

- Read [references/workspace-protocol.md](references/workspace-protocol.md)
  when defining or reviewing the protocol. This file is also the canonical
  template source; `{{DATE}}` is replaced during workspace bootstrap.
- Read
  [references/workspace-protocol.zh-CN.md](references/workspace-protocol.zh-CN.md)
  when bootstrapping or reviewing a Simplified Chinese workspace. Use
  `--language zh-CN` so this file becomes the generated canonical protocol.
- Read [references/adapters.md](references/adapters.md) when installing or
  troubleshooting agent entry files.
- Read [references/migration-and-audit.md](references/migration-and-audit.md)
  when applying the protocol to an existing messy workspace.
