# Installation Scopes

There are two different things to install. Treating them as one is the main
source of confusion.

If you remember one rule: install the reusable skill at agent scope, and put
the workspace-specific rules and memory at workspace scope.

## Agent Scope

Agent scope installs the reusable skill into an agent runtime's skill
directory.

Examples:

| Runtime | Common user-level skill root |
| --- | --- |
| Codex | `$CODEX_HOME/skills`, fallback `~/.codex/skills` |
| Claude Code | `~/.claude/skills` |
| Custom Agent Skills runtime | Path supplied with `--skill-root` |

Agent-scope files are device/user configuration. They are not project memory
and should not be committed to every project.

Use agent scope when you want a future session in any workspace to be able to
say:

> Audit this workspace using the Agent Workspace Protocol.

## Workspace Scope

Workspace scope installs the actual project-facing convention:

- `AGENTS.md`;
- `CLAUDE.md`, `GEMINI.md`, Cursor, and Copilot adapters;
- `MEMORY/` structure;
- the project's canonical
  `MEMORY/01-rules/workspace-protocol.md`;
- project maps and indexes.

These files belong with the project because they define the project's context
boundaries. They should be reviewed, versioned, and copied only through an
intentional template or migration.

Use workspace scope when you want every human and agent entering the project to
follow the same rules.

## Project-Level Skill Installation

Some runtimes support project-level skills such as `.agents/skills/`. This is
useful for teams that want the skill itself versioned with the repository.

It is still not the same as workspace memory:

- the skill contains reusable instructions;
- workspace memory contains facts and decisions about this project.

The installer supports both:

```sh
# User/device skill
python skill/agent-workspace-protocol/scripts/install.py \
  --scope agent --runtime codex

# Project-local skill
python skill/agent-workspace-protocol/scripts/install.py \
  --scope project --workspace .
```

## Recommended Default

For an individual user:

1. Install the skill once at agent scope.
2. Run the workspace bootstrap in each project that needs the convention.
3. Keep project rules and memory in the repository.
4. Review generated entry files before committing them.

For a team:

1. Decide whether the skill is installed by each developer or vendored at
   project scope.
2. Commit the workspace adapters and canonical protocol.
3. Add a CI check for links, secrets, and obvious root-level clutter.

## `CLAUDE.md` Is Not the Protocol

`CLAUDE.md` is a Claude Code entry adapter. It belongs in workspace scope and
must point to the shared canonical protocol. It is not the cross-agent rule
book, and it is not the global skill.

The same pattern applies to `GEMINI.md`, Cursor rules, and Copilot
instructions. Runtime-specific entry files are maps; the durable rules remain
in the workspace's canonical protocol.
