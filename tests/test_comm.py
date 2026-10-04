"""Phase 1 — communication channel acceptance tests (see ROADMAP.md)."""
import numpy as np
import pytest

from neuromorphic_swarming.comm import SpikeChannel


@pytest.mark.xfail(reason="Phase 1 TODO: implement SpikeChannel.transmit", strict=True)
def test_deterministic_given_seed():
    ch_args = {"range_m": 30.0, "drop_p": 0.2, "jitter": 1, "seed": 7}
    spikes = np.array([True, False, True])
    pos = np.array([[0.0, 0.0], [10.0, 0.0], [100.0, 100.0]])
    recv = np.arange(3)
    a = SpikeChannel(**ch_args).transmit(spikes, pos, recv)
    b = SpikeChannel(**ch_args).transmit(spikes, pos, recv)
    assert np.array_equal(a, b)


@pytest.mark.xfail(reason="Phase 1 TODO: out-of-range spikes must be dropped", strict=True)
def test_out_of_range_never_delivered():
    ch = SpikeChannel(range_m=30.0, drop_p=0.0, jitter=0, seed=3)
    spikes = np.array([True])
    pos = np.array([[0.0, 0.0], [500.0, 0.0]])
    delivered = ch.transmit(spikes, pos, receiver_idx=np.array([1]))
    # sender 0 is 500 m away from receiver 1 -> nothing should arrive from it
    assert delivered.sum() == 0 or not delivered.any()


@pytest.mark.xfail(reason="Phase 1 TODO: drop-rate convergence test", strict=True)
def test_drop_rate_converges():
    ch = SpikeChannel(range_m=1e9, drop_p=0.3, jitter=0, seed=11)
    pos = np.zeros((1, 2))
    sent = arrived = 0
    for _ in range(2000):
        out = ch.transmit(np.array([True]), pos, receiver_idx=np.array([0]))
        sent += 1
        arrived += int(out.any())
    assert abs(1 - arrived / sent - 0.3) < 0.05
