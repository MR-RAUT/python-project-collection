import json
import csv

# Generates report in JSON and CSV formats
def generate_report(stats, json_path, csv_path):

    # Find best agent based on efficiency
    best_agent = min(
        stats,
        key=lambda a: stats[a]["efficiency"]
        if stats[a]["packages_delivered"] > 0 else float("inf")
    )

    # Create final report structure
    final_report = stats.copy()
    final_report["best_agent"] = best_agent

    # Save JSON report
    with open(json_path, "w") as f:
        json.dump(final_report, f, indent=4)

    # Save CSV report
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)

        # Write header
        writer.writerow([
            "Agent",
            "Packages_delivered",
            "Total_distance",
            "Efficiency",
            "Status"
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
