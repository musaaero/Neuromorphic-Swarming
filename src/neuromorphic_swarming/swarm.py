"""The swarm environment: agents, neighbourhoods, tasks, metrics.

Phase 1/2 core — see ROADMAP.md. Composes neurons + encoding + plasticity + comm + energy
into a gym-like loop so baselines and the SNN controller are evaluated identically.

Paper §4 promises three tasks and four metric families; all live here:
  tasks:   target_localization | formation_keeping | obstacle_avoidance
  metrics: energy_mj_per_task | decision_latency | scalability_curve | adaptability
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class SwarmConfig:
    n_drones: int = 50
    world_size: float = 100.0          # metres, square arena
    dt_ms: float = 1.0
    horizon_steps: int = 2000
    comm_range_m: float = 30.0
    max_speed_mps: float = 5.0
    task: str = "target_localization"  # see module docstring
    seed: int = 0
    disable_fraction: float = 0.0      # robustness stress test (paper §5.4 claims 30%)


class SwarmEnv:
    """Minimal gym-style API: reset() -> obs ; step(actions) -> obs, reward, done, info.

    `info` must carry the EnergyLedger snapshot every tick (no silent accounting).

    Acceptance criteria (tests/test_swarm.py):
      * deterministic under fixed seed
      * neighbours computed from comm_range_m (not global knowledge — decentralised!)
      * disabled drones are excluded from dynamics AND from consensus
      * metrics() returns all four §4.3 families after an episode
    """

    def __init__(self, config: SwarmConfig):
        self.config = config
        self.positions = np.zeros((config.n_drones, 2))
        self.velocities = np.zeros((config.n_drones, 2))
        self.alive = np.ones(config.n_drones, dtype=bool)

    def reset(self, seed: int | None = None):
        raise NotImplementedError("Phase 1: initialise positions/target/obstacles")

    def step(self, actions: np.ndarray):
        raise NotImplementedError("Phase 1: integrate motion, deliver spikes, log energy")

    def neighbour_indices(self) -> list[np.ndarray]:
        raise NotImplementedError("Phase 1: range-limited adjacency")

    def metrics(self) -> dict:
        raise NotImplementedError("Phase 2: energy/latency/scalability/adaptability report")
