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

## Real-data targets (for eventual fitting)
- Low discharge energy PPT, 3.16 kA at 800-1400V, up to 4.41 J.
  Published current waveform, fittable.
- Modified PPT, graphite/tungsten, current+voltage matched to
  RLC with variable plasma resistance. Same physics as our model.
- ASCENT liquid-fed PPT, 380uF at 400V ~30J, fast-camera images
  synced to waveform = current AND position on same shot.
- Phase matters: solid (Teflon ablation, skips gas), liquid-fed
  (flash-ionized), each a different m0 process.
