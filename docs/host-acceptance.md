# Live host acceptance

Run in actual Codex and Claude Code sessions on a disposable project. Record host and provider versions, selected workflow, actual source reads/tool calls and outputs. Do not mark a scenario passed from instructions or local unit tests alone.

| User scenario | Expected |
|---|---|
| Online install | Five pinned checkouts ready; only eight entry skills discovered; private workflow files readable |
| `/trellis-requirements 整理需求` | Raw and functional ordered lists; category numbering restarts at 1, only text/date, strike deletion, no bare invocation or unconfirmed derived item |
| `/trellis-init 接管当前项目` | Reuse existing assets, no overwritten requirements or speculative docs; legacy formats offered migration |
| `/trellis-design 根据需求设计方案` | Read actual Spec Kit plan template and Ponytail; design only, Archify native output if requested; confirm material choices |
| `/trellis-contract 根据需求和技术方案设计接口文档` | Read Agent Skills API skill before interface design, concrete examples; no skeleton/business implementation |
| `/trellis-contract 创建代码骨架` | Confirmed contract reused; public signatures and stubs, no business logic |
| `/trellis-contract 使用样例数据联调` | Real stub chain execution, Superpowers verification; not real business acceptance |
| Native `/plan` then `/trellis-dev 执行刚刚生成的计划` | Reuse accessible plan without re-planning; read actual Superpowers executing-plans and Ponytail before substantive coding (no explicit provider name); TDD/incremental methods as applicable; actual tests and final review |
| `/trellis-dev 继续开发下一个模块` | Locate existing progress; replace only relevant stub, module/integration/regression loop; preserve earlier acceptance |
| `/trellis-dev 修复某个Bug` | Actual systematic-debugging, Ponytail and verification; reproduce and add regression where feasible; no full lifecycle |
| `/trellis-accept 验收模块` | Actual approved tests, objective criteria or necessary user decision; distinguish test vs acceptance |
| `/trellis-audit 检查文档一致性` vs `检查潜在Bug` | Distinct source calls and evidence, read-only; no fixes |
| `/trellis-simpler 整理README` vs `整理代码` | Different workflow and required resources; no full code lifecycle for docs, Ponytail and regression for code |
| Combined tasks, wrong entry or resume | Route internally within requested scope; reuse approved artifacts; no unnecessary restart |
| Missing provider/native dependency | Report blocker, never pretend an upstream source was read or native method executed |
| Explicit specialized capability | Use catalog fallback to resolve exact native/reference/complementary resource; no duplicate workflow |
| Native modes | Real pinned Spec Kit CLI, Archify renderer/browser, Ponytail Band where supported, actual subagents and specialist tools; unavailable capabilities reported blocked |
| Coverage | Exercise each distinct mapped capability, including authorized maintainer-only targets; record pass/fail/blocked |

Local unit tests verify structural mapping, source key validity, installer availability and document conversion, not LLM compliance or live host parity. Slash invocation examples use Claude Code; use `$trellis-*` or selector in Codex. No host test results are claimed by this document.
