# Paper claim ledger

The paper's numbers are hypotheses to investigate, not results reproduced by
this repository. Fill in exact page/section references from the PDF.

| Claim | Exact paper location | Operational definition | Baseline/comparison | Required evidence | Status |
|---|---|---|---|---|---|
| 60% energy reduction | TODO | Define which energy terms are included and over what workload | TODO | State measurement boundary, method, hardware, seeds, and uncertainty | Not tested |
| 100-drone scalability | TODO | Define task success, runtime, and resource limits at each swarm size | TODO | Scaling curve and failure/runtime records | Not tested |
| 30% node-loss robustness | TODO | Define failed-node fraction, timing, and recovery/success metric | TODO | Reproducible failure schedule and multi-seed results | Not tested |

## Status vocabulary

- **Not tested:** no relevant experiment has been run.
- **Partially supported:** a narrower or assumption-dependent version was tested.
- **Reproduced under stated assumptions:** the specified setup and metric were
  independently implemented and evaluated; this does not imply general validity.
- **Not reproduced:** an adequate attempt did not support the stated claim.

For every update, include a link to the relevant configuration, result record,
and analysis. Never mark a claim reproduced from a simulation proxy if the
original claim is about measured hardware energy.
