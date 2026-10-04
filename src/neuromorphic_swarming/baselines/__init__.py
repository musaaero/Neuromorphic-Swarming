"""Baseline controllers for the Phase 2 head-to-head benchmark.

Every baseline must expose the same interface as the SNN controller:
    decide(obs) -> actions, and never peek at global state it shouldn't have.
"""
from __future__ import annotations


class RateCodedANNController:
    """Ablation twin of the SNN: same inputs/outputs, dense rate-coded ANN.

    Purpose: isolate what *spiking* buys us vs. what just being local/decentralised buys us.
    """

    def decide(self, obs):
        raise NotImplementedError("Phase 2")


class ReynoldsFlockingController:
    """Classic separation/alignment/cohesion rules (ABCS-style). Cheap, strong baseline —
    be fair to it; if it wins on energy, that is a result, not a failure."""

    def decide(self, obs):
        raise NotImplementedError("Phase 2")


class CentralizedPlannerController:
    """The paper's 'traditional centralized approach' straw man. Give it the fairest
    implementation you can (MPC or simple assignment), report its compute+comm honestly."""

    def decide(self, obs):
        raise NotImplementedError("Phase 2")


class MappoController:
    """MAPPO multi-agent RL baseline (your home turf; train offline on multiple GPUs,
    then evaluate frozen policies in SwarmEnv)."""

    def decide(self, obs):
        raise NotImplementedError("Phase 2")
