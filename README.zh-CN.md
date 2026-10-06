# 智能体工作区协议

[English](README.md) | 简体中文

Agent Workspace Protocol 是一套可移植、跨智能体的工作区约定，目标是让人类和
AI 都能正确理解一个工作区。

它不是要求所有项目使用完全相同的目录树。它要求每一块上下文都可以被判断、切片
和追溯：

- 可判断：读者能区分规则、输入、输出、历史和临时内容；
- 可切片：智能体只读取当前任务需要的最小上下文；
- 可追溯：内容有来源、状态、权威性和更新时间。

这套规则主要解决一个常见故障：前一个智能体生成报告，后一个智能体却把报告误认为
需求、规范或当前事实。

## 核心模型

| 边界 | 规则 |
| --- | --- |
| 单一事实源 | 每个长期事实只保留一个正本，其他文件链接到正本 |
| 权威顺序 | 用户当前指令 > 有效规则 > 已确认规范 > 代码和测试 > 派生输出 > 历史 |
| 输入与输出 | 生成报告和导出文件默认不是输入，除非经过明确晋升 |
| 代码与知识 | 代码保留独立版本控制；知识层保存路径、用途和提交锚点 |
| 记忆与历史 | 当前状态、决策和会话历史分别存放 |
| 智能体与工作区 | 可复用行为安装在 agent 层；项目规则和记忆放在工作区层 |

## 安装位置

这里有两类完全不同的安装范围：

| 范围 | 内容 | 常见位置 | 是否提交到项目 |
| --- | --- | --- | --- |
| Agent 层 | 可复用的 `agent-workspace-protocol` skill | Codex：`$CODEX_HOME/skills/agent-workspace-protocol` 或 `~/.codex/skills/agent-workspace-protocol`；Claude Code：`~/.claude/skills/agent-workspace-protocol` | 否 |
| 工作区层 | 入口文件、适配器和该工作区的规则正本 | `<workspace>/AGENTS.md`、`<workspace>/MEMORY/`、各智能体适配文件 | 是 |

Agent 层 skill 教智能体如何初始化、审计和维护工作区。工作区层文件定义当前项目的
实际规则。不要把项目密钥、项目历史或项目决策放进全局 skill。

详细说明见 [安装范围](docs/zh-CN/install-scopes.md)。

## 快速开始

预览 Codex 用户级 skill 安装：

```powershell
.\install.ps1 --dry-run
```

安装 Codex skill，并初始化一个中文工作区：

```powershell
.\install.ps1 --workspace C:\path\to\workspace --language zh-CN
```

macOS 或 Linux：

```sh
./install.sh --dry-run
./install.sh --workspace /path/to/workspace --language zh-CN
```

默认行为：

1. 将可复用 skill 安装到用户级 Codex skill 目录。
2. 如果提供 `--workspace`，初始化工作区入口文件和 `MEMORY/` 骨架。
3. 默认拒绝覆盖已有文件，除非提供 `--force`。
4. 默认语言是 `en`，中文模板使用 `--language zh-CN`。

常用参数：

```text
--scope agent|project     安装到 agent 层或项目内部
--runtime codex|claude    选择已知 skill 根目录
--skill-root PATH         指定 skill 根目录
--workspace PATH          要初始化的工作区
--agents LIST             codex,claude,cursor,gemini,copilot,all
--language en|zh-CN       选择英文或简体中文模板
--no-skill                只初始化工作区
--no-workspace            只安装 skill
--dry-run                 只打印计划，不写文件
--force                   覆盖冲突文件
--backup                  覆盖前备份
```

示例：

```sh
# 安装 Claude Code 全局 skill，并创建所有智能体适配器
./install.sh --runtime claude --workspace . --agents all --language zh-CN

# 安装到项目内 .agents/skills，并只创建 Codex 适配器
./install.sh --scope project --workspace . --agents codex --language zh-CN

# 只检查工作区初始化结果
python skill/agent-workspace-protocol/scripts/bootstrap_workspace.py \
  --workspace . --agents all --language zh-CN --dry-run
```

## 默认工作区结构

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

这是推荐默认结构，不是不可修改的协议。可以重命名或合并分类，但必须更新工作区地图，
并保持权威模型不变。

## 新规则会自动放到规定位置吗

不会仅靠文件系统自动完成。

安装 skill 和初始化工作区不会在后台监听文件变化。真正的工作方式是：

1. 智能体进入工作区；
2. 读取 `AGENTS.md` 或其他适配入口；
3. 读取 `MEMORY/README.md` 和规则正本；
4. 在新增长期规则时，按照正本中的“新规则接收与自动归位”表分类；
5. 更新索引、当前状态，必要时新增决策记录。

如果用户或程序直接在目录中创建文件，而没有经过智能体，文件不会自动移动。若希望
更可靠地自动归位，应让支持 skill 或项目规则的智能体处理规则变更，并在提示中明确
要求遵循 `MEMORY/01-rules/workspace-protocol.md`。

完整说明见 [规则归位机制](docs/zh-CN/rule-intake.md)。

## 代码与项目分开存储是否合理

合理，而且在多智能体工作区中应作为强默认。

代码和知识通常有不同的生命周期、审查流程、权限和发布节奏。把正本代码仓库与知识
工作区分开，可以避免智能体把源码、生成工件和项目记忆当成同一个上下文池。

推荐做法：

1. 应用代码放在独立仓库，或者放在 monorepo 中明确的隔离子树。
2. 知识工作区保存规则、规范、项目状态、决策、数据地图和交付物。
3. 代码地图记录仓库 URL 或路径、用途、默认分支、入口文档、验证提交和验证日期。
4. 每个代码仓库维护自己的 `AGENTS.md` 和项目文档。
5. 不要为了让代码可搜索，就把源码复制到知识工作区。

## 智能体适配

| 智能体或工具 | 工作区入口 | 安装参数 |
| --- | --- | --- |
| Codex 和兼容 AGENTS.md 的工具 | `AGENTS.md` | `codex` |
| Claude Code | `CLAUDE.md` | `claude` |
| Cursor | `.cursor/rules/000-agent-workspace.mdc` | `cursor` |
| Gemini CLI | `GEMINI.md` | `gemini` |
| GitHub Copilot | `.github/copilot-instructions.md` | `copilot` |

所有适配器都只是指针，不能复制规则正本。`CLAUDE.md` 只是 Claude Code 适配器，
不是跨智能体规则，也不是全局 skill。

## 安全

本仓库只包含通用模板和工具，不应包含真实凭证、客户数据、私有仓库路径或项目历史。

采用本协议时：

- 密钥放在版本控制之外或正式密钥管理系统中；
- 首次提交前把敏感路径加入 `.gitignore`；
- 发布前扫描仓库；
- 不要把全局 skill 复制成项目记忆；
- 不要把生成报告自动提升为需求。

## 参考和既有实践

完整参考见 [参考文献](docs/zh-CN/references.md)。

## 许可证

MIT，见 [LICENSE](LICENSE)。
