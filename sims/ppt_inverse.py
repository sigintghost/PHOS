
import math, random

def run_ppt(Lp, m0, C=2.0e-6, L0=30.0e-9, V0=1500.0):
    dt, t_end = 1.0e-9, 4.0e-6
    q, i, x, v, t = C*V0, 0.0, 1.0e-4, 0.0, 0.0
    trace = []
    while t < t_end:
        Ltot = L0 + Lp*x
        di = (q/C - Lp*v*i)/Ltot*dt
        q -= i*dt
        M = m0*x + 1.0e-9
        v += (0.5*Lp*i*i - v*(m0*v))/M*dt
        i += di; x += v*dt; t += dt
        trace.append(i)
    return trace

TRUE_Lp, TRUE_m0 = 0.40e-6, 1.0e-6
truth = run_ppt(TRUE_Lp, TRUE_m0)

def add_noise(trace, pct=0.03):
    return [v + random.gauss(0, pct*12000) for v in trace]

measured = add_noise(truth)
print(f"trace length: {len(measured)} samples")
print(f"hidden truth we must recover: Lp={TRUE_Lp:.2e}, m0={TRUE_m0:.2e}")

def error(trace_a, trace_b):
    n = min(len(trace_a), len(trace_b))
    s = 0.0
    for k in range(0, n, 20):
        d = trace_a[k] - trace_b[k]
        s += d*d
    return s

def score(Lp, m0):
    guess = run_ppt(Lp, m0)
    return error(guess, measured)

print("score at truth: ", f"{score(TRUE_Lp, TRUE_m0):.3e}")
print("score at wrong: ", f"{score(0.80e-6, 2.0e-6):.3e}")

best, best_err = None, 1e99
Lp_grid = [0.20e-6, 0.30e-6, 0.40e-6, 0.50e-6, 0.60e-6]
m0_grid = [0.5e-6, 0.8e-6, 1.0e-6, 1.3e-6, 1.6e-6]
for Lp in Lp_grid:
    for m0 in m0_grid:
        e = score(Lp, m0)
        if e < best_err:
            best_err, best = e, (Lp, m0)
print(f"recovered: Lp={best[0]:.2e}, m0={best[1]:.2e}")

print("\n--- RESULT ---")
print(f"truth:     Lp={TRUE_Lp:.2e}  m0={TRUE_m0:.2e}")
print(f"recovered: Lp={best[0]:.2e}  m0={best[1]:.2e}")
hit = (abs(best[0]-TRUE_Lp)/TRUE_Lp < 0.3 and
       abs(best[1]-TRUE_m0)/TRUE_m0 < 0.3)
print("LOOP WORKS" if hit else "missed - needs finer grid")
