# Trellis

**Grow with structure.**

让软件有序生长，让人始终掌握项目。

Trellis 是面向 Codex、Claude Code 的渐进式可控开发 Skill 套件。它不是又一套需要学习的开发工具，而是 **8 个稳定入口 + 动态任务路由 + 可替换的外部能力 + 人工审批和验收基线**。

[English README](README.en.md) · [运行机制](docs/architecture.md) · [执行协议](docs/agent-protocol.md) · [上游依赖](docs/DEPENDENCIES.md) · [发布记录](CHANGELOG.md)

> V0.1.0 是首个可运行的本地预览版本。注册表、状态机、审批、需求记录、安装器、真实测试凭证和基线保护已实现并完成本地测试。五个上游的真实下载、宿主模型工作流执行及原生工具全量集成测试尚待验证，不能将能力映射等同于全部功能已在 Codex/Claude Code 实测通过。

## 快速开始

### 1. 安装前准备

- Linux / macOS（Windows 建议使用 WSL）。Python 3.9+（推荐 3.11+）、Git、Bash、能访问 GitHub 的网络。
- 安装并登录 [Codex](https://developers.openai.com/codex/) 或 [Claude Code](https://code.claude.com/docs/en/overview)。
- 基础运行器只使用 Python 标准库。实际 Archify 图表、Spec Kit 原生扩展、浏览器测试等依赖额外的 Node.js / 浏览器 / uv / 对应宿主和项目测试框架；安装前检查相应上游说明。

获取源代码（仓库发布后）：

```bash
git clone --branch v0.1.0 https://github.com/datanger/Trellis.git
cd Trellis
```

如果拿到 `Trellis-v0.1.0.bundle`，可用 `git clone Trellis-v0.1.0.bundle Trellis && cd Trellis`；也可以解压同版本源码包后进入目录。以下命令在 Trellis 源码目录执行，而非你的业务项目目录。

### 2. 安装到 Codex

用户级：所有本地项目可用。

```bash
./install.sh --host codex --scope user
```

项目级：仅安装到指定项目。

```bash
./install.sh --host codex --scope project --target /path/to/my-project
```

安装位置：`~/.agents/skills/trellis-*/` 或 `<project>/.agents/skills/trellis-*/`。启动新会话，在 Codex CLI 或 IDE 中使用 `$trellis-init`，也可通过 `/skills` 或宿主提供的 Skill 选择器选择 `trellis-init`。

### 3. 安装到 Claude Code

```bash
./install.sh --host claude --scope user
```

项目级：

```bash
./install.sh --host claude --scope project --target /path/to/my-project
```

安装位置：`~/.claude/skills/trellis-*/` 或 `<project>/.claude/skills/trellis-*/`。新建 Claude Code 会话，在对话框使用 `/trellis-init`。

两者同时安装：

```bash
./install.sh --host both --scope user
```

若 Ubuntu 等系统默认 Python 版本较旧，已安装 Python 3.11 时可执行 `PYTHON=python3.11 ./install.sh --host both --scope user`。安装器将实际 Python 路径写入入口指令。

安装器下载并校验五个上游仓库的**精确 Commit**，仅暴露 Trellis 的 8 个入口，不自动启用外部插件、全局 Hook 或额外权限。用户级运行时位于 `~/.trellis/toolkits/0.1.0/`；项目级运行时位于 `<project>/.trellis/toolkit/0.1.0/`。项目级入口含本机运行时路径，不要直接复制到其他机器，重新执行安装器即可。用户级和项目级不建议重复安装同一名称，以免宿主选择冲突。

安装后检查（用户级示例，选择安装时的 Python）：

```bash
python3 ~/.trellis/toolkits/0.1.0/trellis.py validate
python3 ~/.trellis/toolkits/0.1.0/trellis.py deps doctor
```

`deps doctor` 检查五个实际 checkout 和文件清单，并展示本机工具。上游下载失败则安装停止，不会偷偷改用最新分支。`--offline` 仅用于开发和测试入口安装；没有依赖缓存时，上游相关步骤会明确阻断，并不是完整可用的离线套件。

> 如果已经单独安装了 Superpowers、Ponytail 等会自动接管工作流的插件，建议在使用 Trellis 的会话中关闭重复的自动触发规则。Trellis 不会擅自修改你的个人配置。

官方 Skill 加载规则：[Codex Skills](https://developers.openai.com/codex/skills) · [Claude Code Skills](https://code.claude.com/docs/en/skills)。

## 八个入口

以下为 Claude Code 对话中的调用示例。在 Codex 中将 `/` 换成 `$`，或直接从 Skill 选择器选择对应名称。它们不是 Bash 命令。

| 入口 | 适用任务 | 人需要做什么 |
|---|---|---|
| `trellis-init` | 新项目、已有项目接管、文档、工程规范、Skills、Git、CI、上下文 | 确认项目规范和权限 |
| `trellis-requirements` | 原始需求、功能拆解、需求澄清、变更、冲突检查 | 确认需求和功能范围 |
| `trellis-design` | 技术架构、方案、流程、选型、计划、可行性 | 审核原理和技术路线 |
| `trellis-contract` | 接口、数据结构、样例、骨架、全链路联调 | 分别审核接口和代码骨架 |
| `trellis-dev` | 功能实现、Bug 修复、算法优化、前后端、并行开发 | 指定范围及验收目标 |
| `trellis-accept` | 测试、评测、验收、基线、发布检查 | 确认标准及结果 |
| `trellis-audit` | Bug、质量、安全、性能、文档一致性、架构、测试有效性 | 判断问题是否需要修复 |
| `trellis-simpler` | 代码、文档、测试及结构整理 | 批准有风险的整理方案 |

同一个入口可以产生不同工作流。例如：

```text
/trellis-audit 检查项目文档是否与当前代码一致
/trellis-audit 检查数据解析模块的潜在 Bug，只报告问题
/trellis-simpler 整理技术文档，合并重复内容并改善运行原理的可读性
/trellis-simpler 简化重复代码，保持已有接口与行为不变
/trellis-dev 优化算法准确率，不能修改验收数据及评价逻辑
/trellis-accept 执行浏览器端到端测试并提供真实结果
```

Trellis 先识别意图，再选择内部任务模板、组合执行步骤、加载相应的固定版本上游 Skill。不会让你逐个调用上游命令，也不会为每个简单任务机械地走完整流程。

## 推荐使用流程

新项目或复杂功能：

```text
init → requirements → design → contract → dev → accept
          人工确认       人工审核    人工审核接口/骨架      人工验收
                                 骨架联调 → 批准执行计划
```

`audit` 和 `simpler` 随时可以使用。新增需求回到 `requirements`；重大接口、架构变化重新审批受影响的设计；小 Bug 使用 `dev` 的局部修复流程，不强制重做整套文档。

1. **需求**：原始需求按 R 编号追加，功能点按业务类别维护 F 编号，保留原文、来源、修改与撤销历史。AI 推导需求必须显式标记。主要操作均检查对话新增需求；未经过 Trellis 或项目规则的聊天不会被运行器自动拦截。
2. **设计**：先技术原理、总体架构和关键运行路径，再分别确认接口及样例、代码骨架、骨架联调。Stub 联调通过不代表真实功能已经正确。
3. **执行**：在批准范围内逐模块实现，测试、调试、代码审查、文档同步由 AI 内部完成。重大设计用 Plan Mode；确定且可验证的任务用自动执行；算法等迭代任务在宿主支持时可使用 Goal Mode，否则使用限定预算和停止条件的普通执行循环。不会默认打开全权限模式。
4. **验收**：由用户制定或批准验收脚本、指标、数据及保护文件；运行实际测试并记录结果。代码、测试、契约和文档验收基线关联 Git Commit。后续开发不得未经授权破坏。
5. **治理**：Audit 以发现和报告为主，Simpler 以授权范围内的整理为主。减少重复实现和重复文档，合并冗余测试但不能削弱行为保护。

## 人工检查点是什么样的？

Trellis 会在重要决策处暂停，提供简短的审查材料、风险、证据、需要你决定的问题和下一步动作。运行器将审批对象的文件内容绑定到审查令牌。如果审查材料发生变化，旧审批不能继续使用。

例如：接口契约已确认，Trellis 才能搭建公共类/函数骨架；代码骨架确认后，才允许使用样例和 Stub 验证系统连接。等模块真正实现并通过批准的测试后，再建立验收基线。

需要恢复会话时，在相应入口说“继续上一阶段”，Agent 读取项目状态和活动工作流。不需要记忆内部路由 ID。

## 内部能力和目录

```text
Trellis/
├── skills/                         # 八个稳定的 SKILL.md
├── registry/
│   ├── dependencies.lock.json      # 五个上游的精确 Commit
│   ├── upstream-capabilities.json  # 上游文件/资源清单
│   ├── capability-registry.json    # 主实现及互补能力
│   ├── routing-registry.json       # 路由及步骤模板
│   └── coverage.json              # 每个上游资源的归属
├── trellis/                       # Python 状态机、审批、基线、安装及依赖管理
├── docs/                          # 运行机制、Agent 执行协议
├── tests/                         # 本地自动化测试
├── install.sh
└── trellis.py
```

V0.1.0 基于五个固定 Commit 的 Git 树和公开能力清单，登记 **61 个 SKILL.md 文件（含镜像和维护专用 Skill）、136 个上游资源、91 个去重能力族、149 条路由模板**。这是注册表的结构覆盖范围，不能当作语义执行通过率。外部原生管理、维护专用命令和特定宿主功能保留对应入口及适配条件；缺少运行条件时明确阻断。

| 依赖 | Trellis 吸收的能力 |
|---|---|
| [Spec Kit](https://github.com/github/spec-kit) | 规格驱动、需求、计划、任务、一致性、Bug/Assessment、原生扩展及工作流管理 |
| [Superpowers](https://github.com/obra/superpowers) | 方案探索、计划、并行/子 Agent、TDD、调试、独立评审、证据、隔离和分支管理 |
| [Ponytail](https://github.com/DietrichGebert/ponytail) | 实现简化、Diff/全库审查、技术债、模式及宿主特有能力 |
| [Archify](https://github.com/tt-a1i/archify) | 架构、流程、时序、数据流、状态、ERD、源码证据、诊断、故事、PR、验证及导出 |
| [Agent Skills](https://github.com/addyosmani/agent-skills) | 需求访谈、前后端、工程约束、文档、代码质量、安全、性能、可观测性、CI/CD、发布 |

用户无需学习这些命令。上游相同职责由主提供者负责，不重复执行整套流程；有差异的能力作为补充保留。锁文件及覆盖注册表可审查、可升级，不能自动批准新版本。

## 项目状态与需求文件

初始化后最小持久化结构：

```text
my-project/
├── AGENTS.md / CLAUDE.md         # 人工批准的工程入口
├── docs/requirements/
│   ├── raw-requirements.md       # R-xxxx 原始请求
│   └── functional-requirements.md # Fxx-xxx 分类功能点
├── docs/design/                 # 按需：技术方案、架构、机制图
├── contracts/                   # 按需：契约、样例、验收策略
└── .trellis/
    ├── state.json               # 原始记录、任务、审批、基线的机器状态
    ├── receipts/                # 测试凭证
    ├── reports/                 # 必要的短报告及证据
    └── logs/                    # 本地运行日志（可能含敏感内容）
```

两份需求 Markdown 是由内部记录生成的人类可读视图，不是两套独立手工维护的需求数据库。使用 Trellis 更新，避免手工覆盖生成视图。迁移已有需求文档时先保留原文、获得批准、再导入，不会自动覆盖。

## 验收保护示例

由人确认机器可执行的验收策略，例如 `contracts/acceptance/parser.json`：

```json
{
  "commands": [["python", "-m", "pytest", "tests/test_parser.py"]],
  "protect": ["src/parser.py", "contracts/parser.json", "tests/test_parser.py", "docs/modules/parser.md"]
}
```

用户批准验收标准后，Trellis 执行每条命令、记录退出码、代码树哈希、日志哈希及 Git Commit。模块验收必须绑定策略文件、全部保护文件和测试凭证。修改保护文件会使 `guard` 失败，直到经过明确变更授权、回归测试和重新验收。

保护主分支和独立 CI 仍由项目负责人配置。Trellis 的本地审批文件、哈希、测试凭证并不是不可篡改的安全边界；不得给开发 Agent 独立修改评价真值及生产发布权限。

## 开发、测试和维护

```bash
python3 trellis.py validate
python3 trellis.py catalog audit
python3 trellis.py compose audit --route audit.docs-consistency
python3 trellis.py compose audit --route audit.bugs
python3 -m unittest discover -s tests -v
```

上述命令用于开发者检查运行器，不增加用户 Skill 入口。需要查看一个项目的状态时，可运行安装后工具的 `--project /path/to/project status`。详见 [执行协议](docs/agent-protocol.md) 和 [架构说明](docs/architecture.md)。

升级 Trellis 时获取新的发布 Tag，运行新版安装脚本并显式使用 `--replace`。不要修改上游缓存的固定 Commit。卸载时仅删除对应的八个 `trellis-*` 入口目录和不再使用的版本化 toolkit；保留业务项目 `.trellis/state.json` 和验收记录，不要清除整个 `.trellis`。

## 当前边界

- 本地测试覆盖注册表、路由、审批、范围控制、需求保留、测试凭证、基线保护及两种宿主的目录安装（离线）。
- 未在真实 Codex / Claude Code 会话中运行全部上游功能；原生 Spec Kit CLI、Archify Node/浏览器、Ponytail Band 等需具备宿主及额外工具。通过 [依赖检查](docs/DEPENDENCIES.md) 和 [真实宿主验收清单](docs/host-acceptance.md) 完成验证。
- 当前动态编排由宿主 Agent 进行语义选择和执行，Python 负责状态、约束及证据检查；没有另起 LLM API、没有独立进程级沙箱、没有假冒跨平台 Skill RPC。

## License

Trellis 原创代码采用 MIT；上游仓库各自遵循其许可证，见 [NOTICE](NOTICE.md)。
