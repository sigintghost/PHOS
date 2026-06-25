import random

def run_ppt(Lp, kab, C=2.0e-6, L0=30.0e-9, V0=1500.0):
    dt, t_end = 1.0e-9, 4.0e-6
    q, i, x, v, t = C*V0, 0.0, 1.0e-4, 0.0, 0.0
    mass = 1.0e-9
    tr = []
    while t < t_end:
        Ltot = L0 + Lp*x
        R = 0.01 + 8.0e6 * mass
        di = (q/C - Lp*v*i - R*i)/Ltot*dt
        q -= i*dt
        dm = kab * i*i * dt
        mass += dm
        v += (0.5*Lp*i*i - v*dm/dt) / mass * dt
        i += di; x += v*dt; t += dt
        tr.append(i)
    return tr

TRUE_Lp, TRUE_kab = 0.43e-6, 2.0e-18
truth = run_ppt(TRUE_Lp, TRUE_kab)
meas_i = [v + random.gauss(0, 0.03*12000) for v in truth]

def score(Lp, kab):
    g = run_ppt(Lp, kab)
    n = min(len(g), len(meas_i))
    return sum((g[k]-meas_i[k])**2 for k in range(0, n, 20))

def surface():
    N = 15
    Lp_lo, Lp_hi = 0.25e-6, 0.65e-6
    k_lo, k_hi = 0.8e-18, 4.0e-18
    g, emin, emax = [], 1e99, 0
    for r in range(N):
        Lp = Lp_lo + (Lp_hi-Lp_lo)*r/(N-1)
        row = []
        for c in range(N):
            kab = k_lo + (k_hi-k_lo)*c/(N-1)
            e = score(Lp, kab)
            row.append(e); emin=min(emin,e); emax=max(emax,e)
        g.append(row)
    ramp = " .:-=+*#%@"
    for row in g:
        print("".join(ramp[int((e-emin)/(emax-emin+1e-9)*9)] for e in row))

print("CURRENT ONLY, with resistance feedback:\n")
surface()
print("\nrows=Lp  cols=kab  dark=good fit")
print("if kab now couples into current, bands break.")
