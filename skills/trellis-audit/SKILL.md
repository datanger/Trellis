---
name: trellis-audit
description: "Read-only evidence-first inspection of bugs, consistency, quality and architecture. 审查、bug检查、文档一致性、安全、性能"
---

# trellis-audit

<!-- Trellis managed installation -->

Toolkit: `@TRELLIS_TOOLKIT@`; interpreter: `@TRELLIS_PYTHON@`. In source checkout use its root and Python 3.9+. Read project instructions and `docs/agent-protocol.md` in toolkit (relevant sections only).

Default read-only. Identify requested dimension (bugs, docs consistency, security, architecture, performance, tests, PR etc.). Inspect evidence, reproduce where safe, report severity and exact locations, distinguish suspicion from confirmed findings. Do not silently fix. For docs consistency compare actual code/contracts/examples to current descriptions; for bugs use review and targeted reproduction.

Route semantically from user input. When useful run `<python> <toolkit>/trellis.py catalog audit`; examples are hints, not mandatory flows. Select applicable capability families and resolve their actual pinned resources with `deps resolve <key>`. Read selected upstream instructions and provider-specific notes only. Compose the smallest workflow in the host agent; no per-step CLI, state machine or approval token. Consider other entry capabilities internally if required. Record actual new/changed product requirements per `docs/requirements-rules.md`, never command-only input. Report results, evidence and necessary decision in user language.
