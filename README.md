# Agent Workspace Protocol

Agent Workspace Protocol is a portable, cross-agent convention for making a
workspace legible to humans and AI agents.

Its goal is not to prescribe the "perfect" folder tree. Its goal is to make
every piece of context **judgeable, sliceable, and traceable**:

- judgeable: a reader can tell whether content is a rule, input, output,
  history, or scratch material;
- sliceable: an agent can load the smallest relevant context instead of
  reading the whole workspace;
- traceable: content has a source, status, authority, and update date.

This avoids a common failure mode: one agent produces a report, and the next
agent treats that report as a requirement, specification, or current truth.

## Core Model

The protocol keeps six boundaries explicit:

| Boundary | Rule |
| --- | --- |
| Source of truth | One canonical file per durable fact; other files link to it |
| Authority | User instruction > active rules > confirmed specs > code/tests > derived outputs > history |
| Input vs output | Generated reports and exports are not inputs unless explicitly promoted |
| Code vs knowledge | Code keeps its own version control; knowledge stores paths and commit anchors |
| Memory vs history | Current state, decisions, and session logs have separate homes |
| Agent vs workspace | Reusable agent behavior is installed globally; project rules and memory live in the workspace |

## What Is Installed Where

This project deliberately separates two installation scopes:

| Scope | What it contains | Typical location | Should it be committed to a project? |
| --- | --- | --- | --- |
| Agent scope | The reusable `agent-workspace-protocol` skill | Codex: `$CODEX_HOME/skills/agent-workspace-protocol`, or `~/.codex/skills/agent-workspace-protocol`; Claude Code: `~/.claude/skills/agent-workspace-protocol` | No |
| Workspace scope | Entry files, adapters, and the workspace's canonical protocol | `<workspace>/AGENTS.md`, `<workspace>/MEMORY/`, adapter files | Yes |

The agent-scope skill teaches an agent how to bootstrap, audit, and maintain a
workspace. The workspace-scope files define the rules for that specific
workspace. Do not put project secrets, project history, or project-specific
memory in the global skill.

For a fuller explanation, see [docs/install-scopes.md](docs/install-scopes.md).

## Quick Start

Preview a user-level Codex skill installation:

```powershell
.\install.ps1 --dry-run
```

Install the Codex skill and bootstrap a new workspace:

```powershell
.\install.ps1 --workspace C:\path\to\workspace
```

On macOS or Linux:

```sh
./install.sh --dry-run
./install.sh --workspace /path/to/workspace
```

The default behavior is:

1. Install the reusable skill into the user-level Codex skill directory.
2. If `--workspace` is supplied, initialize workspace entry files and a
   `MEMORY/` skeleton.
3. Refuse to overwrite existing files unless `--force` is supplied.

Useful options:

```text
--scope agent|project     Install the skill globally or inside a workspace
--runtime codex|claude    Select a known skill root
--skill-root PATH         Use an explicit skill root
--workspace PATH          Workspace to bootstrap
--agents LIST             codex,claude,cursor,gemini,copilot,all
--no-skill                Bootstrap the workspace only
--no-workspace            Install the skill only
--dry-run                 Print actions without writing
--force                   Overwrite conflicts
--backup                  Back up conflicting files before overwrite
```

Examples:

```sh
# Install for Claude Code globally and initialize this repository
./install.sh --runtime claude --workspace . --agents all

# Install at project scope under .agents/skills and create only Codex adapters
./install.sh --scope project --workspace . --agents codex

# Audit or bootstrap manually
python skill/agent-workspace-protocol/scripts/bootstrap_workspace.py \
  --workspace . --agents all --dry-run
```

## Default Workspace Shape

The bootstrap templates use an opinionated default:

```text
workspace/
  AGENTS.md
  CLAUDE.md
  GEMINI.md
  README.md
  .cursor/rules/000-agent-workspace.mdc
  .github/copilot-instructions.md
  MEMORY/
    01-rules/
    02-structure/
    03-sessions/
    04-glossary/
    05-state/
    06-decisions/
  10-docs/
  20-projects/
  30-data/
  40-deliverables/
  50-assets/
  60-research/
  90-temp/
  99-archive/
```

The layout is a useful default, not a protocol requirement. A workspace may
rename or merge categories if it updates its own map and keeps the authority
model intact. See [references/workspace-protocol.md](skill/agent-workspace-protocol/references/workspace-protocol.md).

## Is "Code and Project Separate" Reasonable?

Yes, as a strong default in multi-agent workspaces.

Code and knowledge usually have different lifecycles, review processes,
permissions, and release rhythms. Keeping the canonical code repository
separate prevents an agent from treating source files, generated artifacts,
and project memory as one context pool.

The general form is:

1. Keep application code in its own version-controlled repository, or at
   least in a clearly isolated subtree of a monorepo.
2. Keep the knowledge workspace focused on rules, specs, project state,
   decisions, data maps, and delivery outputs.
3. Store a code map with repository URL/path, purpose, default branch, entry
   document, last verified commit, and verification date.
4. Give each code repository its own `AGENTS.md` and project documentation.
5. Do not copy source code into the knowledge workspace just to make it
   searchable.

If the team intentionally keeps code and docs in one monorepo, the boundary
still applies inside that repository: use explicit directories and entry
files rather than relying on agents to infer intent.

## Supported Agent Adapters

| Agent/tool | Workspace entry | Installer flag |
| --- | --- | --- |
| Codex and AGENTS.md-compatible tools | `AGENTS.md` | `codex` |
| Claude Code | `CLAUDE.md` | `claude` |
| Cursor | `.cursor/rules/000-agent-workspace.mdc` | `cursor` |
| Gemini CLI | `GEMINI.md` | `gemini` |
| GitHub Copilot | `.github/copilot-instructions.md` | `copilot` |

All adapters are pointers. They must not duplicate the canonical protocol.
See [docs/adapter-matrix.md](docs/adapter-matrix.md).

## Safety

This repository contains only generic templates and tooling. It must never
contain real credentials, customer data, private repository paths, or project
history.

When adopting it:

- keep secrets outside version control or in a deliberate secret store;
- add sensitive paths to `.gitignore` before the first commit;
- scan the repository before publishing it;
- never let an agent copy a global skill into a project and call that project
  memory;
- never promote a generated report to a requirement without an explicit edit
  and review.

## References and Prior Art

The protocol combines ideas from agent instruction files, context engineering,
skills, memory banks, architecture decision records, and documentation
practices. Full links and notes are in [docs/references.md](docs/references.md).

## License

MIT. See [LICENSE](LICENSE).
