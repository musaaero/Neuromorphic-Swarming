"""Phase 1 — spike encoding acceptance tests (see ROADMAP.md)."""
import numpy as np
import pytest

from neuromorphic_swarming.encoding import decode_latency, latency_encode, rate_encode


@pytest.mark.xfail(reason="Phase 1 TODO: implement rate_encode", strict=True)
def test_rate_encode_monotonic_and_shaped():
    vals = np.linspace(0.0, 1.0, 32)
    spikes = rate_encode(vals, n_timesteps=10_000, max_rate_hz=100.0, rng=np.random.default_rng(0))
    assert spikes.shape == (32, 10_000)
    counts = spikes.sum(axis=1)
    assert (np.diff(counts) >= -counts.std() * 0.1).all(), "firing rate must grow with value"


@pytest.mark.xfail(reason="Phase 1 TODO: implement latency_encode/decode", strict=True)
def test_latency_roundtrip_is_order_preserving():
    vals = np.array([0.1, 0.9, 0.5, 0.3, 0.7])
    spikes = latency_encode(vals, n_timesteps=100)
    assert spikes.sum(axis=1).max() <= 1, "first-spike code: at most one spike per neuron"
    recovered = decode_latency(spikes, n_timesteps=100)
    assert np.all(np.argsort(recovered) == np.argsort(vals)), "ordering must survive coding"
    assert np.allclose(recovered, vals, atol=0.02)
