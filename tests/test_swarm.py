"""Phase 1/2 — swarm environment acceptance tests (see ROADMAP.md)."""
import numpy as np
import pytest

from neuromorphic_swarming.swarm import SwarmConfig, SwarmEnv


@pytest.fixture()
def env():
    return SwarmEnv(SwarmConfig(n_drones=20, seed=42))


@pytest.mark.xfail(reason="Phase 1 TODO: SwarmEnv.reset()", strict=True)
def test_reset_shapes_and_determinism(env):
    obs_a = env.reset(seed=42)
    pos_a = env.positions.copy()
    assert np.allclose(pos_a, env.positions), "same seed must reproduce initial state"
    assert obs_a.shape[0] == 20


@pytest.mark.xfail(reason="Phase 1 TODO: decentralised adjacency", strict=True)
def test_neighbours_respect_comm_range(env):
    env.reset(seed=1)
    for i, nbrs in enumerate(env.neighbour_indices()):
        d = np.linalg.norm(env.positions[nbrs] - env.positions[i], axis=1)
        assert (d <= env.config.comm_range_m).all(), "no global knowledge allowed"


@pytest.mark.xfail(reason="Phase 1 TODO: step() with energy logging", strict=True)
def test_step_returns_info_with_energy(env):
    env.reset(seed=0)
    _obs, _r, _done, info = env.step(np.zeros((20, 2)))
    assert "energy_mj_so_far" in info


@pytest.mark.xfail(reason="Phase 1 TODO: disabled drones excluded from dynamics", strict=True)
def test_disabled_drones_do_not_move_or_influence():
    cfg = SwarmConfig(n_drones=20, disable_fraction=0.3, seed=7)
    env = SwarmEnv(cfg)
    env.reset()
    dead = np.flatnonzero(~env.alive)
    env.step(np.ones((20, 2)))
    assert np.allclose(env.positions[dead], 0.0) or not env.alive[dead].any()
