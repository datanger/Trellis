---
name: trellis-init
description: "Initialize or adopt a project; configure docs, rules, skills, context, Git and CI. 初始化、接管、规范、技能管理、环境配置"
---

# trellis-init

<!-- Trellis managed installation -->

Toolkit: `@TRELLIS_TOOLKIT@`; interpreter: `@TRELLIS_PYTHON@`. In source checkout use its root and Python 3.9+. Read project instructions and `docs/agent-protocol.md` in toolkit (relevant sections only).

Initialize or adopt only requested project assets. Inspect existing docs and AGENTS.md/CLAUDE.md; reuse them. For document initialization create missing Markdown templates (optional `bootstrap`), merge approved rules, avoid empty speculative docs. For existing v0.1 projects propose migration first. For Git/CI/skill/environment requests choose matching capabilities; obtain approval for global or destructive changes.

Route semantically from user input. When useful run `<python> <toolkit>/trellis.py catalog init`; examples are hints, not mandatory flows. Select applicable capability families and resolve their actual pinned resources with `deps resolve <key>`. Read selected upstream instructions and provider-specific notes only. Compose the smallest workflow in the host agent; no per-step CLI, state machine or approval token. Consider other entry capabilities internally if required. Record actual new/changed product requirements per `docs/requirements-rules.md`, never command-only input. Report results, evidence and necessary decision in user language.
