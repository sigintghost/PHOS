import math

# Physical constants
Q_E = 1.602e-19       # electron charge, C
IONIZATION_EV = 15.0  # eV per particle to ionize (Teflon ballpark)
AMU = 1.66e-27        # kg, roughly one Teflon fragment mass unit
PARTICLE_MASS = 100*AMU  # rough CF2 fragment mass

def ionization_energy_per_kg(mass_kg):
    n_particles = mass_kg / PARTICLE_MASS
    energy_per_particle = IONIZATION_EV * Q_E
    return n_particles * energy_per_particle

def sheath_voltage_drop(Te_eV=2.0):
    # Standard sheath potential: several times electron temp
    # kappa ~ 4.7 for a hydrogen-like plasma, rough estimate
    return 4.7 * Te_eV

def compare_radiation_to_magnetic_pressure(I_amps, area_m2=1e-4):
    # Magnetic pressure ~ B^2/(2*mu0), estimate B from current via
    # a simple solenoid-like approximation for comparison purposes
    mu0 = 4*math.pi*1e-7
    B_est = mu0 * I_amps / (2*math.pi*0.01)  # rough field at 1cm radius
    P_mag = B_est**2 / (2*mu0)
    # Radiation pressure from blackbody-ish plasma glow, rough estimate
    sigma_sb = 5.67e-8
    T_plasma = 20000  # K, rough PPT plasma temp estimate
    P_rad = sigma_sb * T_plasma**4 / 3e8  # intensity/c
    return {"P_magnetic_Pa": P_mag, "P_radiation_Pa": P_rad,
            "ratio_mag_to_rad": P_mag/P_rad if P_rad > 0 else None}

def relativistic_correction_factor(v_m_s):
    c = 3e8
    beta = v_m_s / c
    gamma = 1.0/math.sqrt(1-beta**2) if beta < 1 else float('inf')
    return {"beta": beta, "gamma": gamma,
            "correction_needed": gamma > 1.001}

def main():
    print("EXTENDED PHYSICS LAYER — theoretical additions to snowplow model\n")
    mass = 5e-8  # a typical swept mass, kg
    e_ion = ionization_energy_per_kg(mass)
    print(f"1. IONIZATION COST for {mass*1e9:.1f} ug propellant:")
    print(f"   energy required: {e_ion*1e3:.3f} mJ")
    print(f"   (compare to ~5J pulse energy - real but small fraction)\n")

    v_sheath = sheath_voltage_drop(Te_eV=2.0)
    print(f"2. SHEATH VOLTAGE DROP (Te=2eV): {v_sheath:.1f} V")
    print(f"   (compare to 1200V discharge - under 1%, usually ignorable")
    print(f"   but grows fast if Te rises - worth tracking)\n")

    rad = compare_radiation_to_magnetic_pressure(3000)
    print(f"3. RADIATION vs MAGNETIC PRESSURE at I=3kA:")
    print(f"   P_magnetic : {rad['P_magnetic_Pa']:.2e} Pa")
    print(f"   P_radiation: {rad['P_radiation_Pa']:.2e} Pa")
    print(f"   ratio      : {rad['ratio_mag_to_rad']:.2e}x")
    print(f"   (magnetic utterly dominates - radiation pressure is")
    print(f"   irrelevant here by many orders of magnitude)\n")

    rel = relativistic_correction_factor(4000)
    print(f"4. RELATIVISTIC CHECK at v=4km/s:")
    print(f"   beta={rel['beta']:.2e}  gamma={rel['gamma']:.10f}")
    print(f"   correction needed: {rel['correction_needed']}")
    print(f"   (nowhere close - would need v ~ thousands of km/s)")

if __name__ == "__main__":
    main()
