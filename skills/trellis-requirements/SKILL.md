---
name: trellis-requirements
description: "Capture exact user requests, maintain functional requirements, clarify and trace changes. 原始需求、功能拆解、澄清、变更"
---

# trellis-requirements

<!-- Trellis managed installation -->

Toolkit: `@TRELLIS_TOOLKIT@`; interpreter: `@TRELLIS_PYTHON@`. In source checkout use its root and Python 3.9+. Read project instructions and `docs/agent-protocol.md` in toolkit (relevant sections only).

Capture real user requests immediately using the raw table, then update linked functional points as needed. Clarify genuine ambiguity; present only changes and pending decisions. Do not record the invocation itself. Read requirements-rules.md. For brainstorming, interview, conflict or quality checks select corresponding capabilities.

Route semantically from user input. When useful run `<python> <toolkit>/trellis.py catalog requirements`; examples are hints, not mandatory flows. Select applicable capability families and resolve their actual pinned resources with `deps resolve <key>`. Read selected upstream instructions and provider-specific notes only. Compose the smallest workflow in the host agent; no per-step CLI, state machine or approval token. Consider other entry capabilities internally if required. Record actual new/changed product requirements per `docs/requirements-rules.md`, never command-only input. Report results, evidence and necessary decision in user language.
