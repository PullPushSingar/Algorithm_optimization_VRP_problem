import re


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
            data["node_coords"].append((int(parts[1]), int(parts[2])))

    return data