---
id: AWP-002
type: reference
status: active
authority: authoritative
scope: workspace
source: agent-workspace-protocol template
updated: {{DATE}}
verified: pending-user-review
---

# 目录布局

| 路径 | 用途 |
| --- | --- |
| `MEMORY/` | 长期规则、状态、决策、术语和会话 |
| `10-docs/` | 需求、设计、手册和会议记录 |
| `20-projects/` | 项目知识、计划、代码地图和本地工具 |
| `30-data/` | 原始数据、处理后数据和数据字典 |
| `40-deliverables/` | 最终输出和生成工件 |
| `50-assets/` | 图片、字体、样式和静态模板 |
| `60-research/` | 外部研究和参考资料 |
| `90-temp/` | 临时工作 |
| `99-archive/` | 为追溯保留的旧内容 |

根目录文件限制为导航、智能体适配器、`.gitignore` 和分类目录。

## 变更流程

如果现有分类无法容纳新的工件类型：

1. 说明现有分类为什么不适合。
2. 记录决策。
3. 更新本文件和规则正本。
4. 更新索引和适配器。
5. 创建目录和 README。
