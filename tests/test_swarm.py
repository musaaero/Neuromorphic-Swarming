"""Phase 1/2 — swarm environment acceptance tests (see ROADMAP.md)."""
import numpy as np
import pytest

from neuromorphic_swarming.swarm import SwarmConfig, SwarmEnv


def make_env():
    """Factory (not a fixture) so xfail-marked tests can use it under pytest >= 9."""
    return SwarmEnv(SwarmConfig(n_drones=20, seed=42))


@pytest.mark.xfail(reason="Phase 1 TODO: SwarmEnv.reset()", strict=True)
def test_reset_shapes_and_determinism():
    obj = make_env()
    obs_a = obj.reset(seed=42)
    pos_a = obj.positions.copy()
    assert np.allclose(pos_a, obj.positions), "same seed must reproduce initial state"
    assert obs_a.shape[0] == 20


@pytest.mark.xfail(reason="Phase 1 TODO: decentralised adjacency", strict=True)
def test_neighbours_respect_comm_range():
    obj = make_env()
    obj.reset(seed=1)
    for i, nbrs in enumerate(obj.neighbour_indices()):
        d = np.linalg.norm(obj.positions[nbrs] - obj.positions[i], axis=1)
        assert (d <= obj.config.comm_range_m).all(), "no global knowledge allowed"


@pytest.mark.xfail(reason="Phase 1 TODO: step() with energy logging", strict=True)
def test_step_returns_info_with_energy():
    obj = make_env()
    obj.reset(seed=0)
    _obs, _r, _done, info = obj.step(np.zeros((20, 2)))
    assert "energy_mj_so_far" in info


@pytest.mark.xfail(reason="Phase 1 TODO: disabled drones excluded from dynamics", strict=True)
def test_disabled_drones_do_not_move_or_influence():
    cfg = SwarmConfig(n_drones=20, disable_fraction=0.3, seed=7)
    obj = SwarmEnv(cfg)
    obj.reset()
    dead = np.flatnonzero(~obj.alive)
    obj.step(np.ones((20, 2)))
    assert np.allclose(obj.positions[dead], 0.0) or not obj.alive[dead].any()
