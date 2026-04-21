"""
ancillary_revenue.py -- Ancillary revenue decomposition for AA and Ryanair.
Breaks down which revenue streams are structurally tied to boarding order.
The Deal & Strategy Project | W5
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from utils import AA_ANCILLARY_PER_PAX, RYANAIR_ANCILLARY_PER_PAX, REVENUE_AT_RISK_PCT


# Revenue categories tied to boarding order and their rationale
BOARDING_REVENUE_RATIONALE = {
    "priority_boarding": {
        "linkage": "Direct",
        "mechanism": "Passengers pay for early boarding access. Eliminates if boarding is unordered.",
        "at_risk_pct": 0.85,
    },
    "baggage_fees": {
        "linkage": "Indirect (overhead bin scarcity)",
        "mechanism": "Bin scarcity from back-to-front boarding forces checked bags. WILMA reduces scarcity.",
        "at_risk_pct": 0.45,
    },
    "seat_selection": {
        "linkage": "Partial",
        "mechanism": "Better seat access for early boarders incentivises upsell. Less relevant if random.",
        "at_risk_pct": 0.20,
    },
    "loyalty_uplift": {
        "linkage": "Indirect (tier differentiation)",
        "mechanism": "Elite tiers partly justified by boarding priority. Reduces programme perceived value.",
        "at_risk_pct": 0.30,
    },
    "other": {
        "linkage": "None",
        "mechanism": "Onboard retail, wifi, ancillary services not tied to boarding sequence.",
        "at_risk_pct": 0.0,
    },
}


def build_revenue_linkage_table(airline="AA") -> pd.DataFrame:
    """Build detailed ancillary revenue linkage table for a given airline."""
    base = AA_ANCILLARY_PER_PAX if airline == "AA" else RYANAIR_ANCILLARY_PER_PAX
    rows = []
    for cat, info in BOARDING_REVENUE_RATIONALE.items():
        per_pax = base.get(cat, 0)
        at_risk = per_pax * info["at_risk_pct"]
        rows.append({
            "Category": cat.replace("_", " ").title(),
            "Per Pax ($)": round(per_pax, 2),
            "Boarding Linkage": info["linkage"],
            "Revenue at Risk/Pax ($)": round(at_risk, 2),
            "Mechanism": info["mechanism"][:60] + "...",
        })
    df = pd.DataFrame(rows)
    total_at_risk = df["Revenue at Risk/Pax ($)"].sum()
    total_rev = base["total"]
    return df, total_at_risk, total_rev


def boarding_revenue_share(airline="AA") -> dict:
    """Calculate what percentage of total ancillary revenue is boarding-linked."""
    _, total_at_risk, total_rev = build_revenue_linkage_table(airline)
    return {
        "total_ancillary_per_pax": total_rev,
        "boarding_linked_per_pax": round(total_at_risk, 2),
        "boarding_linked_pct": round(total_at_risk / total_rev * 100, 1),
        "unlinked_per_pax": round(total_rev - total_at_risk, 2),
    }


def plot_revenue_decomposition(save_path=None):
    """Side-by-side stacked bar chart for AA vs Ryanair ancillary revenue."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 7))
    fig.patch.set_facecolor("#0d1117")

    airlines = [("AA", "American Airlines"), ("Ryanair", "Ryanair")]
    categories = ["priority_boarding", "baggage_fees", "seat_selection",
                  "loyalty_uplift", "other"]
    colours = {
        "priority_boarding": "#e74c3c",
        "baggage_fees":      "#e67e22",
        "seat_selection":    "#f1c40f",
        "loyalty_uplift":    "#9b59b6",
        "other":             "#2ecc71",
    }
    labels = {
        "priority_boarding": "Priority Boarding",
        "baggage_fees":      "Baggage Fees",
        "seat_selection":    "Seat Selection",
        "loyalty_uplift":    "Loyalty Uplift",
        "other":             "Other",
    }

    for ax, (code, name) in zip(axes, airlines):
        base = AA_ANCILLARY_PER_PAX if code == "AA" else RYANAIR_ANCILLARY_PER_PAX
        bottom = 0
        for cat in categories:
            val = base[cat]
            ax.bar(name, val, bottom=bottom, color=colours[cat], width=0.5)
            if val > 2:
                ax.text(0, bottom + val/2, f"${val:.1f}", ha="center",
                        va="center", color="white", fontsize=9, fontweight="bold")
            bottom += val
        ax.set_facecolor("#161b22")
        ax.set_ylabel("Ancillary Revenue per Passenger ($)", color="white")
        ax.set_title(f"{name}\n${base[chr(116)+chr(111)+chr(116)+chr(97)+chr(108)]:.0f}/pax total",
                     color="white", pad=10)
        ax.tick_params(colors="white")
        for spine in ax.spines.values():
            spine.set_edgecolor("#444")

    patches = [mpatches.Patch(color=colours[c], label=labels[c]) for c in categories]
    fig.legend(handles=patches, loc="lower center", ncol=5, frameon=False,
               labelcolor="white", fontsize=9)
    fig.suptitle("Ancillary Revenue Decomposition: What is Boarding-Linked?",
                 color="white", fontsize=13, y=1.01)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    return fig


if __name__ == "__main__":
    for airline in ["AA", "Ryanair"]:
        print(f"\n=== {airline} Ancillary Revenue Linkage ===")
        df, at_risk, total = build_revenue_linkage_table(airline)
        print(df.to_string(index=False))
        share = boarding_revenue_share(airline)
        print(f"\nBoarding-linked revenue: ${share[chr(98)+chr(111)+chr(97)+chr(114)+chr(100)+chr(105)+chr(110)+chr(103)+chr(95)+chr(108)+chr(105)+chr(110)+chr(107)+chr(101)+chr(100)+chr(95)+chr(112)+chr(101)+chr(114)+chr(95)+chr(112)+chr(97)+chr(120)]:.2f}/pax ({share[chr(98)+chr(111)+chr(97)+chr(114)+chr(100)+chr(105)+chr(110)+chr(103)+chr(95)+chr(108)+chr(105)+chr(110)+chr(107)+chr(101)+chr(100)+chr(95)+chr(112)+chr(99)+chr(116)]}% of total)")
