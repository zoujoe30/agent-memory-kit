# Obsidian 使用指南

本仓库包含 Obsidian 的 Vault 布局、通用配置和笔记模板。应用请从 [Obsidian 官网](https://obsidian.md/download) 安装；应用本体、商标及官方服务不属于本项目的 MIT 授权范围。

## 开始使用

1. 先按 README 初始化独立私人知识库，再运行 `python3 tools/refresh.py`。
2. 在 Obsidian 中选择 **Open folder as vault / 打开文件夹作为仓库**，只选择私人库的 `memory/`。
3. 打开“记忆首页”，通过“项目目录”和“日记”浏览。
4. 在设置 → 核心插件中启用 Daily notes（每日笔记）和 Templates（模板）。本模板不安装社区插件。
5. 首次检查每日笔记设置：日期格式 `YYYY/MM/YYYY-MM-DD`、新建位置 `日记`、模板文件 `模板/日记`；检查模板插件目录为 `模板`。

初始化会将 `templates/obsidian/` 中的新建通用配置复制至私人库的 `memory/.obsidian/`，并把项目、日记和经验模板复制至 `memory/模板/`。配置使用相对路径，不包含工作区布局、最近打开记录、账户、同步或原库插件数据。已有知识库请逐项参考设置，不覆盖自己的 `.obsidian/`。

## 日常操作

- **项目**：从项目目录进入知识页，保留来源、核验日期和未决事项。
- **日记**：使用“打开今天的每日笔记”命令，新页位于 `日记/YYYY/MM/YYYY-MM-DD.md`；Agent 生成日记也使用该路径。双方编辑同一页前先协调。
- **模板**：使用“插入模板”命令插入项目或经验模板。每日笔记自动使用日记模板。
- **搜索与反向链接**：使用内置搜索、反向链接和关系图查看关联；关系图展示链接，不自动判断事实关联。
- **导航**：新增笔记后运行刷新脚本；Obsidian 会读取磁盘上的 Markdown 变化。

Obsidian 的每日笔记日期取决于本机日期设置；Agent 日记应明确使用者时区。Markdown 文件本身不带时区执行逻辑。

## 公开与同步

只分享 `templates/obsidian/` 的通用配置。私人 `.obsidian/` 可能包含插件设置、界面状态和文件名，不直接复制公开。Sync、备份和多设备同步需另行配置，本模板没有启用任何云同步。

## 官方参考与验证范围

- [配置文件夹](https://help.obsidian.md/configuration-folder)
- [每日笔记与日期子目录](https://help.obsidian.md/plugins/daily-notes)
- [模板及日期变量](https://help.obsidian.md/plugins/templates)

已验证配置 JSON、复制路径及 Markdown 导航；尚未在新建的 Obsidian GUI Vault 中完整操作验收。不同版本的设置字段可能变化，首次打开请按上述步骤核对。
