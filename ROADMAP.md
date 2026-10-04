# 🗺️ Contribution Roadmap — Neuromorphic Swarming

> **No fixed calendar.** Everything below is organized as ordered *phases* with honest time
> estimates, not months. Do them whenever your schedule allows — skipping weeks or entire
> semesters between phases is fine. Each phase ends with a concrete deliverable (a PR, a tool,
> a paper), so progress is always resumable.
>
> **Legend:** ⏱️ = realistic estimate for someone with ~10 hrs/week who already knows Python,
> Git, and DRL (i.e., you). Items marked 🔴 are hard blockers for later phases.

---

## Phase 0 — Foundations: SNNs & the tools of the field
**⏱️ Total: ~3–4 weeks (splittable)**

- [ ] **SNN theory crash course** *(~1 week)*
  - [ ] LIF neuron dynamics: membrane potential, threshold, reset, refractory behaviour
  - [ ] Neuron models to know by name: ALIF, Izhikevich, adaptive-exponential (Loihi's default)
  - [ ] Encoding schemes: rate coding vs. **temporal/latency coding** (the one this repo needs)
  - [ ] Learning rules: STDP (the repo's core claim), reward-modulated STDP, surrogate gradients
  - [ ] Resources: `neurons.org/neurons/` interactive lessons; Gerstner & Kistler textbook (theory); Intel's Loihi course on Coursera (free audit)
- [ ] **Pick ONE framework and go deep** *(~1 week)* 🔴
  - [ ] Recommended: **BindsNET** (Loihi-friendly, batteries-included) + **Lava-NC** (Intel's modern stack for real chip deployment)
  - [ ] Secondary: snnTorch / SpikingJelly (GPU-native, good for your multi-GPU background)
  - [ ] Train a toy SNN on a static dataset (e.g., digit classification) end-to-end in each
- [ ] **Swarm-sim environment hands-on** *(~1–2 weeks)*
  - [ ] Run **ABCS-Flocking** (Crazyswarm2-based) — get the demo flock flying in Gazebo
  - [ ] Skim **Pymavlink + ArduPilot SITL** (needed later if we ever fly anything real)
  - [ ] Understand what a `.msg` bridge would need (relevant to ABCS issue #79)

**✅ Deliverable:** a personal notes repo/gist: "SNN from zero" + working BindsNET & Lava demos committed.

---

## Phase 1 — Rebuild this repo's toy simulation into a real codebase
**⏱️ Total: ~4–6 weeks** 🔴 *(everything downstream lives here)*

The PDF appendix is ~40 lines of NumPy that plots 10 dots drifting toward `[50,50]`. It has no LIF neurons, no STDP, no inter-drone communication, and its "energy savings" are unmeasured. Replace it honestly:

- [ ] **Repo scaffolding** *(~3 days)*
  - [ ] Convert flat repo → installable package (`pyproject.toml`, `neuromorphic_swarming/`)
  - [ ] CI: GitHub Actions running `pytest` + linting on every push
  - [ ] Pin dependencies; add `requirements-dev.txt`
- [ ] **Proper LIF neuron model** *(~1 week)*
  - [ ] Discrete-time LIF integrator with configurable tau, threshold, reset, refractory period
  - [ ] Unit tests against analytic solutions (e.g., constant-input leak-integrate-and-fire firing rate)
  - [ ] Benchmark: vectorised NumPy vs. Numba JIT (measure and report honestly)
- [ ] **Spike-based inter-drone communication** *(~1–2 weeks)*
  - [ ] Temporal/latency encoding of neighbour state (heading, distance, task priority)
  - [ ] Simulated packet channel: bandwidth cap, latency jitter, packet loss, sensor noise
  - [ ] Ablation switch: rate-coded ANN baseline vs. temporal SNN — measure spike count per control tick
- [ ] **STDP for consensus / leader-following** *(~1–2 weeks)*
  - [ ] Implement STDP weight updates over the dynamic interaction graph
  - [ ] Test: does the swarm reach heading consensus? Under node dropout?
- [ ] **Energy accounting model** *(~1 week)* 🔴
  - [ ] Count synaptic ops, spikes, and comm packets per timestep → map to mJ using published Loihi 2 energy figures
  - [ ] This is what turns "60% reduction" from a claim into a *measurement* (or refutes it — both are publishable)
- [ ] **Scale study** *(~3–5 days)*
  - [ ] 10 → 50 → 100 → 500 agents; log wall-clock, memory, latency-vs-size curves
- [ ] **Visualization & docs** *(~1 week)*
  - [ ] Headless runs → matplotlib GIF traces + live raster fallback
  - [ ] Docstrings everywhere; short design doc per module

**✅ Deliverable:** the repo goes from "PDF + stars" to an executable, tested reference implementation. This alone is the single biggest contribution to *this* project.

---

## Phase 2 — Make good on the paper's claims (benchmark or refute them)
**⏱️ Total: ~4–6 weeks**

The paper asserts: 60% energy reduction, stable scaling to 100 drones, functionality with 30% disabled. None are backed by data. Build the benchmark suite that produces real numbers:

- [ ] **Baselines** *(~2 weeks)*
  - [ ] Centralised MPC-style planner (the "traditional" straw man — be fair to it)
  - [ ] Rule-based Reynolds flocking (ABCS-style)
  - [ ] MAPPO multi-agent RL (your home turf — use your multi-GPU training experience)
- [ ] **Head-to-head evaluation** *(~2 weeks)*
  - [ ] Same tasks: target localisation, formation keeping, obstacle avoidance
  - [ ] Metrics exactly as §4.3 promises: energy (mJ/task via Phase 1 accounting), decision latency, scalability curve, adaptability (novel scenario transfer)
  - [ ] Robustness stress test: disable 10/30/50% of agents, measure task completion
- [ ] **Honest reporting** *(~1 week)*
  - [ ] Reproducible experiment configs (`experiments/` dir, seed control, one-command rerun)
  - [ ] Results table in README; write-up in `docs/BENCHMARKS.md`
  - [ ] If the numbers don't support the paper's claims — say so plainly. A repo that self-corrects earns more credibility than one that confirms itself.

**✅ Deliverable:** first credible empirical artifact of the project; strong conference/workshop poster material.

---

## Phase 3 — Upstream contributions to the ecosystem
**⏱️ Total: ~3–5 weeks, fully parallelisable with Phases 1–2**

Your credibility (and network) grows fastest by contributing where maintainers already ask for help. Verified open issues worth checking (re-verify before starting — they may be closed):

- [ ] **SpikingJelly** *(GPU-native SNN lib — perfect fit for your multi-GPU background)*
  - [ ] Issue **#753**: CUDA error when using `Conv2d` after pooling — reproduce, bisect, fix or file a detailed repro
  - [ ] Issue **#757**: how to implement recurrent connections — writing a documented tutorial is a very mergeable contribution
  - [ ] Issue **#654**: example reproducing results of arXiv:2208.10570 — an examples PR is high-value, low-risk
- [ ] **Awesome-SNN** — issue **#13**: tidy up the list format; easy first OSS merge + visibility
- [ ] **ABCS-Flocking** — issue **#79**: MAVROS ↔ ROS 2 `nav_msgs/Path.msg` bridge (directly useful for our sim→real path)
- [ ] **Lava-NC / Lava** — watch for `good-first-issue` labels; offer a swarm-controller example once Phase 1 exists
- [ ] **Etch (etchjs)** — event-driven scripting for neuromorphic apps; a drone-perception example would stand out

**✅ Deliverable:** 2–4 merged upstream PRs + maintainer relationships that make the eventual big submission welcome rather than cold.

---

## Phase 4 — The aero bridge (your unique angle) + real hardware
**⏱️ Total: ~4–8 weeks**

This is where *you* differ from every other contributor to this repo: an aeronautical engineer who can connect neuromorphic control to flight physics.

- [ ] **Sim-to-real interface** *(~2 weeks)*
  - [ ] Bridge Phase 1's output to PX4/ArduPilot SITL via MAVLink — commands, not just pretty plots
  - [ ] Validate on a standard flocking/reposition task in physics-based sim
- [ ] **Aero-aware energy model** *(~1–2 weeks)*
  - [ ] Couple rotor power models (thrust → induced power) with the compute-energy accounting → per-agent battery ODE
  - [ ] This upgrades the whole project's realism: "energy" stops meaning only "compute"
- [ ] **Neuromorphic flow sensing (moonshot, park if busy)** *(~2–4 weeks)*
  - [ ] Event-camera / optical-flow pipeline as a spiking controller primitive — connects to de Croon et al. (refs #1, #5 in the paper)
  - [ ] Even a small demo positions you at the intersection nobody else in this repo's orbit occupies
- [ ] **Real hardware access** *(admin lead-time: apply 1–2 months ahead)* 🔴
  - [ ] Apply for **IRIS** (European Open Research Centres for Neuromorphic Computing) remote Loihi 2 access — students eligible
  - [ ] Fallbacks: Intel's Lava cloud demos; SpiNNaker2 via Manchester group outreach
  - [ ] Port the Phase 1 controller to Loihi 2; compare simulated vs. chip energy/latency

**✅ Deliverable:** the first *actual* neuromorphic-swarming result on silicon under this repo's name — the difference between a concept paper and a research program.

---

## Phase 5 — Write it up & ship it
**⏱️ Total: ~4–6 weeks**

- [ ] **Publication** *(~3–4 weeks, overlaps packaging)*
  - [ ] Target: ICRA/IROS workshop, IEEE Conf. on Neuromorphic Systems (ICONS), or NeurIPS Workshop on Efficient Systems (no full-paper commitment needed at first)
  - [ ] Structure: concept (the PDF) → reference implementation (P1) → benchmarks (P2) → silicon (P4). Honest limitations section.
  - [ ] Preprint on arXiv regardless of acceptance
- [ ] **Packaging & release** *(~1 week)*
  - [ ] `pip install neuromorphic-swarming`; tagged GitHub releases; versioned docs (Sphinx/MkDocs)
  - [ ] Zenodo DOI for citation
- [ ] **Visibility** *(~1 week)*
  - [ ] Demo GIF/video at top of README (spikes animating is inherently eye-catching)
  - [ ] Short technical thread/blog aimed at the SNN + swarm communities

**✅ Deliverable:** citable, installable, demonstrated body of work — plus a graduate-school/industry portfolio piece.

---

## Phase 6 — Community & compounding
**⏱️ Ongoing, ~1–2 hrs/week forever**

- [ ] Answer issues/PRs on this repo (you'll be the most active contributor by far)
- [ ] Present at NUAA robotics/AI seminars; local meetups
- [ ] Keep a public "what I learned building this" blog series — recruitment-grade content for PhD/lab offers
- [ ] Mentor one junior contributor through Phase 0–1 checklist

---

## Dependency graph (do-not-skip order)

```
Phase 0 ──► Phase 1 ──► Phase 2 ──► Phase 5
                │           ▲
                ├──► Phase 3┘   (parallel anytime after P0)
                └──► Phase 4 ───► Phase 5
                     (start IRIS application EARLY — admin lead time)
```

**Rule of thumb:** finish Phase 1 before polishing anything else; submit the IRIS application before finishing Phase 3; never start Phase 5 writing until Phase 2 produced at least one honest number.
