"""Phase 1 — energy accounting acceptance tests (see ROADMAP.md)."""
import pytest

from neuromorphic_swarming import energy


@pytest.mark.xfail(reason="Phase 1 TODO: implement EnergyLedger.record_tick/total_mj", strict=True)
def test_ledger_sums_components():
    led = energy.EnergyLedger(n_agents=2)
    led.record_tick(n_syn_ops=100, n_neuron_updates=200, n_spikes_tx=10, n_sensor_events=50)
    expected = (100 * energy.SYNAPTIC_OP_MJ + 200 * energy.NEURON_UPDATE_MJ
                + 10 * energy.SPIKE_TX_MJ + 50 * energy.SENSOR_EVENT_MJ)
    assert led.total_mj == pytest.approx(expected)


@pytest.mark.xfail(reason="Phase 1 TODO: summary() dict", strict=True)
def test_summary_reports_dominant_cost():
    led = energy.EnergyLedger(n_agents=2)
    led.record_tick(n_syn_ops=100, n_neuron_updates=200, n_spikes_tx=10, n_sensor_events=50)
    s = led.summary()
    assert "dominant_cost" in s and s["dominant_cost"] == "spike_tx"


@pytest.mark.xfail(reason="Phase 4 TODO: battery_ode (aero bridge)", strict=True)
def test_battery_endurence_order_of_magnitude():
    # 250 g quad, ~80 W hover, 2000 mAh @ 11.1 V -> roughly tens of minutes
    mins = energy.battery_ode(mass_kg=0.25, rotor_power_w=80.0, compute_mw=500.0,
                              capacity_mah=2000.0)
    assert 5.0 < mins < 60.0
