# Trellis

**Grow with structure.** 让软件有序生长，让人始终掌握项目。

Trellis 是面向 Codex 和 Claude Code 的轻量开发 Skill 套件。八个稳定入口，按用户意图动态选择五个上游项目的能力，宿主 Agent 自主执行；关键设计和验收由人掌控。

[English](README.en.md) · [架构](docs/architecture.md) · [依赖](docs/DEPENDENCIES.md) · [更新记录](CHANGELOG.md)

## 在线安装

**无需手动 `git clone`，在终端运行对应命令即可。**

需要 Bash、curl、tar、Git、Python 3.9+（Linux、macOS 或具备这些工具的 WSL）。安装器从 GitHub 下载临时源码包，再自动下载五个锁定 Commit 的上游仓库，仅将八个 Trellis 入口放入宿主 Skills 目录；不会执行上游安装器或自动启用全局 Hook。Archify 等原生工具另需 Node、浏览器等环境，按任务准备。

**Codex**

```bash
curl -fsSL https://raw.githubusercontent.com/datanger/Trellis/main/install-online.sh | bash -s -- --host codex
```

**Claude Code**

```bash
curl -fsSL https://raw.githubusercontent.com/datanger/Trellis/main/install-online.sh | bash -s -- --host claude
```

**同时安装两端**

```bash
curl -fsSL https://raw.githubusercontent.com/datanger/Trellis/main/install-online.sh | bash -s -- --host both
```

默认使用 `main` 分支及用户级安装。需要固定发布版本时，使用对应 [Release](https://github.com/datanger/Trellis/releases) 的 Tag，例如：

```bash
curl -fsSL https://raw.githubusercontent.com/datanger/Trellis/v0.2.2/install-online.sh | bash -s -- --host codex --version v0.2.2
```

**项目级安装**（在项目目录中运行，或显式指定 `--target`）：

```bash
curl -fsSL https://raw.githubusercontent.com/datanger/Trellis/main/install-online.sh | bash -s -- --host both --scope project --target /path/to/project
```

用户级入口位于 `~/.agents/skills`（Codex）、`~/.claude/skills`（Claude Code）；项目级入口位于项目对应目录。私有依赖位于版本化 toolkit，下载的临时源码包在退出后清理。安装后开启新会话。Codex 使用 `$trellis-init`（或 Skills 选择器）；Claude Code 使用 `/trellis-init`。其他入口同理。`--offline` 只用于包装器开发，缺少上游时相关能力不可用。

如果希望先检查下载的脚本再执行，可以先用 `curl -fsSL <上述脚本 URL> -o install-online.sh` 下载，阅读后运行 `bash install-online.sh --host codex`。已有源码的开发者也可以继续直接执行 `./install.sh`。

## 在线升级

不需要保留源码目录。使用原来的 host、scope、target 加 `--replace`：

```bash
curl -fsSL https://raw.githubusercontent.com/datanger/Trellis/main/install-online.sh | bash -s -- --host both --replace
```

此选项仅替换 Trellis 管理的入口，不覆盖其他 Skills。旧 toolkit 不会被自动删除。升级后开启新会话。

### 迁移已有项目需求

已有表格、无序列表或 v0.1 状态文件的项目，先保存 Git 修改，然后使用已安装的新版本 toolkit 执行（先预览，人工确认再 apply）。用户级安装示例，项目级安装则将路径替换为项目下的 `.trellis/toolkit/0.2.2/trellis.py`：

```bash
python3 ~/.trellis/toolkits/0.2.2/trellis.py --project /path/to/project migrate-requirements
python3 ~/.trellis/toolkits/0.2.2/trellis.py --project /path/to/project migrate-requirements --apply
python3 ~/.trellis/toolkits/0.2.2/trellis.py --project /path/to/project requirements-check
```

迁移先预览，确认后才写入。原文档、旧状态及迁移报告保留在 `.trellis/requirements-list-backup/` 或 `.trellis/v0.1-backup/`。旧需求没有日期时采用迁移日期，并在报告中明确列出；待确认项不纳入正式列表，保留在报告中供人工确认。旧审批不自动生效；人工审查并更新旧 AGENTS.md/CLAUDE.md 规则。

## 八个入口

| Skill | 使用场景 |
|---|---|
| `trellis-init` | 初始化文档、工程规则、接管已有项目 |
| `trellis-requirements` | 原始需求、功能拆解、修改删除、澄清 |
| `trellis-design` | 技术方案、架构、流程、技术对比 |
| `trellis-contract` | 接口、样例、代码骨架、骨架联调 |
| `trellis-dev` | 功能实现、算法优化、前后端、Bug 修复 |
| `trellis-accept` | 测试、验收、发布检查 |
| `trellis-audit` | Bug、文档一致性、安全、质量审查 |
| `trellis-simpler` | 文档、代码、测试整理 |

例如 `$trellis-audit 检查文档一致性` 与 `$trellis-audit 检查潜在 Bug` 选择不同能力；`$trellis-simpler 整理 README` 无需完整开发流程。审查默认只读，整理保持既有行为。用户无需记住内部能力名。

## 需求文档

两个文档均为可直接编辑的 Markdown 有序列表，只记录需求说明及最后编辑日期。删除使用删除线，Git 追溯历史，不使用表格或永久需求 ID。

原始需求：

```markdown
1. 将 AGENT.md 更名为 AGENTS.md。（2026-11-24）
2. ~~每个模块独立创建测试说明。~~（2026-11-24）
```

需求拆解（每个分类从 1 开始）：

```markdown
## 技术设计

1. 使用 Archify 生成架构图。（2026-11-24）
2. 将 SVG 嵌入技术文档。（2026-11-24）

## 测试验收

1. 支持自动化回归测试。（2026-11-24）
```

AI 推导的功能需求经人工确认后纳入正式列表。详见 [规则](docs/requirements-rules.md)。

## 使用方式

用户只需要选择入口并用自然语言描述任务，不需要知道上游 Skill 名称。支持从任意阶段切入、复用已有需求/设计/接口，以及继承宿主原生 `/plan` 的计划。

```text
/trellis-contract 根据已有需求及技术方案设计接口文档
/trellis-contract 根据已确认的接口创建代码骨架
/trellis-contract 使用样例数据进行骨架联调
/trellis-dev 执行刚刚生成的计划
/trellis-dev 继续开发下一个模块
/trellis-accept 验收当前模块
```

以上是 Claude Code 示例；Codex 使用 `$trellis-contract`、`$trellis-dev` 等。只执行当前请求的范围，不强制重新初始化或重复规划。对于复杂项目，按[渐进式开发规范](docs/progressive-development.md)衔接设计、接口、骨架、样例联调、逐模块实现及验收；简单任务直接执行和验证。

### 内部 Skill 调用

八个入口均有独立工作流说明，按用户任务选择具体上游子 Skill，并区分必需和条件调用。Agent 在相关操作之前读取真正的上游文件，而非仅参考能力名称。默认开发自动使用 Ponytail full，无需用户指定；已有 Plan 自动复用 Superpowers 的 executing-plans 方法，按需引入 TDD 和渐进式实现、代码审查，最终执行真实验证。

| 入口 | 典型任务的主要子能力（按需选择） |
|---|---|
| [init](skills/trellis-init/workflows.md) | constitution、context-engineering、ci-cd-and-automation |
| [requirements](skills/trellis-requirements/workflows.md) | specify、clarify、interview-me、checklist |
| [design](skills/trellis-design/workflows.md) | plan、brainstorming、ponytail、archify |
| [contract](skills/trellis-contract/workflows.md) | api-and-interface-design、ponytail、archify、test-driven-development |
| [dev](skills/trellis-dev/workflows.md) | executing-plans、ponytail、incremental-implementation、test-driven-development、systematic-debugging、verification-before-completion |
| [accept](skills/trellis-accept/workflows.md) | test-engineer、verification-before-completion、converge、shipping-and-launch |
| [audit](skills/trellis-audit/workflows.md) | code-review-and-quality、ponytail-audit、ponytail-review、archify |
| [simpler](skills/trellis-simpler/workflows.md) | ponytail、code-simplification、documentation-and-adrs、verification-before-completion |

五个锁定上游：Spec Kit、Superpowers、Ponytail、Archify、Agent Skills。保留原有 136 项资源、61 个 Skill 文件及 91 个能力族，具体工作流与能力清单互补；特殊能力通过 `catalog` 反查，重复能力仅选择主要方法。原生工具需要对应宿主和环境，不可用时明确报告。详见[依赖说明](docs/DEPENDENCIES.md)。

Trellis 由宿主 Agent 解释执行，未引入自定义状态机、审批 Token 或测试凭证数据库。真实宿主执行效果需要独立验证；不会将结构化映射当作已经执行的证据。

## 可选工具

以下命令在 Trellis 源码目录执行；只做在线安装的用户可使用相应版本 toolkit 中的 `trellis.py`。

```bash
python3 trellis.py validate
python3 trellis.py catalog audit
python3 trellis.py deps doctor
python3 trellis.py --project /path/to/project requirements-check
python3 -m unittest discover -s tests -v
```

本地测试验证安装、能力映射、文档检查和迁移等确定性能力；不能证明所有原生工作流在 Codex/Claude Code 的实际运行效果，详见 [真实宿主验收](docs/host-acceptance.md)。

## 版本发布（维护者）

更新 `VERSION` 和 `CHANGELOG.md` 后推送到 `main`，GitHub Actions 会在验证通过后创建对应 Tag 和 Release。也可以在 Actions 中手动运行 **Publish release**，或在与远程 `main` 一致的本地源码目录运行 `./publish.sh`（需要已登录的 GitHub CLI）。已有版本不会被覆盖。
