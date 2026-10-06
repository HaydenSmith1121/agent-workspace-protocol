# AGENTS.md

This repository publishes a reusable workspace convention. It is not a project
memory store.

## Source Map

- Public overview: `README.md`
- Simplified Chinese overview: `README.zh-CN.md`
- Reusable skill: `skill/agent-workspace-protocol/SKILL.md`
- Canonical protocol reference:
  `skill/agent-workspace-protocol/references/workspace-protocol.md`
- Agent adapter guidance:
  `skill/agent-workspace-protocol/references/adapters.md`
- Installer: `skill/agent-workspace-protocol/scripts/install.py`
- Workspace bootstrap:
  `skill/agent-workspace-protocol/scripts/bootstrap_workspace.py`

## Rules

- Keep public content generic. Do not add customer names, private paths,
  credentials, proprietary data, or session history.
- Keep one canonical protocol reference. Documentation and templates may link
  to it but must not fork the authority model.
- Treat generated examples as examples, not specifications.
- Preserve the installer's no-overwrite default.
- Keep English and Simplified Chinese workspace templates path-compatible.
- Run `python -m unittest discover -s tests -v`, the skill validator, and a
  secret scan before publishing.
- Any adapter change must update the adapter matrix and installer.
