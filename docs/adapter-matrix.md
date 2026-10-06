# Adapter Matrix

Adapters are deliberately small. Their job is to route an agent to the
workspace's canonical protocol.

| Agent/tool | File created by default | Discovery behavior | Canonical target |
| --- | --- | --- | --- |
| Codex / AGENTS.md tools | `AGENTS.md` | Usually discovered automatically from repository root toward the current directory | `MEMORY/01-rules/workspace-protocol.md` |
| Claude Code | `CLAUDE.md` | Read by Claude Code and compatible Claude workflows | Same canonical protocol |
| Cursor | `.cursor/rules/000-agent-workspace.mdc` | Cursor rule discovery | Same canonical protocol |
| Gemini CLI | `GEMINI.md` | Gemini CLI project instruction discovery | Same canonical protocol |
| GitHub Copilot | `.github/copilot-instructions.md` | GitHub Copilot repository instruction discovery | Same canonical protocol |

## Adapter Rules

1. Keep the adapter under about 40 lines.
2. Link to the canonical protocol and workspace index.
3. Include only the minimum startup path and red lines.
4. Do not paste the full protocol into multiple adapter files.
5. If an adapter cannot link to a file, include a short bootstrap instruction
   that tells the agent to read the canonical path.
6. Update the adapter when the canonical path moves; do not keep a stale
   duplicate alive.

## Nested Repositories and Monorepos

If a code repository is nested or vendored, add a nested `AGENTS.md` near the
code subtree. The nested file should explain local build/test commands and
state which parent rules still apply. Nested instructions should not fork the
authority model.
