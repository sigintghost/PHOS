import math
from agents.progress import bar
from rlc_ref import rlc_discharge, analyze

# REAL published target: PuLSA thruster paper
# V0 800-1400V, peak I up to 3.16 kA, ring ~100 kHz,
# decays 10x by ~5us
TARGET_V0 = 1200.0
TARGET_PEAK_KA = 3.16
TARGET_RING_KHZ = 100.0

def score(C, L, R):
    I, err = rlc_discharge(C, L, R, TARGET_V0)
    if err:
        return 1e12
    res = analyze(I)
    if res['ring_kHz'] is None:
        return 1e12
    dI = res['peak_kA'] - TARGET_PEAK_KA
    dF = res['ring_kHz'] - TARGET_RING_KHZ
    return dI*dI + (dF/10.0)**2

def search():
    best, be = None, 1e18
    C_opts = [0.5e-6, 1.0e-6, 2.0e-6, 4.0e-6, 8.0e-6]
    L_opts = [20e-9, 40e-9, 80e-9, 150e-9, 300e-9]
    R_opts = [0.02, 0.05, 0.1, 0.2, 0.4]
    for C in C_opts:
        for L in L_opts:
            for R in R_opts:
                e = score(C, L, R)
                if e < be:
                    be, best = e, (C, L, R)
    return best, be

def main():
    print("Fitting RLC model to PuLSA paper (real published data)")
    print(f"  target: V0={TARGET_V0}V peak={TARGET_PEAK_KA}kA ring={TARGET_RING_KHZ}kHz\n")
    (C, L, R), err = search()
    I, e2 = rlc_discharge(C, L, R, TARGET_V0)
    res = analyze(I)
    print(f"  best fit: C={C*1e6:.2f}uF L={L*1e9:.0f}nH R={R:.3f}ohm")
    print(f"  model peak : {res['peak_kA']:.2f} kA  (target {TARGET_PEAK_KA})")
    rk = res['ring_kHz']
    print(f"  model ring : {rk:.1f} kHz  (target {TARGET_RING_KHZ})" if rk else "  ring: none")
    print(f"  fit score  : {err:.4f}  (lower is better)")

if __name__ == "__main__":
    main()

def log_fit(C, L, R, res, err, target):
    import json, os, time
    os.makedirs('data', exist_ok=True)
    entry = {"time": time.time(), "target": target,
             "fit": {"C": C, "L": L, "R": R},
             "result": res, "score": err}
    path = "data/fit_log.json"
    log = []
    if os.path.exists(path):
        with open(path) as f:
            log = json.load(f)
    log.append(entry)
    with open(path, 'w') as f:
        json.dump(log, f, indent=1)
