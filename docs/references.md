# References and Prior Art

These are useful references, not authorities over this project. Where they
conflict, this repository's documented protocol is the maintainer's chosen
interpretation; project-level rules still win inside their own workspace.

## Agent Instructions and Skills

- AGENTS.md: <https://agents.md/>
  A simple, tool-friendly convention for repository instructions.
- Agent Skills standard: <https://agentskills.io/home>
  The open folder-based convention for a required `SKILL.md` plus optional
  scripts, references, and assets.
- OpenAI Codex documentation: <https://developers.openai.com/codex/>
  Current Codex capabilities, configuration, skills, and `AGENTS.md` behavior.
- OpenAI Codex skills: <https://developers.openai.com/codex/skills>
  Official Codex skill guidance, including user and repository scopes.
- OpenAI Skills repository: <https://github.com/openai/skills>
  Official examples of the folder-based skill format and validation tooling.
- OpenAI Skills guide: <https://learn.chatgpt.com/docs/build-skills>
  Skill packaging and progressive disclosure concepts.
- Anthropic Agent Skills:
  <https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills>
  Reusable capability packages and progressive context loading.

## Context Engineering

- Anthropic, Effective context engineering for AI agents:
  <https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents>
  Context as a finite resource; compaction, memory, and tool design.
- Anthropic, Claude Code best practices:
  <https://www.anthropic.com/engineering/claude-code-best-practices>
  Project instructions, exploration, verification, and context management.
- Chroma, Context Rot:
  <https://www.trychroma.com/research/context-rot>
  Evidence that more context is not always better context.

## Memory and Documentation Structures

- Cline Memory Bank:
  <https://github.com/cline/cline/blob/main/docs/best-practices/memory-bank.mdx>
  Active context files and a project brief pattern.
- Architecture Decision Records:
  <https://adr.github.io/>
  Capturing decisions and consequences.
- MADR:
  <https://github.com/adr/madr>
  A practical ADR template.
- Diataxis:
  <https://diataxis.fr/>
  Separating tutorials, how-to guides, reference, and explanation.
- Docs as Code:
  <https://www.writethedocs.org/guide/docs-as-code/>
  Review, version, test, and publish documentation like code.
- Johnny.Decimal:
  <https://johnnydecimal.com/documentation/introduction>
  Stable, short, human-readable numbered categories.
- llms.txt:
  <https://llmstxt.org/>
  A lightweight map for language models; useful as a public documentation
  index, not a substitute for authority metadata.

## Engineering and Specification Workflows

- GitHub Spec Kit:
  <https://github.github.com/spec-kit/>
  Structured specification, planning, implementation, and validation flow.
- OpenAI Harness Engineering:
  <https://openai.com/index/harness-engineering/>
  Practical framing for making agent work observable and verifiable.

## What This Project Takes From Each

| Source | Adopted idea |
| --- | --- |
| AGENTS.md | One common project entry file |
| Agent Skills | Progressive disclosure and reusable capability packaging |
| Context engineering | Small maps before large manuals |
| Memory Bank | Separate active context from history |
| ADR/MADR | Decisions need their own record and rationale |
| Diataxis | Different documentation purposes should not be mixed |
| Docs as Code | Version, review, and validate knowledge |
| Johnny.Decimal | Stable numbered categories |
| Spec Kit | Explicit specification and validation stages |
| Harness Engineering | Verification evidence and observable outcomes |
