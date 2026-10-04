"""Phase 1 — STDP acceptance tests (see ROADMAP.md)."""
import numpy as np
import pytest

from neuromorphic_swarming.plasticity import STDPRule


@pytest.fixture()
def rule():
    return STDPRule(n_pre=4, n_post=4, w_min=0.0, w_max=1.0)


@pytest.mark.xfail(reason="Phase 1 TODO: implement STDPRule.inject", strict=True)
def test_causal_pair_strengthens(rule):
    before = rule.W[0, 1].copy()
    rule.inject(pre_idx=0, post_idx=1, dt=+5.0)   # pre fires 5ms BEFORE post -> LTP
    assert rule.W[0, 1] > before


@pytest.mark.xfail(reason="Phase 1 TODO: implement STDPRule.inject", strict=True)
def test_acyclic_pair_weaken(rule):
    before = rule.W[0, 1].copy()
    rule.inject(pre_idx=0, post_idx=1, dt=-5.0)   # anti-causal -> LTD
    assert rule.W[0, 1] < before


@pytest.mark.xfail(reason="Phase 1 TODO: implement STDPRule.update", strict=True)
def test_weights_stay_bounded(rule):
    rng = np.random.default_rng(1)
    for t in range(5000):
        rule.update(rng.random(4) > 0.7, rng.random(4) > 0.7, t)
    assert rule.W.min() >= rule.w_min and rule.W.max() <= rule.w_max


@pytest.mark.xfail(reason="Phase 1 TODO: adjacency-mask support in update()", strict=True)
def test_mask_blocks_plasticity_on_absent_edges(rule):
    mask = np.zeros((4, 4), dtype=bool)  # no edges exist this tick
    before = rule.W.copy()
    rule.update(np.array([1, 0, 1, 0], bool), np.array([0, 1, 0, 1], bool), t=10,
                adjacency_mask=mask)
    assert np.array_equal(rule.W, before), "masked synapses must not change"
