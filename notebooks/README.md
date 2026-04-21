# Notebooks

Analysis notebooks for the W5 Airline Boarding Revenue Analysis.

## Execution Order

1. `01_data_exploration.ipynb` — Load and validate data sources, basic EDA
2. `02_financial_model.ipynb` — Core P&L model: four boarding methods compared
3. `03_scenario_analysis.ipynb` — Sensitivity analysis and scenario modelling
4. `04_ai_testing_layer.ipynb` — AI designer + AI analyst tests with findings
5. `05_final_report.ipynb` — Full report with executive summary and conclusions

## Requirements

Run `pip install -r requirements.txt` before executing notebooks.
API keys required for `04_ai_testing_layer.ipynb` (see `.env.example`).

## Key Outputs

- `outputs/figures/boarding_time_comparison.png` — Boarding method comparison chart
- `outputs/figures/pnl_waterfall.png` — P&L waterfall: status quo vs alternatives
- `outputs/figures/ancillary_decomposition.png` — Revenue decomposition by airline
- `outputs/figures/sensitivity_analysis.png` — Load factor sensitivity
- `outputs/report/w5_airline_boarding_report.pdf` — Final printable report
