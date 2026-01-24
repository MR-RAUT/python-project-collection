from src.data_loader import load_data
from src.distance import euclidean_distance
from src.assignment import assign_packages_to_agents
from src.simulation import simulate_deliveries
from src.report import generate_report


def main():
    # --------------------------------
    # Load base_case.json data or data.json

    data = load_data("base_case.json")
    # data = load_data("data/data.json")

    # --------------------------------
    # New agent joins mid-day 
    data["agents"].append({
        "id": "A4",
        "location": [20, 20]
    })

    # --------------------------------
    # Distance sanity check (optional)
    # print("Distance A1 -> W1:", euclidean_distance([5, 5], [0, 0]))

    # --------------------------------
    # Assign packages to agents
    assignments = assign_packages_to_agents(data)

    # DEBUG assignment (KEEP THIS HERE)
    print("DEBUG assignments:")
    for agent, pkgs in assignments.items():
        print(agent, [p["id"] for p in pkgs])

    # --------------------------------
    # Simulate deliveries
    stats = simulate_deliveries(assignments, data, enable_delay=True)

    # DEBUG simulation output
    # for agent, info in stats.items():
    #     print(agent, info)

    # --------------------------------
    # Generate report
    generate_report(
        stats,
        json_path="output/report.json",
        csv_path="output/top_agent.csv"
    )

    print("✅ FastBox Simulation Completed Successfully")


if __name__ == "__main__":
    main()
