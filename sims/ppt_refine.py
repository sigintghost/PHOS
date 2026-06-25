import random

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

TRUE_Lp, TRUE_m0 = 0.43e-6, 1.15e-6
truth = run_ppt(TRUE_Lp, TRUE_m0)
measured = [v + random.gauss(0, 0.03*12000) for v in truth]

def score(Lp, m0):
    g = run_ppt(Lp, m0)
    n = min(len(g), len(measured))
    return sum((g[k]-measured[k])**2 for k in range(0, n, 20))

def search(lo_Lp, hi_Lp, lo_m0, hi_m0, n=6):
    best, be = None, 1e99
    for a in range(n):
        Lp = lo_Lp + (hi_Lp-lo_Lp)*a/(n-1)
        for b in range(n):
            m0 = lo_m0 + (hi_m0-lo_m0)*b/(n-1)
            e = score(Lp, m0)
            if e < be:
                be, best = e, (Lp, m0)
    return best, be

c, ce = search(0.20e-6, 0.70e-6, 0.5e-6, 1.8e-6)
print(f"coarse: Lp={c[0]:.3e} m0={c[1]:.3e} err={ce:.2e}")

span_Lp, span_m0 = 0.10e-6, 0.30e-6
f, fe = search(c[0]-span_Lp, c[0]+span_Lp,
               c[1]-span_m0, c[1]+span_m0, n=8)
print(f"fine:   Lp={f[0]:.3e} m0={f[1]:.3e} err={fe:.2e}")

print("\n--- RESULT ---")
print(f"truth:     Lp={TRUE_Lp:.3e}  m0={TRUE_m0:.3e}")
print(f"recovered: Lp={f[0]:.3e}  m0={f[1]:.3e}")
eLp = abs(f[0]-TRUE_Lp)/TRUE_Lp*100
em0 = abs(f[1]-TRUE_m0)/TRUE_m0*100
print(f"error: Lp {eLp:.1f}%  m0 {em0:.1f}%")
print("CONVERGED" if eLp<5 and em0<5 else "needs another pass")
