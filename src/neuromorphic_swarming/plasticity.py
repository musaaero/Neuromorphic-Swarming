"""Spike-Timing-Dependent Plasticity (STDP).

Phase 1 task: "STDP for consensus / leader-following" — see ROADMAP.md.
Paper §2.2.2 claims STDP adapts inter-drone communication weights. Here we make it real.
"""
from __future__ import annotations

import numpy as np


class STDPRule:
    """Pair-based additive STDP over a weight matrix W of shape (n_pre, n_post).

    Convention dt = t_post - t_pre:
        dt > 0 (causal)   -> LTP:  dW = +A_plus  * exp(-dt / tau_plus)
        dt < 0 (acyclic)  -> LTD:  dW = -A_minus * exp(+dt / tau_minus)
    Weights clamped to [w_min, w_max].

    Acceptance criteria (tests/test_plasticity.py):
      * causal pairs strengthen, acyclic pairs weaken
      * weights stay bounded
      * supports a dynamic adjacency mask (drones entering/leaving radio range)
    """

    def __init__(self, n_pre: int, n_post: int,
                 a_plus: float = 0.01, a_minus: float = 0.012,
                 tau_plus: float = 20.0, tau_minus: float = 20.0,
                 w_min: float = 0.0, w_max: float = 1.0):
        self.a_plus, self.a_minus = a_plus, a_minus
        self.tau_plus, self.tau_minus = tau_plus, tau_minus
        self.w_min, self.w_max = w_min, w_max
        self.W = np.full((n_pre, n_post), 0.5 * (w_min + w_max))

    def update(self, pre_spikes: np.ndarray, post_spikes: np.ndarray,
               t: int, adjacency_mask: np.ndarray | None = None) -> None:
        raise NotImplementedError("Phase 1: implement STDPRule.update")

    def inject(self, pre_idx: int, post_idx: int, dt: float) -> float:
        """Eligibility-trace-free single-pair delta, exposed for unit testing."""
        raise NotImplementedError("Phase 1: implement STDPRule.inject")
