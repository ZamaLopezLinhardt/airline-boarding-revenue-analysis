"""
boarding_model.py -- Core financial model for the airline boarding revenue analysis.
Models four boarding methods and calculates the P&L trade-off.
The Deal & Strategy Project | W5
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from utils import (
    BOARDING_TIMES, GROUND_DELAY_COST_PER_MIN, NARROWBODY_SEATS,
    AA_ANCILLARY_PER_PAX, RYANAIR_ANCILLARY_PER_PAX, DAILY_ROTATIONS,
    boarding_time_savings, operational_cost_savings, revenue_at_risk, net_pnl_per_rotation
)


class AirlineBoardingModel:
    """
    Financial model comparing four boarding methods for a given airline.
    
    Core question: Does the operational inefficiency of status-quo boarding
    pay more than it costs in ancillary revenue terms?
    """

    METHODS = ["status_quo", "wilma", "random", "steffen"]
    METHOD_LABELS = {
        "status_quo": "Status Quo (Back-to-Front)",
        "wilma":      "WILMA (Window-Middle-Aisle)",
        "random":     "Random / Open Seating",
        "steffen":    "Steffen Optimal",
    }

    def __init__(self, airline="AA", fleet_size=100, load_factor=0.85,
                 daily_rotations=DAILY_ROTATIONS, annual_pax=None):
        self.airline = airline
        self.fleet_size = fleet_size
        self.load_factor = load_factor
        self.daily_rotations = daily_rotations
        self.pax_per_flight = int(NARROWBODY_SEATS * load_factor)
        # Estimate annual pax if not provided
        self.annual_pax = annual_pax or (
            fleet_size * daily_rotations * 365 * self.pax_per_flight
        )
        self.annual_rotations = fleet_size * daily_rotations * 365

    def boarding_time_table(self)-> pd.DataFrame:
        """Create summary table of boarding times and operational impacts."""
        rows = []
        for method in self.METHODS:
            time = BOARDING_TIMES[method]
            savings_min = boarding_time_savings(method)
            op_savings = operational_cost_savings(method)
            annual_op_savings = op_savings * self.annual_rotations
            rows.append({
                "Method": self.METHOD_LABELS[method],
                "Boarding Time (min)": time,
                "Time Saved vs SQ (min)": savings_min,
                "Op Savings/Rotation ($)": round(op_savings, 0),
                "Annual Op Savings ($M)": round(annual_op_savings / 1e6, 1),
            })
        return pd.DataFrame(rows)

    def ancillary_revenue_table(self) -> pd.DataFrame:
        """Decompose ancillary revenue and identify what is tied to boarding order."""
        base = AA_ANCILLARY_PER_PAX if self.airline == "AA" else RYANAIR_ANCILLARY_PER_PAX
        categories = ["baggage_fees", "priority_boarding", "seat_selection",
                      "loyalty_uplift", "other", "total"]
        rows = []
        for cat in categories:
            per_pax = base[cat]
            annual = per_pax * self.annual_pax
            boarding_linked = cat in ["priority_boarding", "baggage_fees", "loyalty_uplift"]
            rows.append({
                "Category": cat.replace("_", " ").title(),
                "Per Pax ($)": per_pax,
                "Annual ($M)": round(annual / 1e6, 0),
                "Linked to Boarding Order": "Yes" if boarding_linked else "No",
            })
        return pd.DataFrame(rows)

    def full_pnl_comparison(self) -> pd.DataFrame:
        """Full P&L comparison: operational savings vs revenue at risk for each method."""
        rows = []
        for method in self.METHODS:
            pnl = net_pnl_per_rotation(self.airline, method, self.load_factor)
            rar = revenue_at_risk(self.airline, method)
            annual_op = pnl["operational_savings_usd"] * self.annual_rotations
            annual_rev_risk = pnl["revenue_at_risk_usd"] * self.annual_rotations
            rows.append({
                "Method": self.METHOD_LABELS[method],
                "Annual Op Savings ($M)": round(annual_op / 1e6, 1),
                "Annual Rev at Risk ($M)": round(annual_rev_risk / 1e6, 1),
                "Net P&L Impact ($M)": round((annual_op - annual_rev_risk) / 1e6, 1),
                "Break-even Load Factor": round(pnl["break_even_load_factor"], 3),
                "Verdict": "Profitable switch" if annual_op > annual_rev_risk else "Revenue costs exceed savings",
            })
        return pd.DataFrame(rows)

    def plot_pnl_waterfall(self, method="wilma", save_path=None):
        """Waterfall chart showing P&L components for a specific method switch."""
        pnl = net_pnl_per_rotation(self.airline, method, self.load_factor)
        rar = revenue_at_risk(self.airline, method)
        
        categories = [
            "Op Savings",
            "Priority Boarding\nRevenue Lost",
            "Bag Fee\nRevenue Lost",
            "Loyalty\nRevenue Lost",
            "Net Impact",
        ]
        annual_rotations = self.annual_rotations
        pax_per_rotation = self.pax_per_flight
        
        values = [
            pnl["operational_savings_usd"] * annual_rotations / 1e6,
            -rar["priority_boarding"] * pax_per_rotation * annual_rotations / 1e6,
            -rar["overhead_bin_premium"] * pax_per_rotation * annual_rotations / 1e6,
            -rar["loyalty_differentiation"] * pax_per_rotation * annual_rotations / 1e6,
            pnl["net_per_rotation_usd"] * annual_rotations / 1e6,
        ]
        
        colours = ["#2ecc71" if v >= 0 else "#e74c3c" for v in values]
        fig, ax = plt.subplots(figsize=(12, 6))
        bars = ax.bar(categories, values, color=colours, width=0.6, edgecolor="white")
        ax.axhline(0, color="white", linewidth=0.8, linestyle="--", alpha=0.5)
        ax.set_ylabel("Annual Impact ($M USD)", color="white")
        ax.set_title(
            f"P&L Impact: Switching {self.airline} from Status Quo to {self.METHOD_LABELS[method]}\n"
            f"Fleet: {self.fleet_size} aircraft | Load factor: {self.load_factor:.0%} | Annual rotations: {annual_rotations:,.0f}",
            color="white", pad=15
        )
        ax.set_facecolor("#1a1a2e")
        fig.patch.set_facecolor("#1a1a2e")
        ax.tick_params(colors="white")
        for spine in ax.spines.values():
            spine.set_edgecolor("#444")
        for bar, val in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + (0.5 if val >= 0 else -1.5),
                    f"${val:+.1f}M", ha="center", va="bottom", color="white", fontsize=9)
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches="tight")
        return fig

    def sensitivity_analysis(self, method="wilma", param="load_factor",
                              low=0.70, high=0.95, steps=10) -> pd.DataFrame:
        """Run sensitivity analysis on key parameters."""
        results = []
        for val in np.linspace(low, high, steps):
            if param == "load_factor":
                m = AirlineBoardingModel(self.airline, self.fleet_size, val,
                                        self.daily_rotations)
            elif param == "ground_delay_cost":
                import utils
                original = utils.GROUND_DELAY_COST_PER_MIN
                utils.GROUND_DELAY_COST_PER_MIN = val
                m = AirlineBoardingModel(self.airline, self.fleet_size,
                                        self.load_factor, self.daily_rotations)
                utils.GROUND_DELAY_COST_PER_MIN = original
            pnl = net_pnl_per_rotation(m.airline, method, m.load_factor)
            net_annual = pnl["net_per_rotation_usd"] * m.annual_rotations / 1e6
            results.append({param: round(val, 3), "Net Annual Impact ($M)": round(net_annual, 1)})
        return pd.DataFrame(results)


if __name__ == "__main__":
    print("=== American Airlines Boarding Revenue Model ===\n")
    model = AirlineBoardingModel(airline="AA", fleet_size=950, load_factor=0.85)
    
    print("--- Boarding Time Comparison ---")
    print(model.boarding_time_table().to_string(index=False))
    
    print("\n--- Ancillary Revenue Breakdown ---")
    print(model.ancillary_revenue_table().to_string(index=False))
    
    print("\n--- Full P&L Comparison ---")
    print(model.full_pnl_comparison().to_string(index=False))
