# Agent Workspace Protocol

English | [简体中文](README.zh-CN.md)

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

## Installation

There are two supported paths. Pick one:

| Path | Who runs it | Use it when |
| --- | --- | --- |
| Let an agent install it | An AI agent session | You want the workspace inspected and initialized from one instruction. This is the recommended path. |
| Manual installation | You, in a terminal | You want to run every command yourself, or the agent cannot clone and run scripts. |

Both paths need Python 3 and Git. The installer lives inside this repository,
so the repository has to reach the machine first. The agent path downloads it
for you.

### 1. Let an Agent Install It (Recommended)

Paste this into an agent session that can run shell commands, and replace the
placeholder:

```text
Install the agent-workspace-protocol skill from this public repository:
https://github.com/HaydenSmith1121/agent-workspace-protocol

Install it as a user-level Codex skill. Then initialize the workspace at
<ABSOLUTE_WORKSPACE_PATH> with all agent adapters and the Simplified Chinese
templates. Run the installer with --dry-run first, show me the planned changes,
and only continue after the dry run is valid.
```

Adjust the parts that matter for your case:

- `<ABSOLUTE_WORKSPACE_PATH>`: the project that should receive `AGENTS.md`, adapters, and `MEMORY/`;
- runtime: Codex, Claude Code, or a custom skill root (`--runtime`, `--skill-root`);
- adapters: `--agents codex,claude,cursor,gemini,copilot` or `--agents all`;
- language: `--language en` or `--language zh-CN`;
- existing project files: no extra flag is needed; local `AGENTS.md` or
  `README.md` files stay untouched and only missing files are added. Add
  `--force --backup` only when you explicitly want to replace them.

If you only want the reusable skill and no workspace files, the whole request
is one line:

```text
Install the agent-workspace-protocol skill from
https://github.com/HaydenSmith1121/agent-workspace-protocol as a user-level
Codex skill. Do not initialize any workspace.
```

The agent should clone the repository and run the included `install.ps1` or
`install.sh`. It should not invent a package-manager installation command,
because this skill is distributed as a repository rather than a published
package. Ask for `--dry-run` first: the installer refreshes its own agent-level
skill in place, skips existing workspace files by default, and the dry run
lists what it would create, update, skip, or overwrite.

### 2. Manual Installation

#### Windows PowerShell

Install the reusable Codex skill with one command, without cloning anything:

```powershell
irm https://raw.githubusercontent.com/HaydenSmith1121/agent-workspace-protocol/main/install.ps1 | iex
```

The script downloads the repository to a temporary directory and installs the
skill into the user-level Codex skill directory. It does not initialize any
workspace.

Install the skill and initialize a workspace in one command:

```powershell
$s=irm https://raw.githubusercontent.com/HaydenSmith1121/agent-workspace-protocol/main/install.ps1; & ([scriptblock]::Create($s)) --workspace "C:\path\to\workspace" --agents all --language zh-CN
```

This is one installation workflow with two targets:

- the reusable skill is installed at the agent level;
- the selected workspace receives `AGENTS.md`, adapters, and `MEMORY/`.

It does not create a Git repository or publish anything. If the workspace
already has its own `AGENTS.md` or `README.md`, those files are skipped by
default while missing files are added. Use `--force --backup` only when you
want the installer to replace them.

#### macOS or Linux

```sh
git clone https://github.com/HaydenSmith1121/agent-workspace-protocol.git
cd agent-workspace-protocol
./install.sh --no-workspace --dry-run
./install.sh --no-workspace
./install.sh --workspace /path/to/workspace --agents all --language en
```

#### From a Git Checkout

`install.ps1` and `install.sh` accept the same arguments, so a checkout can run
either of them:

```powershell
git clone https://github.com/HaydenSmith1121/agent-workspace-protocol.git
cd agent-workspace-protocol
.\install.ps1 --dry-run
.\install.ps1 --no-workspace
.\install.ps1 --workspace C:\path\to\workspace --agents all --language zh-CN
```

#### Codex Plugin Marketplace

Codex can also install the reusable skill through its plugin system:

```powershell
codex plugin marketplace add HaydenSmith1121/agent-workspace-protocol; codex plugin add agent-workspace-protocol@agent-workspace-protocol
```

This installs the skill only. After installing a plugin, restart Codex or open
a new session so the skill is discovered. Then initialize a target workspace
by asking the agent to use the skill, or use the workspace command above.

#### Defaults and Options

The default behavior is:

1. Install the reusable skill into the user-level Codex skill directory.
2. If `--workspace` is supplied, initialize workspace entry files and a
   `MEMORY/` skeleton.
3. Refresh the agent-level skill in place, and skip existing workspace files
   unless `--force` is supplied.
4. Use English templates unless `--language zh-CN` is supplied.

Useful options:

```text
--scope agent|project     Install the skill globally or inside a workspace
--runtime codex|claude    Select a known skill root
--skill-root PATH         Use an explicit skill root
--workspace PATH          Workspace to bootstrap
--agents LIST             codex,claude,cursor,gemini,copilot,all
--language en|zh-CN       Select English or Simplified Chinese templates
--no-skill                Bootstrap the workspace only
--no-workspace            Install the skill only
--dry-run                 Print actions without writing
--force                   Overwrite existing workspace files
--backup                  Back up the previous agent skill and overwritten files
```

Examples:

```sh
# Install for Claude Code globally and initialize this repository
./install.sh --runtime claude --workspace . --agents all

# Install at project scope under .agents/skills and create only Codex adapters
./install.sh --scope project --workspace . --agents codex

# Adopt the protocol in a project that already has its own AGENTS.md
./install.sh --workspace . --agents all --language zh-CN

# Audit or bootstrap manually
python skill/agent-workspace-protocol/scripts/bootstrap_workspace.py \
  --workspace . --agents all --dry-run
```

### One Command Does Not Mean One Location

The reusable skill belongs to the agent and can serve many projects. The
workspace files belong to one project and may be committed with it. A one-line
command can perform both installations, but it cannot merge those two
lifecycles into one shared directory.

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

## Will New Rules Be Placed Automatically?

Not by the filesystem alone.

Installing the skill and bootstrapping a workspace do not create a background
watcher. When an agent has loaded the workspace entry file and canonical
protocol, it can classify a new durable rule, update the canonical file, and
update the relevant index or state. Files created manually outside an agent
session are not moved automatically.

The protocol therefore includes a rule-intake table and requires agents to
classify durable content before writing. See
[docs/rule-intake.md](docs/rule-intake.md) and
[简体中文说明](docs/zh-CN/rule-intake.md).

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
