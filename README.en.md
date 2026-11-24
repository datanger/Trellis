# Trellis

**Grow with structure.** Eight stable entry skills, adaptive host-agent workflows, replaceable pinned capabilities and human control. [中文](README.md)

## Online installation

No manual repository clone is needed. Requires Bash, curl, tar, Git and Python 3.9+ (Linux, macOS or WSL with these tools).

**Codex**

```bash
curl -fsSL https://raw.githubusercontent.com/datanger/Trellis/main/install-online.sh | bash -s -- --host codex
```

**Claude Code**

```bash
curl -fsSL https://raw.githubusercontent.com/datanger/Trellis/main/install-online.sh | bash -s -- --host claude
```

**Both hosts**

```bash
curl -fsSL https://raw.githubusercontent.com/datanger/Trellis/main/install-online.sh | bash -s -- --host both
```

Defaults to the main branch and user scope. To pin a published [release](https://github.com/datanger/Trellis/releases):

```bash
curl -fsSL https://raw.githubusercontent.com/datanger/Trellis/v0.2.2/install-online.sh | bash -s -- --host codex --version v0.2.2
```

**Project scope** (run in the project directory or specify its path):

```bash
curl -fsSL https://raw.githubusercontent.com/datanger/Trellis/main/install-online.sh | bash -s -- --host both --scope project --target /path/to/project
```

Codex uses `.agents/skills`; Claude Code uses `.claude/skills`, relative to home or project scope. Start a new session. Invoke `$trellis-init` in Codex or `/trellis-init` in Claude Code. Five pinned upstream checkouts are stored privately in the versioned toolkit; native tools may need additional approved setup. No hooks are automatically installed. The downloaded temporary source archive is cleaned up. `--offline` is for wrapper development only; missing providers remain unavailable.

To review before running, download the script with `curl -fsSL <script URL above> -o install-online.sh`, inspect it, then run `bash install-online.sh --host codex`. Developers with a source checkout can still run `./install.sh` directly.

## Online upgrade

Run the online installer again with the original host/scope/target and `--replace`:

```bash
curl -fsSL https://raw.githubusercontent.com/datanger/Trellis/main/install-online.sh | bash -s -- --host both --replace
```

Only managed Trellis entries are replaced. Old toolkits are retained. Start a fresh host session.

### Migrate existing requirements

Preview `python3 ~/.trellis/toolkits/0.2.2/trellis.py --project /path/to/project migrate-requirements` and apply with `--apply` after review. Supports legacy state, tables and bullet lists. Original documents and metadata are backed up; pending items remain in the migration report for review. Missing historical dates use the explicitly reported migration date. Review obsolete project instructions separately.

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

Both requirements documents use editable ordered Markdown lists (`1. Description (YYYY-MM-DD)`). Functional categories each restart at 1. No tables or permanent IDs. Strike out deleted descriptions; retain the last edit date. Discuss AI-derived proposals before adding them. Use Git history; skip bare invocations.

The host agent chooses minimal steps based on intent and risk. Major design/interface/skeleton decisions require explicit review; small reversible tasks do not run a full lifecycle. Real tests and Git/CI protect accepted behavior. There is no custom runtime cursor, approval token or receipt database.

Each entry has a [task-specific workflow](skills/trellis-dev/workflows.md) specifying exact required and conditional upstream resource keys. Users never have to name the providers. In development, Ponytail full is the default before substantive coding, and an accessible existing native `/plan` is reused through applicable Superpowers executing-plans methods. See [progressive development](docs/progressive-development.md) for stage boundaries and module acceptance cycles. The catalog is the fallback for specialized capabilities. The registry retains all 136 previously registered upstream resources, 61 skill files and 91 capability families. Native execution parity remains subject to live host tests. Run `python3 trellis.py validate` and `python3 -m unittest discover -s tests -v`. See [dependencies](docs/DEPENDENCIES.md), [architecture](docs/architecture.md) and [host acceptance](docs/host-acceptance.md).

## Publishing (maintainers)

A push to main changing `VERSION` triggers the tested release workflow. Update `CHANGELOG.md` with the version. Manual workflow dispatch or `./publish.sh` from a clean checkout matching remote main is also supported (local use requires authenticated `gh`). Existing tags/releases are not overwritten.
