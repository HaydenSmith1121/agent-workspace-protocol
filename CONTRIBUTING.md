# Contributing

Contributions should improve portability, safety, or clarity.

Before opening a pull request:

1. Run the skill validator.
2. Run the installer in `--dry-run` mode against a temporary workspace.
3. Run the bootstrap script against a temporary workspace.
4. Check for secrets and private paths.
5. Confirm that all adapter files still point to the canonical protocol.
6. When changing workspace templates, update both `workspace` and
   `workspace-zh-CN`, then run the template-parity test.

Do not add a new top-level directory merely to hold project-specific history.
Add a reference, an optional template, or a documented extension instead.

Changes to the authority model should include an ADR in this repository using
the same reasoning the protocol asks other workspaces to use.
