---
id: AWP-000
type: rule
status: active
authority: authoritative
scope: workspace
source: user + agent-workspace-protocol
updated: {{DATE}}
verified: pending-user-review
version: 1.0
---

# Agent Workspace Protocol

This is the canonical workspace protocol. Agent-specific files such as
`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, Cursor rules, and Copilot instructions
are adapters that point here. They must not maintain competing copies.

## 0. Purpose

The workspace must let a new human or agent answer four questions before
changing anything:

1. Which content is authoritative?
2. Which content is input, and which is output or history?
3. What should be read first, and when should reading stop?
4. Where should new content be stored, indexed, and marked?

The goal is not perfect aesthetics. The goal is context that is judgeable,
sliceable, and traceable.

## 1. Core Principles

### AWP-1: Single Source of Truth

Keep one canonical file for each durable fact, rule, specification, or
decision. Indexes and summaries link to the canonical file and must not
duplicate a second full version.

### AWP-2: Authority Tiering

Classify content by authority:

| Level | Content |
| --- | --- |
| L0 | The user's current instruction |
| L1 | Active workspace rules |
| L2 | Active, authoritative specifications and contracts |
| L3 | Code and executable tests |
| L4 | Derived outputs: reports, exports, generated documentation |
| L5 | History: sessions, archives, scratch work |

Higher levels win. A derived output does not become a requirement because it
is newer.

### AWP-3: Maps Before Manuals

Automatically loaded entry files should be short navigation maps. Put detailed
procedures in references and read them only when relevant.

### AWP-4: Status, Authority, and Provenance

Formal files must be able to answer:

- What kind of file is this?
- Is it active, draft, superseded, deprecated, or archived?
- Is it authoritative, derived, or non-authoritative?
- Where did it come from?
- When was it last materially updated?
- Has it been verified?

### AWP-5: Outputs Are Not Inputs

AI-generated deliverables and exports live in the output layer. They are
non-authoritative by default. They may become inputs only after explicit human
approval or a reproducible verification and promotion step.

### AWP-6: Code and Knowledge Are Separate

Application code normally keeps its own version control. The knowledge
workspace stores a code map, purpose, branch, entry document, and verified
commit anchor. Do not copy source code into the knowledge workspace merely to
make it searchable.

### AWP-7: Current State, Decisions, and History Are Separate

- Current state is short and replaces outdated conclusions.
- Decision records explain why a durable choice was made.
- Session records explain what happened and are non-authoritative history.

Do not make a growing session log the only place where current truth exists.

### AWP-8: Stable Top-Level Categories

Prefer a small, stable set of top-level categories. Add a new category only
after explaining how the existing categories failed and updating the layout
document.

### AWP-9: Sensitive Data Is Isolated

Credentials must not be copied into summaries, examples, reports, logs, or
generated artifacts. Use a secret manager or an explicitly ignored local file.
If a credential is exposed, rotate it first.

### AWP-10: Conflicts Are Surfaced

If two authoritative sources conflict and the authority order does not resolve
them, stop the affected write and ask the user. Do not silently choose.

## 2. Default Workspace Layout

This layout is a default. Rename or merge categories only by updating this
protocol and the directory-layout document.

| Path | Purpose | Default authority |
| --- | --- | --- |
| `MEMORY/` | Durable workspace memory | High, by subtype |
| `10-docs/` | Requirements, design, manuals, meeting records | Input when active |
| `20-projects/` | Project knowledge, plans, state, code maps, local tools | Medium |
| `30-data/` | Raw and processed data plus data dictionaries | Medium |
| `40-deliverables/` | Final reports, exports, presentations | Derived output |
| `50-assets/` | Images, fonts, styles, static templates | Medium |
| `60-research/` | External research and reference material | Medium-low |
| `90-temp/` | Scratch work and intermediate results | Lowest |
| `99-archive/` | Superseded material kept for traceability | History |

Root-level files should be limited to navigation and governance files such as
`README.md`, `AGENTS.md`, agent adapters, `.gitignore`, and the category
directories.

## 3. Memory Structure

The recommended `MEMORY/` structure is:

| Path | Purpose |
| --- | --- |
| `MEMORY/01-rules/` | Active user rules and this protocol |
| `MEMORY/02-structure/` | Directory, naming, and classification rules |
| `MEMORY/03-sessions/` | Non-authoritative task history |
| `MEMORY/04-glossary/` | Terms and abbreviations |
| `MEMORY/05-state/` | Short current-state summary |
| `MEMORY/06-decisions/` | Architecture and process decision records |

`MEMORY/README.md` is the index. Every new durable memory entry must be
registered there.

## 4. Metadata Standard

Use YAML front matter for formal files under `MEMORY/`, `10-docs/`,
`20-projects/`, `30-data/`, `40-deliverables/`, and `60-research/`.

Suggested fields:

```yaml
---
id: AWP-000
type: rule
status: active
authority: authoritative
scope: workspace
source: user
updated: 2026-01-01
verified: pending-user-review
derived_from: optional/path/or/url
supersedes: optional/path
sensitivity: internal
---
```

Controlled values:

| Field | Values |
| --- | --- |
| `type` | `rule`, `spec`, `reference`, `output`, `session`, `decision`, `data`, `asset` |
| `status` | `draft`, `active`, `deprecated`, `superseded`, `archived` |
| `authority` | `authoritative`, `derived`, `non-authoritative` |
| `verified` | `verified`, `pending-user-review`, `not-verified` |
| `sensitivity` | `internal`, `sensitive`, `credential` |

Adapters and simple README files may be exempt when the workspace's rules say
so, but they must still be concise and accurate.

## 5. Reading Protocol

Use this order:

1. Read the nearest agent entry map.
2. Read the workspace memory index.
3. Read only relevant active rules.
4. Read current state.
5. Read the relevant category README or index.
6. Read specific files.
7. Read code only when behavior must be understood, and record the code
   revision used.

Do not bulk-read unrelated directories. For long files, read metadata,
headings, and summaries first.

## 6. Content That Is Not Automatically Input

The following are not requirements or current truth by default:

- final outputs under `40-deliverables/`;
- scratch work under `90-temp/`;
- archived material under `99-archive/`;
- session logs;
- files with `draft`, `deprecated`, `superseded`, or `archived` status.

They become usable as inputs only when the user explicitly references them or
when a documented promotion changes their status and authority.

## 7. Writing Protocol

Before writing:

1. Check whether a canonical file already exists.
2. Decide the category, status, authority, and source.
3. Decide whether the memory index must be updated.
4. Decide whether the change requires a decision record.
5. Check for credentials and sensitive data.

After writing:

1. Add or update metadata.
2. Update the relevant index.
3. Distill durable current conclusions into state.
4. Record a concise session entry when the workspace requires it.
5. Mark replaced content as `superseded` and link the replacement.
6. Clean temporary work or mark what must remain.

Never silently overwrite durable content or duplicate a canonical rule.

## 8. Rule Intake and Placement

Installing the skill or bootstrapping a workspace does not create a background
watcher. When an agent writes a new or changed rule during a session, classify
it before writing.

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

Before writing, search for an existing canonical file. If one exists, update it
instead of creating a duplicate. After writing, update the relevant index,
current state, and decision record when the change affects structure or
authority. Move valuable `90-temp/inbox/` material to a durable category before
task completion.

Manual edits made outside an agent session are not moved automatically.

## 9. Output Promotion

To promote a generated output to an input:

1. Identify the consumer and the exact promoted scope.
2. Verify the content or obtain explicit user confirmation.
3. Change status to `active` and authority to `authoritative`.
4. Move it to the correct canonical category.
5. Record the promotion in state or a decision record.

Promotion is a deliberate event, not an incidental file move.

## 10. Code Map

Each external code repository should have a row in the workspace code map:

| Field | Meaning |
| --- | --- |
| Repository | Stable short name |
| Location | Repository URL or external path |
| Purpose | What the repository owns |
| Default branch | Branch used as the baseline |
| Entry document | Usually the repository's `AGENTS.md` or README |
| Verified commit | Commit SHA used for the last verified conclusion |
| Verified date | When the anchor was checked |

Each code repository should carry its own local agent instructions, build/test
commands, and documentation. The knowledge workspace links to it rather than
duplicating it.

## 11. Secrets and Sensitive Data

1. Prefer a real secret manager for credentials.
2. If local secret files are unavoidable, place them outside version control
   and ignore their paths before committing.
3. Never copy secrets into a session summary, report, prompt template,
   example, or adapter.
4. Record the location and purpose of a secret reference, not the value.
5. Rotate a credential immediately if it is committed or exposed.

## 12. Naming and Links

1. Use lowercase short directory names with a two-digit ordering prefix.
2. Do not use spaces or platform-reserved characters in filenames.
3. Prefix date-sorted files with `YYYY-MM-DD-`.
4. Use Markdown and UTF-8 for text.
5. Use relative links inside the workspace.
6. Keep one canonical path per artifact; update the index when a path moves.

## 13. Task Lifecycle

### Start

- read the entry map and relevant indexes;
- identify input authority;
- identify code revision and environment assumptions;
- state the intended write scope when it is not obvious.

### Execute

- read progressively;
- do not promote derived content implicitly;
- surface unresolved conflicts;
- keep temporary artifacts in the temporary category.

### Finish

- place durable files in their categories;
- add status and provenance;
- update indexes and current state;
- preserve or clean temporary files intentionally;
- report paths, verification evidence, and unverified items.

## 14. Documentation Gardening

Run periodically:

- root has no accidental files;
- indexes cover durable entries;
- links resolve on case-sensitive systems;
- outputs are marked derived;
- current state does not contradict canonical rules;
- code anchors still exist;
- superseded files point to replacements;
- temporary directories are clean;
- no credentials appear outside the intended secret location.

## 15. Changing the Protocol

For a material change:

1. State the failure or need.
2. Consider at least one alternative.
3. Record the decision.
4. Update the canonical protocol.
5. Update indexes and adapters.
6. Mark superseded content.
7. Verify the result.

If the workspace has no decision-record process, create one before making a
large structural change.

## 16. Minimum Compliance Checklist

- [ ] One canonical source for each durable fact.
- [ ] Authority levels are explicit.
- [ ] Outputs are distinguishable from inputs.
- [ ] Code and knowledge have a documented boundary.
- [ ] Current state, decisions, and sessions are separate.
- [ ] Agent adapters all point to this protocol.
- [ ] Secrets are not in tracked files.
- [ ] Indexes and links are current.

## 17. Customization

A workspace may change directory names, numbering, metadata fields, and
adapter choices. It may not remove the need to answer the four questions at
the top of this document without documenting an equivalent mechanism.

When customizing:

1. Update this protocol and the structure document together.
2. Update every adapter and index.
3. Keep the authority model explicit.
4. Verify the new workspace with a new agent or a fresh-context review.
