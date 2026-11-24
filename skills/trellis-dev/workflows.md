# Dev workflows

Select the section matching the requested task, not all sections. Required steps apply within that selected task; conditional steps apply only when the stated condition is true. Load the exact registered resource before the related action using the shared routing rules; retain its applicable instructions for the task. Do not re-read or execute a duplicate full upstream lifecycle. Combine compatible tasks only within user scope. For an unusual request or a unique native sub-capability, use the mandatory fallback described below.

## Execute an existing plan

**Select when:** user asks to execute/continue a plan, including host-native `/plan`, session plan or existing project plan.

1. **Required before writing** — `superpowers:skills/executing-plans/SKILL.md`, `ponytail:skills/ponytail/SKILL.md`. Read the existing plan and relevant approved spec/contract; do not regenerate a plan merely because it came from a host. Ponytail full is the default (unless explicitly overridden); use its real smallest-complete-change checklist throughout execution. Review for conflicts, scope and excessive abstraction.
2. **For a plan with independent tasks and available/authorized subagents** — `superpowers:skills/subagent-driven-development/SKILL.md`. Use as the alternative executor to inline executing-plans, not a second full execution; load before dispatch. Use existing plan. No fabricated subagent review.
3. **For nontrivial business logic** — `superpowers:skills/test-driven-development/SKILL.md`. Write meaningful failing tests before implementation when possible; observe failure then success; use appropriate equivalent if genuine constraints prevent TDD.
4. **For multi-step/multi-file work** — `agent-skills:skills/incremental-implementation/SKILL.md`. Implement the next smallest working slice, test and verify it, carry forward progress; for progressive projects use the module cycle below.
5. **If debugging needed** — `superpowers:skills/systematic-debugging/SKILL.md`. Reproduce and locate root cause before changing code.
6. **For substantive change** — `agent-skills:skills/code-review-and-quality/SKILL.md`. Review actual diff, scope and failure modes; use independent review when supported.
7. **Required before completion** — `superpowers:skills/verification-before-completion/SKILL.md`. Run relevant real checks and report results. Respect approved acceptance criteria and regressions.

**Done:** Existing plan executed within scope; no duplicate plan or unnecessary ceremony. Report actual tests, omissions and risks.

**Human decision:** Material change to approved requirements/design/interface/evaluation, destructive action or missing essential input; not between every routine task.

## Plan new work or implement a feature

**Select when:** no suitable existing plan, requested implementation planning, new/changed scoped feature.

1. **For planning** — `superpowers:skills/writing-plans/SKILL.md`, `spec-kit:templates/commands/tasks.md`. Break work into testable tasks with dependencies and acceptance. If user asks only to plan, stop before code. For consequential design/contract gaps use corresponding entry, not invent approvals.
2. **Required for implementation** — `ponytail:skills/ponytail/SKILL.md`. Read Ponytail before code, reuse existing implementation and avoid unrequested abstractions.
3. **For nontrivial logic** — `superpowers:skills/test-driven-development/SKILL.md`. Build meaningful tests; preserve existing acceptance tests.
4. **For multi-file or multi-module work** — `agent-skills:skills/incremental-implementation/SKILL.md`. Follow incremental module/slice development below.
5. **For substantive change** — `agent-skills:skills/code-review-and-quality/SKILL.md`. Review implementation, use requested domain capability below.
6. **Required for completion** — `superpowers:skills/verification-before-completion/SKILL.md`. Run actual targeted, integration and regression tests as applicable.

**Done:** Requested plan or implemented feature, verified against approved criteria. No unnecessary re-planning.

## Fix a bug

**Select when:** reproduce and fix a defect rather than implement an unrelated feature.

1. **Required before change** — `superpowers:skills/systematic-debugging/SKILL.md`, `ponytail:skills/ponytail/SKILL.md`. Reproduce and locate root cause; inspect callers; use minimum complete fix, no unrelated cleanup.
2. **For regression** — `superpowers:skills/test-driven-development/SKILL.md`. Add a test that exposes the bug when feasible.
3. **For substantive change** — `agent-skills:skills/code-review-and-quality/SKILL.md`. Inspect impact, compatibility and error handling.
4. **Required** — `superpowers:skills/verification-before-completion/SKILL.md`. Rerun reproduction, regression and relevant integration checks.

**Done:** Root-cause fix and actual verification, not symptom suppression.

## Algorithm development or optimization

**Select when:** improve algorithm accuracy, quality or runtime.

1. **Required** — `ponytail:skills/ponytail/SKILL.md`, `agent-skills:skills/doubt-driven-development/SKILL.md`. Understand baseline and mechanism; avoid speculative complexity. Freeze independent metric/data split and evaluation logic before optimization.
2. **For measured performance bottlenecks** — `agent-skills:skills/performance-optimization/SKILL.md`. Measure and localize bottlenecks; distinguish accuracy from runtime.
3. **For failures** — `superpowers:skills/systematic-debugging/SKILL.md`. Investigate errors and data/algorithm failure modes.
4. **For changes across modules** — `agent-skills:skills/incremental-implementation/SKILL.md`, `superpowers:skills/test-driven-development/SKILL.md`. Make bounded hypothesis-driven changes; run minimal meaningful experiments/tests.
5. **Required** — `superpowers:skills/verification-before-completion/SKILL.md`. Evaluate against fixed criteria and independent holdout where applicable; retain experiment results and risks.

**Done:** Real measured outcome with unchanged evaluation truth; not a claim based on unrun experiments.

**Human decision:** Confirm metrics/data splits and material algorithm changes; do not modify independent evaluator to get a passing result.

## Domain-specific implementation

**Select when:** frontend, backend, security, migration, observability or performance task.

1. **Required before coding** — `ponytail:skills/ponytail/SKILL.md`. Ponytail full by default; preserve design and approved contracts.
2. **For frontend** — `agent-skills:skills/frontend-ui-engineering/SKILL.md`, `agent-skills:skills/browser-testing-with-devtools/SKILL.md`, `agent-skills:skills/accessibility-engineering/SKILL.md`. Implement approved layout, reuse UI components, check actual interaction/visual and accessibility behavior.
3. **For backend** — `agent-skills:skills/api-and-interface-design/SKILL.md`, `agent-skills:skills/security-and-hardening/SKILL.md`, `agent-skills:skills/observability-and-instrumentation/SKILL.md`. Apply relevant interface/error/security/observability checks; validate actual integration.
4. **For migration/performance** — `agent-skills:skills/deprecation-and-migration/SKILL.md`, `agent-skills:skills/performance-optimization/SKILL.md`. Use the respective capability when compatibility or measured performance is affected.
5. **For business logic or multi-file work** — `superpowers:skills/test-driven-development/SKILL.md`, `agent-skills:skills/incremental-implementation/SKILL.md`. Apply meaningful tests and thin slices.
6. **For substantive change** — `agent-skills:skills/code-review-and-quality/SKILL.md`. Review actual changes.
7. **Required** — `superpowers:skills/verification-before-completion/SKILL.md`. Run relevant tests/browser/build/integration commands.

**Done:** Requested domain implementation with actual evidence; no extra domain work.

## Execution helpers

**Select when:** parallel tasks, review feedback, branch isolation or explicit simplification preference.

1. **For independent parallel work** — `superpowers:skills/dispatching-parallel-agents/SKILL.md`, `superpowers:skills/subagent-driven-development/SKILL.md`. Choose supported orchestration; do not dispatch dependent work as independent.
2. **For isolation when beneficial and authorized** — `superpowers:skills/using-git-worktrees/SKILL.md`, `agent-skills:skills/git-workflow-and-versioning/SKILL.md`. Reuse authorized workspace; no forced worktrees or unapproved commits/branches.
3. **For review feedback** — `superpowers:skills/receiving-code-review/SKILL.md`. Check evidence, act on valid issues; avoid blind compliance.
4. **For requested Ponytail level** — `ponytail:skills/ponytail/SKILL.md`. Use explicit lite/full/ultra/off; off disables only simplification guidance, not tests, security or project constraints.

**Done:** The requested helper is used if supported; otherwise report the limitation.

## Progressive module cycle

For a complex new or cross-module feature, follow `docs/progressive-development.md` and reuse approved artifacts. For each next module: read its confirmed contract and criteria, load the relevant implementation/test capabilities above, replace the stub with the smallest real behavior, run module and end-to-end integration tests, regress earlier accepted behavior, record objective acceptance or ask for a necessary decision, then continue. Do not restart previous modules or repeat a confirmed plan.

## Other registered capabilities

If no section covers the intent, run `catalog dev` (or the matching other entry internally) and select the exact source key(s) from the pinned inventory. Read the actual source and its provider adapter; apply the matching unique method, including native commands/references or maintainer-only capabilities when actually applicable. Do not force a normal workflow when the user requests a specialized upstream operation. For overlapping/mirrored resources prefer the primary and add only distinct complementary semantics.
