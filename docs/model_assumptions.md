# Model and measurement assumptions

Record decisions here before using them in reported experiments. Every
assumption should have a rationale, a test or sensitivity analysis where
possible, and a note describing which conclusions it limits.

## Environment and dynamics

- Coordinate system and units: TODO
- State and update equations: TODO
- Time step and integration method: TODO
- Speed/acceleration limits: TODO
- Boundary and episode termination rules: TODO
- Target motion model: TODO
- Obstacle geometry and collision margin: TODO

## Observation and communication

- What each agent observes: TODO
- Sensing range/noise/update rate: TODO
- Neighbor discovery and message contents: TODO
- Communication range, latency, drop assumptions, and accounting: TODO
- Which information is unavailable to decentralized controllers: TODO

## Energy accounting

Keep estimated/proxy terms separate from measured quantities.

| Term | Formula or measurement method | Units | Coefficients/source | Limitations |
|---|---|---|---|---|
| Motion/propulsion proxy | TODO | TODO | TODO | Not aircraft power unless validated |
| Sensing | TODO | TODO | TODO | TODO |
| Communication | TODO | TODO | TODO | TODO |
| Controller computation | TODO | TODO | TODO | Distinguish proxy from measured device energy |
| Total | TODO | TODO | TODO | State included/excluded components |

## Validation and change log

| Date | Assumption checked or changed | Evidence | Consequence |
|---|---|---|---|
| TODO | TODO | TODO | TODO |
