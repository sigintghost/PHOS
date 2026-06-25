# PHOS

Controls-first research into pulsed plasmoid propulsion. Plasma
treated as a black-box dynamic system: probe, measure, recover
hidden dynamics from observed telemetry.

Pure stdlib Python. Runs in iSH on iPhone. No deps.

## Layout
- sims/    forward models and inverse recovery
- models/  reduced-order fits, recovered parameter sets
- data/    current traces, generated datasets
- notes/   research log and roadmap

## Status
Forward PPT discharge model working. Inverse parameter-recovery
loop working on clean simulated traces.

## Discipline
Findings classified: Established / Strong / Emerging / Speculative.
Simulation is not reality. A working toy is not a validated model.
