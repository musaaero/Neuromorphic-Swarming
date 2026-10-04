"""Leaky Integrate-and-Fire (LIF) neuron model.

Phase 1 task: "Proper LIF neuron model" — see ROADMAP.md.
Discrete-time update:
    v[t+1] = decay * v[t] + input[t]        (decay = exp(-dt/tau))
    spike  = v[t+1] >= threshold ; then hard-reset v and start refractory counter.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np


@dataclass
class LIFParams:
    tau_ms: float = 20.0          # membrane time constant
    dt_ms: float = 1.0            # simulation timestep
    threshold: float = 1.0        # firing threshold
    reset: float = 0.0            # post-spike membrane value (hard reset)
    refractory_steps: int = 2     # dead time after each spike

    @property
    def decay(self) -> float:
        return math.exp(-self.dt_ms / self.tau_ms)


class LIFNeuron:
    """Single scalar LIF neuron (reference implementation — readable, not fast)."""

    def __init__(self, params: LIFParams | None = None):
        self.params = params or LIFParams()
        self.v = 0.0
        self._refractory = 0

    def step(self, current: float) -> bool:
        """Advance one timestep; return True if this neuron spiked."""
        p = self.params
        if self._refractory > 0:
            self._refractory -= 1
            self.v = p.reset
            return False
        self.v = p.decay * self.v + current
        if self.v >= p.threshold:
            self.v = p.reset
            self._refractory = p.refractory_steps
            return True
        return False


class PopulationLIF:
    """Vectorised LIF population, shape (n_neurons,) — the workhorse for the swarm.

    Acceptance criteria (tests/test_neurons.py):
      * constant subthreshold input never spikes
      * constant suprathreshold input fires regularly at ~1/(tau_eff) analytic rate
      * refractory period suppresses spikes for exactly `refractory_steps` ticks
      * NO per-neuron Python loop in the hot path; benchmark vs. naive loop and report
    """

    def __init__(self, n: int, params: LIFParams | None = None):
        self.params = params or LIFParams()
        self.n = n
        self.v = np.zeros(n, dtype=np.float64)
        self._refractory = np.zeros(n, dtype=np.int32)

    def step(self, currents: np.ndarray) -> np.ndarray:
        raise NotImplementedError("Phase 1: vectorise LIFNeuron.step over `currents`")
