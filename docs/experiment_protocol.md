# Experiment protocol

Freeze and date this protocol before the main benchmark. Changes after results
are seen must be documented with the reason and their effect on interpretation.

**Status:** draft v0.1 (2026-10-12), **not frozen**. Written before any Phase 1
code exists. Values marked *provisional* mirror `docs/model_assumptions.md` and
must be validated by the Phase 1 tests. Values marked *unknown* must be decided
(and logged in `docs/decisions.md`) before this protocol is frozen. Freezing
means: set the status to "frozen", record the date and git revision below, and
make no further edits except through the Deviations table.

## Research question and hypotheses

Link: `research_question.md` (hypotheses H1, H2, H0)  
Protocol version/date: v0.1 draft, 2026-10-12  
Freeze date / git revision: not yet frozen

Pre-registered decision rules (fixed before any result is generated):

- **H1 (task performance):** supported only if, for the SNN versus the
  recurrent baseline on the first scenario, the ratio of success rates and the
  ratio of time-to-target performance (recurrent time / SNN time) are both
  >= 0.80 with the **lower bound of the 95% bootstrap CI** also >= 0.80.
  A point estimate >= 0.80 with a lower bound below 0.80 is reported as
  "inconclusive", not as support.
- **H2 (cost):** supported only if the SNN's simulation-proxy energy per
  agent-step is lower than the recurrent baseline's with a 95% CI for the
  difference that excludes zero, **and** H1 is not rejected. Always labeled as
  a simulation proxy.
- **H0:** retained when the CIs on the H1 ratios and the H2 difference
  overlap the no-difference value. An outcome of "no meaningful difference" is
  a valid, reportable result.

## Task and scenarios

- Environment/configuration files: `configs/environment/small_swarm.yaml`
  (provisional; 5 agents, 100 x 100 arena, `dt = 0.1` s, `max_steps = 500`).
  The exact file content is recorded by git revision in every result record.
- Training scenario distribution: `small_swarm` only. Per episode, the seeded
  reset samples initial agent positions uniformly in the arena and the
  stationary target uniformly in the central region (margin >= 15 units from
  walls, per `docs/model_assumptions.md`). Initial velocities are zero.
- Evaluation scenarios and stress tests: the primary evaluation uses the same
  scenario distribution as training but with **held-out seeds** (see
  Reproducibility). Stress tests (moving target, obstacles, node loss, larger
  swarms) are **out of scope for the first experiment** and enter only through
  a new `docs/decisions.md` entry and a new protocol version.
- Agent counts: primary N = 5 (`small_swarm.yaml`). An optional N = 3 and
  N = 10 sweep may be added as a secondary analysis, clearly labeled as such,
  only after the N = 5 run is complete.
- Target/obstacle conditions: one stationary target, no obstacles, zero sensing
  noise, zero communication latency, zero packet drops.
- Node-loss schedule: none in the first experiment (deferred to the
  robustness stage, `evaluation/robustness.py`).

## Controllers and fairness controls

- Controllers and exact revisions: (1) rule-based baseline, (2) recurrent
  non-spiking learned baseline, (3) small spiking (SNN) controller. The git
  revision of each controller implementation and its config under
  `configs/controllers/` is recorded in every result record. A controller
  revision change after freezing requires a new protocol version.
- Shared observation/action contract: all three controllers use the identical
  observation vector and action format defined in `docs/model_assumptions.md`
  and exposed through `src/neuromorphic_swarming/controllers/base.py`. Action:
  2D vector clipped to norm <= 1. A unit test must assert that observation
  shape, ordering, and gating are identical across controllers before any
  comparison is run. Controllers receive no global state and no remaining-step
  count.
- Training budget and stopping rule: the recurrent baseline and the SNN get the
  **same budget**, measured as equal numbers of environment steps and equal
  numbers of episodes (exact numbers *unknown*; set once from a pilot run and
  frozen). Training stops at the budget; there is no early stopping on
  evaluation data. The checkpoint at the final step is used (no best-checkpoint
  selection on evaluation seeds). The rule-based baseline is not trained.
- Parameter count and compute reporting: report trainable parameter count,
  training environment steps, training wall-clock time, and the machine
  profile for each learned controller. Parameter counts should be of
  comparable order; if they differ by more than 2x, report that explicitly as a
  limitation next to every comparison.
- Hyperparameter selection procedure: a fixed, equal tuning budget per learned
  controller (number of trials *unknown*, set at freeze), selected using a
  **separate validation seed set** that is disjoint from both training and
  evaluation seeds. Every tried configuration and its validation score is
  logged, including the bad ones. The rule-based baseline's gains are tuned on
  the same validation seeds with the same number of trials.

## Reproducibility

- Software/hardware versions: record Python, PyTorch (and the SNN library, if
  any), NumPy, OS, CPU/GPU model, and driver versions in each result record
  (`docs/results_template.md`). Install from `pyproject.toml` and record the
  resolved versions (for example `pip freeze` output) alongside the results.
- Seed list and number of independent runs (provisional, finalized at freeze):
  - Training seeds: 1000-1009 (10 independent training runs per learned
    controller).
  - Validation seeds (hyperparameters only): 3000-3049.
  - Evaluation seeds: 2000-2099 (100 held-out episodes per trained model).
    The same 100 evaluation episodes are used for every controller, so
    comparisons are paired.
  - The rule-based baseline is deterministic and evaluated on the same
    evaluation seeds.
- Checkpoint and output naming scheme:
  `results/<experiment_id>/<controller>/seed<train_seed>/` containing
  `checkpoint_final.pt`, `config_snapshot.yaml`, `train_log.csv`, and
  `eval_episodes.csv` (one row per evaluation episode). `experiment_id` is
  `YYYYMMDD_<short-name>`. Generated outputs stay out of version control by
  default; summary records go in `docs/` using `docs/results_template.md`.
- Failure, retry, and exclusion policy: every run is kept. A run may be
  **retried only for infrastructure failures** (crash, out-of-memory, node
  preemption) with the same seed and config, and the retry is logged. A run
  that trains but performs poorly, diverges, or yields NaNs is **not**
  excluded and not re-seeded; it is reported as a failed run and included in
  the aggregates (diverged runs score zero success). Any exclusion is a
  deviation and must appear in the Deviations table.

## Metrics and analysis

Metric definitions live in `src/neuromorphic_swarming/metrics.py` (Phase 4) and
must match this section; if the code and this text disagree, fix the code or
log a deviation.

- Primary success metric: **success rate**, the fraction of evaluation episodes
  in which all active agents are simultaneously within the convergence radius
  `r_c` (provisional 5.0 units) of the target at some step before `max_steps`.
  Secondary primary metric: **time-to-target**, steps (and seconds) until the
  first such step; failed episodes are right-censored at `max_steps` and
  reported both as censored-at-cap mean and as success-only mean, never mixed
  silently.
- Safety/collision metrics: inter-agent collision rate and minimum
  inter-agent distance per episode. The collision radius `r_col` is *unknown*
  and must be added to `docs/model_assumptions.md` before freezing; until then
  only minimum inter-agent distance is reported. Wall contacts are counted
  separately from collisions (no obstacles in this experiment).
- Time, communication, spikes, latency, and compute: time-to-target as above;
  communication load as total received neighbor messages per episode and per
  agent-step (definition in `docs/model_assumptions.md`); mean spikes per
  agent-step and spike sparsity for the SNN only (reported as not applicable
  for non-spiking controllers, not as zero); inference latency in ms per
  agent-step measured on the recorded machine profile; training compute as
  environment steps and wall-clock time.
- Energy terms and measurement boundary: the four proxy terms (motion,
  sensing, communication, controller computation) and their total as defined in
  `docs/model_assumptions.md`, in arbitrary energy units (eu). **All energy
  figures are simulation proxies**; nothing is measured on neuromorphic
  hardware. Report each term separately as well as the total. Measured wall-clock
  compute time on CPU/GPU is reported separately and is never presented as
  device energy. The coefficients are uncalibrated, so only relative
  cross-controller differences under this one protocol are interpretable.
  A sensitivity table varying each coefficient (for example 0.5x and 2x) must
  accompany any energy claim.
- Aggregation and uncertainty method: per-controller metrics are first computed
  per training seed (mean over the 100 evaluation episodes), then summarized
  across training seeds as mean with a 95% percentile bootstrap CI
  (10,000 resamples, fixed bootstrap seed). Paired differences and ratios
  between controllers use the shared evaluation episodes. Report per-seed values
  in full (table or CSV), not only aggregates. No multiple-comparison
  correction is applied to the pre-registered H1/H2 tests; any additional
  comparison is labeled exploratory.
- Planned plots/tables:
  1. Table: all metrics per controller (mean, 95% CI, N seeds), using the
     format in `docs/results_template.md`.
  2. Plot: success rate and time-to-target per controller with per-seed points.
  3. Plot: training curves (return/success vs environment steps) for each
     learned controller across seeds.
  4. Table: energy-proxy breakdown by term plus the coefficient sensitivity
     table.
  5. Table: hyperparameter search log (all trials).

## Pre-run checklist

Do not start the main benchmark until all items are checked:

- [ ] Phase 1 environment tests pass and seeded resets are deterministic.
- [ ] Observation-contract unit test passes for all three controllers.
- [ ] `r_c`, `v_max`, and `max_steps` validated so success is reachable
  (see `docs/model_assumptions.md` change log).
- [ ] `r_col` defined in `docs/model_assumptions.md`.
- [ ] Training budget, tuning-trial count, and seed lists finalized.
- [ ] Protocol status set to "frozen" with date and git revision recorded.

## Deviations

| Date | Planned protocol item | Deviation | Reason | Interpretation impact |
|---|---|---|---|---|
| (none yet) | | | | |
