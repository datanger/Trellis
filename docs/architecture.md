# Architecture

```mermaid
flowchart TD
  U[Eight stable entries + user intent] --> A[Host selects relevant capability families]
  A --> P[Read pinned provider resources on demand]
  P --> W[Host builds and executes minimal workflow]
  W --> H{Material human decision?}
  H -->|Yes| R[Review and explicit approval]
  R --> W
  H -->|No| V[Actual tests and evidence]
  V --> D[Markdown / Git / CI]
```

Two registry files: exact upstream lock and unified capability inventory with primary/complement choices and optional task hints. No fixed step templates or persistent execution engine. Python is used only for installation, dependency integrity, inventory checks, Markdown validation and legacy migration. Host agent owns semantic routing and execution. Markdown is authoritative; Git retains history. Human decisions and independent CI protect accepted behavior. This is a cooperative skill, not a security boundary.
