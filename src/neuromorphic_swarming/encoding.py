"""Spike encoding schemes.

Phase 1 task: "Spike-based inter-drone communication" — see ROADMAP.md.
The paper (§2.2.1) claims information is encoded in *spike timing*; this module makes
that concrete and testable.
"""
from __future__ import annotations

import numpy as np


def rate_encode(values: np.ndarray, n_timesteps: int, max_rate_hz: float = 100.0,
                dt_ms: float = 1.0, rng: np.random.Generator | None = None) -> np.ndarray:
    """Encode continuous values as Poisson spike trains, shape (n_values, n_timesteps).

    Baseline encoder — required for the ANN-rate vs. SNN-temporal ablation.
    """
    raise NotImplementedError("Phase 1: implement rate_encode")


def latency_encode(values: np.ndarray, n_timesteps: int,
                   v_min: float = 0.0, v_max: float = 1.0) -> np.ndarray:
    """First-spike-latency code: larger value -> earlier spike (<=1 spike per neuron).

    Returns boolean array (n_values, n_timesteps). This is the encoder behind
    "temporal spike patterns" in §2.2.1 of the paper.
    """
    raise NotImplementedError("Phase 1: implement latency_encode")


def decode_latency(spikes: np.ndarray, n_timesteps: int,
                   v_min: float = 0.0, v_max: float = 1.0) -> np.ndarray:
    """Inverse of latency_encode; NaN where no spike arrived within the window."""
    raise NotImplementedError("Phase 1: implement decode_latency")
