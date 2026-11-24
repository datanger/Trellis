# Trellis — Grow with structure

[中文说明](README.md) · [Architecture](docs/architecture.md) · [Agent protocol](docs/agent-protocol.md)

A human-in-control development workflow for Codex and Claude Code. Eight stable entry skills route natural language to task-specific workflows, use pinned external capabilities, pause at meaningful approvals and preserve accepted baselines.

## Install

Requires Python 3.9+, Git, Bash (Linux/macOS or WSL), access to GitHub, and a local supported coding agent. After the repository is published, clone its tag:

```bash
git clone --branch v0.1.0 https://github.com/datanger/Trellis.git
cd Trellis
# Codex, personal scope
./install.sh --host codex --scope user
# Claude Code, personal scope
./install.sh --host claude --scope user
# Both hosts
./install.sh --host both --scope user
# Or project scope
./install.sh --host both --scope project --target /path/to/project
```

From a distributed Git bundle use `git clone Trellis-v0.1.0.bundle Trellis` instead. `PYTHON=python3.11` selects a suitable interpreter. Codex entries are installed under `~/.agents/skills/` (or project `.agents/skills/`); Claude Code entries under `~/.claude/skills/` (or project `.claude/skills/`). The installer fetches exact upstream commits privately and installs only Trellis entry skills. It does not activate third-party plugins or hooks. Reopen your coding agent and invoke `$trellis-init` in Codex (or select from `/skills`) or `/trellis-init` in Claude Code. In the following examples use the host's invocation syntax.

| Entry | Use |
|---|---|
| `trellis-init` | Adopt/init project, documents, rules, skills and CI |
| `trellis-requirements` | Capture raw requests; classify functional requirements and changes |
| `trellis-design` | Review architecture, technical plan and alternatives |
| `trellis-contract` | Approve interfaces/examples, skeleton and integration |
| `trellis-dev` | Implement progressively, debug, optimize, automate testing |
| `trellis-accept` | Define acceptance, run tests/evaluation, establish baselines |
| `trellis-audit` | Read-only bug, quality, security, architecture, documentation and test audit |
| `trellis-simpler` | Approved code, document and test simplification |

Example: `/trellis-audit Check implementation/document consistency` and `/trellis-audit Find bugs in the parser` select different workflows. The user does not invoke individual upstream skills. Trellis resolves them from its pinned registry and asks the host to execute real steps with evidence. Human approval is required for key design and acceptance decisions. See [the full Chinese README](README.md) for lifecycle, baseline policy and project structure.

## Validate

```bash
python3 trellis.py validate
python3 trellis.py catalog audit
python3 trellis.py compose audit --route audit.docs-consistency
python3 -m unittest discover -s tests -v
python3 ~/.trellis/toolkits/0.1.0/trellis.py deps doctor
```

v0.1.0 is a locally tested preview: 8 entries, 5 pinned repositories, 61 inventoried SKILL.md files, 136 registered source resources, 91 capability families, 149 workflow templates. These are structural coverage figures, **not** proof of complete native behavior parity. Offline tests cover the runtime and installation; live provider installation and Codex/Claude execution across every route require further validation. Native-only capabilities depend on their host/tools. See [host acceptance](docs/host-acceptance.md) and [dependency policy](docs/DEPENDENCIES.md).

This is cooperative orchestration, not a security boundary. Use independently controlled branch protection, evaluators and CI. Update by installing a new reviewed version with `--replace`; no automatic upstream updates.

MIT for original Trellis code. Third-party sources retain their own licenses; see [NOTICE](NOTICE.md).
