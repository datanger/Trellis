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
curl -fsSL https://raw.githubusercontent.com/datanger/Trellis/v0.2.1/install-online.sh | bash -s -- --host codex --version v0.2.1
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

### 从 v0.1.0 迁移项目需求

旧项目如果存在 `.trellis/state.json`，先在项目中停用旧工作流、保存 Git 修改，然后使用已安装的新版本 toolkit 执行（先预览，人工确认再 apply）。用户级安装示例，项目级安装则将路径替换为项目下的 `.trellis/toolkit/0.2.1/trellis.py`：

```bash
python3 ~/.trellis/toolkits/0.2.1/trellis.py --project /path/to/project migrate-requirements
python3 ~/.trellis/toolkits/0.2.1/trellis.py --project /path/to/project migrate-requirements --apply
python3 ~/.trellis/toolkits/0.2.1/trellis.py --project /path/to/project requirements-check
```

迁移拒绝覆盖已被手工修改的旧需求文档；先人工协调。它保留原 ID、历史状态及旧文件备份，省略未被功能需求引用的纯调用指令；被引用的历史无效项保留删除线并需要人工核对。第一次新增 ID 必须大于迁移报告的 `highest_legacy_id`。备份位于 `.trellis/v0.1-backup/`，历史审批、基线和测试证据不自动转换成新的有效审批。请通过现有设计文档、Git 和真实测试重新确认关键决策，移除 AGENTS.md/CLAUDE.md 中过时的逐步运行协议、旧 CI guard 调用（先审核，不自动修改）。新版本不再读写旧状态。

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

## 原始需求

Markdown 为唯一事实源，直接编辑；Git 追溯历史。纯 Skill 调用不是需求。新增编号递增，修改原行，删除加删除线，日期只保留最后编辑日期。

| 序号 | 需求描述 |
|---|---|
| R-0001 | 将 AGENT.md 更名为 AGENTS.md。（2026-11-24） |
| R-0002 | ~~每个模块独立创建测试说明。~~（2026-11-24） |

功能需求按业务分类，关联 R 编号，AI 推导待人工确认。详见 [规则](docs/requirements-rules.md)。

## 运行方式

入口识别意图 → 选择必要能力 → 宿主动态计划与执行 → 必要时人工审批 → 实际验证。轻量任务直接执行；复杂任务分阶段审查技术方案、接口、骨架及验收目标。保护已验收行为、公共契约和独立评测，不冻结全部代码文件。Git、实际测试和 CI 是证据；不再维护运行状态机、审批 Token 或测试凭证数据库。

五个锁定上游：Spec Kit、Superpowers、Ponytail、Archify、Agent Skills。保留 v0.1 的 136 项资源、61 个 Skill 文件及 91 个去重能力族；58 项任务提示仅用于语义路由，不是固定工作流。实际原生能力需要对应工具和宿主支持；不可用时报告阻塞，不伪造执行。详细见 [依赖](docs/DEPENDENCIES.md)。

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
