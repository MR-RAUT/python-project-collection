import os
import csv
from src.data_loader import load_data
from src.assignment import assign_packages_to_agents
from src.simulation import simulate_deliveries

# Normalize data structure for test cases
def normalize_data(data):
    # Normalize warehouses
    if isinstance(data.get("warehouses"), dict):
        data["warehouses"] = [
            {"id": k, "location": v}
            for k, v in data["warehouses"].items()
        ]

    # Normalize agents
    if isinstance(data.get("agents"), dict):
        data["agents"] = [
            {"id": k, "location": v}
            for k, v in data["agents"].items()
        ]

    # Normalize packages (warehouse -> warehouse_id)
    if data.get("packages"):
        sample = data["packages"][0]
        if "warehouse" in sample:
            for pkg in data["packages"]:
                pkg["warehouse_id"] = pkg.pop("warehouse")

    return data

# Run all test cases in the Test_cases directory
def run_all_test_cases():
    test_dir = "Test_cases"
    report_dir = os.path.join("output", "test_case_report")

    os.makedirs(report_dir, exist_ok=True)

    print("\nRunning FastBox Test Cases\n")

    # Iterate through all test case files
    for file in sorted(os.listdir(test_dir)):
        if not file.endswith(".json"):
            continue

        print(file)

        data = load_data(os.path.join(test_dir, file))
        data = normalize_data(data)

        assignments = assign_packages_to_agents(data)
        stats = simulate_deliveries(assignments, data)

        # Validate results
        total_packages = len(data["packages"])
        delivered = sum(
            agent["packages_delivered"] for agent in stats.values()
        )

        print(f"   Packages Expected : {total_packages}")
        print(f"   Packages Delivered: {delivered}")

        # Find best agent (lowest efficiency, must have delivered packages)
        best_agent = min(
            stats,
            key=lambda a: stats[a]["efficiency"]
            if stats[a]["packages_delivered"] > 0 else float("inf")
        )

        csv_name = file.replace(".json", "_report.csv")
        csv_path = os.path.join(report_dir, csv_name)
        
        # Save CSV report
        with open(csv_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "agent",
                "packages_delivered",
                "total_distance",
                "efficiency",
                "status"
            ])
            # Write each agent's stats
            for agent, data in stats.items():
                status = "best_agent" if agent == best_agent else ""

                writer.writerow([
                    agent,
                    data["packages_delivered"],
                    data["total_distance"],
                    data["efficiency"],
                    status
                ])

        # Final pass/fail check
        if total_packages == delivered:
            print(f"   PASS → {csv_name}\n")
        else:
            print(f"   FAIL → {csv_name}\n")


if __name__ == "__main__":
    run_all_test_cases()
