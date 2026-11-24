# v0.1.0 local validation

Executed in the build container:

- `python3 trellis.py validate`: passed; eight entry skills, five pinned repositories, 61 registered SKILL.md files, 136 registered resources, 91 capability families, 149 workflow templates, zero unmapped registered resources.
- `python3 -m unittest discover -s tests -v`: 25 tests passed.
- Local Git bundle clone / tag and source archive: verified as part of packaging.

Provider checkouts were not downloaded in the build environment (GitHub DNS/network unavailable there). Provider-based runtime tests use explicit test doubles where necessary; the missing-provider path is tested without a double. Actual Codex / Claude Code discovery and execution, native renderer/CLI/browser integration and full semantic capability parity remain unverified. See `host-acceptance.md` for the required next validation stage.
