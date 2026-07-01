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

## OPEN BACKLOG (designed, not built)
- THUMMIM: adversarial critic agent, attacks URIM conclusions, toggle
- RLC reference model: real rig values, validated discharge eqn (BUILDING)
- Spectral diagnostic layer (GPT): reads traces, reports freq/decay/residual,
  never alters physics. Kill H0 before calling anything a plasma mode.
- Driven/resonance sandbox: tagged modes baseline_lc/driven_test/raw,
  full provenance logging. Separate branch, never hidden in ppt_sim.
- Hypothesis ladder H0-H4 as governing discipline for all resonance claims
- Real published trace ingestion via digitizing (WebPlotDigitizer path)
- Sandbox sweep mode: auto-run one variable across a range
- URIM: route cheap tasks to sonnet/haiku, opus for heavy synthesis

## STATUS UPDATE (day 2)
DONE: RLC reference built + validated (4.84 kA, 514 kHz, matches theory).
DONE: URIM orchestrator live, 3 runs, explore + physics modes working.
DONE: URIM cross-referenced model vs AF-MPD literature (Jahn, Burton/Turchi).
FINDING: b=1.8 hotspot cluster is a grid/metric artifact, flagged 3x.
NOW BUILDING: THUMMIM adversarial critic.

## STATUS UPDATE (day 3)
DONE: THUMMIM live. First run caught URIM citation inflation
(AF-MPD literature misapplied to snowplow model) and L-prime vs
L0 misattribution. Self-audit loop confirmed working.
DONE: First real-data fit. RLC model fit to PuLSA paper (published,
not synthetic): target 1200V/3.16kA/100kHz. Result: 99.3kHz ring
(near exact), 3.92kA peak (24% high). sims/rlc_fit.py.
NEXT: finer fit grid to close the peak-current gap. Feed real
PuLSA numbers to URIM directly (physics mode) - not done yet.

## STATUS UPDATE (day 3, cont.)
DONE: Spectral diagnostic layer built (sims/spectral.py). H0 test:
does baseline LC model fully explain a trace, or is there residual?
First run: crude fit showed 31% residual (looked like H1). Diagnosed
as a fitter bug via real-vs-baseline comparison, not physics - found
a 2.5x amplitude scaling error. Fixed with proper least-squares
amplitude fit. Correct result: 0.00% residual. H0 HOLDS - the RLC
model is exactly a damped sinusoid, nothing hidden. This validates
the diagnostic tool itself: it can correctly report a clean null.
