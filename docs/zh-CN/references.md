# 参考文献和既有实践

以下资料是参考，不是本项目的上级权威。它们发生冲突时，以本仓库记录的协议为准；
进入某个项目后，以该项目自己的规则为准。

## 智能体说明和 Skills

- AGENTS.md：<https://agents.md/>
  面向工具的项目说明约定。
- Agent Skills：<https://agentskills.io/home>
  基于目录的 skill 约定，要求 `SKILL.md`，可选脚本、参考和资产。
- OpenAI Codex 文档：<https://developers.openai.com/codex/>
  Codex 能力、配置、skill 和 `AGENTS.md` 行为。
- OpenAI Codex Skills：<https://developers.openai.com/codex/skills>
  Codex skill 的用户级和仓库级范围。
- OpenAI Skills 仓库：<https://github.com/openai/skills>
  官方 skill 格式和校验工具示例。
- OpenAI Skills 指南：<https://learn.chatgpt.com/docs/build-skills>
  skill 打包和渐进披露。
- Anthropic Agent Skills：
  <https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills>
  可复用能力包和渐进上下文加载。

## 上下文工程

- Anthropic，Effective context engineering for AI agents：
  <https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents>
  上下文是有限资源；压缩、记忆和工具设计。
- Anthropic，Claude Code best practices：
  <https://www.anthropic.com/engineering/claude-code-best-practices>
  项目说明、探索、验证和上下文管理。
- Chroma，Context Rot：
  <https://www.trychroma.com/research/context-rot>
  更多上下文不总是更好的上下文。

## 记忆和文档结构

- Cline Memory Bank：
  <https://github.com/cline/cline/blob/main/docs/best-practices/memory-bank.mdx>
  活跃上下文文件和项目简述模式。
- Architecture Decision Records：<https://adr.github.io/>
  记录决策和后果。
- MADR：<https://github.com/adr/madr>
  实用 ADR 模板。
- Diataxis：<https://diataxis.fr/>
  区分教程、操作指南、参考和解释。
- Docs as Code：<https://www.writethedocs.org/guide/docs-as-code/>
  像代码一样审查、版本化、测试和发布文档。
- Johnny.Decimal：<https://johnnydecimal.com/documentation/introduction>
  稳定、简短、人类可读的数字分类。
- llms.txt：<https://llmstxt.org/>
  面向语言模型的轻量地图，适合公开文档索引，但不能替代权威元数据。

## 工程和规范流程

- GitHub Spec Kit：<https://github.github.com/spec-kit/>
  结构化规范、计划、实现和验证流程。
- OpenAI Harness Engineering：<https://openai.com/index/harness-engineering/>
  让智能体工作可观察、可验证。

## 本项目采用的思想

| 来源 | 采用内容 |
| --- | --- |
| AGENTS.md | 使用统一项目入口文件 |
| Agent Skills | 渐进披露和可复用能力打包 |
| 上下文工程 | 先读小地图，再读大手册 |
| Memory Bank | 活跃上下文和历史分离 |
| ADR / MADR | 决策需要单独记录并说明理由 |
| Diataxis | 不同文档目的不应该混在一起 |
| Docs as Code | 知识应版本化、审查和验证 |
| Johnny.Decimal | 使用稳定编号分类 |
| Spec Kit | 明确规范和验证阶段 |
| Harness Engineering | 保留验证证据和可观察结果 |
