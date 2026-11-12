# Motherboard VRM Electrical Loss, Thermal Physics & Load-Line Calibration (LLC) Simulator

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Hardware Engineering](https://img.shields.io/badge/Power_Electronics-VRM_%26_LLC_Physics-FF6F00?style=for-the-badge)

> **English:** Electrical and thermal physics modeling suite for motherboard **Voltage Regulator Modules (VRMs)** and **Load-Line Calibration (LLC)**. Simulates multi-phase synchronous buck converter **MOSFET conduction losses ($I^2 \cdot R_{DS(on)}$)**, **switching losses ($f_{sw}$)**, inductor DCR heat dissipation, steady-state **VRM heatsink temperatures** under varying case airflow, and **transient Vdroop / voltage overshoot** during heavy AVX current steps.
>
> **Português:** Suíte de modelagem física (elétrica e térmica) para **VRMs de placas-mãe** e **Load-Line Calibration (LLC)**. Simula **perdas por condução ($I^2 \cdot R_{DS(on)}$)** e **chaveamento ($f_{sw}$)** em MOSFETs de conversores buck síncronos multifásicos, dissipação em indutores (DCR), **temperatura estacionária dos dissipadores do VRM** e **Vdroop / picos transientes de tensão** durante variações bruscas de corrente (carga AVX).

---

## Included Simulation Engines / Motores de Simulação Inclusos

| File | Description (EN) | Descrição (PT-BR) |
| :--- | :--- | :--- |
| [`src/vrm_efficiency_thermal_model.py`](src/vrm_efficiency_thermal_model.py) | Calculates per-phase current, High-Side & Low-Side MOSFET conduction loss, gate switching loss (`300 kHz` - `600 kHz`), VRM conversion efficiency (`%`), total dissipated heat (`W`), and MOSFET junction/PCB temperature (`C`). | Calcula corrente por fase, perdas por condução nos MOSFETs de alta/baixa, perdas de chaveamento (`300 kHz` - `600 kHz`), eficiência do VRM (`%`), calor dissipado (`W`) e temperatura de junção (`C`). |
| [`src/llc_vdroop_transient_sim.py`](src/llc_vdroop_transient_sim.py) | Simulates Load-Line Calibration (`Standard`, `Medium`, `High/Turbo`, `Extreme`) under a `15A -> 125A` CPU load step, computing steady-state Vdroop (`mV`), transient undershoot, and load-release voltage overshoot. | Simula níveis de Load-Line Calibration (`Standard`, `Medium`, `High/Turbo`, `Extreme`) em um salto de corrente de `15A -> 125A`, calculando Vdroop estacionário, *undershoot* e *overshoot* de tensão. |
| [`profiles/motherboard_vrm_database.json`](profiles/motherboard_vrm_database.json) | Electrical specifications of real B550/X570 VRM topologies (including the **Gigabyte B550M Aorus Elite** discrete Low-$R_{DS(on)}$ MOSFET stage and 50A DrMOS stages). | Especificações elétricas de topologias reais de VRM B550/X570 (incluindo o estágio discreto da **Gigabyte B550M Aorus Elite** e estágios DrMOS de 50A). |

---

## Quick Start / Como Executar

### 1. Run Motherboard VRM Thermal & Power Loss Simulation
```bash
python src/vrm_efficiency_thermal_model.py \
    --database profiles/motherboard_vrm_database.json \
    --cpu-current-a 95 \
    --vcore-v 1.28 \
    --ambient-c 28
```

### 2. Simulate Load-Line Calibration (LLC) Vdroop & Transient Spikes
```bash
python src/llc_vdroop_transient_sim.py --bios-vcore 1.300 --idle-current-a 12 --load-current-a 110
```
