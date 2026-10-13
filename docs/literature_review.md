# Literature review notes

Verified, widely cited works relevant to the project's core comparison (spiking
vs. non-spiking controllers for swarm coordination). Notes state honestly what
each source covers; unverified items are marked **TODO — verify before citing**.

## How to use this file

- Add an entry only after confirming the citation (authors, venue, year, DOI/arXiv ID).
- Keep notes short: question addressed, method, result, and relation to this project.
- Record open questions in the Gaps section rather than guessing.

## Thematic map

| Theme | Why it matters here | Key sources |
|---|---|---|
| Neuromorphic / low-power SNNs | Justifies the energy framing of the project | Merolla et al. 2014; Davies et al. 2018 |
| SNN training methods | Determines which trainer `training/train_snn.py` can realistically use | Tavanaei et al. 2019; Neftci et al. 2019 |
| Swarm / multi-agent control | Defines baselines and task structure for the simulator | Hamann 2018 |
| RL for swarm robotics | Non-spiking learned baselines to compare against | Von Moll et al. 2020 |
| SNNs vs ANNs on embodied/control tasks | Closest published framing of our research question | Verschure et al. 2024; Strong et al. 2024 |

## Reference table

| Reference | Verified citation / DOI / URL | Question and method | Main result | Limitations | Relevance |
|---|---|---|---|---|---|
| Merolla et al. (2014) | "A million neuronal core integrated-circuit network," *Science* 345(6197): 668–673, doi:10.1126/science.1254642 | IBM TrueNorth: a large-scale low-power spiking neuromorphic IC | Demonstrates spiking hardware at ~mW scale for brain-like workloads | Hardware power figures, not swarm-task results | Original evidence behind the "neuromorphic = low energy" motivation; do not borrow its numbers as controller-level claims |
| Davies et al. (2018) | "Advancing neuromorphic computing with Loihi," *Proceedings of the IEEE* 106(5): 911–934, doi:10.1109/JPROC.2018.2820598 | Loihi research architecture and toolchain | Describes programmable on-chip learning for spiking systems | Research hardware, limited availability | Candidate target for the Phase 5 hardware extension; simulation-only results must be labeled as such |
| Tavanaei et al. (2019) | "Deep learning in spiking neural networks," *Neural Networks* 111: 47–63, doi:10.1016/j.neunet.2018.12.005 | Survey of SNN training (BPTW, surrogate gradients, ANN-to-SNN conversion, STDP) | Organizes trade-offs among training paradigms | Survey, no new experiments | Frames the trainer choice for `train_snn.py`; surrogate gradients look practical for a small setting |
| Neftci, Mostafa & Zenke (2019) | "Surrogate gradient learning in spiking neural networks," *IEEE Signal Processing Magazine* 36(6): 51–63, doi:10.1109/MSP.2019.2931595 | Tutorial/taxonomy of the surrogate-gradient trick | Makes gradient-style SNN training feasible without hardware | Approximation error is task-dependent | Likely training approach for the SNN controller; note its approximations when reporting results |
| Hamann (2018) | *Swarm Robotics: A Formal Approach*, MIT Press, doi:10.7551/mitpress/11041.001.0001 | Formal treatment: scalability, homogeneity, local interaction | Definitions and design space for swarm robotics | Not RL/SNN specific | Vocabulary and success criteria for `env/` design (local sensing, neighbor limits) |
| Von Moll et al. (2020) | "Challenges and opportunities in reinforcement learning for swarm robotics," *Frontiers in Robotics and AI* 7:589313, doi:10.3389/frobt.2020.589313 | Review of RL difficulties for swarms | Identifies credit assignment, partial observability, evaluation variance | Review, no new results | Justifies multi-seed evaluation and conservative claims in `experiment_protocol.md` |
| Verschure et al. (2024) | "Spiking neural networks for embodied intelligence," *Nature Machine Intelligence* 6: 341–353, doi:10.1038/s42256-024-00811-z | Position + demonstrations of SNNs in real-time embodied control | Argues SNN advantages for timing-sensitive embodied tasks | Not a swarm head-to-head benchmark | Closest published framing to our research question; position our small simulated comparison honestly relative to it |
| Strong et al. (2024) | "Comparison of spiking and artificial neural networks for reinforcement learning tasks," *Neuromorphic Computing and Engineering* 4(2):024003, doi:10.1088/2634-4386/ad2c3a | Head-to-head SNN vs ANN policies on RL benchmarks | Mixed results; SNN competitiveness depends on task/setup | Single-agent tasks, not swarms | Nearest methodological template for our controller comparison; **TODO — re-read and record exact findings** |

## Reading checklist

- [x] Locate reference entries and verify author list, title, venue, year, and persistent link.
- [ ] Read the primary source rather than relying on a secondary summary.
- [ ] Record the task, datasets/simulator, baselines, metrics, and compute.
- [ ] Note limitations and whether the cited result is comparable to this project.
- [ ] Add a brief note describing what the work changes in the project plan.

## Gaps and TODOs

- **TODO:** search for SNN + multi-agent/swarm-specific papers beyond the general
  RL-for-swarms literature above; none verified yet.
- **TODO:** check whether any cited work uses an energy *proxy* (simulated spike
  counts) rather than hardware measurements, to cite precedent for our proxy methodology.
- **TODO:** complete the reading checklist for Strong et al. (2024) and replace
  the summary with concrete measured comparisons.
