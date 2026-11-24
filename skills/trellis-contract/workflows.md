# Contract workflows

Select the section matching the requested task, not all sections. Required steps apply within that selected task; conditional steps apply only when the stated condition is true. Load the exact registered resource before the related action using the shared routing rules; retain its applicable instructions for the task. Do not re-read or execute a duplicate full upstream lifecycle. Combine compatible tasks only within user scope. For an unusual request or a unique native sub-capability, use the mandatory fallback described below.

## Design or review interfaces

**Select when:** design an interface document from requirements and technical design; update, review or add examples.

1. **Required** — `agent-skills:skills/api-and-interface-design/SKILL.md`. Locate approved requirements and design, identify module boundaries and dependencies. Define purpose, input/output types, units/ranges, errors and examples. Reuse existing conventions. Review-only requests do not change implementation.
2. **For new or changed interfaces** — `ponytail:skills/ponytail/SKILL.md`. Check smallest complete interface, avoid speculative fields and abstractions.
3. **For dataflow, sequence, class or ERD** — `archify:archify/SKILL.md`. Run actual Archify in selected mode when a diagram is requested or necessary.
4. **For backward compatibility** — `agent-skills:skills/deprecation-and-migration/SKILL.md`. Identify callers and compatibility/migration effects; protect accepted behavior.
5. **For documentation consistency** — `agent-skills:skills/documentation-and-adrs/SKILL.md`, `spec-kit:templates/commands/analyze.md`. Check requirement/design consistency and example validity; use only the applicable methods.

**Done:** Interface document and concrete input/output examples; review findings only if requested.

**Human decision:** Confirm material contract decisions. If asked only for interface documentation, stop there; do not create skeleton or business code.

## Create a public code skeleton

**Select when:** approved interface document exists and user requests code skeleton.

1. **Required** — `agent-skills:skills/api-and-interface-design/SKILL.md`, `ponytail:skills/ponytail/SKILL.md`. Read confirmed contracts/examples, create only modules/classes/functions and public signatures, purpose and types; no business implementation.
2. **For complex structure** — `archify:archify/SKILL.md`. Use Archify class/tree/dataflow when helpful, do not create unrelated diagrams.

**Done:** Inspectable public structure, matching signatures/examples, clearly marked stubs; no implemented business behavior.

**Human decision:** Confirm the public skeleton before integrating or filling it, if material. Only advance when requested or included in authorized scope.

## Integrate the skeleton

**Select when:** validate approved public structure using sample data and stubs.

1. **Required** — `superpowers:skills/test-driven-development/SKILL.md`, `ponytail:skills/ponytail/SKILL.md`. Use concrete representative samples to test data flow; connect stubs without real business logic. Mark stub outputs clearly.
2. **If failures** — `superpowers:skills/systematic-debugging/SKILL.md`. Find contract mismatch or wiring root cause; do not silently change approved interfaces.
3. **Required** — `superpowers:skills/verification-before-completion/SKILL.md`. Run the actual sample path and boundary checks; report integration vs real feature acceptance separately.

**Done:** A runnable sample/stub end-to-end chain and real execution evidence; cannot be presented as business acceptance.

**Human decision:** Material interface changes require approval.

## Other registered capabilities

If no section covers the intent, run `catalog contract` (or the matching other entry internally) and select the exact source key(s) from the pinned inventory. Read the actual source and its provider adapter; apply the matching unique method, including native commands/references or maintainer-only capabilities when actually applicable. Do not force a normal workflow when the user requests a specialized upstream operation. For overlapping/mirrored resources prefer the primary and add only distinct complementary semantics.
