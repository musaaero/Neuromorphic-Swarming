# Neuromorphic Swarming

**A reproducible path from a neuromorphic-drone-swarming concept to measured, openly documented experiments.**

This repository contains a concept paper, not a finished simulator or validated implementation. The plan below is deliberately organized into stages rather than calendar months: estimates are for active work, so stages can be paused, reordered where dependencies allow, or dropped without implying a missed schedule.

**Paper:** [Brain-Inspired Framework for Autonomous Drone Coordination](./Untitled%20document.pdf)

**Illustration:**

![Neuromorphic swarming concept illustration](https://github.com/user-attachments/assets/088e5a5f-3b8c-4467-8387-f4ae3b49fc5c)

## 🔍 What This Repo Actually Is

Neuromorphic-Swarming (musaaero/Neuromorphic-Swarming) — a concept/position paper only:
Untitled document.pdf — "Brain-Inspired Framework for Autonomous Drone Coordination": SNNs + neuromorphic hardware (Loihi 2/SpiNNaker), spike-based comms, STDP plasticity, reservoir computing, event cameras (DVS). Claims 60% energy reduction, 100-drone scalability, 30% node-loss robustness.
The Appendix code is a ~40-line toy NumPy script (threshold spikes → velocity nudge). No real training loop, no RL, no benchmarks.
README = one link + an image. No code directory, no docs, no CI. 2 stars, 0 forks, 0 open issues.
Honest assessment: the topic is hot (neuromorphic flight control — Paredes-Vallés/de Croon at TU Delft, FlyDrone project), but the repo has a credibility gap: it claims "simulations and prototype tests" that don't exist in code. For you specifically (aero + multi-GPU DRL), this is actually good news — the fastest path to "decent contribution" here isn't upstream PRs into a dead repo; it's becoming the person who makes this idea reproducible, then porting those skills into the active ecosystems.

The paper's numerical statements are **claims to investigate**, not results established by this repository. The roadmap treats them as hypotheses: any reproduced result must state its assumptions, measurement method, hardware, and limitations.

## How to Use This Roadmap

- Work through the stages in order when practical; later experimental and publication stages depend on a defined, tested environment and baseline.
- Estimates are rough **active effort**, not calendar deadlines. Add time for learning, compute queues, hardware access, and review. A stage may take longer or be deferred.
- A stage is complete when its exit checklist is satisfied and the result is recorded in the repository. A merged upstream PR, paper acceptance, or access to neuromorphic hardware is not a required completion condition.
- Keep every result honest: label simulations, analytical estimates, GPU measurements, and measurements on neuromorphic hardware separately.
- At each decision gate, narrow scope rather than silently skipping validation. The smallest valid experiment is more useful than an ambitious, irreproducible one.

## Staged Roadmap and To-Do List

### Stage 1 — Understand the paper and establish the foundation

**Estimated active effort:** 1–3 weeks
**Goal:** Turn the paper's ideas into a clearly scoped, technically grounded experiment plan.

- [ ] Read the full paper, including its appendix and references; keep a notes file or literature table in the eventual project documentation.
- [ ] Extract every quantitative claim into a claim ledger. For each item, record the exact paper location, what is claimed, required assumptions, a measurable definition, and what evidence would or would not count as reproduction.
  - [ ] Define what “60% energy reduction” compares against and whether energy means modeled propulsion energy, processor energy, communication energy, or a measured total.
  - [ ] Define the workload, success condition, and resource limits behind “100-drone scalability.”
  - [ ] Define the node-loss procedure, failure timing, and recovery metric behind “30% node-loss robustness.”
- [ ] Read the cited work named in the initial research plan: Vitale; Paredes-Vallés; Taylor & Atkeson; Xu et al.; and Batra et al. Verify the full bibliographic details from the PDF before citing them.
- [ ] For each paper, record its research question, method, dataset or task, main result, limitations, and one way it relates to this project.
- [ ] Study the SNN concepts needed for the experiment: LIF neurons, membrane state and reset, spike encoding/decoding, surrogate gradients, recurrent state, and ANN-to-SNN conversion. Note which are actually needed rather than treating every topic as a project requirement.
- [ ] Set up a clean development environment and record the supported Python/PyTorch/CUDA versions, hardware, installation steps, and random-seed policy. Choose libraries only after confirming their current APIs and compatibility.
- [ ] Run one small tutorial/example using SpikingJelly or another suitable SNN framework; record the exact command and expected output. Optionally compare with sLIFELT after the basic experiment works.
- [ ] Decide the initial question in one sentence. Suggested starting question: *Under a fixed simulated swarm task and matched observation/action constraints, how does a small spiking controller compare with simple non-spiking controllers on task success, communication, and explicitly defined energy proxies?*
- [ ] Write down non-goals for the first experiment: real aircraft deployment, claims of hardware energy savings, a full flight-dynamics model, and scaling to 100 agents before smaller cases are validated.

**Exit checklist**

- [ ] Paper claims and cited references have been checked against the PDF.
- [ ] The initial research question, success metric, scope, and terminology are written down.
- [ ] One SNN tutorial/example runs in the documented environment.
- [ ] No paper claim is presented as an experimentally reproduced result.

### Stage 2 — Build a small, inspectable swarm simulation

**Estimated active effort:** 2–4 weeks
**Goal:** Replace the appendix toy example with a deterministic, testable simulation before adding learning complexity.

- [ ] Inspect the appendix example and describe exactly what it does, what it omits, and which behavior is worth preserving.
- [ ] Specify a minimal 2D environment: coordinate system, agent state, update interval, velocity/acceleration limits, boundaries, target motion, and episode termination.
- [ ] Implement the smallest useful baseline environment, initially with a handful of agents and one target. Keep simulation mechanics separate from controller logic.
- [ ] Add configurable scenarios, with defaults stored in a human-readable configuration file rather than hidden constants.
- [ ] Add moving-target behavior with configurable speed and trajectory; ensure target state is available to the environment and only the intended observations reach each agent.
- [ ] Add obstacle geometry and a documented collision/near-collision definition. Start with simple static obstacles; defer moving obstacles unless the basic case is reliable.
- [ ] Define local sensing and communication explicitly: range, neighbor information, message content, latency/drop assumptions, and whether communication is event/spike-based or merely represented by a proxy.
- [ ] Add a transparent energy **proxy** with separately reported terms (for example propulsion/work proxy, sensing, communication, and controller computation). Document units, equations, coefficients, and assumptions; do not call an arbitrary score “measured energy.”
- [ ] Add deterministic seeding and save enough configuration and run metadata to reproduce a trajectory.
- [ ] Add unit tests for motion updates, boundary handling, target motion, collision detection, energy bookkeeping, and deterministic runs.
- [ ] Add a headless smoke run and a simple visualization that can export a short GIF or video of a rollout.
- [ ] Check that the simulation behaves sensibly with 2, then 5–10 agents before increasing complexity.

**Possible future layout (planning reference only; these files are not created by this README change):**

```text
src/                 simulation and controller modules
configs/             named experiment configurations
tests/               deterministic environment and metric tests
scripts/              training, evaluation, and visualization entry points
results/              generated outputs (usually ignored by version control)
docs/                 model assumptions, experiment protocol, and results notes
```

**Exit checklist**

- [ ] A small seeded scenario runs end-to-end and can be visualized.
- [ ] Core simulation behavior and energy-proxy accounting have tests.
- [ ] A new reader can identify what is modeled versus omitted.
- [ ] Increasing the agent count does not silently change the task definition.

### Stage 3 — Implement SNN and non-SNN controllers

**Estimated active effort:** 3–6 weeks
**Goal:** Compare controllers on the same task without giving one method extra information or tuning.

- [ ] Define observations and actions once and share the interface across all controllers.
- [ ] Implement and test a simple hand-designed controller (for example, seek-target plus separation and obstacle avoidance). Use it as a sanity check, not as a straw-man comparison.
- [ ] Implement a small non-spiking learned controller. Select a baseline such as a recurrent policy or MAPPO only after deciding whether centralized training/decentralized execution fits the task.
- [ ] Implement a modest LIF-based spiking controller in the selected SNN framework. Begin with the smallest architecture that can solve a simple scenario.
- [ ] Choose a training approach (surrogate-gradient learning, ANN-to-SNN conversion, reservoir/fixed dynamics, or another justified method). Record why it fits the question; do not combine approaches before establishing a working baseline.
- [ ] Make observation encoding, recurrent state, reset behavior, output decoding, and spike count explicit in the implementation and experiment configuration.
- [ ] Use the same scenario distribution, observation limits, action bounds, episode budget, and evaluation seeds for all controllers.
- [ ] Define success before tuning: for example, target coverage or arrival, collision rate, completion time, and constraint violations.
- [ ] Verify each controller against basic cases: one agent, stationary target, no obstacles, and a deliberately achievable target.
- [ ] Track training curves and evaluation separately. Do not report training performance as final benchmark performance.
- [ ] Keep model sizes and training compute visible; state when parameter counts or training budgets are not matched.
- [ ] Add checkpointing and a documented way to load a trained policy for evaluation.

**Exit checklist**

- [ ] Each controller uses the same documented environment API and observation/action contract.
- [ ] A simple known scenario is solved or any failure is understood and reported.
- [ ] Training and evaluation are separate, seeded, and repeatable.
- [ ] The comparison protocol and controller differences are documented.

### Stage 4 — Validate claims with controlled experiments

**Estimated active effort:** 3–6 weeks, plus compute time
**Goal:** Produce fair, uncertainty-aware evidence at modest scale before attempting headline numbers.

- [ ] Freeze an evaluation protocol before the main runs: scenarios, training budget, evaluation seeds, metrics, aggregation, and exclusion rules.
- [ ] Begin with small swarms (for example 5, 10, and 20 agents). Increase scale only after smaller cases are stable and resource costs are understood.
- [ ] Add a scenario matrix covering target motion, obstacle density, sensing/communication range, and selected disturbances.
- [ ] Add node-loss tests with a reproducible failure schedule. Report the fraction and timing of failures, task success, collisions, and recovery behavior.
- [ ] Add ablations one factor at a time: communication enabled/disabled, SNN state/spiking choices, energy terms, sensing assumptions, and controller components relevant to the research question.
- [ ] Run multiple independent seeds. Use a modest pilot to estimate variability, then choose a justified number of seeds rather than relying on one favorable run.
- [ ] If using Ray, `torchrun`, or another parallel runner, first confirm that a single run is correct; record worker count, hardware, software versions, and resource allocation for sweeps.
- [ ] Report task reward/success, completion time, collision and safety measures, communication volume, spike count, inference latency, parameter count, training time, and compute use where applicable.
- [ ] Report distributions or uncertainty (not only a best run). Keep failed runs and explain exclusions.
- [ ] Separate simulator energy proxies from measured wall-clock/GPU power and from neuromorphic-chip measurements. Never infer chip energy from spike counts alone without a validated model.
- [ ] Treat 50–100-agent runs as a stretch test: establish a measurable scaling curve and disclose hardware/runtime limits. A smaller verified result is acceptable if larger cases are infeasible.
- [ ] Compare results to the paper's claim ledger. Mark each claim as reproduced under stated assumptions, partially supported, not reproduced, or not tested.
- [ ] Publish scripts/configuration and raw or suitably summarized result data needed to regenerate plots.

**Exit checklist**

- [ ] Main comparisons use the predeclared protocol and more than one seed.
- [ ] Plots/tables include uncertainty and disclose failures and limits.
- [ ] Every energy number is labeled with its measurement or estimation method.
- [ ] Paper claims are assessed individually; unsupported claims remain explicitly unsupported.

### Stage 5 — Extend toward aero and neuromorphic hardware

**Estimated active effort:** 3–8+ weeks; hardware access can add substantial waiting time
**Goal:** Explore one carefully chosen application bridge without conflating simulation results with flight or chip results.

- [ ] Choose **one** aero direction based on available data, compute, and expertise: airfoil/design optimization, flow control, or gust-load alleviation. Write a short feasibility note before implementation.
- [ ] Define an interface between the chosen aero task and the controller, and first establish a conventional baseline using the same task and constraints.
- [ ] Start with a low-cost surrogate or reduced-order model if full CFD is too expensive; validate it against known cases and state its limits.
- [ ] Keep the aero extension as a separate experiment from the core swarm benchmark unless a clear shared research question justifies combining them.
- [ ] Investigate access to Loihi 2 or another neuromorphic platform, including current program eligibility, queue, tooling, supported operations, and data-export restrictions. Treat access as uncertain, not guaranteed.
- [ ] If hardware is available, map only a tested controller; document conversion/mapping changes, unsupported operations, compiler/runtime versions, and functional equivalence checks.
- [ ] Measure chip power/energy using the platform's supported measurement method. Report boundaries (chip-only versus host/system), workload, duration, and instrumentation.
- [ ] Run a matched GPU or CPU reference workload and report the comparison conditions. Avoid comparing unlike batch sizes, precision, or workloads.
- [ ] If hardware access is unavailable, finish with a clearly labeled simulator/software mapping study; do not describe it as a hardware energy measurement.

**Exit checklist**

- [ ] One aero or hardware extension has a defined, bounded question and baseline.
- [ ] Simulation, surrogate, and physical-hardware evidence are clearly distinguished.
- [ ] Any performance or energy comparison reports its measurement boundary and limitations.

### Stage 6 — Package, publish, and contribute upstream

**Estimated active effort:** 2–4 weeks for a solid release; ongoing for writing and community work
**Goal:** Make the work understandable, reproducible, and useful to others.

- [ ] Replace this roadmap's future-tense items with links to implemented modules, tests, datasets, and experiment results as they become available.
- [ ] Add installation instructions, supported environment details, a quick-start example, configuration guide, and troubleshooting notes.
- [ ] Ensure one documented command can run a small evaluation from a clean environment.
- [ ] Add continuous integration for formatting/linting and tests once the package and test suite exist.
- [ ] Add a model/data/results license review; document third-party datasets, models, and code licenses before redistribution.
- [ ] Include a limitations section covering toy simulation assumptions, reward/metric choices, energy proxies, seed variance, scaling limits, and lack of flight validation.
- [ ] Create a concise report or blog post with the research question, methods, fair-comparison protocol, figures, negative results, and reproducibility links.
- [ ] Consider a workshop or conference submission only after checking current scope, deadlines, artifact policies, and evidence requirements. Potential venues from the initial plan include event-based vision, robotics, or neuromorphic-learning workshops; venue fit is not guaranteed.
- [ ] Prepare a release with tagged code, configurations, and a small demonstration video or GIF. Make sure the media is generated by the released version.
- [ ] Before proposing an upstream contribution, re-check the current issues, contribution guidelines, and project activity. Candidate ecosystems mentioned in the initial plan include SpikingJelly, TheBrainLab/Awesome-SNN, and YunxiaoGuo/ABCS-Flocking; specific issue numbers and requests may have changed.
- [ ] Pick one appropriately scoped contribution, discuss it with maintainers if needed, add focused tests, and submit it independently of claims about this repository.
- [ ] Share the finished work with relevant researchers or groups (for example, the TU Delft neuromorphic/event-based vision community or Intel Neuromorphic Research Community) using a concise, evidence-backed message. Outreach is optional and does not guarantee a response, internship, or admission.

**Exit checklist**

- [ ] A clean checkout can reproduce at least the documented small evaluation.
- [ ] The release and write-up accurately distinguish results from hypotheses.
- [ ] Limitations, licenses, environment, and citation instructions are present.
- [ ] Any upstream or research outreach points to a stable, reviewable artifact.

## Suggested Project Milestones

Use these as evidence checkpoints rather than deadlines:

1. **Scope note:** one question, claim ledger, literature notes, and chosen first experiment.
2. **Inspectable simulation:** seeded small swarm, visualization, tests, and documented model assumptions.
3. **Controller comparison:** SNN, non-spiking learned baseline, and simple sanity baseline under a shared protocol.
4. **Reproducible results:** multi-seed evaluation, scaling/robustness tests, uncertainty, and transparent energy accounting.
5. **Optional extension:** one aero task or real neuromorphic hardware experiment, with evidence type stated accurately.
6. **Public artifact:** documented release, reproducible command, report/blog, and (if useful) a focused upstream contribution.

## Match the Work to Your Strengths

| Strength or context | Where it can help |
|---|---|
| Multi-GPU pipelines | Parallel, reproducible seed/configuration sweeps after single-run correctness is established |
| DRL/MARL experience | Designing a fair MAPPO or recurrent-policy baseline and a careful evaluation protocol |
| Aero background | Choosing and validating one meaningful flow-control, airfoil, or gust-load application |
| NUAA student status | Exploring academic collaboration, eligibility, and possible neuromorphic-hardware access; availability must be confirmed |

**Rule of thumb:** every completed stage should leave a public, inspectable artifact—notes, tests, a reproducible result, a release, a write-up, or a merged contribution. Visible, honest progress is more valuable than an unsupported headline claim.
