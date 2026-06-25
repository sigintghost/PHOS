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
        tr.append((i, x))
    return tr

TRUE_Lp, TRUE_m0 = 0.43e-6, 1.15e-6
truth = run_ppt(TRUE_Lp, TRUE_m0)
meas_i = [s[0] + random.gauss(0, 0.03*12000) for s in truth]
meas_x = [s[1] + random.gauss(0, 0.03*0.003) for s in truth]

def score(Lp, m0, use_x):
    g = run_ppt(Lp, m0)
    n = min(len(g), len(meas_i))
    e = sum((g[k][0]-meas_i[k])**2 for k in range(0, n, 20))
    if use_x:
        ex = sum((g[k][1]-meas_x[k])**2 for k in range(0, n, 20))
        e += ex * 1.0e14
    return e

def surface(use_x):
    N = 15
    Lp_lo, Lp_hi = 0.25e-6, 0.65e-6
    m0_lo, m0_hi = 0.5e-6, 1.8e-6
    g, emin, emax = [], 1e99, 0
    for r in range(N):
        Lp = Lp_lo + (Lp_hi-Lp_lo)*r/(N-1)
        row = []
        for c in range(N):
            m0 = m0_lo + (m0_hi-m0_lo)*c/(N-1)
            e = score(Lp, m0, use_x)
            row.append(e); emin = min(emin,e); emax = max(emax,e)
        g.append(row)
    ramp = " .:-=+*#%@"
    for row in g:
        print("".join(ramp[int((e-emin)/(emax-emin+1e-9)*9)] for e in row))

print("SENSOR 1 ONLY (current):\n")
surface(False)
print("\nSENSOR 1 + POSITION (current + sheet position):\n")
surface(True)
print("\nrows=Lp  cols=m0  dark=good fit")
print("position is optical, independent of current.")
