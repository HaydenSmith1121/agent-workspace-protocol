# Core Model

## The Problem

An AI workspace is not just a folder tree. It is a context system.

When requirements, source code, raw data, generated reports, session logs,
scratch files, and durable rules share the same visual level, an agent has to
guess what each file means. The next agent may then:

- treat a previous model's output as a requirement;
- follow an expired rule because it cannot see status;
- read a large historical document when a short current map would be enough;
- edit a duplicate copy while the canonical file drifts elsewhere;
- leak credentials because every file looks like fair game for summarization;
- mix code changes with knowledge changes that have different owners and
  release processes.

The protocol replaces guessing with explicit context boundaries.

## Four Questions

Every workspace should let a new agent answer four questions before it edits:

1. What is authoritative?
2. What is input, and what is merely an output or history?
3. What should be read first, and when can reading stop?
4. Where should new information be written, indexed, and statused?

If any answer is unclear, the workspace is not yet agent-ready.

## The Six Invariants

### 1. One Canonical Source

Durable information has one canonical location. Indexes, summaries, and entry
files link to it. They do not duplicate the full rule text.

### 2. Authority Is Ordered

Use this default order, highest first:

1. The user's current instruction.
2. Active workspace rules.
3. Active and authoritative specifications or contracts.
4. Code and executable tests.
5. Derived outputs such as reports and exports.
6. History, scratch work, and archives.

A lower level must never silently override a higher one.

### 3. Outputs Are Not Inputs

A model-generated report, table, diagram, or summary is an artifact. It is not
a requirement. It becomes an input only after a human or a documented review
process explicitly promotes it.

### 4. Code and Knowledge Have Different Jobs

Code has a build and release lifecycle. Knowledge has an interpretation and
decision lifecycle. Keep them separate by default. The knowledge layer stores
the repository map, purpose, branch, entry documentation, and a verified commit
anchor, not a copy of the code.

### 5. Current State, Decisions, and History Are Different

- Current state answers "what is true now?"
- Decisions answer "why did we choose this?"
- Sessions answer "what happened during this task?"

Do not make a long session log the only source of current truth. Distill
durable conclusions into state, rules, or decision records.

### 6. Reading Is Progressive

Entry files teach navigation. Indexes list relevant files. Detailed documents
are opened only when the task needs them. This reduces context rot and makes
the same workspace usable by models with different context limits.

## Why Cross-Agent Adapters Matter

Different tools discover different files:

- Codex and several agent tools recognize `AGENTS.md`;
- Claude Code uses `CLAUDE.md`;
- Gemini CLI uses `GEMINI.md`;
- Cursor uses `.cursor/rules/`;
- GitHub Copilot uses `.github/copilot-instructions.md`.

If each adapter contains a different full copy of the rules, every tool
eventually follows a different version. The adapter should therefore contain
only a short pointer to the canonical workspace protocol.

## What Is Reusable

The reusable part is the model and the installer, not one project's memory.

A global skill can:

- inspect an existing workspace;
- bootstrap the standard entry files;
- explain the authority model;
- detect unsafe or ambiguous structure;
- help migrate files into clearer categories.

A global skill must not:

- carry project credentials;
- contain a project's session logs;
- become the canonical home for a project's rules;
- overwrite a workspace without an explicit request and a backup path.
