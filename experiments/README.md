# Experiments (Phase 2 — benchmark suite)

One folder per experiment; each is rerunnable with a single command and pinned seeds.

Planned configs (add as YAML/JSON once `SwarmEnv.metrics()` exists):

```
experiments/
├── e01_energy_headtohead.yaml     # SNN vs ANN-rate vs Reynolds vs Centralized vs MAPPO
│                                  #   -> the honest version of paper §5.1 ("60% reduction")
├── e02_scalability.yaml           # 10 → 50 → 100 → 500 agents  (paper §5.3)
├── e03_robustness_dropout.yaml    # disable 10/30/50% of agents  (paper §5.4 claims 30%)
├── e04_adaptability_transfer.yaml # unseen scenario transfer     (paper §5.2)
└── e05_ablation_encoding.yaml     # latency code vs rate code under jitter/loss
```

Rules:
- Every result committed as JSON + one-line README table row. No cherry-picking.
- If a claim in `Untitled document.pdf` fails to reproduce, open an issue titled
  "Claim §X.Y does not reproduce" and link the config. That is a contribution, not a failure.
