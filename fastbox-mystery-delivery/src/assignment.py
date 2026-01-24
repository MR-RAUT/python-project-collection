from src.distance import euclidean_distance

# Assign packages to agents based on nearest warehouse
def assign_packages_to_agents(data):
    warehouses = data["warehouses"]
    agents = data["agents"]
    packages = data["packages"]

    # Create a map of warehouse IDs to their locations
    warehouse_map = {
        wh["id"]: wh["location"] for wh in warehouses
    }

    # Initialize assignments dictionary
    assignments = {
        agent["id"]: [] for agent in agents
    }

    # Assign each package to the nearest agent based on warehouse location
    for package in packages:
        warehouse_location = warehouse_map[package["warehouse_id"]]

        nearest_agent = None
        min_distance = float("inf")

        # Find the nearest agent to the warehouse
        for agent in agents:
            distance = euclidean_distance(
                agent["location"],
                warehouse_location
            )

            # Update nearest agent if this one is closer
            if distance < min_distance:
                min_distance = distance
                nearest_agent = agent["id"]

        assignments[nearest_agent].append(package)

    # Return the assignments
    return assignments
