# 安装范围

这里有两样不同的东西需要安装。把它们混为一谈，是使用中最大的困惑来源。

如果只记住一条规则：可复用 skill 安装在 agent 层，工作区特定规则和记忆安装在工作区层。

## Agent 层

Agent 层将可复用 skill 安装到智能体运行时的 skill 目录。

| 运行时 | 常见用户级 skill 根目录 |
| --- | --- |
| Codex | `$CODEX_HOME/skills`，回退到 `~/.codex/skills` |
| Claude Code | `~/.claude/skills` |
| 自定义 Agent Skills 运行时 | 通过 `--skill-root` 指定 |

Agent 层文件属于设备或用户配置，不是项目记忆，也不应提交到每个项目。

使用 agent 层后，未来任意工作区中的智能体都可以执行类似请求：

> 使用 Agent Workspace Protocol 审计这个工作区。

## 工作区层

工作区层安装实际面向项目的约定：

- `AGENTS.md`；
- `CLAUDE.md`、`GEMINI.md`、Cursor 和 Copilot 适配器；
- `MEMORY/` 结构；
- 项目规则正本 `MEMORY/01-rules/workspace-protocol.md`；
- 项目地图和索引。

这些文件属于项目，因为它们定义项目的上下文边界。应经过审查、版本管理，并且只通过
明确模板或迁移流程复制。

使用工作区层后，进入项目的每个人和智能体都会遵守同一套规则。

## 项目内 skill 安装

某些运行时支持 `.agents/skills/` 之类的项目内 skill。这适合希望把 skill 本身和
仓库一起版本化的团队。

它仍然不同于工作区记忆：

- skill 包含可复用说明；
- 工作区记忆包含当前项目的事实和决策。

安装器同时支持两种：

```sh
# 用户或设备级 skill
python skill/agent-workspace-protocol/scripts/install.py \
  --scope agent --runtime codex

# 项目内 skill
python skill/agent-workspace-protocol/scripts/install.py \
  --scope project --workspace .
```

## 推荐默认方案

个人用户：

1. 在 agent 层安装一次 skill。
2. 每个需要约定的项目运行一次工作区 bootstrap。
3. 项目规则和记忆跟随仓库提交。
4. 提交前审查生成的入口文件。

团队：

1. 决定每位开发者安装 skill，还是将 skill 放进项目内。
2. 提交工作区适配器和规则正本。
3. 增加链接、密钥和根目录杂项文件的 CI 检查。

## `CLAUDE.md` 不是协议正本

`CLAUDE.md` 是 Claude Code 入口适配器，属于工作区层，并且必须指向共享规则正本。
它不是跨智能体规则手册，也不是全局 skill。

`GEMINI.md`、Cursor 规则和 Copilot 说明遵循同一模式。运行时特定入口文件都是地图，
长期规则保留在工作区规则正本中。
