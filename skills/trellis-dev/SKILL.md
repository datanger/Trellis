---
name: trellis-dev
description: "Implement approved work; debug, optimize and coordinate iterative development. 执行、开发、算法优化、前端、后端、修复"
---

# trellis-dev

<!-- Trellis managed installation -->

Toolkit: `@TRELLIS_TOOLKIT@`; interpreter: `@TRELLIS_PYTHON@`. In source checkout use its root and Python 3.9+. Read project instructions and `docs/agent-protocol.md` in toolkit (relevant sections only).

Identify authorized module or bug, inspect relevant approved decisions; small changes execute directly. Choose implementation, debugging, frontend/backend, performance, security, migration or algorithm capability. Use real tests, minimal change and relevant docs; for major features respect design/contract/skeleton gates. Use subagents/worktrees only when supported and beneficial.

Route semantically from user input. When useful run `<python> <toolkit>/trellis.py catalog dev`; examples are hints, not mandatory flows. Select applicable capability families and resolve their actual pinned resources with `deps resolve <key>`. Read selected upstream instructions and provider-specific notes only. Compose the smallest workflow in the host agent; no per-step CLI, state machine or approval token. Consider other entry capabilities internally if required. Record actual new/changed product requirements per `docs/requirements-rules.md`, never command-only input. Report results, evidence and necessary decision in user language.
