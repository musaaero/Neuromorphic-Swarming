# Neuromorphic Swarming

## Building neuromorphic swarms — contributors welcome

I'm starting this project to learn, experiment, and build in neuromorphic computing, autonomous drones, and swarm coordination. I want to explore the field through hands-on trial and error: make ideas concrete, test them in simulation, learn from what fails, and keep building toward more capable systems.

I'm based at a university in China (Nanjing university of Aeronautics and Astronautics mail me:uma_aero@nuaa.edu.cn) with strong unmanned-aircraft and helicopter research, and I hope to connect this project with the expertise and resources around me as it develops.

I'm looking for collaborators who are curious about robotics, control, spiking neural networks, reinforcement learning, simulation, or experimental research. You don't need to know everything already. Bring what you know, learn as we go, and help shape the direction.

Possible ways to contribute:
- build and test the swarm simulator
- explore control and learning approaches
- improve scenarios, visualizations, and evaluation
- document experiments, including failures and open questions
- suggest future directions and help turn them into small, testable steps

The goal is to learn together and steadily build something useful. The project is early, so contributors can help decide what to try next.

**Illustration:**

![Neuromorphic swarming concept illustration](https://github.com/user-attachments/assets/088e5a5f-3b8c-4467-8387-f4ae3b49fc5c)

## Project status

This is an early-stage, evolving project. The repository contains a scaffold for a swarm simulation, controllers, training, evaluation, and tests; many modules are placeholders and still need implementation. The roadmap below is a guide, not a fixed promise about what the project must become. We'll choose directions as we learn, validate each step, and record what worked, what failed, and what we want to try next.

## How to Use This Roadmap

- Work through the stages in order when practical; later experimental and publication stages depend on a defined, tested environment and baseline.
- Start by reading the project map below, then work only on the files listed for the current stage. Placeholder Python files are intentionally nonfunctional until you implement them.
- Estimates are rough **active effort**, not calendar deadlines. Add time for learning, compute queues, hardware access, and review. A stage may take longer or be deferred.
- A stage is complete when its exit checklist is satisfied and the result is recorded in the repository. External recognition or access to specialized hardware is not a requirement for making progress.
- Keep every result honest: label simulations, analytical estimates, GPU measurements, and measurements on neuromorphic hardware separately.
- At each decision gate, narrow scope rather than silently skipping validation. The smallest valid experiment is more useful than an ambitious, irreproducible one.

## Project Map

The scaffold separates simulation mechanics, controllers, training, evaluation, configuration, and research records. Files marked as placeholders contain only a short purpose note (or a documentation template); they do **not** implement the described behavior.

```text
.
├── README.md
├── pyproject.toml                  package/test configuration starter
├── configs/
│   ├── environment/                small, moving-target, and obstacle scenarios
│   ├── controllers/                rule-based, recurrent, and SNN settings
│   └── experiments/                smoke-test and benchmark run settings
├── docs/
│   ├── research_question.md        scope and hypotheses
│   ├── literature_review.md        notes on relevant research
│   ├── model_assumptions.md        simulator and energy assumptions
│   ├── experiment_protocol.md      pre-registered comparison procedure
│   ├── results_template.md         results reporting template
│   ├── decisions.md                dated decision log
│   ├── upstream_contributions.md    optional contribution tracker
│   └── publication_checklist.md    research write-up and release checklist
├── scripts/                        future command-line entry points
├── src/neuromorphic_swarming/
│   ├── env/                         dynamics, scenarios, observations, environment
│   ├── controllers/                 shared interface and controller implementations
│   ├── training/                    SNN and non-SNN training
│   └── evaluation/                  evaluation, robustness, scaling
├── tests/
│   ├── unit/                        isolated mechanics and metric tests
│   └── integration/                 end-to-end rollout tests
└── results/                         generated outputs; not committed by default
```

## Exact file-by-file development order

This is the actual coding sequence to follow. Do not jump ahead. Each phase depends on the previous one being tested and documented.

### Phase 0 — project framing and research

- `README.md` — write the repo purpose, scope, and the final story first. Update it again at the end, but do not treat it as the implementation.
- `pyproject.toml` — set the package name, Python version, dependencies, and dev/test tools.
- `docs/README.md` — create the docs index and list the research record for the repo.
- `docs/research_question.md` — write the first precise research question and non-goals.
- `docs/literature_review.md` — collect the references and summarize how they relate to the project.
- `docs/decisions.md` — record each design choice as you make it.
- `docs/model_assumptions.md` — write the initial simulator assumptions before building code.
- `docs/experiment_protocol.md` — define how the first experiment will be run and compared.
- `docs/results_template.md` — define a standard output format before any result is generated.
- `docs/publication_checklist.md` and `docs/upstream_contributions.md` — do these later, after the repo has evidence.

### Phase 1 — environment and simulation mechanics

- `src/neuromorphic_swarming/config.py` — add the configuration loader and schema.
- `src/neuromorphic_swarming/seeds.py` — add deterministic random seeding.
- `src/neuromorphic_swarming/env/__init__.py` — export the environment package.
- `src/neuromorphic_swarming/env/dynamics.py` — implement agent motion, velocity limits, boundaries, and simple physics.
- `src/neuromorphic_swarming/env/observations.py` — define local sensing, neighbor state, and observation packing.
- `src/neuromorphic_swarming/env/scenarios.py` — implement target motion, obstacle geometry, and scenario generation.
- `src/neuromorphic_swarming/env/swarm_env.py` — build the main environment loop and reset/step API.
- `src/neuromorphic_swarming/energy.py` — add the energy proxy after the movement model is defined.
- `src/neuromorphic_swarming/visualization.py` — add rollout rendering only after the environment is stable.
- `configs/environment/*.yaml` — define small-swarm, moving-target, and obstacle scenarios.
- `random.py` — leave it for local scratch or debugging only; do not let it become the main simulation logic.

### Phase 2 — controller interfaces and controller logic

- `src/neuromorphic_swarming/controllers/base.py` — define a shared controller interface and action format.
- `src/neuromorphic_swarming/controllers/rule_based.py` — implement the simple hand-designed baseline controller first.
- `src/neuromorphic_swarming/controllers/recurrent.py` — add the recurrent learned baseline after the rule-based controller works.
- `src/neuromorphic_swarming/controllers/snn.py` — implement the spiking controller only after the same task interface works for the baselines.
- `src/neuromorphic_swarming/controllers/__init__.py` — expose controller classes and factories.
- `configs/controllers/*.yaml` — define controller hyperparameters once the interface is fixed.

### Phase 3 — training and model learning

- `src/neuromorphic_swarming/training/__init__.py` — export training modules.
- `src/neuromorphic_swarming/training/train_baseline.py` — train the non-spiking baseline.
- `src/neuromorphic_swarming/training/train_snn.py` — train the spiking model.
- `scripts/train.py` — create the top-level training entry point once the training scripts run.
- `scripts/smoke_test.py` — add a quick smoke test for environment/controller sanity.

### Phase 4 — metrics, evaluation, and experiment automation

- `src/neuromorphic_swarming/metrics.py` — define task metrics, success criteria, and aggregation logic.
- `src/neuromorphic_swarming/evaluation/evaluate.py` — implement single-run evaluation logic.
- `src/neuromorphic_swarming/evaluation/robustness.py` — add node-loss and perturbation checks.
- `src/neuromorphic_swarming/evaluation/scaling.py` — benchmark scaling and swarm-size behavior.
- `src/neuromorphic_swarming/evaluation/__init__.py` — expose the evaluation package.
- `configs/experiments/*.yaml` — define the smoke and benchmark runs.
- `scripts/evaluate.py` — build the evaluation command line.
- `scripts/run_sweep.py` — add parameter sweeps once the single-run path works.
- `scripts/render_rollout.py` — create export/visualization of a short rollout after validation.
- `results/` — generated outputs only; leave this folder empty except for `.gitkeep` until runs exist.

### Phase 5 — tests and verification

- `tests/unit/test_dynamics.py` — verify motion, boundaries, and target logic.
- `tests/unit/test_environment.py` — verify environment setup and transitions.
- `tests/unit/test_observations.py` — verify what each agent sees.
- `tests/unit/test_controllers.py` — verify controller outputs and action validity.
- `tests/unit/test_energy.py` — verify the energy proxy calculations.
- `tests/unit/test_metrics.py` — verify the metric definitions and edge cases.
- `tests/unit/test_training.py` — verify that training runs and objective functions are valid.
- `tests/integration/test_rollout.py` — test a small end-to-end rollout.
- `tests/integration/test_config_loading.py` — confirm YAML config compatibility.

### Phase 6 — final polish and release

- Revisit `README.md` and clean up the project story and roadmap.
- Finalize `pyproject.toml` and recorded dependencies.
- Complete `docs/publication_checklist.md`.
- Add final evidence in `docs/` and record what is proven versus what is still a claim.
- Use `results/` for generated outputs only and keep the repo honest about what was measured.

### Simple rule for this repo

- If a file is in an earlier phase, do it before touching a later file.
- If a config file changes, update the corresponding code path and tests in the same pass.
- Do not write training or evaluation code before the environment and controller interfaces are stable.
- Do not claim a result before the relevant test and documentation exist.

### Which files belong to which stage?

| Stage | Main files to implement or fill in |
|---|---|
| 1. Foundation | `docs/research_question.md`, `docs/literature_review.md`, `docs/decisions.md`, environment setup in `pyproject.toml` |
| 2. Simulation | `src/neuromorphic_swarming/env/`, `src/neuromorphic_swarming/energy.py`, `src/neuromorphic_swarming/seeds.py`, `src/neuromorphic_swarming/visualization.py`, `configs/environment/`, `tests/unit/` |
| 3. Controllers | `src/neuromorphic_swarming/controllers/`, `src/neuromorphic_swarming/training/`, `configs/controllers/`, `scripts/train.py`, controller and training tests |
| 4. Experiments | `src/neuromorphic_swarming/evaluation/`, `src/neuromorphic_swarming/metrics.py`, `configs/experiments/`, `scripts/evaluate.py`, `scripts/run_sweep.py`, `docs/experiment_protocol.md`, `docs/results_template.md`, `tests/integration/` |
| 5. Aero/hardware extension | record the selected direction in `docs/decisions.md`; document model changes in `docs/model_assumptions.md`; add extension-specific modules/configs only after choosing the task or hardware |
| 6. Release/outreach | complete `README.md` and `pyproject.toml`; add final evidence to `docs/`; use `scripts/render_rollout.py` for the released demonstration |

### Implementation order inside the scaffold

1. Fill in the research notes and decide the first question; do not start with a 100-agent or hardware claim.
2. Build and test the deterministic environment mechanics before writing a trainable policy.
3. Add a transparent energy proxy and metrics before comparing controllers.
4. Implement the hand-designed controller, then a non-spiking learned baseline, then the SNN controller against the same interface.
5. Make one small end-to-end run work; only then add multi-seed sweeps, obstacles, moving targets, node loss, and larger swarms.
6. Freeze the evaluation protocol, run experiments, record results and limitations, then decide whether an aero/hardware extension is feasible.
7. Finish packaging, reproducibility instructions, and a public report after the evidence exists.

### Development setup

The package is a scaffold, so training and simulation commands do not work until their TODO modules are implemented. From the repository root, create an isolated environment and install the base development dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Before adding the optional SNN dependencies, check the official PyTorch installation selector for the correct CPU/CUDA build for your machine; then install the project extra with `python -m pip install -e ".[dev,snn]"` if the selected versions are compatible. Record exact versions and hardware in `docs/experiment_protocol.md`. Once the tests have been implemented, run them from the repository root with `python -m pytest`.

**Important:** the scaffold is a project organizer, not a functioning package yet. The Python files intentionally have no simulation, learning, or evaluation code; configurations and research templates must be reviewed and completed before being treated as experiment specifications.

## Staged Roadmap and To-Do List

### Stage 1 — Learn the field and shape the first experiment

**Estimated active effort:** 1–3 weeks
**Goal:** Learn the tools and concepts needed for a small, well-defined first experiment, then adjust the plan as results come in.

- [ ] Write down the questions and ideas that currently motivate the project in `docs/research_question.md`; expect them to evolve as you learn.
- [ ] Use `docs/literature_review.md` to keep useful notes on relevant research, methods, and tools you encounter.
- [ ] Study the SNN concepts that are useful for the next experiment: LIF neurons, membrane state and reset, spike encoding/decoding, surrogate gradients, recurrent state, and ANN-to-SNN conversion. Learn these as needed rather than treating them all as requirements.
- [ ] Set up a clean development environment and record the supported Python/PyTorch/CUDA versions, hardware, installation steps, and random-seed policy. Choose libraries only after confirming their current APIs and compatibility.
- [ ] Run one small tutorial/example using SpikingJelly or another suitable SNN framework; record the exact command and expected output. Optionally compare with sLIFELT after the basic experiment works.
- [ ] As a separate learning exercise, train or run a small LIF network on N-MNIST or DVS Gesture using a verified tutorial. Record dataset provenance, preprocessing, and the distinction between this exercise and the swarm-control experiment; do not claim event-camera swarm capability from a classification demo.
- [ ] Choose one initial question in `docs/research_question.md`. For example: *How does a small spiking controller compare with simple non-spiking controllers on a shared simulated swarm task?*
- [ ] Write down non-goals for the first experiment in `docs/research_question.md`: real aircraft deployment, claims of hardware energy savings, a full flight-dynamics model, and scaling to 100 agents before smaller cases are validated.

**Exit checklist**

- [ ] The initial research question, success metric, scope, and terminology are written down.
- [ ] One SNN tutorial/example runs in the documented environment.

### Stage 2 — Build a small, inspectable swarm simulation

**Estimated active effort:** 2–4 weeks
**Goal:** Build a deterministic, testable simulation before adding learning complexity.

- [ ] Specify a minimal 2D environment in `docs/model_assumptions.md`: coordinate system, agent state, update interval, velocity/acceleration limits, boundaries, target motion, and episode termination.
- [ ] Implement the smallest useful baseline environment in `src/neuromorphic_swarming/env/`, initially with a handful of agents and one target. Keep simulation mechanics separate from controller logic.
- [ ] Add configurable scenarios in `configs/environment/`, with defaults stored in human-readable files rather than hidden constants.
- [ ] Add moving-target behavior with configurable speed and trajectory; ensure target state is available to the environment and only the intended observations reach each agent.
- [ ] Add obstacle geometry and a documented collision/near-collision definition. Start with simple static obstacles; defer moving obstacles unless the basic case is reliable.
- [ ] Define local sensing and communication explicitly: range, neighbor information, message content, latency/drop assumptions, and whether communication is event/spike-based or merely represented by a proxy.
- [ ] Add a transparent energy **proxy** in `src/neuromorphic_swarming/energy.py` with separately reported terms (for example propulsion/work proxy, sensing, communication, and controller computation). Document units, equations, coefficients, and assumptions in `docs/model_assumptions.md`; do not call an arbitrary score “measured energy.”
- [ ] Add deterministic seeding and save enough configuration and run metadata to reproduce a trajectory.
- [ ] Add unit tests in `tests/unit/` for motion updates, boundary handling, target motion, collision detection, energy bookkeeping, and deterministic runs.
- [ ] Add a headless smoke run through `scripts/smoke_test.py` and a simple visualization in `src/neuromorphic_swarming/visualization.py` that can export a short GIF or video of a rollout.
- [ ] Check that the simulation behaves sensibly with 2, then 5–10 agents before increasing complexity.

**Simulation area of the scaffold:**

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

- [ ] Define observations and actions once in `src/neuromorphic_swarming/controllers/base.py` and share the interface across all controllers.
- [ ] Implement and test a simple hand-designed controller (for example, seek-target plus separation and obstacle avoidance). Use it as a sanity check, not as a straw-man comparison.
- [ ] Implement a small non-spiking learned controller in `src/neuromorphic_swarming/controllers/recurrent.py` or an explicitly selected MAPPO implementation. Decide whether centralized training/decentralized execution fits the task first.
- [ ] Implement a modest LIF-based spiking controller in `src/neuromorphic_swarming/controllers/snn.py` using the selected SNN framework. Begin with the smallest architecture that can solve a simple scenario.
- [ ] Choose a training approach (surrogate-gradient learning, ANN-to-SNN conversion, reservoir/fixed dynamics, or another justified method). Record why it fits the question in `docs/decisions.md`; do not combine approaches before establishing a working baseline.
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

### Stage 4 — Explore with controlled experiments

**Estimated active effort:** 3–6 weeks, plus compute time
**Goal:** Produce fair, uncertainty-aware evidence at modest scale before attempting headline numbers.

- [ ] Freeze `docs/experiment_protocol.md` before the main runs: scenarios, training budget, evaluation seeds, metrics, aggregation, and exclusion rules.
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
- [ ] Publish scripts/configuration and raw or suitably summarized result data needed to regenerate plots; use `docs/results_template.md` to record each experiment.

**Exit checklist**

- [ ] Main comparisons use the predeclared protocol and more than one seed.
- [ ] Plots/tables include uncertainty and disclose failures and limits.
- [ ] Every energy number is labeled with its measurement or estimation method.
- [ ] Results are described with their assumptions and limitations; unanswered questions remain open.

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

- [ ] Replace this roadmap's future-tense items with links to implemented modules, tests, datasets, and experiment results as they become available. Remove placeholder notes only after the corresponding implementation exists and is tested.
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
- [ ] Track candidate projects, current issue links, contribution status, and PR links in `docs/upstream_contributions.md`. Reconfirm issue numbers and project activity before acting; do not rely on the historical issue numbers in the original research plan.
- [ ] Share the finished work with relevant researchers or groups (for example, the TU Delft neuromorphic/event-based vision community or Intel Neuromorphic Research Community) using a concise, evidence-backed message. Outreach is optional and does not guarantee a response, internship, or admission.
- [ ] Use `docs/publication_checklist.md` before sharing a research write-up, blog post, or release. Check current venue deadlines and policies before any submission.

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
