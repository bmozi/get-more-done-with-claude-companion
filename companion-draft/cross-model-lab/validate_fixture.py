"""Check this fixed fictional fixture, not model quality. Standard library only."""
import csv
import io
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
packet = (ROOT / "evidence-packet.md").read_text()
key = json.loads((ROOT / "answer-key.json").read_text())
cases = json.loads((ROOT / "cases.json").read_text())

def check(condition, message):
    if not condition:
        raise ValueError(message)

rows = list(csv.DictReader(io.StringIO(re.search(r"```csv\n(.*?)```", packet, re.S)[1])))
latest = {}
seen = set()
for row in rows:
    pair = (row["registration_id"], int(row["revision"]))
    check(pair not in seen, "Duplicate revision")
    seen.add(pair)
    check(row["status"] in {"confirmed", "cancelled", "waitlisted"}, "Invalid status")
    check(int(row["party_size"]) > 0, "Invalid party size")
    if pair[0] not in latest or pair[1] > int(latest[pair[0]]["revision"]):
        latest[pair[0]] = row
confirmed = {k: v for k, v in latest.items() if v["status"] == "confirmed"}
guests = sum(int(r["party_size"]) for r in confirmed.values())
check("Add two staff" in packet, "Staff rule changed; review fixture")
occupancy = guests + 2
check(sorted(confirmed) == key["C2"]["confirmed_registration_ids"], "Included IDs mismatch")
check(len(confirmed) == key["C2"]["confirmed_registrations"], "Registration count mismatch")
check(guests == key["C2"]["confirmed_guests"], "Guest count mismatch")
check(occupancy == key["C2"]["occupancy"], "Occupancy mismatch")
budget = int(re.search(r"maximum total commitment of \$(\d+)", packet)[1])
reserve_text = re.search(r"Reserve (.*?)these are separate", packet, re.S)[1]
reserves = [int(x) for x in re.findall(r"\$(\d+)", reserve_text)]
totals = {}
for source_id, name in [("S5", "North Hall"), ("S6", "Oak Room")]:
    section = re.search(rf"## {source_id} .*?(?=\n## |\Z)", packet, re.S)[0]
    capacity = int(re.search(r"Capacity: (\d+)", section)[1])
    room = int(re.search(r"Room: \$(\d+)", section)[1])
    cleaning = int(re.search(r"Mandatory cleaning: \$(\d+)", section)[1])
    projector = re.search(r"projector rental: \$(\d+)", section)
    venue_cost = room + cleaning + (int(projector[1]) if projector else 0)
    total = venue_cost + sum(reserves)
    expected = {"venue_cost": venue_cost, "event_commitment": total,
                "remaining_budget": budget - total, "capacity_margin": capacity - occupancy}
    check(expected == key["C3"][name], f"{name} arithmetic mismatch")
    check(total <= budget and occupancy <= capacity, f"{name} no longer eligible")
    totals[name] = total
check(min(totals, key=totals.get) == key["C4"]["recommended"], "Recommendation mismatch")
check(abs(totals["North Hall"] - totals["Oak Room"]) == key["C4"]["savings"], "Savings mismatch")
check([c["id"] for c in cases["cases"]] == [f"C{i}" for i in range(1, 6)], "Case IDs mismatch")
source_ids = set(re.findall(r"^## (S\d+)", packet, re.M))
for case in cases["cases"]:
    check(set(key[case["id"]]["source_ids"]) <= source_ids, "Missing source")
with (ROOT / "results-template.csv").open(newline="") as f:
    template = list(csv.reader(f))
check(len(template) == 1, "Results template must contain headers only")
check(len(template[0]) == len(set(template[0])), "Duplicate result fields")
print(json.dumps({"status": "passed", "registration_rows": len(rows),
                  "confirmed_registrations": len(confirmed), "guests": guests,
                  "occupancy": occupancy, "event_commitments": totals,
                  "case_count": len(cases["cases"]), "result_rows": 0,
                  "scope": "fixture arithmetic and structure only; no model calls"}, indent=2))
