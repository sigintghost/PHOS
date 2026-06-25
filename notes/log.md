# PHOS Research Log

## Entry 1 - forward PPT model
Snowplow model of a pulsed plasma thruster. Current peaks ~12 kA,
sheet reaches ~4 km/s. Real PPT ballpark without tuning.

## Entry 2 - inverse recovery loop
Hid two parameters, generated a noisy current trace, recovered
them from the trace alone via grid search. Recovered exact truth.
System identification on a black-box thruster. Works on clean
simulated data only.

## Next
Fine search plus off-grid truth. Then add a third hidden parameter.
