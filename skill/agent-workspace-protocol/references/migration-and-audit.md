# Migration and Audit

Use this reference when applying the protocol to an existing workspace.

## Audit Questions

### Authority

- Is there one canonical protocol?
- Are active rules distinguishable from drafts and history?
- Can a reader tell whether a specification is approved?
- Are conflicts resolved by a documented order?

### Input and Output

- Are generated reports stored separately from requirements?
- Can outputs be promoted deliberately?
- Are scratch files cleaned or clearly isolated?

### Memory

- Is there an index for durable memory?
- Are sessions separated from current state?
- Is there a record of why the structure changed?

### Code

- Is code in its own repository or clearly isolated subtree?
- Does the knowledge layer store commit anchors?
- Does each code repository have local instructions?

### Safety

- Are secrets outside version control?
- Do templates contain placeholders rather than private endpoints?
- Are generated logs and screenshots checked for credentials?

## Safe Migration Order

Do not move everything at once.

1. Inventory the current top-level structure.
2. Identify active rules and canonical files.
3. Identify secrets and exclude them from version control.
4. Add the entry map and adapter files.
5. Add indexes and status metadata to the most important files.
6. Move one category at a time and update links.
7. Mark old locations as moved or superseded.
8. Record the decision and verification evidence.
9. Add a recurring link/secret check when practical.

## Handling Duplicates

When two files appear to contain the same rule:

1. Decide which one is canonical.
2. Compare dates and provenance, but do not choose by date alone.
3. Merge missing content into the canonical file.
4. Replace the duplicate with a pointer or mark it `superseded`.
5. Update the index.
6. If the difference is consequential and cannot be resolved, ask the user.

## Handling Outputs Mixed With Inputs

Separate by lifecycle, not by file extension:

- requirement or approved design: input/specification;
- generated report or export: output;
- working notes and intermediate data: temporary;
- old final artifact: archive.

If an output contains a useful conclusion, distill that conclusion into state
or a reviewed specification. Do not make the report itself authoritative by
accident.

## Code and Knowledge Migration

When code and knowledge are mixed:

1. Identify the actual code repository root.
2. Verify its version-control state and entry documentation.
3. Create a code-map row with purpose and a commit anchor.
4. Move or link project knowledge into the knowledge workspace.
5. Leave source code under its own version-control lifecycle.
6. Add nested `AGENTS.md` for a monorepo subtree when needed.

Do not perform a large move while the code repository has uncommitted work
unless the user explicitly accepts the risk.

## Audit Output

Report findings as:

```text
Finding: what is ambiguous or unsafe
Impact: what a future agent may do incorrectly
Location: canonical path or path range
Recommendation: smallest corrective change
Priority: high/medium/low
```

Do not rewrite the workspace merely because it does not match the default
folder names. A good migration preserves working conventions and adds the
missing authority boundaries.

## Completion Criteria

A migration is complete when:

- a new agent can find the entry map and canonical protocol;
- the adapter files agree on the canonical target;
- outputs cannot be mistaken for requirements;
- durable entries have status and provenance;
- the code map has valid anchors;
- secrets are not tracked;
- links and indexes resolve;
- temporary files are intentionally retained or removed.
