---
name: trellis-design
description: "Design and compare architecture, algorithms and execution flows; plan before implementation. 技术架构、技术方案、技术流程、方案确认"
---

# trellis-design

<!-- Trellis managed installation -->

Toolkit: `@TRELLIS_TOOLKIT@`; interpreter: `@TRELLIS_PYTHON@`. In source checkout use its root and Python 3.9+. Read project instructions and `docs/agent-protocol.md` in toolkit (relevant sections only).

Choose design, research, feasibility, comparison or visualization based on intent. Inspect current constraints, compare viable alternatives, prefer minimal reasonable architecture, use Archify when useful. For major changes present design before implementation; do not force unrelated contract or coding steps.

Route semantically from user input. When useful run `<python> <toolkit>/trellis.py catalog design`; examples are hints, not mandatory flows. Select applicable capability families and resolve their actual pinned resources with `deps resolve <key>`. Read selected upstream instructions and provider-specific notes only. Compose the smallest workflow in the host agent; no per-step CLI, state machine or approval token. Consider other entry capabilities internally if required. Record actual new/changed product requirements per `docs/requirements-rules.md`, never command-only input. Report results, evidence and necessary decision in user language.
