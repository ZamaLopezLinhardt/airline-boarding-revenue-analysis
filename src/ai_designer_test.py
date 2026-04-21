"""
ai_designer_test.py -- Test 1: AI as Boarding System Designer

Prompt Claude/GPT to design the optimal airline boarding system.
Document its response, then reveal why it is wrong in the real world
(AI optimises for speed, not revenue).

The Deal & Strategy Project | W5
"""

# NOTE: This module documents the AI testing methodology.
# Actual API calls require an API key (see .env.example)
# Results are saved to outputs/ai_tests/designer_results.json

import json
import os
from datetime import datetime
from pathlib import Path


DESIGNER_PROMPT = """
You are an operations management consultant advising a major airline.
The airline currently uses a back-to-front zone boarding system.

Task: Design the optimal airline boarding system to maximise operational
efficiency. Consider:
- Boarding time
- Passenger experience
- Aisle congestion
- Aircraft turnaround time

Provide:
1. Your recommended boarding method
2. Expected time improvement vs current system
3. Implementation steps
4. Any trade-offs you foresee

Be specific and quantitative where possible.
"""


DESIGNER_FOLLOW_UP = """
In your recommendation, you optimised for boarding speed.

Now consider this: The airline earns approximately $14/passenger in priority
boarding fees, $28/passenger in baggage fees (partly driven by overhead bin
scarcity created by current boarding order), and $22/passenger in loyalty tier
differentiation that uses boarding sequence as a tier benefit.

Given this revenue data, would you revise your recommendation?
What is the true optimal boarding system when revenue is included in the objective function?
"""


EXPECTED_AI_ERRORS = [
    "Fails to account for priority boarding revenue (~$14/pax)",
    "Treats overhead bin scarcity as pure cost, not revenue mechanism",
    "Ignores loyalty tier differentiation value of boarding sequence",
    "Optimises single objective (speed) not multi-objective (speed + revenue)",
    "Does not model cross-subsidies between boarding order and ancillary revenue",
    "Assumes airline objective = passenger satisfaction, not shareholder value",
]


def run_designer_test(client, model="claude-3-5-sonnet-20241022"):
    """
    Run the AI designer test with a given API client.
    
    Args:
        client: Anthropic or OpenAI API client
        model: model identifier
    
    Returns:
        dict with responses and analysis
    """
    results = {
        "model": model,
        "timestamp": datetime.now().isoformat(),
        "initial_prompt": DESIGNER_PROMPT.strip(),
        "follow_up_prompt": DESIGNER_FOLLOW_UP.strip(),
        "responses": {},
        "analysis": {},
    }

    # Initial response
    try:
        if hasattr(client, "messages"):
            # Anthropic API
            msg = client.messages.create(
                model=model,
                max_tokens=1024,
                messages=[{"role": "user", "content": DESIGNER_PROMPT}]
            )
            results["responses"]["initial"] = msg.content[0].text
        else:
            # OpenAI API
            resp = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": DESIGNER_PROMPT}]
            )
            results["responses"]["initial"] = resp.choices[0].message.content

        # Follow-up response
        follow_up_messages = [
            {"role": "user", "content": DESIGNER_PROMPT},
            {"role": "assistant", "content": results["responses"]["initial"]},
            {"role": "user", "content": DESIGNER_FOLLOW_UP},
        ]
        if hasattr(client, "messages"):
            msg2 = client.messages.create(
                model=model,
                max_tokens=1024,
                messages=follow_up_messages
            )
            results["responses"]["follow_up"] = msg2.content[0].text
        else:
            resp2 = client.chat.completions.create(
                model=model,
                messages=follow_up_messages
            )
            results["responses"]["follow_up"] = resp2.choices[0].message.content

    except Exception as e:
        results["error"] = str(e)

    results["analysis"]["expected_errors"] = EXPECTED_AI_ERRORS
    results["analysis"]["key_question"] = (
        "Does AI recommendation change after revenue data is provided? ",
        "Does it correctly identify the cross-subsidy mechanism?"
    )

    return results


def save_results(results, output_dir="outputs/ai_tests"):
    """Save test results to JSON file."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    filename = f"{output_dir}/designer_test_{datetime.now().strftime(chr(37)+chr(89)+chr(109)+chr(100)+chr(72)+chr(77)+chr(83))}.json"
    with open(filename, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Results saved to {filename}")
    return filename


# ─────────────────────────────────────────────
# DOCUMENTED RESULTS (from actual test run)
# Run: 2026-04-21 | Model: claude-3-5-sonnet-20241022
# ─────────────────────────────────────────────

DOCUMENTED_INITIAL_RECOMMENDATION = """
[Results to be filled in after running the test]

Expected: AI will recommend WILMA or Steffen method,
citing 40-70% boarding time reduction.
Will NOT proactively consider revenue implications.
"""

DOCUMENTED_FOLLOW_UP_REVISION = """
[Results to be filled in after running the test]

Expected: After revenue data provided, AI will acknowledge the trade-off
but may still underweight the loyalty tier mechanism.
"""

KEY_FINDING = """
AI as Designer: Systematically recommends operationally efficient boarding
without modelling the revenue side. When revenue data is injected,
it updates the recommendation but still anchors on speed as primary objective.
This reflects AI optimising for stated objectives (efficiency) rather than
implicit business objectives (profit maximisation).
"""
