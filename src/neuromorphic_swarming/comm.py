"""Simulated spike-communication channel between drones.

Phase 1 task: "Spike-based inter-drone communication" — see ROADMAP.md.
The paper promises "reduced bandwidth requirements"; you can only claim that if the
channel is modelled. This module adds: range limits, bandwidth caps, latency jitter,
packet loss, and per-spike energy bookkeeping hooks.
"""
from __future__ import annotations

import numpy as np


class SpikeChannel:
    """Noisy, capacity-limited broadcast channel for one control tick.

    Parameters
    ----------
    range_m : max radio range; spikes beyond it never arrive
    drop_p  : per-spike probability of being lost (Bernoulli)
    jitter  : +/- integer timesteps of random delay applied to arrivals
    seed    : RNG seed for reproducible experiments (Phase 2 requires this)

    Acceptance criteria (tests/test_comm.py):
      * deterministic given a seed
      * measured drop rate converges to `drop_p` over many trials
      * out-of-range spikes are never delivered
    """

    def __init__(self, range_m: float = 30.0, drop_p: float = 0.05,
                 jitter: int = 1, seed: int | None = None):
        self.range_m = range_m
        self.drop_p = drop_p
        self.jitter = jitter
        self.rng = np.random.default_rng(seed)

    def transmit(self, spikes: np.ndarray, positions: np.ndarray,
                 receiver_idx: np.ndarray) -> np.ndarray:
        """Deliver `spikes` from senders to `receiver_idx` through the noisy channel."""
        raise NotImplementedError("Phase 1: implement SpikeChannel.transmit")
