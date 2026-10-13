# Research question and scope

## Current status

Framed (draft v1, 2026-10-09). Planning stage: no controller or benchmark
result is implemented yet. This document defines the first precise research
question and the explicit non-goals; it will be revised only through entries
in `docs/decisions.md`.

## Research question

> Under a fixed simulated swarm task and matched observation/action
> constraints, how does a small spiking neural network (SNN) controller
> compare with non-spiking controllers (a rule-based baseline and a recurrent
> learned baseline) on task success, communication load, and explicitly
> defined energy proxies?

Concretely: a swarm of N agents in a bounded 2D arena must cooperatively
track and converge on a moving target using only local observations (own
state, target bearing/distance, and neighbor states within a limited
communication range), subject to shared velocity and boundary limits. All
controllers receive the identical observation spec and action format, are
trained/evaluated under the same seeds and protocol defined in
`docs/experiment_protocol.md`, and are compared on the metrics reported via
`docs/results_template.md`.

## Hypotheses

| ID | Hypothesis | Observable measure | Status |
|---|---|---|---|
| H1 | An SNN controller trained with the same interface and observation budget reaches at least 80% of the recurrent baseline's task performance (success rate and mean time-to-convergence) on the first scenario. | Success rate and mean time-to-target per controller over the pre-registered multi-seed evaluation runs. | Not tested |
| H2 | The SNN's advantage, if any, appears in per-agent-step inference cost (proxy energy/compute) rather than in raw task success. | Energy-proxy totals and wall-clock compute per agent-step, each clearly labeled as simulation-derived. | Not tested |
| H0 | Null hypothesis: on this task scale the SNN shows no meaningful performance or cost difference versus the recurrent baseline. | Overlapping confidence intervals on H1 and H2 measures. | Not tested |

The first experiment is designed to distinguish H1/H2 from H0, not to prove
them.

## Scope and non-goals

- Initial agent count and environment: 3–10 agents in a single bounded 2D
  arena with one moving target, no obstacles, fixed noise levels, and
  deterministic seeded resets. Obstacles, node loss, and larger swarms (up to
  ~30 agents) are deferred until the small-N environment passes its tests.
- Controller families being compared: (1) rule-based baseline, (2) recurrent
  non-spiking learned baseline, (3) small spiking (SNN) controller — all
  behind the shared controller interface in
  `src/neuromorphic_swarming/controllers/base.py`.
- Out of scope for the first experiment: real aircraft deployment, a full
  flight-dynamics model, hardware-energy claims without hardware measurements
  (no neuromorphic chips are used or assumed; all energy figures are
  simulation proxies and will be labeled as such), centralized/oracle control
  (global information is used only for computing metrics), pursuit of
  state-of-the-art benchmark scores, inventing new SNN training algorithms,
  and large-scale claims before smaller cases are validated.

## Success criteria for the first experiment

- One fixed scenario configuration runs end-to-end deterministically under
  seeded conditions.
- All three controllers produce valid action streams through the shared
  interface.
- Metrics are computed and reported using `docs/results_template.md`, with
  limitations recorded honestly.
- A go/no-go decision on extending to obstacles and node-loss scenarios is
  logged in `docs/decisions.md`.

## Decision gate

Do not begin the main benchmark until the task, success criteria, baseline,
observation/action constraints, and energy terminology have been reviewed.
Open risks to resolve at that review: the observation packing may unfairly
favor one controller family (mitigation: the identical observation spec is
enforced by unit tests), and the energy proxy's validity is unknown
(mitigation: treat it strictly as a relative indicator, never as absolute
power).
