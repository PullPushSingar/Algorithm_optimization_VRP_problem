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
        "node_coords": []
    }

    # Regex patterns
    name_pattern = re.compile(r'NAME\s*:\s*(\w+)')
    dimension_pattern = re.compile(r'DIMENSION\s*:\s*(\d+)')
    capacity_pattern = re.compile(r'CAPACITY\s*:\s*(\d+)')
    node_coord_pattern = re.compile(r'\d+\s+\d+\s+\d+')

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

    return data



# Main execution
if __name__ == "__main__":
    file_path = r'data/att48.vrp'
    vrp_data = parse_vrp_file(file_path)


    print(vrp_data['node_coords'])
    client_cords = vrp_data['node_coords']
    map = Map()
    map.add_clients(client_cords)
    map.print_cilents()
    map.plot_node_distribution()
    map.add_drone()
    map.drone.set_capacity(vrp_data['capacity'])



