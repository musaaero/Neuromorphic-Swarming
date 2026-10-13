# Project decision log

Record decisions that affect scope, methodology, dependencies, or interpretation.
Use one dated entry per decision; do not erase superseded reasoning.

## Entry template

### YYYY-MM-DD — Short decision title

- **Decision:** TODO
- **Alternatives considered:** TODO
- **Reason/evidence:** TODO
- **Consequences and revisit trigger:** TODO

## Decisions

### 2026-10-04 — Scaffold before implementation

- **Decision:** Organize work into effort-estimated stages and create named
  placeholders before writing simulation or learning code.
- **Alternatives considered:** Calendar-month deadlines; building a large
  implementation before defining a reproducible experiment.
- **Reason/evidence:** The schedule is user-dependent, and the paper's numerical
  claims need operational definitions and a testable baseline.
- **Consequences and revisit trigger:** Placeholder files are not functional.
  Resolve research and environment choices before filling in implementation.

### 2026-10-10 — First experiment scope: small swarm, stationary target, local observations only

- **Decision:** The first benchmark uses the `configs/environment/small_swarm.yaml`
  scenario: 5 agents in a bounded 100 x 100 unit 2D arena, one stationary
  target, Euler integration with `dt = 0.1` s, episodes capped at 500 steps,
  deterministic seeded resets (seed recorded per run), and decentralized
  controllers that see only their own state, a target bearing/distance within
  sensing range, and neighbor states inside communication range. All three
  controller families (rule-based, recurrent, SNN) share this identical
  observation spec and action format through
  `src/neuromorphic_swarming/controllers/base.py`.
- **Alternatives considered:** Starting with the moving-target or obstacle
  scenarios; allowing global/oracle state to any controller; unbounded arenas
  or variable time steps.
- **Reason/evidence:** Matches the framing in `docs/research_question.md`: the
  smallest valid experiment is the one whose hypotheses (H1/H2 vs H0) can be
  tested end-to-end. A fixed, deterministic, obstacle-free scenario isolates
  controller differences from environment complexity and lets Phase 1 tests
  assert exact behavior. Global information stays reserved for metric
  computation only.
- **Consequences and revisit trigger:** Results generalize only to small-N,
  non-obstacle settings until later stages add complexity. Revisit when the
  small-swarm environment passes its unit/integration tests and completes one
  multi-seed run of all three controllers; moving-target and obstacle
  scenarios then enter scope via new entries here and updated values in
  `docs/model_assumptions.md`.
