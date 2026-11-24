---
name: trellis-requirements
description: "Capture exact user requests, maintain functional requirements, clarify and trace changes. 原始需求、功能拆解、澄清、变更。"
---

# trellis-requirements

<!-- Trellis managed installation -->

This is one of the **eight stable Trellis entry skills**, not a fixed pipeline. Interpret the user's natural-language request and compose only the relevant task routes. Trellis keeps the human in control of goals, approvals and acceptance; upstream skills are private implementation capabilities.

## Start

1. Locate the actual project root and the installed toolkit at `@TRELLIS_TOOLKIT@`. Use the installation interpreter `@TRELLIS_PYTHON@` (or Python 3.9+ in a source checkout), with absolute toolkit paths; pass `--project <absolute-project-root>` before the subcommand. If this file is being read from a source checkout rather than an installation, use the checkout root (contains `VERSION`, `trellis.py`, `registry/`).
2. **Read `docs/agent-protocol.md` in the toolkit in full.** It defines the authoritative execution, approval, requirement capture, provider adaptation, and evidence rules. Do not proceed if it is missing.
3. Read applicable project `AGENTS.md` or `CLAUDE.md`, project requirements, current state and relevant approved design; run `catalog requirements` to list this entry's precise task routes. If useful run `status` and `guard`.
4. Use the request, context and route descriptions to select one or more routes; call `compose requirements --route <route-id> ...` to inspect the resulting steps. For another entry's capability, explain the route change and obtain user agreement if it changes the intended operation. Never ask the user to memorize route IDs or upstream skill names.
5. Capture any newly stated user requirements, regardless of the current entry. Start or resume the workflow and follow the shared protocol. Use the smallest appropriate route; never run every available provider by default.

## Entry-specific behavior

Keep original requests verbatim or faithful source excerpts. Maintain the two generated requirement documents using `raw-add`, `functional-upsert` and `confirm-functional`. Present only the delta and impact for approval; mark AI-derived functional points pending until approved. Never silently rewrite original user requests.

## User-facing output

Use the user’s language. Show the current result, evidence, the exact decision needed (if any), and the next automatic action. Prefer a concise mechanism explanation with source paths and a real example over long progress narration. Never report unrun checks as passed.
