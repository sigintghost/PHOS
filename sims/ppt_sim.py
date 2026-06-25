
import math
C   = 2.0e-6
L0  = 30.0e-9
V0  = 1500.0
Lp  = 0.40e-6
m0  = 1.0e-6
w   = 0.05
dt  = 1.0e-9
t_end = 4.0e-6
q  = C * V0
i  = 0.0
x  = 1.0e-4
v  = 0.0
t  = 0.0
log = []
def swept_mass(x):
    return m0 * x + 1.0e-9
def inductance(x):
    return L0 + Lp * x
def step(q, i, x, v):
    Ltot = inductance(x)
    di = (q / C - Lp * v * i) / Ltot * dt
    dq = -i * dt
    M  = swept_mass(x)
    F  = 0.5 * Lp * i * i
    dv = (F - v * (m0 * v)) / M * dt
    return q + dq, i + di, x + v * dt, v + dv
while t < t_end:
    q, i, x, v = step(q, i, x, v)
    if int(t / dt) % 50 == 0:
        log.append((t * 1e6, i, x * 1000, v))
    t += dt
print("t(us)  I(A)     x(mm)   v(m/s)")
for r in log[:20]:
    print(f"{r[0]:5.2f} {r[1]:8.0f} {r[2]:6.2f} {r[3]:7.0f}")
peakI = max(abs(r[1]) for r in log)
print(f"\npeak current ~ {peakI:.0f} A, exit v ~ {log[-1][3]:.0f} m/s")

