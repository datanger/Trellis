---
name: trellis-contract
description: "Define interfaces and examples; build reviewed skeletons and test their integration. 接口、样例数据、代码骨架、骨架联调"
---

# trellis-contract

<!-- Trellis managed installation -->

Toolkit: `@TRELLIS_TOOLKIT@`; interpreter: `@TRELLIS_PYTHON@`. In source checkout use its root and Python 3.9+. Read project instructions and `docs/agent-protocol.md` in toolkit (relevant sections only).

For interface tasks define input/output, errors, examples and compatibility. For major new features confirm interfaces then public code skeleton (no business implementation) separately; run sample/stub integration and report that it is not actual feature acceptance. Only do requested stages; reuse approved artifacts.

Route semantically from user input. When useful run `<python> <toolkit>/trellis.py catalog contract`; examples are hints, not mandatory flows. Select applicable capability families and resolve their actual pinned resources with `deps resolve <key>`. Read selected upstream instructions and provider-specific notes only. Compose the smallest workflow in the host agent; no per-step CLI, state machine or approval token. Consider other entry capabilities internally if required. Record actual new/changed product requirements per `docs/requirements-rules.md`, never command-only input. Report results, evidence and necessary decision in user language.
