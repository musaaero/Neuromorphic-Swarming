"""Headless visualization: trajectory GIFs and raster plots.

Phase 1 task: "Visualization & docs" — see ROADMAP.md.
Must run without a display (CI-safe): Agg backend only, write files instead of plt.show().
"""
from __future__ import annotations


def plot_trajectories(position_log, target, out_path: str = "swarm.gif", fps: int = 30):
    """Animate (n_steps, n_drones, 2) position log -> GIF/PNG via matplotlib Agg."""
    raise NotImplementedError("Phase 1: implement plot_trajectories")


def plot_raster(spike_trains, out_path: str = "raster.png"):
    """Spike raster plot of the population — the 'proof' figure for SNN behaviour."""
    raise NotImplementedError("Phase 1: implement plot_raster")
