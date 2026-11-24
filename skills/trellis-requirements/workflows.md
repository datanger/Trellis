# Requirements workflows

Select the section matching the requested task, not all sections. Required steps apply within that selected task; conditional steps apply only when the stated condition is true. Load the exact registered resource before the related action using the shared routing rules; retain its applicable instructions for the task. Do not re-read or execute a duplicate full upstream lifecycle. Combine compatible tasks only within user scope. For an unusual request or a unique native sub-capability, use the mandatory fallback described below.

## Capture and decompose requirements

**Select when:** organize user requests, add/modify/delete requirements or derive functional requirements.

1. **Required** — `spec-kit:templates/commands/specify.md`. Capture actual user wording in the raw numbered list, then decompose into concrete functional categories. Adapt Spec Kit template semantics, do not create a second spec tree.
2. **For meaningful functional specification** — `agent-skills:skills/spec-driven-development/SKILL.md`. Use its distinct specification/implementation boundary and verifiability checks; do not repeat the entire specify flow.
3. **If ambiguity changes implementation** — `spec-kit:templates/commands/clarify.md`, `agent-skills:skills/interview-me/SKILL.md`. Resolve consequential uncertainties with minimal questions; do not record questions or bare commands as requirements.
4. **When checking completeness** — `spec-kit:templates/commands/checklist.md`, `spec-kit:templates/commands/analyze.md`. Identify missing, conflicting or unverifiable requirements and affected existing assets.

**Done:** Directly editable numbered Markdown; only real product requests and confirmed functional items. No table or permanent IDs.

**Human decision:** AI-derived functional proposals and consequential ambiguity need user confirmation before formal inclusion. A request to organize raw requirements alone does not authorize functional expansion.

## Explore or assess a proposal

**Select when:** unclear goal, idea feasibility or value assessment, alternative problem framing.

1. **For open-ended intent** — `superpowers:skills/brainstorming/SKILL.md`, `agent-skills:skills/idea-refine/SKILL.md`. Explore goals/constraints and viable options; use complementary idea-refinement, not duplicate brainstorming.
2. **For assessment** — `spec-kit:extensions/assess/commands/speckit.assess.intake.md`, `spec-kit:extensions/assess/commands/speckit.assess.define.md`. Clarify problem and success definition.
3. **For research/decision as requested** — `spec-kit:extensions/assess/commands/speckit.assess.research.md`, `spec-kit:extensions/assess/commands/speckit.assess.shape.md`, `spec-kit:extensions/assess/commands/speckit.assess.decide.md`, `agent-skills:skills/doubt-driven-development/SKILL.md`. Gather evidence, compare tradeoffs and challenge assumptions; distinguish hypothesis from evidence.

**Done:** A clearly stated problem, choices and decisions; add only user-confirmed functional items.

## Other registered capabilities

If no section covers the intent, run `catalog requirements` (or the matching other entry internally) and select the exact source key(s) from the pinned inventory. Read the actual source and its provider adapter; apply the matching unique method, including native commands/references or maintainer-only capabilities when actually applicable. Do not force a normal workflow when the user requests a specialized upstream operation. For overlapping/mirrored resources prefer the primary and add only distinct complementary semantics.
