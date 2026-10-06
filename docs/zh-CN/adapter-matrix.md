# 适配矩阵

适配器刻意保持简短，职责是让智能体找到工作区规则正本。

| 智能体或工具 | 默认创建文件 | 发现方式 | 正本目标 |
| --- | --- | --- | --- |
| Codex / AGENTS.md 工具 | `AGENTS.md` | 通常从仓库根目录向当前目录自动发现 | `MEMORY/01-rules/workspace-protocol.md` |
| Claude Code | `CLAUDE.md` | Claude Code 和兼容工作流读取 | 同一规则正本 |
| Cursor | `.cursor/rules/000-agent-workspace.mdc` | Cursor 规则发现机制 | 同一规则正本 |
| Gemini CLI | `GEMINI.md` | Gemini CLI 项目说明发现机制 | 同一规则正本 |
| GitHub Copilot | `.github/copilot-instructions.md` | GitHub Copilot 仓库说明发现机制 | 同一规则正本 |

## 适配器规则

1. 适配器保持在约 40 行以内。
2. 指向规则正本和工作区索引。
3. 只包含最小启动路径和红线。
4. 不要把完整协议粘贴到多个适配器。
5. 如果适配器不能链接文件，写一句最短指令，让智能体读取正本路径。
6. 正本路径移动时同步更新适配器，不能保留过期副本。

## 嵌套仓库和 Monorepo

如果代码仓库嵌套或 vendor 在工作区中，在代码子树附近增加嵌套 `AGENTS.md`。嵌套
文件说明本地构建和测试命令，以及哪些父级规则仍然适用。嵌套说明不得分叉权威模型。
