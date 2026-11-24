---
name: trellis-accept
description: "Define acceptance, test, verify, baseline and prepare delivery. 验收、自动化测试、评测、基线、发布"
---

# trellis-accept

<!-- Trellis managed installation -->

Toolkit: `@TRELLIS_TOOLKIT@`; interpreter: `@TRELLIS_PYTHON@`. In source checkout use its root and Python 3.9+. Read project instructions and `docs/agent-protocol.md` in toolkit (relevant sections only).

Choose test design, execution, metric evaluation, module acceptance, branch finishing or release according to input. Actual tests and approved criteria are required; distinguish passing test from user acceptance. Do not publish or merge without approval. Read verification.md.

Route semantically from user input. When useful run `<python> <toolkit>/trellis.py catalog accept`; examples are hints, not mandatory flows. Select applicable capability families and resolve their actual pinned resources with `deps resolve <key>`. Read selected upstream instructions and provider-specific notes only. Compose the smallest workflow in the host agent; no per-step CLI, state machine or approval token. Consider other entry capabilities internally if required. Record actual new/changed product requirements per `docs/requirements-rules.md`, never command-only input. Report results, evidence and necessary decision in user language.
