#!/usr/bin/env python3
"""
vrm_efficiency_thermal_model.py
EN: Models synchronous buck converter VRM efficiency, MOSFET conduction/switching power losses,
    and steady-state VRM temperature across different motherboard VRM topologies.
PT: Modela a eficiência do VRM (conversor buck síncrono), perdas de condução e chaveamento
    nos MOSFETs e temperatura estacionária do VRM em diferentes placas-mãe.
"""

import argparse
import json
from typing import Dict


def simulate_vrm_board(
    board: Dict[str, object],
    cpu_current_a: float,
    vcore_v: float,
    ambient_c: float,
    vin_v: float = 12.0,
) -> Dict[str, float]:
    phases = int(board["vcore_phases"])
    rds_on_hs_mohm = float(board["high_side_rds_on_mohm"])
    rds_on_ls_mohm = float(board["low_side_rds_on_mohm"])
    f_sw_khz = float(board["switching_freq_khz"])
    t_sw_ns = float(board["switching_transition_ns"])
    inductor_dcr_mohm = float(board["inductor_dcr_mohm"])
    heatsink_r_theta = float(board["heatsink_r_theta_c_per_w"])

    duty_cycle = vcore_v / vin_v
    i_phase = cpu_current_a / phases

    # 1. Conduction Losses per phase: I_phase^2 * (D * Rds_HS + (1 - D) * Rds_LS)
    r_eff_ohm = (duty_cycle * (rds_on_hs_mohm / 1000.0)) + ((1.0 - duty_cycle) * (rds_on_ls_mohm / 1000.0))
    p_cond_per_phase_w = (i_phase ** 2) * r_eff_ohm

    # 2. Switching Losses per phase: 0.5 * Vin * I_phase * (t_rise_fall) * f_sw
    p_sw_per_phase_w = 0.5 * vin_v * i_phase * (t_sw_ns * 1e-9) * (f_sw_khz * 1e3)

    # 3. Inductor DCR Conduction Loss per phase
    p_ind_per_phase_w = (i_phase ** 2) * (inductor_dcr_mohm / 1000.0)

    total_vrm_loss_w = phases * (p_cond_per_phase_w + p_sw_per_phase_w + p_ind_per_phase_w)
    cpu_power_w = vcore_v * cpu_current_a
    input_power_w = cpu_power_w + total_vrm_loss_w
    efficiency_pct = (cpu_power_w / input_power_w) * 100.0

    # Steady-state VRM MOSFET temperature: T_ambient + (P_loss * R_theta_heatsink)
    vrm_temp_c = ambient_c + (total_vrm_loss_w * heatsink_r_theta)

    return {
        "i_phase": round(i_phase, 1),
        "cpu_power_w": round(cpu_power_w, 1),
        "total_loss_w": round(total_vrm_loss_w, 2),
        "efficiency_pct": round(efficiency_pct, 2),
        "vrm_temp_c": round(vrm_temp_c, 1),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Motherboard VRM Electrical & Thermal Physics Simulator")
    parser.add_argument(
        "--database",
        default="profiles/motherboard_vrm_database.json",
        help="Path to VRM topology database JSON",
    )
    parser.add_argument("--cpu-current-a", type=float, default=95.0, help="CPU TDC/EDC load current in Amps")
    parser.add_argument("--vcore-v", type=float, default=1.28, help="Operating CPU Vcore in Volts")
    parser.add_argument("--ambient-c", type=float, default=28.0, help="Case ambient temperature in Celsius")
    args = parser.parse_args()

    with open(args.database, mode="r", encoding="utf-8") as f:
        db = json.load(f)

    print("=" * 98)
    print(
        f"  MOTHERBOARD VRM THERMAL & EFFICIENCY SIMULATOR | "
        f"Load: {args.cpu_current_a:.0f}A @ {args.vcore_v:.3f}V ({args.cpu_current_a * args.vcore_v:.1f}W)"
    )
    print("=" * 98)
    print(
        f"  {'Motherboard Model':<30} | {'VCore Topology':<16} | {'Current/Phase':<13} | "
        f"{'VRM Loss':<10} | {'Efficiency':<10} | {'Est. VRM Temp'}"
    )
    print("-" * 98)

    for board in db["motherboards"]:
        res = simulate_vrm_board(board, args.cpu_current_a, args.vcore_v, args.ambient_c)
        status = "OK" if res["vrm_temp_c"] < 85.0 else "HOT"
        print(
            f"  {board['name']:<30} | {board['topology_label']:<16} | {res['i_phase']:>8.1f} A    | "
            f"{res['total_loss_w']:>6.2f} W  | {res['efficiency_pct']:>8.2f}% | "
            f"{res['vrm_temp_c']:>6.1f} C [{status}]"
        )

    print("=" * 98)


if __name__ == "__main__":
    main()
