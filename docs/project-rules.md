# Suggested shared project rule block

After approval, merge a single shared rule document into the project and place a short, effective pointer in `AGENTS.md` and `CLAUDE.md` (only for hosts used). Preserve existing instructions. Verify each host actually reads the shared rules; put essential safeguards inline if file references are not auto-loaded.

```markdown
<!-- trellis-managed-start -->
Use Trellis for progressive, human-controlled development. For each explicit new, changed or cancelled product requirement from chat or uploaded documents, register the exact user request before implementing and maintain linked numbered functional requirements. Do not record AI suggestions as confirmed user requests. Use the Trellis entry matching intent: trellis-init, trellis-requirements, trellis-design, trellis-contract, trellis-dev, trellis-accept, trellis-audit, trellis-simpler.

Major changes: approve design, interface/examples, code skeleton and module plan separately before production implementation. Respect scope, public contracts and approved criteria; do not weaken tests or edit independent evaluator truth. Protect accepted baselines with Git, contract/regression tests and a human-approved change gate. Update actual mechanism docs only when affected; do not rewrite approved design to hide implementation drift. Never claim unrun tests passed. Keep status, decisions and evidence durable. If blocked, explain what human decision is required.
<!-- trellis-managed-end -->
```

The block is an agent instruction, not a security boundary. Branch protection and CI must be configured separately by the project owner. Put tool-specific differences in the respective host entry file, not in duplicate shared standards.
