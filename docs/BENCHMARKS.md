# Benchmarks (Phase 2 output — fill this in as experiments complete)

Head-to-head against the paper's §5 claims. Every cell must link to an `experiments/` config + seed.

## §5.1 "60% reduction in power consumption vs traditional centralized approaches"

| Controller | Energy (mJ/task) | Δ vs centralized | Latency (ms/decision) | Task success | Config |
|---|---|---|---|---|---|
| Centralized planner | _tbd_ | baseline | _tbd_ | _tbd_ | e01 |
| Reynolds flocking | _tbd_ | _tbd_ | _tbd_ | _tbd_ | e01 |
| Rate-coded ANN (ablation twin) | _tbd_ | _tbd_ | _tbd_ | _tbd_ | e01 |
| MAPPO | _tbd_ | _tbd_ | _tbd_ | _tbd_ | e01 |
| **SNN w/ STDP (ours)** | _tbd_ | _tbd_ | _tbd_ | _tbd_ | e01 |

> Verdict on the 60% claim: ☐ confirmed ☐ partially ☐ refuted → discuss honestly.

## §5.3 Scalability ("stable up to 100 drones")

Agents: 10 / 50 / 100 / 500 → wall-clock, memory, latency-vs-size curves from e02.

## §5.4 Robustness ("functional with 30% disabled")

Dropout 10/30/50% via `SwarmConfig.disable_fraction`, task completion in e03.

## Notes for fair comparison
- Identical tasks, sensors, channel model, and seeds across controllers.
- Report compute AND radio energy separately (`EnergyLedger.summary()`); radio TX dominates — say so.
- Negative results are first-class citizens here.
