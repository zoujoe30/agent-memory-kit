# 接入与使用

## 建立私人工作区

在公共模板仓库运行 `python3 tools/init.py --destination ../my-agent-knowledge`。目标目录独立于模板仓库；私人区默认没有 Git 历史。避免将私人目录直接推到公开仓库。

向 Agent 提供私人知识库的绝对路径，按宿主支持的方式加载 `AGENTS.md`。本项目不修改任何全局 Agent 设置。接入后实际测试：让 Agent 读取入口、解释路由规则、定位一个虚构项目，并在你授权后做一次可回读的更新。

## 登记项目

`index/projects.json` 保存 `schemaVersion`、`routingPolicy` 和 `projects`。每个项目使用唯一 `id`、`name`、`aliases`、`currentKnowledgeTarget` 与 `knowledgeTargetStatus`；可增加来源日期等字段。核验状态只接受 `verified` 或 `unverified`。有实际读取证据后再标记 verified。

`index/local-paths.json` 是本机映射列表，每条包含 `id` 和绝对 `localPath`。它不替代项目身份核验。不存在的工作目录会显示警告，不阻止已有知识页的阅读。示例字段可参考 `examples/`，不要将示例事件当作事实。

当前知识目标支持知识库内相对路径或显式绝对路径。外部路径只作为导航入口；工具不会读取该文件正文。迁移机器后重新核验本机路径和权威目标。

## 日常使用

- 延续项目：先读索引、知识页和相关来源，再工作。
- 更新项目：核对目标与授权，写来源和核验日期，回读、审计。
- 整理日记：按使用者时区核验当日活动，保留非项目事项与来源缺口。
- 刷新导航：执行 `python3 tools/refresh.py`。它仅更新生成导航和日记年月索引，不改项目正文或日日记正文。

私人记忆可以由你自己的加密备份方案保护；本模板没有提供加密或云同步。不要把 `.gitignore` 当作访问控制。
