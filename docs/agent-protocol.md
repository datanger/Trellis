# Trellis shared rules (read only the relevant sections)

Trellis selects capabilities; the host agent plans and executes. Do not create a second workflow engine. Follow user/host permissions and project instructions. Do not invoke every provider or create a report per step. If a provider is unavailable, say what is blocked; do not pretend it ran.

## Route
Read the entry's instructions. Identify intent, scope, risk and expected result. Read `python3 <toolkit>/trellis.py catalog <entry>` if the task needs a capability lookup; the catalog lists candidates and example task labels, not executable workflows. Use the primary provider, adding complementary unique methods only as needed. Resolve selected source using `deps resolve <key>`; read that file and relevant references, plus `docs/providers/<provider>.md` when using that provider. Cross-entry capabilities may be used internally when consistent with the user request. Ask only when authorization or expected behavior is genuinely unclear. Compose the minimum necessary steps in the host's plan; adapt on failure. Never assume a native plugin is executable from its instructions alone.

## Human control
Small reversible changes: execute then verify, no extra approval unless requested. Ordinary scoped features: plan briefly, implement and test within authorized scope. Major new or cross-module features: confirm requirements, design, interface/examples, public skeleton, then validate skeleton integration before business implementation. Confirm the module plan and acceptance criteria when consequential. Each distinct decision is reviewed before proceeding; do not pre-generate all later designs before approval. Approval may be explicit in chat. For major decisions record scope, decision, date and reviewed Git revision or artifact in the existing design/plan or a short project decision log; no tokens or per-step receipts. A material change invalidates the relevant approval, not unrelated work. Resume from Git, current docs and outstanding decisions, not a private cursor. Record a short handoff for long tasks only.

## Requirements
Read `docs/requirements-rules.md` only for new/changed/deleted product requirements. Capture across all entries; an invocation, test request, question, temporary operation or AI suggestion is not automatically a requirement. Markdown is canonical and directly editable. No state.json writes or generated views. For v0.1 projects use the optional reviewed migration, not bootstrap overwrite.

## Verification and protection
Read `docs/verification.md` for code changes, testing or acceptance. Real tests and Git diff are evidence; no custom receipt wrapper. Preserve existing changes. Protect accepted behavior, public contracts and independent evaluation criteria, not every file byte. For protected interfaces, evaluator truth, destructive actions or material design changes obtain explicit approval before changing. Do not weaken tests or alter data splits to make results pass. Independent CI and required reviews enforce policy; Skill instructions alone do not. Never automatically commit, merge, push, publish, attach PR assets or install unrelated tools without authorization.

## Reporting
Return outcome, actual evidence, unresolved issues, and only the decision needed now. Never claim unrun tests passed. Use concise, human-readable documents. No redundant execution logs or compulsory status files.
