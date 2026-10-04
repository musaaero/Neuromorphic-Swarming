"""Energy accounting: turn spikes/syn-ops/packets into millijoules.

Phase 1 task: "Energy accounting model" 🔴 — see ROADMAP.md.
This module is what upgrades the paper's "60% power reduction" from a *claim* into a
*measurement* (or refutes it — both are publishable). Numbers below use published
Loihi 2 / DVS figures; keep them in ONE place with citations so reviewers can check.
"""
from __future__ import annotations

from dataclasses import dataclass, field

# --- Reference energies (mJ per operation). UPDATE WITH CITATIONS in docs/ENERGY.md ---
# Placeholder magnitudes consistent with public Loihi 2 datasheets/talks (~pJ–nJ range).
SYNAPTIC_OP_MJ = 3.0e-6      # per synaptic event on-chip
NEURON_UPDATE_MJ = 0.5e-6    # per membrane-state update
SPIKE_TX_MJ = 100.0e-3       # per radio spike-packet transmitted (dominant cost!)
SENSOR_EVENT_MJ = 5.0e-3     # per event-camera readout


@dataclass
class EnergyLedger:
    """Accumulates per-agent energy counters over a run."""
    n_agents: int
    synaptic_ops: int = 0
    neuron_updates: int = 0
    spikes_tx: int = 0
    sensor_events: int = 0
    per_agent: list = field(default_factory=list)

    def record_tick(self, *, n_syn_ops: int, n_neuron_updates: int,
                    n_spikes_tx: int, n_sensor_events: int) -> None:
        raise NotImplementedError("Phase 1: accumulate counters")

    @property
    def total_mj(self) -> float:
        """Total compute+communication energy in millijoules."""
        raise NotImplementedError("Phase 1: apply the constants above")

    def summary(self) -> dict:
        """Dict for JSON logging: totals + per-agent breakdown + dominant-cost note
        (spoiler: radio TX will dwarf on-chip compute — say so in the writeup)."""
        raise NotImplementedError


def battery_ode(mass_kg: float, rotor_power_w: float, compute_mw: float,
                capacity_mah: float, voltage: float = 11.1) -> float:
    """Phase 4 (aero bridge): endurance estimate in minutes incl. flight power.

    Rotor power may come from a simple induced-power model; keep the coupling here.
    """
    raise NotImplementedError("Phase 4: implement battery endurance ODE")
