import random

def run_ppt(Lp, m0, C=2.0e-6, L0=30.0e-9, V0=1500.0):
    dt, t_end = 1.0e-9, 4.0e-6
    q, i, x, v, t = C*V0, 0.0, 1.0e-4, 0.0, 0.0
    tr = []
    while t < t_end:
        Ltot = L0 + Lp*x
        di = (q/C - Lp*v*i)/Ltot*dt
        q -= i*dt
        M = m0*x + 1.0e-9
        v += (0.5*Lp*i*i - v*(m0*v))/M*dt
        i += di; x += v*dt; t += dt
        tr.append(i)
    return tr

TRUE_Lp, TRUE_m0 = 0.43e-6, 1.15e-6
truth = run_ppt(TRUE_Lp, TRUE_m0)
meas = [v + random.gauss(0, 0.03*12000) for v in truth]

def score(Lp, m0):
    g = run_ppt(Lp, m0)
    n = min(len(g), len(meas))
    return sum((g[k]-meas[k])**2 for k in range(0, n, 20))

N = 15
Lp_lo, Lp_hi = 0.25e-6, 0.65e-6
m0_lo, m0_hi = 0.5e-6, 1.8e-6
grid = []
emin, emax = 1e99, 0
for r in range(N):
    Lp = Lp_lo + (Lp_hi-Lp_lo)*r/(N-1)
    row = []
    for c in range(N):
        m0 = m0_lo + (m0_hi-m0_lo)*c/(N-1)
        e = score(Lp, m0)
        row.append(e)
        emin = min(emin, e); emax = max(emax, e)
    grid.append(row)

ramp = " .:-=+*#%@"
print("rows = Lp (top low, bottom high)")
print("cols = m0 (left low, right high)")
print("dark = good fit, bright = bad fit\n")
for row in grid:
    line = ""
    for e in row:
        f = (e-emin)/(emax-emin+1e-9)
        line += ramp[int(f*(len(ramp)-1))]
    print(line)
print("\ntruth sits near center. look for the dark valley shape.")
