"""Export a first reproducible synthetic test report to CSV and JSON."""
import csv
import json
from pathlib import Path
from aeb import Scenario, simulate

SCENARIOS = [
    Scenario("safe_stop", gap_m=30, ego_speed_mps=15, lead_speed_mps=0),
    Scenario("late_detection", gap_m=8, ego_speed_mps=20, lead_speed_mps=0, response_delay_s=0.5, braking_mps2=4),
    Scenario("same_speed", gap_m=25, ego_speed_mps=10, lead_speed_mps=10),
    Scenario("moving_lead_vehicle", gap_m=24, ego_speed_mps=18, lead_speed_mps=8),
]


def main():
    results = [simulate(s) for s in SCENARIOS]
    output = Path("reports")
    output.mkdir(parents=True, exist_ok=True)
    (output / "aeb_results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    with (output / "aeb_results.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(results[0]))
        writer.writeheader()
        writer.writerows(results)
    for item in results:
        print(f"{item['scenario']}: collision={item['collision']}, triggered={item['aeb_triggered']}, TTC={item['initial_ttc_s']}")
    print("Reports: reports/aeb_results.csv and reports/aeb_results.json")


if __name__ == "__main__":
    main()
