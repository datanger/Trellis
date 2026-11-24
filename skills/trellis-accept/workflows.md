# Accept workflows

Select the section matching the requested task, not all sections. Required steps apply within that selected task; conditional steps apply only when the stated condition is true. Load the exact registered resource before the related action using the shared routing rules; retain its applicable instructions for the task. Do not re-read or execute a duplicate full upstream lifecycle. Combine compatible tasks only within user scope. For an unusual request or a unique native sub-capability, use the mandatory fallback described below.

## Define acceptance or test design

**Select when:** prepare tests/metrics, acceptance criteria or test scripts.

1. **Required** — `agent-skills:agents/test-engineer.md`. Derive observable criteria from confirmed requirements/contracts, include representative, boundary and failure cases; use test-engineer as a method/persona, not pretend an agent was launched.
2. **For coverage/completeness** — `spec-kit:templates/commands/checklist.md`, `spec-kit:templates/commands/analyze.md`. Check requirement and implementation consistency.
3. **For new automated tests** — `superpowers:skills/test-driven-development/SKILL.md`. Ensure meaningful tests detect failures; avoid altering previously approved truth.

**Done:** Test plan, criteria or executable test code as requested.

**Human decision:** Confirm consequential criteria/metrics before implementation or formal acceptance.

## Verify and accept a module or system

**Select when:** run tests, evaluate a module, accept actual work or execute regression.

1. **Required** — `superpowers:skills/verification-before-completion/SKILL.md`. Run real relevant test commands and compare actual results to approved criteria; do not claim tests passed without evidence.
2. **For requirement coverage** — `spec-kit:templates/commands/converge.md`, `spec-kit:templates/commands/analyze.md`. Check completed behaviors and unresolved gaps, adapt Spec Kit semantics.
3. **For frontend** — `agent-skills:skills/browser-testing-with-devtools/SKILL.md`, `agent-skills:skills/accessibility-engineering/SKILL.md`. Inspect actual browser interaction and rendering.
4. **For measured performance/security** — `agent-skills:skills/performance-optimization/SKILL.md`, `agent-skills:skills/security-and-hardening/SKILL.md`. Run appropriate evidence-based checks, not merely a checklist.
5. **For formal acceptance** — `agent-skills:skills/code-review-and-quality/SKILL.md`. Present risk and evidence; record accepted scope/Git revision and repeatable tests in existing plan/acceptance artifact.

**Done:** Pass/fail/blocked with real evidence; distinguish module tests, stub integration, actual feature acceptance and human judgment.

**Human decision:** Automate acceptance only if user-approved objective criteria are satisfied; pause for subjective/major decisions.

## Prepare delivery or release

**Select when:** review branch completion, merge or publish readiness.

1. **Required** — `superpowers:skills/verification-before-completion/SKILL.md`, `agent-skills:skills/shipping-and-launch/SKILL.md`. Check required real tests, scope, dependencies and release readiness.
2. **For independent review** — `superpowers:skills/requesting-code-review/SKILL.md`. Use supported fresh-context reviewer if appropriate.
3. **For authorized branch delivery** — `superpowers:skills/finishing-a-development-branch/SKILL.md`, `agent-skills:skills/git-workflow-and-versioning/SKILL.md`. Apply branch finishing options; do not merge, publish or push without authorization.

**Done:** Release readiness or authorized delivery result with actual evidence.

## Other registered capabilities

If no section covers the intent, run `catalog accept` (or the matching other entry internally) and select the exact source key(s) from the pinned inventory. Read the actual source and its provider adapter; apply the matching unique method, including native commands/references or maintainer-only capabilities when actually applicable. Do not force a normal workflow when the user requests a specialized upstream operation. For overlapping/mirrored resources prefer the primary and add only distinct complementary semantics.
