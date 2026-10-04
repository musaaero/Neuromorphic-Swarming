# Energy Model Sources (fill in before Phase 2 publishes anything)

Constants live in `src/neuromorphic_swarming/energy.py`. Each needs a citable source here;
placeholders until verified against primary literature/datasheets:

| Constant | Current value | Source status | Candidate references to verify |
|---|---|---|---|
| `SYNAPTIC_OP_MJ` | 3.0e-6 mJ/syn-event | ⚠️ placeholder | Loihi 2 public talks/datasheet; Davies et al. 2018 (Loihi 1, ~pJ-scale synaptic ops) |
| `NEURON_UPDATE_MJ` | 0.5e-6 mJ/update | ⚠️ placeholder | same |
| `SPIKE_TX_MJ` | 100e-3 mJ/packet | ⚠️ placeholder — **dominant cost**, measure properly | WiFi/802.15.4 per-packet energy literature; drone telemetry measurements |
| `SENSOR_EVENT_MJ` | 5e-3 mJ/event | ⚠️ placeholder | DAVIS346 power figures (iniVation docs); de Croon et al. 2021 |

Rules:
1. No benchmark result ships while any constant is unverified.
2. When you replace a placeholder, cite DOI/link + date checked + the exact figure quoted.
3. Sensitivity analysis: rerun e01 with constants ±1 order of magnitude; report whether the
   SNN-vs-centralized ranking survives. (If it doesn't, that IS the finding.)
