---
name: trellis-simpler
description: "Simplify code, docs and tests without changing approved behavior. 文档整理、代码整理、测试整理、复杂度治理"
---

# trellis-simpler

<!-- Trellis managed installation -->

Toolkit: `@TRELLIS_TOOLKIT@`; interpreter: `@TRELLIS_PYTHON@`. In source checkout use its root and Python 3.9+. Read project instructions and `docs/agent-protocol.md` in toolkit (relevant sections only).

Determine whether user wants code, docs, tests or combined cleanup. For docs remove duplication and outdated content without losing valid requirements/decisions; use Archify for real mechanism explanation if useful. For code/test cleanup establish relevant baseline, use Ponytail, preserve behavior and evaluation strength, run regression. Ask approval for material architecture/API changes or irreversible removal. Small formatting/README work needs no full lifecycle.

Route semantically from user input. When useful run `<python> <toolkit>/trellis.py catalog simpler`; examples are hints, not mandatory flows. Select applicable capability families and resolve their actual pinned resources with `deps resolve <key>`. Read selected upstream instructions and provider-specific notes only. Compose the smallest workflow in the host agent; no per-step CLI, state machine or approval token. Consider other entry capabilities internally if required. Record actual new/changed product requirements per `docs/requirements-rules.md`, never command-only input. Report results, evidence and necessary decision in user language.
