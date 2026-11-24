# Design workflows

Select the section matching the requested task, not all sections. Required steps apply within that selected task; conditional steps apply only when the stated condition is true. Load the exact registered resource before the related action using the shared routing rules; retain its applicable instructions for the task. Do not re-read or execute a duplicate full upstream lifecycle. Combine compatible tasks only within user scope. For an unusual request or a unique native sub-capability, use the mandatory fallback described below.

## Design a technical solution

**Select when:** derive architecture, algorithm or technical solution from approved requirements.

1. **Required** — `spec-kit:templates/commands/plan.md`, `ponytail:skills/ponytail/SKILL.md`. Reuse existing requirements and plans. Define constraints, compare alternatives and select the simplest complete solution; do not import Spec Kit project management files.
2. **For an unresolved choice** — `superpowers:skills/brainstorming/SKILL.md`, `agent-skills:skills/doubt-driven-development/SKILL.md`. Assess alternatives and counterexamples; avoid brainstorming if the design is already settled.
3. **For external research** — `agent-skills:skills/source-driven-development/SKILL.md`. Use actual primary evidence and identify uncertainties.
4. **For architecture/flow diagrams** — `archify:archify/SKILL.md`. Run real Archify architecture/workflow mode; use actual repo evidence or label proposed design; prefer SVG in Markdown.
5. **For specialized design** — `agent-skills:skills/frontend-ui-engineering/SKILL.md`, `agent-skills:skills/security-and-hardening/SKILL.md`, `agent-skills:skills/performance-optimization/SKILL.md`, `agent-skills:skills/observability-and-instrumentation/SKILL.md`. Load only the relevant one(s) for UI, trust boundary, measured performance or observability.
6. **For documenting decisions** — `agent-skills:skills/documentation-and-adrs/SKILL.md`. Record important mechanism, alternatives and decisions concisely.

**Done:** Technical design with scope, mechanism, architecture, dependencies, constraints and acceptance approach; no business code.

**Human decision:** Stop for confirmation of material design choices; do not auto-enter interface or implementation stages.

## Compare, review or visualize a design

**Select when:** compare options, evaluate feasibility, visualize current code or generate a particular diagram.

1. **For comparison** — `agent-skills:skills/doubt-driven-development/SKILL.md`, `agent-skills:skills/source-driven-development/SKILL.md`, `ponytail:skills/ponytail/SKILL.md`. Evaluate relevant tradeoffs and existing evidence; report counterexamples and costs.
2. **For visualization** — `archify:archify/SKILL.md`, `archify:archify/references/repository-authoring.md`. Select actual Archify mode (architecture, workflow, lifecycle, deployment or analysis); for existing systems trace code; read references only for selected mode.
3. **For research-based assessment** — `spec-kit:extensions/assess/commands/speckit.assess.research.md`, `spec-kit:extensions/assess/commands/speckit.assess.shape.md`, `spec-kit:extensions/assess/commands/speckit.assess.decide.md`. Apply requested stage of the assessment method; do not create unrelated artifacts.

**Done:** A comparison/diagram/assessment answering only the requested question.

## Other registered capabilities

If no section covers the intent, run `catalog design` (or the matching other entry internally) and select the exact source key(s) from the pinned inventory. Read the actual source and its provider adapter; apply the matching unique method, including native commands/references or maintainer-only capabilities when actually applicable. Do not force a normal workflow when the user requests a specialized upstream operation. For overlapping/mirrored resources prefer the primary and add only distinct complementary semantics.
