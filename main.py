import re
import matplotlib.pyplot as plt
from map import Map
from drone import Drone

# Function to parse the VRP data file
def parse_vrp_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Data storage
    data = {
        "name": None,
        "dimension": None,
        "capacity": None,
        "node_coords": [],
        "demands": []
    }

    # Regex patterns
    name_pattern = re.compile(r'NAME\s*:\s*(\w+)')
    dimension_pattern = re.compile(r'DIMENSION\s*:\s*(\d+)')
    capacity_pattern = re.compile(r'CAPACITY\s*:\s*(\d+)')
    node_coord_pattern = re.compile(r'\d+\s+\d+\s+\d+')
    demand_section = False
    demand_pattern = re.compile(r'\d+\s+\d+')

    # Parse data
    for line in lines:
        if name_match := name_pattern.search(line):
            data["name"] = name_match.group(1)
        elif dimension_match := dimension_pattern.search(line):
            data["dimension"] = int(dimension_match.group(1))
        elif capacity_match := capacity_pattern.search(line):
            data["capacity"] = int(capacity_match.group(1))
        elif node_coord_match := node_coord_pattern.match(line):
            parts = line.split()
            data["node_coords"].append((int(parts[0]),int(parts[1]), int(parts[2])))
        elif 'DEMAND_SECTION' in line:
            demand_section = True
        elif demand_section:
            if demand_match := demand_pattern.match(line):
                parts = line.split()
                data["demands"].append((int(parts[0]), int(parts[1])))
            elif 'DEPOT_SECTION' in line:  # Assuming this marks the end of the DEMAND_SECTION
                break

    return data




# Main execution
if __name__ == "__main__":
    num_drones = 3
    file_path = r'data/att48.vrp'
    vrp_data = parse_vrp_file(file_path)

    depot_node = vrp_data['node_coords'][0]
    client_coords = vrp_data['node_coords'][1:] # all except 0 node
    client_capacity = vrp_data['demands'][1:]
    drones_capacity = vrp_data['capacity']



    map = Map(depot_node)
    map.add_clients(client_coords,client_capacity)
    map.print_clients()
    map.add_drones(num_drones, drones_capacity)
    map.print_drones()

    map.plot_node_distribution()

    map.add_route()
    map.move_drone()
    map.print_drones()

    map.plot_node_distribution()



