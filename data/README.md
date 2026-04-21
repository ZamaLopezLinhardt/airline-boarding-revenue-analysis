# Data Directory

This directory contains the data sources used in the W5 airline boarding analysis.

## Structure

```
data/
  raw/          -- Original source data (not committed for large files)
  processed/    -- Cleaned and transformed data for modelling
```

## Data Sources

### Airline Financials
- **American Airlines 10-K (FY2023):** https://ir.aa.com/sec-filings
- **Ryanair Annual Report (FY2024):** https://investor.ryanair.com

### Ancillary Revenue
- **IdeaWorksCompany Global Ancillary Revenue Report 2024**
  - Available from: https://ideaworkscompany.com
  - Key metric: $148.6B global ancillary revenue in 2024

### Boarding Time Benchmarks
- Steffen, J.H. (2008). "Optimal boarding method for airline passengers."
  *Journal of Air Transport Management*, 14(3), 146-150.
- Ferrari, P. & Nagel, K. (2005). "Robustness of efficient passenger boarding strategies."
  *Transportation Research Record*, 1915, 44-54.
- Van den Briel, M.H.L. et al. (2005). "America West Airlines develops efficient boarding strategies."
  *Interfaces*, 35(3), 191-201.

### Ground Operations Costs
- FAA Aviation Environmental Design Tool documentation
- EUROCONTROL Performance Review Report
- Industry benchmark: ~$100-140/minute ground delay for narrowbody aircraft

### Aircraft Utilisation
- CAPA Centre for Aviation fleet and utilisation data
- Bureau of Transportation Statistics (BTS) Form 41

## File Naming Convention

- `raw/aa_10k_2023_extract.csv` -- American Airlines financial data
- `raw/ryanair_ar_2024_extract.csv` -- Ryanair financial data
- `raw/boarding_time_benchmarks.csv` -- Academic boarding time data
- `raw/ground_ops_costs.csv` -- Ground delay cost benchmarks
- `processed/model_inputs.csv` -- Combined model inputs
- `processed/scenario_outputs.csv` -- Model scenario results

## Notes

Raw data files are not committed to the repository for size/licensing reasons.
Run `src/data_prep.py` to generate processed files from raw sources.
See `notebooks/01_data_exploration.ipynb` for data quality checks.
