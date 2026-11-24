# Audit workflows

Select the section matching the requested task, not all sections. Required steps apply within that selected task; conditional steps apply only when the stated condition is true. Load the exact registered resource before the related action using the shared routing rules; retain its applicable instructions for the task. Do not re-read or execute a duplicate full upstream lifecycle. Combine compatible tasks only within user scope. For an unusual request or a unique native sub-capability, use the mandatory fallback described below.

## Find bugs or review changes

**Select when:** read-only bug check, code review or Git diff assessment.

1. **Required** — `agent-skills:skills/code-review-and-quality/SKILL.md`. Inspect actual code/diff, report severity, exact locations and why the behavior fails.
2. **For suspected bugs** — `superpowers:skills/systematic-debugging/SKILL.md`. Reproduce safely when possible; distinguish confirmed from hypothetical.
3. **For simplification-focused diff** — `ponytail:skills/ponytail-review/SKILL.md`. Inspect complexity, duplication, unnecessary code; no automatic changes.
4. **For delegated review** — `superpowers:skills/requesting-code-review/SKILL.md`. Use independent reviewer if available; do not invent review output.
5. **For Spec Kit bug assessment** — `spec-kit:extensions/bug/commands/speckit.bug.assess.md`, `spec-kit:extensions/bug/commands/speckit.bug.test.md`. Use applicable assessment/test methods without changing business code.

**Done:** Evidence-backed findings, no fixes unless authorized via an execution request.

## Audit project architecture or excessive complexity

**Select when:** project health, architectural dependencies, design bloat, technical debt.

1. **Required** — `ponytail:skills/ponytail-audit/SKILL.md`. Inspect actual repository for over-engineering and duplication; prioritize correctness and maintenance cost rather than line count.
2. **For architecture/coupling** — `archify:archify/SKILL.md`, `archify:archify/references/repository-authoring.md`. Use Archify real code analysis with source evidence; generate diagram only if useful/requested.
3. **For technical debt** — `ponytail:skills/ponytail-debt/SKILL.md`. Identify and prioritize debt.
4. **For claimed gain** — `ponytail:skills/ponytail-gain/SKILL.md`. Use actual supported evidence; never fabricate savings.
5. **For requirement/design consistency** — `spec-kit:templates/commands/analyze.md`. Check relevant artifacts and actual implementation.

**Done:** Prioritized findings and evidence, not a rewritten architecture.

## Audit documents or requirements consistency

**Select when:** compare docs/contracts/examples with actual code and user requirements.

1. **Required** — `agent-skills:skills/documentation-and-adrs/SKILL.md`, `spec-kit:templates/commands/analyze.md`. Trace claims to real code/config/test and approved requirements; list inaccurate or missing content.
2. **For architecture claims** — `archify:archify/SKILL.md`. Use actual source-backed analysis when needed.
3. **For checklist completeness** — `spec-kit:templates/commands/checklist.md`. Check only relevant specifications.

**Done:** Read-only inconsistencies and evidence; no edits.

## Specialist audit

**Select when:** security, performance, accessibility, observability, PR visualization or native diagnostics.

1. **For security** — `agent-skills:skills/security-and-hardening/SKILL.md`. Use applicable actual review/checks, avoid destructive probing.
2. **For performance** — `agent-skills:skills/performance-optimization/SKILL.md`, `agent-skills:agents/web-performance-auditor.md`. Measure actual bottleneck where possible.
3. **For accessibility** — `agent-skills:skills/accessibility-engineering/SKILL.md`. Inspect rendered UI and applicable checklist.
4. **For observability** — `agent-skills:references/observability-checklist.md`. Inspect instrumentation/diagnostic evidence.
5. **For explicit PR visualization** — `archify:archify-pr/SKILL.md`. Use native Archify PR workflow; no remote attachment without authorization.
6. **For skill or Band diagnostics** — `superpowers:skills/diagnosing-superpowers/SKILL.md`, `ponytail:README.md`. Read actual host-specific instructions; require explicit permission before telemetry/history operations.

**Done:** Evidence-backed specialist findings or precise native blocker.

## Other registered capabilities

If no section covers the intent, run `catalog audit` (or the matching other entry internally) and select the exact source key(s) from the pinned inventory. Read the actual source and its provider adapter; apply the matching unique method, including native commands/references or maintainer-only capabilities when actually applicable. Do not force a normal workflow when the user requests a specialized upstream operation. For overlapping/mirrored resources prefer the primary and add only distinct complementary semantics.
