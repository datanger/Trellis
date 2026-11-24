# Progressive development

Use this only for major new features or cross-module development where contract-first progression reduces integration risk. For small reversible work use the chosen entry workflow directly. The user can enter at any stage, use a native host plan, or request several stages together. Inspect existing approved artifacts first; do not regenerate them. An instruction for a single stage does not authorize subsequent stages.

| Stage | Required input | Output and completion condition |
|---|---|---|
| Requirements | Real user intent | Raw and categorized functional numbered lists; meaningful AI-derived proposals confirmed |
| Design | Relevant requirements | Confirmed technical mechanism, architecture, constraints and choices |
| Interfaces | Relevant approved design | Confirmed module purpose, inputs/outputs, types, error cases and concrete samples |
| Skeleton | Approved contracts | Reviewed public modules/classes/functions and signatures; no business logic |
| Stub integration | Reviewed skeleton and samples | Actual execution of complete sample path, clearly identified stubs and compatibility checks |
| Module plan | Working skeleton and criteria, or existing suitable host plan | Ordered small slices, dependencies and observable acceptance criteria; confirm consequential choices |
| Development | Next authorized slice and its contract | Replace its stub, run real module/integration/regression checks; no broken earlier acceptance |
| Acceptance | Implemented behavior, approved criteria | Actual evidence and accepted scope/revision; unresolved cases identified; independent Git/CI protection where required |

Each stage uses the corresponding entry's `workflows.md` and its exact upstream sources, not a separate engine. A native `/plan` is valid input: reuse it if accessible and suitable, check missing material prerequisites and ask only for decisions that actually block execution. Do not insist on a Trellis-authored plan or full lifecycle for an existing project.

## Module cycle

1. Read only the next module/slice's confirmed scope, interface, samples and acceptance criteria. Establish the current test baseline for affected behavior.
2. Load Ponytail before writing code, use Superpowers TDD for applicable nontrivial logic and Agent Skills incremental implementation for multi-file work, as prescribed by `trellis-dev/workflows.md`. Replace the relevant stub with the smallest complete implementation; keep unaffected stubs/accepted modules intact.
3. Execute module tests, then the relevant full sample/real chain with actual implemented modules and remaining clearly marked stubs; verify contract boundaries. Stub integration is not final end-to-end business acceptance.
4. Rerun relevant regression tests for previously accepted modules and interfaces. On failure use systematic debugging and correct root cause before moving on; do not weaken independent tests, evaluator or accepted criteria.
5. Evaluate actual results against approved criteria. Objective acceptance may proceed automatically where explicitly authorized; stop for human decisions on material design/API/evaluator changes or subjective/major acceptance. Record accepted scope and evidence in the existing plan or acceptance artifact. Use Git checkpoints/CI only as authorized, no private workflow state database.
6. Proceed with the next module/slice. At the end run real integrated acceptance without stubs for required business behaviors; report gaps honestly.

Resume using accessible plan, Git diff/history, current docs and actual verification, not a hidden cursor. For changed requirements identify affected artifacts and modules, revisit only invalidated decisions and regress affected accepted behavior. Never restart the whole lifecycle by default.
