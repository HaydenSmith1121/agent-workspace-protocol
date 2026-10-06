# Agent Adapters

An adapter is a small discovery file for one tool. It routes the agent to the
workspace's canonical protocol.

## Canonical Target

The default canonical target is:

```text
MEMORY/01-rules/workspace-protocol.md
```

If a workspace moves that file, update every adapter.

## Codex and AGENTS.md

- Workspace entry: `AGENTS.md`
- Global skill root: `$CODEX_HOME/skills`, falling back to `~/.codex/skills`
- Project skill root supported by the installer: `.agents/skills`
- Skill folder: `agent-workspace-protocol/`

`AGENTS.md` should be short and should point to the canonical protocol and
memory index. In nested repositories, a nested `AGENTS.md` may add local
commands and path boundaries.

## Claude Code

- Workspace entry: `CLAUDE.md`
- Common user-level skill root: `~/.claude/skills`
- Common project-level skill root: `.claude/skills`

`CLAUDE.md` is an adapter, not a second copy of the protocol.

## Cursor

- Workspace rule: `.cursor/rules/000-agent-workspace.mdc`
- Legacy alternative: `.cursorrules` for older Cursor versions

The rule should use normal front matter and point to the canonical protocol.
Keep it narrowly scoped; do not create one reloaded rule per category.

## Gemini CLI

- Workspace entry: `GEMINI.md`
- Common user-level entry: `~/.gemini/GEMINI.md`

The repository-level file is the portable adapter. A user-level file can
remind Gemini to look for `AGENTS.md` and the canonical protocol, but it must
not contain project-specific memory.

## GitHub Copilot

- Workspace entry: `.github/copilot-instructions.md`

Keep the file short and link to the canonical protocol and workspace index.
Confirm the repository's Copilot setting allows repository instructions.

## Adding a New Adapter

1. Identify the exact discovery path and current official documentation.
2. Create a short pointer to the canonical protocol.
3. Add the adapter to the installer's agent list.
4. Add it to the adapter matrix.
5. Test discovery in a temporary workspace.
6. Do not copy the full protocol.

## Adapter Failure Checks

If an agent ignores the workspace rules, check:

- the file is in the discovery path expected by that tool;
- the file is tracked and present in the checkout the tool opened;
- the tool reads repository instructions only for trusted workspaces;
- nested working directories do not hide the root instructions;
- another instruction file is overriding or conflicting;
- the adapter points to a file that still exists.
