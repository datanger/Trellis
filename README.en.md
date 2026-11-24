# Trellis

**Grow with structure.** Eight stable entry skills, adaptive host-agent workflows, replaceable pinned capabilities and human control. [中文](README.md)

## Install

Requires Git, Bash and Python 3.9+. Clone the repository, then run:

```bash
git clone https://github.com/datanger/Trellis.git
cd Trellis
./install.sh --host codex --scope user
./install.sh --host claude --scope user
# Or both:
./install.sh --host both --scope user
# Project scope:
./install.sh --host both --scope project --target /path/to/project
```

Codex uses `.agents/skills`; Claude Code uses `.claude/skills`, relative to home or project scope. Start a new session. Invoke `$trellis-init` in Codex or `/trellis-init` in Claude Code. Five pinned upstream checkouts are stored privately; native tools may need additional approved setup. No hooks are automatically installed.

## Upgrade from v0.1.0

Pull the current code and reinstall with the original scope/host/target plus `--replace`. For legacy projects, preview `python3 trellis.py --project /path/to/project migrate-requirements` and apply with `--apply` only after review. The migration preserves legacy evidence and backs up the old state, refuses manually modified generated docs, and reports the highest legacy ID. New IDs must exceed that number. Review obsolete project rules and CI guard references; re-confirm important legacy approvals and acceptance using Git and actual tests. See the Chinese README for full migration notes.

## Entries

| Entry | Purpose |
|---|---|
| trellis-init | Project documentation, rules, adoption |
| trellis-requirements | Raw and functional requirements |
| trellis-design | Architecture, solution, technical flow |
| trellis-contract | Interfaces, examples, skeleton integration |
| trellis-dev | Implementation, debugging, optimization |
| trellis-accept | Tests, acceptance, release checks |
| trellis-audit | Read-only bug, consistency, quality review |
| trellis-simpler | Simplify code, docs, tests |

Markdown requirements are directly editable; raw rows have only stable ID and description with last edit date. Strike out deleted descriptions. Use Git history. Never treat a bare invocation as a requirement.

The host agent chooses minimal steps based on intent and risk. Major design/interface/skeleton decisions require explicit review; small reversible tasks do not run a full lifecycle. Real tests and Git/CI protect accepted behavior. There is no custom runtime cursor, approval token or receipt database.

The registry retains all 136 previously registered upstream resources, 61 skill files and 91 capability families. Native execution parity remains subject to live host tests. Run `python3 trellis.py validate` and `python3 -m unittest discover -s tests -v`. See [dependencies](docs/DEPENDENCIES.md), [architecture](docs/architecture.md) and [host acceptance](docs/host-acceptance.md).
