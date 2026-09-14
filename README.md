# ⚡ Solarnex BESS Dispatch Engine

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://solarnex-bess-engine-ngcyftziwz5vapvogn8bje.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Optimization](https://img.shields.io/badge/Solver-PuLP%20%28CBC%29-brightgreen.svg)]()
[![License](https://img.shields.io/badge/License-MIT-purple.svg)]()

**Solarnex BESS Engine** is an advanced quantitative optimization framework designed to maximize the economic efficiency of Battery Energy Storage Systems (BESS) in volatile power markets. By utilizing a **Rolling Horizon** approach paired with **Price Spike Filtering**, it provides robust dispatch strategies against market anomalies, solver bottlenecks, and forecasting drift.

---

## 🚀 Live Dashboard

Experience the optimization engine in real-time through our interactive web application. Modify asset properties, simulate market conditions, and visualize dispatch strategies on the fly:

👉 **[Launch Solarnex BESS Simulator](https://solarnex-bess-engine-ngcyftziwz5vapvogn8bje.streamlit.app/)**

---

## 📊 Visuals & Simulation Output

### Rolling Horizon Optimization Dynamics (Dark Theme)
*The animation below demonstrates the dispatch logic (Charge/Discharge) responding to market price signals while maintaining the State of Charge (SoC) within precise physical limits.*

![Solarnex BESS Simulation](https://raw.githubusercontent.com/Mohammadrezarefaei/solarnex-bess-engine/main/solarnex_bess_simulation.gif)
> *Note: This visualization simulates the asset's response to volatile pricing across consecutive optimization windows.*

### Streamlit Dashboard Interface
A complete SaaS-style interface allowing stakeholders to interact directly with the underlying MILP (Mixed-Integer Linear Programming) models.

<img src="https://via.placeholder.com/1000x450/0f172a/38bdf8?text=Solarnex+Interactive+Dashboard+-+BESS+Dispatch" alt="Dashboard Preview" width="100%">
> *(Tip: Take a screenshot of your live Streamlit dashboard, upload it to your repo, and replace the placeholder link above with its raw URL).*

---

## ⚙️ Core Engine Parameters

The optimization model relies on physical constraints and market assumptions to ensure realistic asset dispatching. The table below outlines the primary configuration capabilities:

| Parameter | Description | Default | Unit |
| :--- | :--- | :---: | :---: |
| **Energy Capacity** | Total structural storage capacity of the battery | `10.0` | MWh |
| **Max Power** | Maximum grid connection threshold (Charge/Discharge) | `2.5` | MW |
| **Round-Trip Efficiency (RTE)**| Mathematical penalty accounting for thermal & conversion losses | `90%` | % |
| **Rolling Horizon Window** | The look-ahead forecasting timeframe for the solver | `48` | Hours |
| **Horizon Step Size** | Timestep execution before locking in variables and moving | `24` | Hours |
| **Spike Filter Threshold** | Dynamic upper/lower boundary multiplier for price noise | `2.5` | $\sigma$ (Std) |

---

## 🧠 Key Features & Methodology

Our framework bridges the gap between raw data forecasting and actionable trading dispatch:

| Feature Module | Description & Methodology |
| :--- | :--- |
| **MILP Dispatch Optimizer** | Formulates the dispatch problem as a Mixed-Integer Linear Program using `PuLP`. Built-in constraints guarantee mutual exclusivity between charging and discharging states. |
| **Rolling Horizon Simulator** | Prevents solver stagnation on large datasets by chunking the timeline into overlapping operational windows, updating the initial SoC dynamically per step. |
| **Market Anomaly Filtering** | Implements a statistical rolling bounds filter to clip extreme price spikes, mitigating concept drift and ensuring the solver isn't biased by black-swan pricing events. |
| **Interactive SaaS Interface** | Built purely in `Streamlit`, offering instant parameter tuning, institutional-grade dark visualizations (`matplotlib`), and one-click operational CSV exports. |

---

## 💻 Installation & Quick Start

Clone the repository and install the required dependencies to run the quantitative engine locally.

```bash
# 1. Clone the repository
git clone [https://github.com/Mohammadrezarefaei/solarnex-bess-engine.git](https://github.com/Mohammadrezarefaei/solarnex-bess-engine.git)

# 2. Navigate to the project directory
cd solarnex-bess-engine

# 3. Install core dependencies
pip install -r requirements.txt
