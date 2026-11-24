---
name: trellis-contract
description: "Define interfaces and examples; build reviewed skeletons and test their integration. 接口、样例数据、代码骨架、骨架联调"
---

# trellis-contract

<!-- Trellis managed installation -->

Toolkit: `@TRELLIS_TOOLKIT@`; interpreter: `@TRELLIS_PYTHON@`. In source checkout use the root and Python 3.9+.

Design interfaces/examples, create public skeleton or integrate stubs only as requested. For major changes respect distinct contract and skeleton approvals. Never present stubs as implemented business logic.

1. Identify intent, scope and accessible existing project assets (including current host plan); read project instructions and the relevant sections of `<toolkit>/docs/agent-protocol.md`.
2. **Read `<toolkit>/skills/trellis-contract/workflows.md` before selecting actions.** Choose the matching task section(s); follow required/conditional upstream calls there. For uncovered or specialized requests, query `catalog contract` or the relevant other entry internally. The user does not need to name any upstream Skill.
3. Resolve each selected actual resource with `<python> <toolkit>/trellis.py deps resolve <source-key>` and read it and applicable provider notes before its action. Apply its real method, not only a name; do not silently skip required resources. Use one primary for overlapping workflows and complementary unique steps only. The host owns execution; no private cursor, per-step CLI, forced worktrees or duplicate plans.
4. Respect scope and human decisions. Capture real new/changed/deleted product requirements per `docs/requirements-rules.md`. For complex progressive work consult `docs/progressive-development.md`; for code/test/acceptance use `docs/verification.md`.
5. Report the requested outcome, real evidence, unresolved risks and only necessary decisions. Briefly identify upstream resources actually used (or blocked); never claim a planned/loaded skill was fully executed if not.
