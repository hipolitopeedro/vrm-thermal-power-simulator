#!/usr/bin/env python3
"""
llc_vdroop_transient_sim.py
EN: Simulates Load-Line Calibration (LLC) settings during a transient CPU load step (Idle -> Full AVX
    -> Idle), computing steady-state Vdroop, transient voltage undershoot, and load-release overshoot.
PT: Simula diferentes níveis de Load-Line Calibration (LLC) durante saltos transientes de corrente,
    calculando Vdroop estacionário, undershoot na entrada de carga e overshoot na saída de carga.
"""

import argparse

LLC_PROFILES = [
    {"name": "Normal / Standard (Intel/AMD Spec)", "r_ll_mohm": 1.15, "transient_k": 0.45},
    {"name": "Medium / Regular", "r_ll_mohm": 0.80, "transient_k": 0.55},
    {"name": "High / Turbo (Recommended Daily OC)", "r_ll_mohm": 0.45, "transient_k": 0.72},
    {"name": "Extreme (Zero Vdroop - High Overshoot)", "r_ll_mohm": 0.10, "transient_k": 1.05},
]


def simulate_llc(bios_vcore: float, idle_current_a: float, load_current_a: float) -> None:
    delta_i = load_current_a - idle_current_a

    print("=" * 102)
    print(
        f"  LOAD-LINE CALIBRATION (LLC) & TRANSIENT VDROOP SIMULATOR | "
        f"Set Vcore: {bios_vcore:.3f}V | Step: {idle_current_a:.0f}A -> {load_current_a:.0f}A"
    )
    print("=" * 102)
    print(
        f"  {'LLC Profile':<38} | {'Idle Vcore':<10} | {'Load Vcore':<10} | "
        f"{'Vdroop':<9} | {'Min Undershoot':<14} | {'Peak Overshoot'}"
    )
    print("-" * 102)

    for p in LLC_PROFILES:
        r_ohm = p["r_ll_mohm"] / 1000.0
        v_idle = bios_vcore - (idle_current_a * r_ohm)
        v_load = bios_vcore - (load_current_a * r_ohm)
        vdroop_mv = (v_idle - v_load) * 1000.0

        # Transient spike modeled by output capacitor ESL/ESR & inductor di/dt response
        transient_dip_v = (delta_i * 0.00038)
        min_undershoot_v = v_load - transient_dip_v
        peak_overshoot_v = v_load + (delta_i * 0.00052 * p["transient_k"])

        print(
            f"  {p['name']:<38} | {v_idle:>8.3f} V | {v_load:>8.3f} V | "
            f"-{vdroop_mv:>5.0f} mV | {min_undershoot_v:>11.3f} V  | {peak_overshoot_v:>11.3f} V"
        )

    print("=" * 102)


def main() -> None:
    parser = argparse.ArgumentParser(description="Load-Line Calibration (LLC) Transient Simulator")
    parser.add_argument("--bios-vcore", type=float, default=1.300, help="Target Vcore set in BIOS (V)")
    parser.add_argument("--idle-current-a", type=float, default=12.0, help="CPU current at idle (A)")
    parser.add_argument("--load-current-a", type=float, default=110.0, help="CPU current under heavy AVX load (A)")
    args = parser.parse_args()

    simulate_llc(args.bios_vcore, args.idle_current_a, args.load_current_a)


if __name__ == "__main__":
    main()
