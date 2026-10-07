# Neuromorphic Swarming

## Building neuromorphic swarms — contributors welcome

I'm starting this project to learn, experiment, and build in autonomous drones and swarm coordination. I want to explore the field through hands-on trial and error: make ideas concrete, test them in simulation, learn from what fails, and keep building toward more capable systems.

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

