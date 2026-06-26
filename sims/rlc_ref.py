import math

# Analytic underdamped series-RLC discharge. Closed-form decaying
# sinusoid - cannot numerically blow up because nothing is integrated.
# i(t) = (V0/(L*wd)) * exp(-alpha t) * sin(wd t)
def rlc_discharge(C, L, R, V0, dt=2e-9, tEnd=8e-6):
    alpha = R/(2*L)
    w0 = 1.0/math.sqrt(L*C)
    if alpha >= w0:
        return None, "overdamped - no ring"
    wd = math.sqrt(w0*w0 - alpha*alpha)
    I = []
    t = 0.0
    while t < tEnd:
        i = (V0/(L*wd))*math.exp(-alpha*t)*math.sin(wd*t)
        I.append(i)
        t += dt
    return I, None

def analyze(I, dt=2e-9):
    peak = max(abs(v) for v in I)
    crossings = []
    for k in range(1, len(I)):
        if I[k-1] <= 0 < I[k] or I[k-1] >= 0 > I[k]:
            crossings.append(k)
        if len(crossings) >= 3:
            break
    freq = None
    if len(crossings) >= 2:
        freq = 1.0/(2*(crossings[1]-crossings[0])*dt)
    return {"peak_kA": peak/1000, "ring_kHz": (freq/1000 if freq else None)}

def main():
    C, L, R, V0 = 2.0e-6, 30e-9, 0.15, 1200.0
    I, err = rlc_discharge(C, L, R, V0)
    if err:
        print("RLC:", err); return
    res = analyze(I)
    f_theory = 1.0/(2*math.pi*math.sqrt(L*C))
    rk = res['ring_kHz']
    print("RLC reference discharge (analytic, literature rig values)")
    print(f"  C={C*1e6}uF  L={L*1e9:.0f}nH  R={R}ohm  V0={V0}V")
    print(f"  peak current : {res['peak_kA']:.2f} kA")
    print(f"  ring freq    : {rk:.1f} kHz (measured)" if rk else "  ring freq    : none")
    print(f"  theory freq  : {f_theory/1000:.1f} kHz")
    print(f"  real PPT band: peak ~1-5 kA, ring ~100s kHz")

if __name__ == "__main__":
    main()
