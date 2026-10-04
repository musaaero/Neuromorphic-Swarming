![Untitled design](https://github.com/user-attachments/assets/088e5a5f-3b8c-4467-8387-f4ae3b49fc5c)

# Neuromorphic Swarming 🐝⚡

A concept paper on brain-inspired drone-swarm coordination — now growing into a real, tested codebase.

- 📄 **The paper:** [`Untitled document.pdf`](Untitled%20document.pdf) ([direct link](https://github.com/musabumair2004/Neuromorphic-Swarming/blob/main/Untitled%20document.pdf))
- 🧭 **What to do next, phase by phase (no fixed calendar):** [`ROADMAP.md`](ROADMAP.md)
- 🔬 **Phase 1 scaffold:** `src/neuromorphic_swarming/` + `tests/` (pip-installable, CI-ready)

---

## Honest Assessment of the Current State

*(Written October 2026. Read this before touching any code — the roadmap exists because of it.)*

## What this repository is today

- **A concept paper, not a codebase.** The repo contains `Untitled document.pdf` (8 pages), a MIT license, and a README that links to the PDF. There is no executable code at all — the only "implementation" is ~40 lines of NumPy pasted inside the PDF's appendix.
- **The appendix simulation does not match the paper's claims.** It plots 10 dots drifting toward a fixed point `[50, 50]`. Despite the framing:
  - There are **no LIF neurons** — "spikes" are just a boolean distance check (`distances < threshold`).
  - There is **no STDP**, no plasticity, no learning of any kind.
  - There is **no inter-drone communication** — drones never exchange information; each reacts only to a globally known target.
  - There is **no energy measurement**, so the paper's headline "60% power reduction" (§5.1) is unmeasured and currently unfalsifiable.
- **The paper's §4.2 hardware prototyping ("Intel Loihi processors", "event-driven vision sensors") has no supporting artifact** in this repository — no data, no figures, no code, nothing to reproduce it from. As written, those results cannot be verified.
- **Scale mismatch:** the paper describes 50–100 drone simulations; the appendix demo runs 10 agents in a 2D grid with no obstacles, no noise, and no channel model.
- **Repository signals:** ~2 stars, 0 open issues, effectively one author. This means two things simultaneously: (a) nobody is reviewing or demanding anything here yet, and (b) *whatever you contribute becomes the de facto reference implementation* — an unusually low-competition place to build visible work.

## Why this is actually good news for a contributor

Every gap above is a well-scoped, high-leverage contribution waiting to be claimed:

1. **Turn the toy snippet into a tested package** (Phase 1). Biggest single jump from "PDF + stars" to "real project."
2. **Make the paper's claims measurable — then benchmark them honestly** (Phase 2). If the numbers refute the claims, publishing that refutation is *still* a contribution and arguably a braver one. A repo that self-corrects earns more credibility than one that confirms itself.
3. **Bridge to real flight physics and real silicon** (Phase 4) — an aeronautical engineer who can couple rotor-power models to compute-energy accounting and port controllers to Loihi 2 is exactly the person this project needs and does not have.

## Ground rules adopted by this roadmap

- **No claim without a counter.** Every number in a README/paper must trace to a committed experiment config and seed (`experiments/`).
- **Baselines get treated fairly.** If Reynolds flocking beats the SNN on energy, that goes in the table.
- **Cite the constants.** Energy figures live in one module (`energy.py`) with sources, so reviewers can check them.
- **Time estimates, not calendar promises.** Life and coursework come first; phases are ordered, resumable, and skippable (see `ROADMAP.md`).

---

# 📋 Detailed To-Do List

The full phase-by-phase checklist with time estimates lives in **[ROADMAP.md](ROADMAP.md)**. Quick index:

| Phase | What | ⏱️ Estimate | Status |
|-------|------|------------|--------|
| 0 | Foundations: SNN theory, BindsNET/Lava, ABCS-Flocking hands-on | ~3–4 wks | ☐ |
| 1 | Rebuild the toy sim into a real, tested package (**this repo's scaffold is already here**) | ~4–6 wks | ◐ started |
| 2 | Benchmark suite: verify/refute the paper's §5 claims vs. fair baselines | ~4–6 wks | ☐ |
| 3 | Upstream PRs (SpikingJelly #753/#757/#654, Awesome-SNN #13, ABCS-Flocking #79, Lava) | ~3–5 wks, parallelisable | ☐ |
| 4 | Aero bridge: MAVLink/PX4 SITL, rotor-power energy model, IRIS Loihi 2 access ⚠️ apply early | ~4–8 wks | ☐ |
| 5 | Write-up: workshop paper + `pip install neuromorphic-swarming` release | ~4–6 wks | ☐ |
| 6 | Community: maintain, present, blog, mentor | ongoing | ☐ |

## Scaffold already created in this repo (Phase 1 starting point)

```
src/neuromorphic_swarming/
├── __init__.py      # package metadata
├── neurons.py       # LIFNeuron (reference impl ✓) + PopulationLIF (stub → tests define contract)
├── encoding.py      # rate / latency spike encoders (stubs)
├── plasticity.py    # STDPRule (stub)
├── comm.py          # SpikeChannel: range, jitter, loss (stub)
├── energy.py        # EnergyLedger mJ accounting + battery_ode (stubs)
├── swarm.py         # SwarmEnv gym-like API + §4.3 metrics (stubs)
├── viz.py           # headless GIF/raster plotting (stubs)
└── baselines/       # ANN-rate / Reynolds / centralized / MAPPO controllers (stubs)
tests/               # acceptance tests per module — strict-xfail = living to-do list
experiments/README   # planned benchmark configs e01–e05
.github/workflows/ci.yml
pyproject.toml       # pip-installable, [dev] extras, ruff+pytest configured
docs/BENCHMARKS.md · docs/ENERGY.md
```

**How the test suite doubles as your progress tracker:** every stubbed feature has a
`@pytest.mark.xfail(strict=True)` test. When you implement something, its xfail test flips to
XPASS-strict → CI fails loudly → you delete the marker → green. A fully green `pytest` run
means Phase 1 is done. Run it now:

```bash
pip install -e ".[dev]"
pytest -q
```
