"""Deterministic Chapter 44 reference. No network, model, booking, or sending."""
import argparse
import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def extract(source):
    """Map the supplied structured fixture, not arbitrary natural-language text."""
    return {
        "task_id": source["task_id"], "source_version": source["source_version"],
        "output_version": "1", "budget": source["B1"]["budget"],
        "reserve": source["B1"]["materials_reserve"], "budget_source": "B1",
        "occupancy": source["B2"]["occupancy"], "occupancy_source": "B2",
        "includes_volunteers": source["B2"]["includes_volunteers"],
        "availability": source["U1"]["availability"], "availability_source": "U1",
        "venues": [
            {"name": source["Q1"]["venue"], "source": "Q1",
             "charges": {"rental": source["Q1"]["rental"],
                         "required_cleaning": source["Q1"]["required_cleaning"]},
             "capacity": source["Q1"]["capacity"]},
            {"name": source["Q2"]["venue"], "source": "Q2",
             "charges": {"all_inclusive": source["Q2"]["all_inclusive"]},
             "capacity": source["Q2"]["capacity"]}
        ]
    }


def validate_handoff(source, handoff):
    # Exact source fidelity is intentionally strict for this small fixed schema.
    # This is a deterministic reference check, not semantic validation of prose.
    if handoff != extract(source):
        raise ValueError("Extracted handoff differs from the source; repair extraction before recommending.")


def calculate(handoff):
    results = []
    for venue in handoff["venues"]:
        venue_cost = sum(venue["charges"].values())
        total = venue_cost + handoff["reserve"]
        balance = handoff["budget"] - total
        spare = venue["capacity"] - handoff["occupancy"]
        results.append({"name": venue["name"], "venue_cost": venue_cost,
                        "total": total, "budget_remaining": balance,
                        "spare_capacity": spare, "meets_constraints": balance >= 0 and spare >= 0,
                        "sources": [venue["source"], "B1", "B2"]})
    return {"task_id": handoff["task_id"], "source_version": handoff["source_version"],
            "input_output_version": handoff["output_version"], "venues": results,
            "eligible_venues": [v["name"] for v in results if v["meets_constraints"]],
            "availability": handoff["availability"], "availability_source": "U1"}


def explain(calculation):
    if calculation["eligible_venues"] == ["Pine Room"]:
        text = ("Pine Room fits the current plan at $420 including materials, leaving $30. "
                "Its ten places exactly match our expected occupancy. Elm would cost $470 "
                "and exceed the budget. Confirm Pine's availability before making a commitment.")
    elif not calculation["eligible_venues"]:
        text = ("Neither venue meets both constraints. Elm costs $470, exceeding the $450 budget. "
                "Pine costs $420 but holds only ten of the eleven people. Seek another venue "
                "or ask whether a constraint may change. Availability remains unconfirmed.")
    else:
        raise ValueError("This reference explanation supports only the two supplied attendance cases.")
    return {"text": text, "sources": ["B1", "B2", "Q1", "Q2", "U1"],
            "booking": "not established", "actions_taken": [], "state": "draft"}


def run(variant="base", handoff_override=None):
    if variant not in {"base", "occupancy11", "omitted-cleaning"}:
        raise ValueError("Unknown case")
    source = json.loads((ROOT / "source.json").read_text())
    if variant == "occupancy11":
        source["B2"]["occupancy"] = 11
        source["source_version"] = "2-occupancy11"
    handoff = extract(source) if handoff_override is None else copy.deepcopy(handoff_override)
    if variant == "omitted-cleaning":
        del handoff["venues"][0]["charges"]["required_cleaning"]
    record = {"case": variant, "execution_kind": "deterministic reference; no model calls",
              "source": source, "extraction": handoff}
    try:
        validate_handoff(source, handoff)
    except ValueError as exc:
        return {**record, "status": "rejected", "validation": str(exc),
                "calculation": None, "explanation": None}
    calculation = calculate(handoff)
    return {**record, "status": "completed", "validation": "source fidelity passed",
            "calculation": calculation, "explanation": explain(calculation)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", choices=["base", "occupancy11", "omitted-cleaning"], default="base")
    result = run(parser.parse_args().case)
    print(json.dumps(result, indent=2))
    raise SystemExit(2 if result["status"] == "rejected" else 0)
