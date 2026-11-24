# Init workflows

Select the section matching the requested task, not all sections. Required steps apply within that selected task; conditional steps apply only when the stated condition is true. Load the exact registered resource before the related action using the shared routing rules; retain its applicable instructions for the task. Do not re-read or execute a duplicate full upstream lifecycle. Combine compatible tasks only within user scope. For an unusual request or a unique native sub-capability, use the mandatory fallback described below.

## Initialize or adopt a project

**Select when:** initialize a new/existing project, create project rules or documentation (not a request to develop features).

1. **Required** — `agent-skills:skills/context-engineering/SKILL.md`, `spec-kit:templates/commands/constitution.md`. Read existing assets and actual project constraints; define the minimal shared project rules. Reuse existing plans/docs, not a blank reinitialization.
2. **For existing code** — `ponytail:skills/ponytail-audit/SKILL.md`. Identify missing/duplicated assets without rewriting business code.
3. **For requested docs** — `agent-skills:skills/documentation-and-adrs/SKILL.md`. Create only missing necessary docs; bootstrap the two editable numbered requirement documents. For legacy formats preview migration; never overwrite existing files.
4. **For requested diagrams** — `archify:archify/SKILL.md`. Trace actual architecture and use Archify for the requested diagram, prefer SVG in Markdown.

**Done:** An inventory of retained and newly created assets, useful project rules and only necessary docs. No speculative empty docs or dependency installs.

**Human decision:** Confirm consequential structure or global configuration changes; ordinary authorized file creation does not require a second approval.

## Configure engineering tools

**Select when:** Git, CI, test environment or project context setup.

1. **For Git** — `agent-skills:skills/git-workflow-and-versioning/SKILL.md`. Inspect repository conventions; preserve user work; only configure what is requested.
2. **For CI/test setup** — `agent-skills:skills/ci-cd-and-automation/SKILL.md`, `agent-skills:agents/test-engineer.md`. Use existing test stack where possible; run actual commands.
3. **For context setup** — `agent-skills:skills/context-engineering/SKILL.md`. Keep concise shared instructions, verify applicable host reads them.

**Done:** Working requested configuration and verification; no unrelated tool installation.

## Create, diagnose or manage Skills

**Select when:** project-specific skill authoring, provider discovery, dependency/installation diagnostics.

1. **For authoring** — `superpowers:skills/writing-skills/SKILL.md`. Write a scoped skill and test trigger behavior.
2. **For routing/help** — `superpowers:skills/using-superpowers/SKILL.md`, `ponytail:skills/ponytail-help/SKILL.md`. Use discovery advice, not global auto-injection.
3. **For diagnostics** — `superpowers:skills/diagnosing-superpowers/SKILL.md`. Inspect actual installation, commands and host paths.
4. **For native Spec Kit administration** — `spec-kit:docs/installation.md`. Use catalog to select exact extension/preset/bundle/workflow/step/integration resource; only use the authorized native environment. Read provider adapter.
5. **For Archify doctor/demo/update** — `archify:archify/SKILL.md`, `archify:archify/references/update-awareness.md`. Use applicable native CLI and actual results; do not auto-update.

**Done:** Requested capability is configured or an explicit blocker is reported.

## Other registered capabilities

If no section covers the intent, run `catalog init` (or the matching other entry internally) and select the exact source key(s) from the pinned inventory. Read the actual source and its provider adapter; apply the matching unique method, including native commands/references or maintainer-only capabilities when actually applicable. Do not force a normal workflow when the user requests a specialized upstream operation. For overlapping/mirrored resources prefer the primary and add only distinct complementary semantics.
