import sys, json, time
sys.path.insert(0, 'agents')
sys.path.insert(0, 'sims')
from progress import bar
from spectral import h0_test, dominant_freq, decay_rate, baseline_fit

def run_ppt_R(Lp, m0, B, R=0.15, C=2.0e-6, L0=30e-9, V0=1200.0):
    dt, tEnd = 1e-9, 4e-6
    q=C*V0; i=0.0; x=1e-4; v=0.0; t=0.0
    I=[]
    while t < tEnd:
        Ltot=L0+Lp*x
        di=(q/C - R*i - Lp*v*i)/Ltot*dt
        q-=i*dt
        M=m0*x+1e-9
        v+=(0.5*Lp*i*i + B*i*0.02 - v*(m0*v))/M*dt
        i+=di; x+=v*dt; t+=dt
        I.append(i)
    return I

def main():
    Lp_vals = [0.10e-6, 0.32e-6, 0.55e-6, 0.77e-6, 1.00e-6]
    m0_vals = [0.5e-6, 0.87e-6, 1.25e-6, 1.62e-6, 2.0e-6]
    B_vals  = [0.0, 0.5, 1.0, 1.5, 2.0]
    total = len(Lp_vals)*len(m0_vals)*len(B_vals)
    results = []
    n = 0
    t0 = time.time()
    for Lp in Lp_vals:
        for m0 in m0_vals:
            for B in B_vals:
                I = run_ppt_R(Lp, m0, B)
                baseline, residual, err = baseline_fit(I, 1e-9)
                if not err:
                    sig_e = sum(v*v for v in I)
                    res_e = sum(v*v for v in residual)
                    frac = res_e/sig_e if sig_e > 0 else 0
                else:
                    frac = None
                results.append({"Lp": Lp, "m0": m0, "B": B,
                                 "residual_pct": frac*100 if frac is not None else None})
                n += 1
                bar(n, total, "grid3d")
    bar(total, total, "grid3d")
    elapsed = time.time() - t0
    print(f"\\n  {total} points in {elapsed:.0f}s")
    with open("data/grid3d_results.json", "w") as f:
        json.dump({"sweep": "Lp x m0 x B, R=0.15 fixed",
                    "results": results}, f, indent=1)
    print("  saved -> data/grid3d_results.json")

if __name__ == "__main__":
    main()
