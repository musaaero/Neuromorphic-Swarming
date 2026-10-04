"""Phase 1 — STDP acceptance tests (see ROADMAP.md)."""
import numpy as np
import pytest

from neuromorphic_swarming.plasticity import STDPRule


def make_rule():
    """Factory (not a fixture) so xfail-marked tests can use it under pytest >= 9."""
    return STDPRule(n_pre=4, n_post=4, w_min=0.0, w_max=1.0)


@pytest.mark.xfail(reason="Phase 1 TODO: implement STDPRule.inject", strict=True)
def test_causal_pair_strengthens():
    obj = make_rule()
    before = obj.W[0, 1].copy()
    obj.inject(pre_idx=0, post_idx=1, dt=+5.0)   # pre fires 5ms BEFORE post -> LTP
    assert obj.W[0, 1] > before


@pytest.mark.xfail(reason="Phase 1 TODO: implement STDPRule.inject", strict=True)
def test_acyclic_pair_weaken():
    obj = make_rule()
    before = obj.W[0, 1].copy()
    obj.inject(pre_idx=0, post_idx=1, dt=-5.0)   # anti-causal -> LTD
    assert obj.W[0, 1] < before


@pytest.mark.xfail(reason="Phase 1 TODO: implement STDPRule.update", strict=True)
def test_weights_stay_bounded():
    obj = make_rule()
    rng = np.random.default_rng(1)
    for t in range(5000):
        obj.update(rng.random(4) > 0.7, rng.random(4) > 0.7, t)
    assert obj.W.min() >= obj.w_min and obj.W.max() <= obj.w_max


@pytest.mark.xfail(reason="Phase 1 TODO: adjacency-mask support in update()", strict=True)
def test_mask_blocks_plasticity_on_absent_edges():
    obj = make_rule()
    mask = np.zeros((4, 4), dtype=bool)  # no edges exist this tick
    before = obj.W.copy()
    obj.update(np.array([1, 0, 1, 0], bool), np.array([0, 1, 0, 1], bool), t=10,
                adjacency_mask=mask)
    assert np.array_equal(obj.W, before), "masked synapses must not change"
