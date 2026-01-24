import random
from src.distance import euclidean_distance


# Simulate deliveries based on assignments and data
def simulate_deliveries(assignments, data, enable_delay=False):
    warehouses = data["warehouses"]
    agents = data["agents"]

    # Create a map of warehouse IDs to their locations
    warehouse_map = {
        wh["id"]: wh["location"] for wh in warehouses
    }

    # Create a map of agent IDs to their locations
    agent_map = {
        agent["id"]: agent["location"] for agent in agents
    }

    report = {}

    # Simulate each agent's deliveries
    for agent_id, packages in assignments.items():
        current_position = agent_map[agent_id]
        total_distance = 0.0
        delivered = 0

        # Deliver each package
        for package in packages:
            warehouse_pos = warehouse_map[package["warehouse_id"]]
            destination_pos = package["destination"]

            # Normal travel distance
            total_distance += euclidean_distance(current_position, warehouse_pos)
            total_distance += euclidean_distance(warehouse_pos, destination_pos)

            # Update current position to destination
            # Random delivery delay
            if enable_delay and random.random() < 0.2:  # 20% chance
                delay_distance = random.uniform(1, 5)
                total_distance += delay_distance

            current_position = destination_pos
            delivered += 1

        # Calculate efficiency
        efficiency = total_distance / delivered if delivered else 0
        
        # Record agent's stats
        report[agent_id] = {
            "packages_delivered": delivered,
            "total_distance": round(total_distance, 2),
            "efficiency": round(efficiency, 2)
        }

    return report
