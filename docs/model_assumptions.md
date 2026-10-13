# Model and measurement assumptions

Record decisions here before using them in reported experiments. Every
assumption should have a rationale, a test or sensitivity analysis where
possible, and a note describing which conclusions it limits.

**Status:** initial version (2026-10-12), written before Phase 1 code exists.
All values below are provisional design assumptions for the first scenario
(`configs/environment/small_swarm.yaml`, per `docs/decisions.md` entry
2026-10-10). Each must be validated against the implementation's unit tests
before any result generated from it is reported. Anything not yet decided is
explicitly marked *unknown* rather than guessed.

## Environment and dynamics

- **Coordinate system and units:** right-handed 2D Cartesian frame with the
  origin at a corner of the arena; x increases rightward, y increases upward.
  Positions in world units (nominally meters at this scale), velocities in
  units/s, time in seconds. Rationale: simplest frame that matches the bounded
  2D arena in `docs/research_question.md`. Limitation: no altitude, attitude,
  or full flight dynamics are modeled; nothing here may be described as
  aircraft dynamics.
- **State and update equations:** each agent state is `(p, v)` with position
  `p` in `[0, W] x [0, H]` and velocity `v` in R^2. The controller outputs a
  commanded direction vector `d` (action space: 2D vector clipped to norm <=
  1). Update: `v <- clip(v + k*(d*v_max - v), ||v|| <= v_max)`, then
  `p <- p + v*dt`, with `k = 0.5` (first-order velocity lag toward the
  commanded velocity) and `v_max = 10.0` units/s. Rationale: double-integrator
  -like lag approximates actuator response without a full dynamics model, and
  every term is simple enough to assert exactly in unit tests. Limitation:
  results transfer only to controllers facing this same interface.
- **Time step and integration method:** fixed `dt = 0.1` s, explicit (forward)
  Euler integration. Rationale: matches `small_swarm.yaml`; deterministic and
  trivially testable. Sensitivity check planned: rerun the first experiment at
  `dt = 0.05` and confirm metric changes are within noise.
- **Speed/acceleration limits:** speed capped at `v_max = 10.0` units/s;
  acceleration implicitly bounded by the lag constant `k` (max effective
  acceleration ~= `k*v_max/dt` = 50 units/s^2). Exact numeric limits are
  *provisional*; they will be revisited once the rule-based baseline either
  converges on the target comfortably or demonstrably cannot.
- **Boundary and episode termination rules:** positions are clamped to the
  arena `[0, W] x [0, H]` (`W = H = 100.0`) after each step; agents sliding
  along a wall keep their tangential velocity. Episodes terminate at
  `max_steps = 500` steps (50 s simulated). Success is defined in metrics
  (Phase 4) as all active agents within a convergence radius `r_c = 5.0`
  units of the target -- *provisional*, to be confirmed against `v_max` and
  `max_steps` so that success is geometrically reachable.
- **Target motion model:** first scenario uses a single stationary target at a
  seeded uniform-random position inside the central region of the arena
  (margin >= 15 units from walls). Moving-target scenarios are deferred; when
  added, target motion will be piecewise-constant-velocity waypoint motion
  with its own documented parameters. No obstacles in the first scenario;
  obstacle geometry and collision margins remain *unknown / out of scope*
  until the small-N environment passes its tests.

## Observation and communication

- **What each agent observes:** a fixed-length packed vector containing (1)
  own normalized velocity `(vx/v_max, vy/v_max)`; (2) target-relative bearing
  as `(sin theta, cos theta)` and normalized distance `||dp||/diag(W,H)`,
  zeroed if the target is outside sensing range; (3) per neighbor slot (fixed
  maximum of `num_agents - 1` slots): normalized relative position and
  velocity, gated to zero when the neighbor is outside communication range;
  (4) an occupancy flag per slot. Rationale: identical packing for all three
  controller families, enforced by unit tests (see decision-gate risk in
  `docs/research_question.md`). Limitation: no absolute positions, no global
  swarm state, no other agents' observations.
- **Sensing range/noise/update rate:** target sensing range `r_s = 40.0`
  units; first scenario runs with **zero sensing noise** to establish the
  deterministic baseline. Noise models (additive Gaussian on bearing and
  distance) are deferred to the robustness stage and will be parameterized in
  `configs/` before use. Observations refresh every step (`dt`).
- **Neighbor discovery and message contents:** neighbor set = agents within
  communication range of the sender, computed from true positions at the start
  of the step (no discovery protocol is simulated). Messages carry only the
  neighbor's current `(p, v)`; no learned or compressed inter-agent channels
  in the first experiment.
- **Communication range, latency, drop assumptions, and accounting:** range
  `r_comm = 30.0` units; zero latency; zero packet drops in the first
  scenario. Accounting: each observation step in which agent i receives data
  from m neighbors contributes m counted messages to the per-run
  communication-load metric. Range/latency/drop values are *provisional*.
- **Which information is unavailable to decentralized controllers:** global
  swarm centroid, global progress/success status, other agents' internal
  states or observations, ground truth beyond what falls inside the sensing
  and communication ranges above, and episode metadata (remaining step count
  is not provided). Global state is used only for computing evaluation
  metrics.

## Energy accounting

Keep estimated/proxy terms separate from measured quantities. **No
neuromorphic hardware is used or assumed; every figure below is a simulation
proxy and must be labeled as such in all reports.** Proxy units are arbitrary
"energy units" (eu); they support only relative comparisons between
controllers run under the identical protocol.

| Term | Formula or measurement method | Units | Coefficients/source | Limitations |
|---|---|---|---|---|
| Motion/propulsion proxy | sum over agents and steps of `c_m*||v||*dt` | eu | `c_m` = 1.0 (placeholder constant, to be calibrated) | Not aircraft power unless validated; ignores lift/drag physics entirely |
| Sensing | `c_s` per step per agent while target is in range | eu | `c_s` = 1.0 (placeholder) | Relative indicator only; not tied to any real sensor part |
| Communication | `c_comm` per received neighbor message | eu | `c_comm` = 1.0 (placeholder) | Assumes fixed-size messages; no PHY-layer modeling |
| Controller computation | `c_cpu` x wall-clock inference time per agent-step, measured on a recorded machine profile | eu (and ms, reported separately) | `c_cpu` = 1.0 (placeholder); machine spec logged per run | Proxy, not measured device energy; never claim chip-level efficiency without hardware measurements |
| Total | Sum of the four rows above, reported per agent-step and per episode | eu | -- | Excludes reset/overhead; coefficients are uncalibrated, so only cross-controller deltas under one protocol are meaningful |

## Validation and change log

| Date | Assumption checked or changed | Evidence | Consequence |
|---|---|---|---|
| 2026-10-12 | Initial assumption set written for the first (small-swarm, stationary-target) scenario | Design rationale above; aligned with `docs/decisions.md` 2026-10-10 and `configs/environment/small_swarm.yaml` | All values provisional; none may back a reported result until the Phase 1 tests validate them |
| TODO | Validate `v_max`, `r_c`, and reachability of success analytically once `env/dynamics.py` exists | Planned: closed-form worst-case convergence-time check + unit tests | Adjust limits or termination rules if success is unreachable within `max_steps` |
| TODO | dt-sensitivity check (0.1 vs 0.05) after environment is stable | Planned: multi-seed metric comparison | Confirm or revise the fixed-dt assumption |
