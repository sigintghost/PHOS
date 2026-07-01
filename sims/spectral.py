import math

def dominant_freq(I, dt):
    # zero-crossing method: robust, no FFT library needed
    crossings = []
    for k in range(1, len(I)):
        if I[k-1] <= 0 < I[k] or I[k-1] >= 0 > I[k]:
            crossings.append(k)
    if len(crossings) < 3:
        return None
    periods = [(crossings[i+1]-crossings[i])*dt*2
               for i in range(len(crossings)-1)]
    avg_period = sum(periods)/len(periods)
    return 1.0/avg_period if avg_period > 0 else None

def decay_rate(I, dt):
    n = len(I)
    window = max(n//40, 5)
    envelope = []
    for k in range(0, n-window, window):
        seg = [abs(v) for v in I[k:k+window]]
        envelope.append((k*dt, max(seg)))
    envelope = [(t,v) for t,v in envelope if v > 0]
    if len(envelope) < 3:
        return None
    xs = [t for t,v in envelope]
    ys = [math.log(v) for t,v in envelope]
    n2 = len(xs)
    mx = sum(xs)/n2; my = sum(ys)/n2
    num = sum((xs[i]-mx)*(ys[i]-my) for i in range(n2))
    den = sum((xs[i]-mx)**2 for i in range(n2))
    if den == 0:
        return None
    slope = num/den
    return -slope

def baseline_fit(I, dt):
    freq = dominant_freq(I, dt)
    alpha = decay_rate(I, dt)
    if freq is None or alpha is None:
        return None, None, "H0 test failed: no clean oscillation found"
    shape = []
    t = 0.0
    for k in range(len(I)):
        shape.append(math.exp(-alpha*t)*math.sin(2*math.pi*freq*t))
        t += dt
    num = sum(I[k]*shape[k] for k in range(len(I)))
    den = sum(shape[k]*shape[k] for k in range(len(I)))
    scale = num/den if den != 0 else 0
    baseline = [scale*s for s in shape]
    residual = [I[k]-baseline[k] for k in range(len(I))]
    return baseline, residual, None

def h0_test(I, dt, label="trace"):
    baseline, residual, err = baseline_fit(I, dt)
    if err:
        print(f"  {label}: {err}")
        return
    sig_energy = sum(v*v for v in I)
    res_energy = sum(v*v for v in residual)
    frac = res_energy/sig_energy if sig_energy > 0 else 0
    freq = dominant_freq(I, dt)
    alpha = decay_rate(I, dt)
    print(f"  {label}")
    print(f"    fitted freq  : {freq/1000:.1f} kHz")
    print(f"    fitted decay : {alpha:.2e} /s")
    print(f"    residual energy fraction: {frac*100:.2f}%")
    verdict = "H0 HOLDS - baseline explains signal" if frac < 0.05 \
        else "H1 CANDIDATE - repeatable residual remains, needs more tests"
    print(f"    -> {verdict}")

if __name__ == "__main__":
    from rlc_ref import rlc_discharge
    I, err = rlc_discharge(2.0e-6, 30e-9, 0.15, 1200.0)
    if not err:
        h0_test(I, 2e-9, "RLC reference trace")
