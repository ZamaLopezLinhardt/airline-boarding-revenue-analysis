# Airline Boarding as a Revenue Mechanism
## W5 | The Deal & Strategy Project

> **Central Thesis:** Airlines don't board inefficiently by accident — they've deliberately chosen a boarding system that is operationally suboptimal because it generates more revenue than the operational cost it creates. This investigation tests that quantitatively.

---

## 🎯 The Question

*If slow, segmented boarding costs airlines ~$100/minute in ground delays, why do they keep doing it?*

The answer: **because it pays more than it costs.**

Priority boarding fees, baggage-scarcity dynamics, and loyalty tier perks tied to boarding sequence generated a material fraction of the **$148B in global ancillary revenue** airlines collected in 2024. This project models both sides of the P&L and asks: does the inefficiency still pencil out as turnaround costs rise?

---

## 📁 Repository Structure

```
airline-boarding-revenue-analysis/
│
├── data/
│   ├── raw/                    # Source data (airline financials, ops benchmarks)
│   └── processed/              # Cleaned datasets for modelling
│
├── src/
│   ├── boarding_model.py       # Core financial model: 4 boarding scenarios
│   ├── ancillary_revenue.py    # Ancillary revenue decomposition (AA & Ryanair)
│   ├── ai_designer_test.py     # Test 1: AI as boarding system designer
│   ├── ai_analyst_test.py      # Test 2: AI as financial analyst
│   └── utils.py                # Helper functions and constants
│
├── notebooks/
│   ├── 01_data_exploration.ipynb      # Initial data review and sources
│   ├── 02_financial_model.ipynb       # Core P&L model walkthrough
│   ├── 03_scenario_analysis.ipynb     # Four boarding method comparisons
│   ├── 04_ai_testing_layer.ipynb      # AI designer + analyst tests
│   └── 05_final_report.ipynb          # Full report with conclusions
│
├── outputs/
│   ├── figures/                # All charts and visualisations
│   └── report/                 # Final report exports
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

## 📊 The Financial Model

### Four Boarding Scenarios Modelled

| Method | Description | Avg. Boarding Time | Operational Cost |
|--------|------------|-------------------|-----------------|
| **Status Quo** (Back-to-front) | Current airline standard | ~25–35 min | Baseline |
| **WILMA** (Window-Middle-Aisle) | Fills seats efficiently | ~15–20 min | -33% vs SQ |
| **Random** | Open seating (Southwest model) | ~15–18 min | -30% vs SQ |
| **Steffen** | Theoretical optimum | ~6–8 min | -75% vs SQ |

### The Core Trade-off

```
Revenue at risk (if switching to Steffen/WILMA):
  - Priority boarding fees:         ~$15–40/passenger
  - Overhead bin scarcity premium:  ~$8–25/passenger (checked bag uplift)
  - Loyalty tier differentiation:   ~$20–60/passenger (lifetime value impact)

Operational savings (from faster turnaround):
  - Gate time reduction:            ~$100–140/minute
  - Aircraft utilisation gain:      ~8% more rotations/day (10-min improvement)
  - Fuel savings (reduced APU):     ~$40–80/rotation
```

---

## 🤖 AI Testing Layer

### Test 1: AI as Designer
Ask Claude/GPT to design the optimal boarding system — then reveal why the AI answer is wrong in the real world (it optimises for speed, not revenue).

### Test 2: AI as Analyst  
Feed an airline 10-K to the AI and ask it to value the priority boarding programme — then show where it under/overestimates (the cross-subsidy between boarding order and bag economics is invisible in standard filings).

**Key finding hypothesis:** AI tools optimise for the stated objective (speed, cost) and systematically miss the second-order revenue effects that make "inefficiency" rational.

---

## 📈 Data Sources

- **Airline financials:** SEC 10-K filings (American Airlines, United), Ryanair Annual Reports
- **Ancillary revenue:** IdeaWorksCompany Global Ancillary Revenue Report 2024
- **Boarding time benchmarks:** Academic literature (Steffen 2012, Ferrari & Nagel 2005)
- **Ground delay costs:** FAA/EUROCONTROL cost benchmarks
- **Aircraft utilisation:** CAPA Centre for Aviation operational data

---

## 🛠️ Setup & Usage

```bash
# Clone the repo
git clone https://github.com/ZamaLopezLinhardt/airline-boarding-revenue-analysis.git
cd airline-boarding-revenue-analysis

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Launch Jupyter
jupyter notebook notebooks/
```

---

## 🗺️ Series Context

This is **Week 5** of [The Deal & Strategy Project](https://github.com/ZamaLopezLinhardt) — a weekly series applying rigorous financial analysis to real-world systems where the obvious answer is wrong.

| Week | Topic |
|------|-------|
| W1 | Prediction Markets |
| W2 | Adobe PE Analysis |
| W3 | Strava / Runna M&A |
| W4 | Bandit Running Marketing |
| **W5** | **Airline Boarding Revenue Analysis** |

---

## 📝 Licence

MIT — see [LICENSE](LICENSE) for details.

---

*Built as part of The Deal & Strategy Project. AI tools (Claude, GPT-4) used as tested instruments within the analysis, not as authors.*
