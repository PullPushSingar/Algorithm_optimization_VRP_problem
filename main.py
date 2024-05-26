import math
import re
import matplotlib.pyplot as plt
from numpy import copy
from client import Client
from map import Map
from drone import Drone
import random
import copy


max_iteration_without_improvment = 500
max_itteration_for_mval = 100
min_itteration_for_mval = 50
cadence = 25
tabu = {}


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

def sort_nodes_by_distance(depot, paths, distances):
    sorted_paths = {}
    for path_id, path in paths.items():
        closest_node_to_depot = min(path[0][1:-1], key=lambda node: distances[(depot, node)])
        # print("path id: ", path_id)
        # print("closest: ", closest_node_to_depot)
        sorted_path = [path[0][0]] 
        sorted_path.append(closest_node_to_depot)  # Dodajemy najbliższy węzeł do depo
        current_node = closest_node_to_depot
        remaining_nodes = set(path[0][1:-1])  # Pomijamy pierwszy i ostatni węzeł
        remaining_nodes.remove(current_node)

        while remaining_nodes:
            next_node = min(remaining_nodes, key=lambda node: distances[(current_node, node)])
            sorted_path.append(next_node)
            remaining_nodes.remove(next_node)
            current_node = next_node

        sorted_paths[path_id] = [sorted_path + [path[0][-1]]]  # Dodajemy ostatni węzeł
        print("sorted: ", sorted_paths)
    return sorted_paths

def genarate_random_solution(drons_list: list[Drone], client_ids: list[int], base_id: int, cost_dictionary: dict) -> dict:
    drons_paths = {}
    
    client_random_ids = random.sample(client_ids, len(client_ids))
    client_iterrator = 0

    for dron in drons_list:
        drons_paths[dron.id] = []

    while client_iterrator < len(client_random_ids):
        for dron in drons_list:
            if client_iterrator >=len(client_random_ids):
                break
            path = []
            path.append(base_id)
            for _ in range(dron.current_capacity):
                if client_iterrator >=len(client_random_ids):
                    break
                path.append(client_random_ids[client_iterrator])
                client_iterrator += 1
            
            path.append(base_id)
            paths = drons_paths[dron.id]
            paths.append(path)
            drons_paths[dron.id] = paths

    # return sort_nodes_by_distance(base_id, drons_paths, cost_dictionary)
    return drons_paths


def crate_cost_dictionary(client_list: list[Client], base_x: int, base_y: int, base_id:int) -> dict:
    cost_dictionary = {}
    for client_1 in client_list:
        distance_base_to_node = math.sqrt((base_x - client_1.x)**2 + (base_y- client_1.y)**2)
        cost_dictionary[(client_1.id, base_id)] = cost_dictionary[(base_id, client_1.id)] = distance_base_to_node

        for client_2 in client_list:
            if client_1.id != client_2.id:
                distance_node_to_node = math.sqrt((client_1.x - client_2.x)**2 + (client_1.y - client_2.y)**2)
                cost_dictionary[(client_1.id, client_2.id)] = cost_dictionary[(client_2.id, client_1.id)] = distance_node_to_node

    return cost_dictionary


#TO DO: pomyśleć jak można to ulepszyć
def change_solution(current_soultion: dict):
    moves = []
    candidate_to_solution = copy.deepcopy(current_soultion)
    for _ in range(1): #czy nie lepiej 1?
        randmon_drons_id = random.sample(list(current_soultion.keys()), 2)
        dron__id_1 = randmon_drons_id[0]
        dron__id_2 = randmon_drons_id[1]

        
        while True:
            randmon_path_1_num =  random.randint(0, len(candidate_to_solution[dron__id_1])-1)
            randmon_path_2_num =  random.randint(0, len(candidate_to_solution[dron__id_2])-1)
            random_node_number_1 = random.randint(1, len(candidate_to_solution[dron__id_1][randmon_path_1_num])-2)
            random_node_number_2 = random.randint(1, len(candidate_to_solution[dron__id_2][randmon_path_2_num])-2)
            move = ((dron__id_1,randmon_path_1_num,random_node_number_1),(dron__id_2,randmon_path_2_num,random_node_number_2))

            if move not in tabu:
                value_1 = candidate_to_solution[dron__id_1][randmon_path_1_num][random_node_number_1]
                value_2 = candidate_to_solution[dron__id_2][randmon_path_2_num][random_node_number_2]
                candidate_to_solution[dron__id_1][randmon_path_1_num][random_node_number_1] = value_2
                candidate_to_solution[dron__id_2][randmon_path_2_num][random_node_number_2] = value_1
                moves.append(move)
                break

    
    return candidate_to_solution, moves
    
def change_solution2(current_soultion: dict):
    moves = []
    candidate_to_solution = copy.deepcopy(current_soultion)
    for dron__id_1 in range(1, len(current_soultion)+1): 
        for dron__id_2 in range(dron__id_1, len(current_soultion)+1):
            while True:
                randmon_path_1_num =  random.randint(0, len(candidate_to_solution[dron__id_1])-1)
                randmon_path_2_num =  random.randint(0, len(candidate_to_solution[dron__id_2])-1)
                random_node_number_1 = random.randint(1, len(candidate_to_solution[dron__id_1][randmon_path_1_num])-2)
                random_node_number_2 = random.randint(1, len(candidate_to_solution[dron__id_2][randmon_path_2_num])-2)
                move = ((dron__id_1,randmon_path_1_num,random_node_number_1),(dron__id_2,randmon_path_2_num,random_node_number_2))

                if move not in tabu:
                    value_1 = candidate_to_solution[dron__id_1][randmon_path_1_num][random_node_number_1]
                    value_2 = candidate_to_solution[dron__id_2][randmon_path_2_num][random_node_number_2]
                    candidate_to_solution[dron__id_1][randmon_path_1_num][random_node_number_1] = value_2
                    candidate_to_solution[dron__id_2][randmon_path_2_num][random_node_number_2] = value_1
                    moves.append(move)
                    break

    
    return candidate_to_solution, moves
        
def caculate_new_solution(current_soultion: dict,cost_dictionary: dict):
    MVal = {}
    current_cost = calculate_cost(current_soultion,cost_dictionary)
    itteration_for_mval = random.randint(min_itteration_for_mval,max_itteration_for_mval)
    for _ in range(itteration_for_mval):
        new_solition, moves =  change_solution(current_soultion)
        new_cost = calculate_cost(new_solition,cost_dictionary)
        m_value = current_cost - new_cost
        MVal[m_value] = (new_solition, moves)
        
        # if(m_value > 0):
        #     MVal_2 = {}
        #     for i in range(10):
        #         new_solition2, moves =  change_solution2(new_solition)
        #         new_cost = calculate_cost(new_solition2,cost_dictionary)
        #         m_value = current_cost - new_cost
        #         MVal_2[m_value] = (new_solition2, moves)
        #         max_m_value2 = max(MVal_2.keys())
        #         # print("it:", i, m_value)
        #         # print("max: ", max_m_value2)
        #     MVal[max_m_value2] = MVal_2[max_m_value2]
        # # print("maxmax: ", max_m_value2)

    max_m_value = max(MVal.keys())
    return MVal[max_m_value]


def calculate_cost(solution: dict, cost_dictionary: dict):
    cost = 0
    for paths in solution.values():
        for path in paths:
            for i in range(len(path) - 1):
                cost  += cost_dictionary[(path[i],path[i+1])]
    return cost



def tabu_search(iteration_number: int, drons_list: list[Drone], client_list: list[Client], base_id: int, base_x: int, base_y: int):
    global cadence
    cost_history = []
    cost_dictionary = crate_cost_dictionary(client_list, base_x, base_y, base_id)
    current_solution = genarate_random_solution(drons_list, [client.id for client in client_list], base_id, cost_dictionary)
    best_solution = copy.deepcopy(current_solution)
    best_cost = calculate_cost(best_solution,cost_dictionary)
    cost_history.append(copy.deepcopy(best_cost))
    iteration_without_improvment = 0
    
    
    for _ in range(iteration_number):
        (new_solition, moves) = caculate_new_solution(current_solution,cost_dictionary)
        new_cost = calculate_cost(new_solition,cost_dictionary)
        if  new_cost < best_cost:
            current_solution =  copy.deepcopy(new_solition)
            best_solution = copy.deepcopy(new_solition)
            best_cost = calculate_cost(best_solution,cost_dictionary)
            cost_history.append(copy.deepcopy( best_cost))
            iteration_without_improvment = 0
        iteration_without_improvment += 1
        
        # if iteration_without_improvment > max_iteration_without_improvment:
        #     current_solution = genarate_random_solution(drons_list, [client.id for client in client_list], base_id, cost_dictionary)
        #     new_cost = calculate_cost(current_solution,cost_dictionary)
        #     if  new_cost < best_cost:
        #         best_solution = copy.deepcopy(current_solution)
        #         best_cost = calculate_cost(best_solution,cost_dictionary)
        #         cost_history.append(copy.deepcopy( best_cost))
        #         cost_history.append(1)
        #     tabu.clear()

        for move in moves:
            tabu[move] = cadence

        for move_key, cadence in list(tabu.items()):
            new_cadence = cadence - 1
            if new_cadence == 0:
                del tabu[move_key]
            else:
                tabu[move_key] = new_cadence

    print(cost_history)
    plt.plot(cost_history)
    plt.show()

    return best_solution






if __name__ == "__main__":
    num_drones = 5
    file_path = r'data/att48.vrp'
    vrp_data = parse_vrp_file(file_path)

    depot_node = vrp_data['node_coords'][0]
    client_coords = vrp_data['node_coords'][1:] # all except 0 node
    client_capacity = vrp_data['demands'][1:]
    drones_capacity = vrp_data['capacity']
    
    map = Map(depot_node)
    map.add_clients(client_coords,client_capacity)
    #map.print_clients()
    map.add_drones(num_drones, drones_capacity)
    #map.print_drones()
    
    best_solution = tabu_search(10000, map.drones, map.clients, depot_node[0], depot_node[1], depot_node[2])
    print(best_solution)

    # for i in range(10):
    #     tabu_search(10000, map.drones, map.clients, depot_node[0], depot_node[1], depot_node[2])

    map.plot_node_distribution(best_solution)

    # while len(map.clients) != 0:
    #     map.move_drones()
    #     map.print_drones()
    #     map.plot_node_distribution()

    # map.move_drones()
    # map.print_drones()
    # map.plot_node_distribution()



