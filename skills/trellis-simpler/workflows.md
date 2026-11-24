# Simpler workflows

Select the section matching the requested task, not all sections. Required steps apply within that selected task; conditional steps apply only when the stated condition is true. Load the exact registered resource before the related action using the shared routing rules; retain its applicable instructions for the task. Do not re-read or execute a duplicate full upstream lifecycle. Combine compatible tasks only within user scope. For an unusual request or a unique native sub-capability, use the mandatory fallback described below.

## Simplify code or technical debt

**Select when:** refactor redundant code, reduce over-engineering or clean up dependencies.

1. **Required before edits** — `ponytail:skills/ponytail-audit/SKILL.md`, `ponytail:skills/ponytail/SKILL.md`, `superpowers:skills/verification-before-completion/SKILL.md`. Use real Ponytail audit + simplification principles; establish relevant behavior baseline with existing tests. Scope cleanup narrowly.
2. **For additional structural cleanup** — `agent-skills:skills/code-simplification/SKILL.md`, `agent-skills:skills/deprecation-and-migration/SKILL.md`. Use only complementary refactor/migration technique; do not duplicate a whole simplification pass.
3. **For coupling or mechanism analysis** — `archify:archify/SKILL.md`. Use Archify only when useful/requested.
4. **For multi-file change** — `agent-skills:skills/incremental-implementation/SKILL.md`. Refactor in verified slices; preserve accepted behavior.
5. **For substantive change** — `ponytail:skills/ponytail-review/SKILL.md`. Review actual diff for unnecessary complexity and regression.
6. **Required after edits** — `superpowers:skills/verification-before-completion/SKILL.md`. Rerun relevant baseline/regression checks.

**Done:** Simpler implementation with preserved behavior and actual tests.

**Human decision:** Approve material API/architecture change or uncertain deletion; do not remove required validation/security.

## Simplify documentation

**Select when:** organize docs, README, explain mechanisms, remove redundancy.

1. **Required** — `agent-skills:skills/documentation-and-adrs/SKILL.md`. Read existing docs and actual code where relevant; keep user requirements/decisions, remove duplication or outdated claims. Preserve required numbered-list format.
2. **For substantial content complexity** — `ponytail:skills/ponytail/SKILL.md`. Apply minimum-complete-change reasoning, no new documentation bureaucracy.
3. **For requested diagrams/explainers** — `archify:archify/SKILL.md`, `archify:archify/references/explainer-authoring.md`. Use actual Archify native workflow; use SVG for Markdown where appropriate, on-demand not unsolicited pages.

**Done:** Human-readable concise documents, valid links/examples; simple README changes do not trigger full code test lifecycle.

## Simplify tests or file organization

**Select when:** reduce duplicate fixtures/tests, organize directories or remove unused files.

1. **Required before edits** — `ponytail:skills/ponytail/SKILL.md`, `superpowers:skills/verification-before-completion/SKILL.md`. Identify actual uses and establish relevant baseline. Preserve meaningful coverage and evaluation truth.
2. **For test design** — `agent-skills:agents/test-engineer.md`. Consolidate only equivalent tests; preserve boundary and failure cases.
3. **For structural migration** — `agent-skills:skills/deprecation-and-migration/SKILL.md`. Check references, imports, callers and compatibility.
4. **For claimed gains** — `ponytail:skills/ponytail-gain/SKILL.md`. Measure only when useful and supported.
5. **Required** — `superpowers:skills/verification-before-completion/SKILL.md`. Run affected tests and verify reference integrity.

**Done:** Cleaner tests/files with no loss of verified behavior.

**Human decision:** Ask before irreversible deletion or changed acceptance criteria.

## Other registered capabilities

If no section covers the intent, run `catalog simpler` (or the matching other entry internally) and select the exact source key(s) from the pinned inventory. Read the actual source and its provider adapter; apply the matching unique method, including native commands/references or maintainer-only capabilities when actually applicable. Do not force a normal workflow when the user requests a specialized upstream operation. For overlapping/mirrored resources prefer the primary and add only distinct complementary semantics.
