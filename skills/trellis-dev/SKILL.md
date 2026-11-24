---
name: trellis-dev
description: "Implement approved work; debug, optimize and coordinate iterative development. 执行、开发、算法优化、前端、后端、修复"
---

# trellis-dev

<!-- Trellis managed installation -->

Toolkit: `@TRELLIS_TOOLKIT@`; interpreter: `@TRELLIS_PYTHON@`. In source checkout use the root and Python 3.9+.

Reuse any accessible approved plan, including native /plan output; do not replan unnecessarily. Apply the selected workflow and load Ponytail automatically before substantive code implementation (default full), plus appropriate execution/testing skills. Preserve accepted behavior.

1. Identify intent, scope and accessible existing project assets (including current host plan); read project instructions and the relevant sections of `<toolkit>/docs/agent-protocol.md`.
2. **Read `<toolkit>/skills/trellis-dev/workflows.md` before selecting actions.** Choose the matching task section(s); follow required/conditional upstream calls there. For uncovered or specialized requests, query `catalog dev` or the relevant other entry internally. The user does not need to name any upstream Skill.
3. Resolve each selected actual resource with `<python> <toolkit>/trellis.py deps resolve <source-key>` and read it and applicable provider notes before its action. Apply its real method, not only a name; do not silently skip required resources. Use one primary for overlapping workflows and complementary unique steps only. The host owns execution; no private cursor, per-step CLI, forced worktrees or duplicate plans.
4. Respect scope and human decisions. Capture real new/changed/deleted product requirements per `docs/requirements-rules.md`. For complex progressive work consult `docs/progressive-development.md`; for code/test/acceptance use `docs/verification.md`.
5. Report the requested outcome, real evidence, unresolved risks and only necessary decisions. Briefly identify upstream resources actually used (or blocked); never claim a planned/loaded skill was fully executed if not.
