"""Phase 1 — LIF neuron acceptance tests (see ROADMAP.md)."""
import numpy as np
import pytest

from neuromorphic_swarming.neurons import LIFNeuron, LIFParams, PopulationLIF


def test_subthreshold_never_spikes():
    n = LIFNeuron(LIFParams(tau_ms=20.0, dt_ms=1.0, threshold=1.0))
    # Steady-state voltage for constant input I: v_inf = I / (1 - decay)
    # Choose I well below threshold*(1-decay) so v stays subthreshold forever.
    spikes = [n.step(0.01) for _ in range(10_000)]
    assert not any(spikes), "Phase 1: subthreshold input must not elicit spikes"


def test_suprathreshold_fires_repeatedly():
    n = LIFNeuron(LIFParams(tau_ms=20.0, dt_ms=1.0, threshold=1.0))
    spikes = np.array([n.step(0.5) for _ in range(1000)])
    assert spikes.sum() > 10, "Phase 1: suprathreshold input must produce repeated spikes"
    # No two consecutive spikes beyond what refractory allows
    gaps = np.diff(np.flatnonzero(spikes))
    assert (gaps >= n.params.refractory_steps + 1).all()


def test_refractory_suppresses_exactly_n_steps():
    p = LIFParams(tau_ms=20.0, dt_ms=1.0, threshold=0.1, reset=0.0, refractory_steps=3)
    n = LIFNeuron(p)
    assert n.step(1.0)          # fires immediately
    assert not any(n.step(1.0) for _ in range(3)), "refractory must block 3 ticks"
    assert n.step(1.0), "must fire again right after refractory ends"


def test_population_init_works():
    """Constructor must work now; step() is the Phase 1 TODO."""
    p = LIFParams(tau_ms=20.0, dt_ms=1.0, threshold=1.0, refractory_steps=2)
    pop = PopulationLIF(64, p)
    assert pop.v.shape == (64,) and pop._refractory.shape == (64,)


@pytest.mark.xfail(reason="Phase 1 TODO: vectorise PopulationLIF.step", strict=True)
def test_population_step_exists():
    import inspect
    src = inspect.getsource(PopulationLIF.step)
    assert "NotImplementedError" not in src, "still a stub"


@pytest.mark.xfail(reason="Phase 1 TODO: vectorise PopulationLIF.step", strict=True)
def test_population_matches_scalar_reference():
    p = LIFParams(tau_ms=20.0, dt_ms=1.0, threshold=1.0, refractory_steps=2)
    rng = np.random.default_rng(42)
    currents = rng.uniform(0.0, 0.6, size=(64, 500))
    pop = PopulationLIF(64, p)
    ref = [LIFNeuron(p) for _ in range(64)]
    for t in range(500):
        got = pop.step(currents[:, t])
        want = np.array([ref[i].step(currents[i, t]) for i in range(64)])
        assert np.array_equal(got, want), f"mismatch at t={t}"
