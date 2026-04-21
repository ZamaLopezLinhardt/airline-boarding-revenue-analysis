"""
utils.py -- Helper functions and constants for the airline boarding revenue analysis.
The Deal & Strategy Project | W5
"""

# CONSTANTS: Ground operations benchmarks

# Cost per minute of ground delay (USD, industry avg)
GROUND_DELAY_COST_PER_MIN = 115

# Average aircraft seat count (narrowbody)
NARROWBODY_SEATS = 165

# Boarding time benchmarks by method (minutes)
BOARDING_TIMES = {
    "status_quo":   30,   # Back-to-front / zone boarding
    "wilma":        18,   # Window-Middle-Aisle method
    "random":       16,   # Open seating / random boarding
    "steffen":       8,   # Steffen optimal method
}

# Turnaround breakdown (minutes)
TURNAROUND_BREAKDOWN = {
    "deplaning":     15,
    "cleaning":      10,
    "catering":       8,
    "fueling":       12,
    "boarding":      30,
    "door_close":     2,
    "pushback":       5,
}

# American Airlines ancillary revenue per passenger (2023, USD)
AA_ANCILLARY_PER_PAX = {
    "baggage_fees":          28.50,
    "priority_boarding":     14.20,
    "seat_selection":        12.80,
    "loyalty_uplift":        22.40,
    "other":                 18.10,
    "total":                 96.00,
}

# Ryanair ancillary revenue per passenger (FY2024, EUR to USD)
RYANAIR_ANCILLARY_PER_PAX = {
    "baggage_fees":          38.20,
    "priority_boarding":     18.60,
    "seat_selection":        16.40,
    "loyalty_uplift":         5.20,
    "other":                 22.60,
    "total":                101.00,
}

# Revenue at risk if switching from status quo to WILMA/random
REVENUE_AT_RISK_PCT = {
    "priority_boarding":     0.85,
    "overhead_bin_premium":  0.45,
    "loyalty_differentiation": 0.30,
}

DAILY_ROTATIONS = 5.2
AVG_STAGE_LENGTH_MIN = 155
APU_FUEL_BURN_KG_MIN = 2.1
JET_FUEL_USD_PER_KG = 0.85


def boarding_time_savings(method, baseline="status_quo"):
    """Return time savings in minutes vs baseline method."""
    return BOARDING_TIMES[baseline] - BOARDING_TIMES[method]


def operational_cost_savings(method, baseline="status_quo"):
    """Return per-rotation operational cost savings (USD)."""
    time_saved = boarding_time_savings(method, baseline)
    delay_savings = time_saved * GROUND_DELAY_COST_PER_MIN
    apu_savings = time_saved * APU_FUEL_BURN_KG_MIN * JET_FUEL_USD_PER_KG
    return delay_savings + apu_savings


def revenue_at_risk(airline="AA", method="wilma"):
    """Estimate ancillary revenue at risk if switching boarding method."""
    base = AA_ANCILLARY_PER_PAX if airline == "AA" else RYANAIR_ANCILLARY_PER_PAX
    at_risk = {
        "priority_boarding": base["priority_boarding"] * REVENUE_AT_RISK_PCT["priority_boarding"],
        "overhead_bin_premium": base["baggage_fees"] * REVENUE_AT_RISK_PCT["overhead_bin_premium"],
        "loyalty_differentiation": base["loyalty_uplift"] * REVENUE_AT_RISK_PCT["loyalty_differentiation"],
    }
    at_risk["total"] = sum(at_risk.values())
    return at_risk


def net_pnl_per_rotation(airline="AA", method="wilma", seats_filled=0.85):
    """Calculate net P&L impact per rotation of switching boarding method."""
    pax = int(NARROWBODY_SEATS * seats_filled)
    op_savings = operational_cost_savings(method)
    rev_risk = revenue_at_risk(airline, method)
    return {
        "passengers": pax,
        "operational_savings_usd": op_savings,
        "revenue_at_risk_usd": rev_risk["total"] * pax,
        "net_per_rotation_usd": op_savings - (rev_risk["total"] * pax),
        "break_even_load_factor": op_savings / (rev_risk["total"] * NARROWBODY_SEATS),
    }
