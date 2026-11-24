# Validation

Run `python3 trellis.py validate` and `python3 -m unittest discover -s tests -v`. Tests cover retained inventory, explicit workflow source keys and fallback routing, private installed workflow paths, numbered Markdown documents and reviewed legacy migrations. Online bootstrap tests use a local archive fixture. No test result substitutes for actual host integration or native provider execution. See `host-acceptance.md`.
