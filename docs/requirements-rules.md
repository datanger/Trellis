# Requirements

Use `docs/requirements/raw-requirements.md` and `docs/requirements/functional-requirements.md` (reuse agreed equivalent locations). Both are canonical, directly editable Markdown. No tables, permanent requirement IDs, source/status/operation fields or compulsory raw-to-functional ID links. Numbers are ordinary Markdown list positions, not identifiers.

Raw requirements:

```markdown
# 原始需求

1. 用户提出的需求。（2026-11-24）
2. ~~已经删除的需求。~~（2026-11-24）
```

Functional requirements, grouped by actual business category:

```markdown
# 需求拆解

## 数据解析

1. 支持解析输入文件。（2026-11-24）
2. ~~支持旧格式。~~（2026-11-24）

## 测试验收

1. 支持自动化回归测试。（2026-11-24）
```

Use `1.`, `2.`, `3.` in sequence, restart at 1 in each functional category. Each item is one concise requirement and its last edit date `(YYYY-MM-DD)` or Chinese parentheses. Add at the end of its list, modify the existing item in place, strike only the description when deleting (retain number and date), unstrike on restoration; update the date only for changed items. Do not physically delete retired requirements. Keep raw wording faithful; split clearly independent requirements. Do not record a bare skill invocation, `/plan`, question, temporary operation or invented requirement. Use Git history, not a separate requirements database. Categories are created as needed, not predefined.

Keep functional behavior implementable and verifiable; discuss AI-derived proposals before adding them to the formal list. Preserve approved acceptance criteria in relevant design/test/acceptance artifacts rather than extra requirement columns; do not lose them during migration. Check downstream impact of changes and cancellations semantically. `requirements-check` optionally validates numbering, dates and deletion syntax; not a semantic approval test.

For old state, tables or bullet lists, use `migrate-requirements` to preview, review and then `--apply`. It preserves source documents/metadata in a backup, reports undated items assigned the migration date, and retains pending legacy proposals and acceptance metadata for review. Unknown content or manually changed v0.1 generated views require manual reconciliation. No automatic migration or overwrite during install/bootstrap.
