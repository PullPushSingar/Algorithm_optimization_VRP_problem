import math
import re
import matplotlib.pyplot as plt
from numpy import copy
from client import Client
from map import Map
from drone import Drone
import random
import copy
import time


max_iteration_without_improvment = 100
max_itteration_for_mval = 100
min_itteration_for_mval = 50
cadence = 5
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

    for path_id, path_list in paths.items():
        sorted_paths[path_id] = []
        
        for sub_path in path_list:
            nodes = sub_path[1:-1] 
            if not nodes:  
                sorted_paths[path_id].append(sub_path)
                continue
            
            closest_node_to_depot = min(nodes, key=lambda node: distances[(depot, node)])  
            sorted_sub_path = [sub_path[0], closest_node_to_depot] 
            current_node = closest_node_to_depot
            remaining_nodes = set(nodes) - {current_node} 

            while remaining_nodes:
                next_node = min(remaining_nodes, key=lambda node: distances[(current_node, node)])
                sorted_sub_path.append(next_node)
                remaining_nodes.remove(next_node)
                current_node = next_node

            sorted_sub_path.append(sub_path[-1])
            sorted_paths[path_id].append(sorted_sub_path)

    return sorted_paths


def genarate_random_solution(drons_list: list[Drone],  client_ids: list[int], base_id: int, clinet_weight_map: dict, cost_dictionary: dict) -> dict:
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
            client_weigth = 0
            path.append(base_id)
            while True:
                if client_iterrator >=len(client_random_ids):
                    break
                weight = clinet_weight_map[client_random_ids[client_iterrator]]
                if  client_weigth + weight <= dron.current_capacity:
                    path.append(client_random_ids[client_iterrator])
                    client_iterrator += 1
                    client_weigth += weight
                else:
                    break
            
            path.append(base_id)
            paths = drons_paths[dron.id]
            paths.append(path)
            drons_paths[dron.id] = paths

    return drons_paths



def __generate_client_weight_map(client_list: list[Client]):
    clinet_weight_map = {}
    for client in client_list:
        clinet_weight_map[client.id] = client.capacity

    return clinet_weight_map


def genarate_random_solution_no_capacity(drons_list: list[Drone], client_list: list[Client], base_id: int, cost_dictionary: dict) -> dict:
    drons_paths = {}
    client_ids = [client.id for client in client_list]
    client_random_ids = random.sample(client_ids, len(client_ids))
    dron_iterrator = 0

    for dron in drons_list:
        drons_paths[dron.id] = []
        path = []
        path.append(base_id)
        drons_paths[dron.id].append(path)


    for client in client_random_ids:
        drone_id = dron_iterrator % len(drons_list) + 1 
        drons_paths[drone_id][0].append(client)
        dron_iterrator += 1

    for drone in drons_list:
        drons_paths[drone.id][0].append(base_id)

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

def __calculate_cost_for_path(path,clinet_weight_map):
    cost =  0
    for node in path:
        if node == 1:
            continue
        cost += clinet_weight_map[node]
    return cost

def change_solution(current_soultion: dict, clinet_weight_map: dict, dron_capacity: int):
    moves = []
    candidate_to_solution = copy.deepcopy(current_soultion)
    for _ in range(1): 
        randmon_drons_id = random.sample(list(current_soultion.keys()), 2)
        dron__id_1 = randmon_drons_id[0]
        dron__id_2 = randmon_drons_id[1]

        
        for _ in range(10000):
            randmon_path_1_num =  random.randint(0, len(candidate_to_solution[dron__id_1])-1)
            randmon_path_2_num =  random.randint(0, len(candidate_to_solution[dron__id_2])-1)
            random_node_number_1 = random.randint(1, len(candidate_to_solution[dron__id_1][randmon_path_1_num])-2)
            random_node_number_2 = random.randint(1, len(candidate_to_solution[dron__id_2][randmon_path_2_num])-2)
            move = ((dron__id_1,randmon_path_1_num,random_node_number_1),(dron__id_2,randmon_path_2_num,random_node_number_2))
            value_1 = candidate_to_solution[dron__id_1][randmon_path_1_num][random_node_number_1]
            value_2 = candidate_to_solution[dron__id_2][randmon_path_2_num][random_node_number_2]
            cost_for_value_1 = __calculate_cost_for_path(candidate_to_solution[dron__id_1][randmon_path_1_num],clinet_weight_map)
            cost_for_value_2 = __calculate_cost_for_path(candidate_to_solution[dron__id_2][randmon_path_2_num],clinet_weight_map)

            # no capacity wariant
            # if move not in tabu:
            #     value_1 = candidate_to_solution[dron__id_1][randmon_path_1_num][random_node_number_1]
            #     value_2 = candidate_to_solution[dron__id_2][randmon_path_2_num][random_node_number_2]
            #     candidate_to_solution[dron__id_1][randmon_path_1_num][random_node_number_1] = value_2
            #     candidate_to_solution[dron__id_2][randmon_path_2_num][random_node_number_2] = value_1
            #     moves.append(move)
            #     break


            # capacity wariant
            if (move not in tabu) and (cost_for_value_1 + clinet_weight_map[value_2] - clinet_weight_map[value_1]  <= dron_capacity) and (cost_for_value_2 + clinet_weight_map[value_1] - clinet_weight_map[value_2]  <= dron_capacity) :
                candidate_to_solution[dron__id_1][randmon_path_1_num][random_node_number_1] = value_2
                candidate_to_solution[dron__id_2][randmon_path_2_num][random_node_number_2] = value_1
                moves.append(move)
                break

    
    return candidate_to_solution, moves
    
        
def caculate_new_solution(current_soultion: dict,cost_dictionary: dict, clinet_weight_map: dict, dron_capacity: int):
    MVal = {}
    current_cost = calculate_cost(current_soultion,cost_dictionary)
    itteration_for_mval = random.randint(min_itteration_for_mval,max_itteration_for_mval)
    for _ in range(itteration_for_mval):
        #strategia bez sortowania - bazowa
        # new_solition, moves =  change_solution(current_soultion, clinet_weight_map, dron_capacity)

        #strategia autorska z sortowaniem po odległości
        new_solition_unsorted, moves =  change_solution(current_soultion, clinet_weight_map, dron_capacity)
        new_solition = sort_nodes_by_distance(1, new_solition_unsorted, cost_dictionary) 
        
        new_cost = calculate_cost(new_solition,cost_dictionary)
        m_value = current_cost - new_cost
        MVal[m_value] = (new_solition, moves)
        
        # strategia aspiracji plus
        # if(m_value > 0):
        #     MVal_2 = {}
        #     for i in range(50):
        #         new_solition2, moves =  change_solution(current_soultion, clinet_weight_map, dron_capacity)
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
    clinet_weight_map = __generate_client_weight_map(client_list)

    # capacity wariant
    current_solution = genarate_random_solution(drons_list, [client.id for client in client_list], base_id, clinet_weight_map, cost_dictionary)
    # no capacity wariant
    # current_solution = genarate_random_solution_no_capacity(drons_list, client_list, base_id, cost_dictionary)

    best_solution = copy.deepcopy(current_solution)
    best_cost = calculate_cost(best_solution,cost_dictionary)
    cost_history.append(copy.deepcopy(best_cost))
    iteration_without_improvment = 0
    best_iteration = 0
    
    
    for i in range(iteration_number):
        (new_solition, moves) = caculate_new_solution(current_solution,cost_dictionary,clinet_weight_map, drons_list[0].current_capacity)
        new_cost = calculate_cost(new_solition,cost_dictionary)
        if  new_cost < best_cost:
            current_solution =  copy.deepcopy(new_solition)
            best_solution = copy.deepcopy(new_solition)
            best_cost = calculate_cost(best_solution,cost_dictionary)
            iteration_without_improvment = 0
            best_iteration = i
        cost_history.append(copy.deepcopy( best_cost))
        iteration_without_improvment += 1
        
        #strategia dywersyfikacji - metoda zdarzeń krytycznych
        # if iteration_without_improvment > max_iteration_without_improvment:
        #     current_solution = genarate_random_solution(drons_list, [client.id for client in client_list], base_id, clinet_weight_map, cost_dictionary)
        #     tabu.clear()
        #     iteration_without_improvment = 0
        #     print("new random solution")
        #     best_solution = copy.deepcopy(current_solution)
        #     best_cost = calculate_cost(best_solution,cost_dictionary)
        #     cost_history.append(copy.deepcopy(best_cost))

        for move in moves:
            tabu[move] = cadence

        for move_key, cadence in list(tabu.items()):
            new_cadence = cadence - 1
            if new_cadence == 0:
                del tabu[move_key]
            else:
                tabu[move_key] = new_cadence


    return best_solution, cost_history, best_iteration






if __name__ == "__main__":
    num_drones = 4
    file_path = r'data/att48.vrp'
    vrp_data = parse_vrp_file(file_path)

    depot_node = vrp_data['node_coords'][0]
    client_coords = vrp_data['node_coords'][1:] # all except 0 node
    client_capacity = vrp_data['demands'][1:]
    drones_capacity = vrp_data['capacity']
    
    map = Map(depot_node)
    map.add_clients(client_coords, client_capacity)
    # map.print_clients()
    map.add_drones(num_drones, drones_capacity)
    # map.print_drones()

    num_iterations = 1
    total_execution_time = 0
    total_best_cost = 0
    total_best_iteration = 0

    execution_times = []
    best_costs = []

    for i in range(num_iterations):
        start_time = time.time()
        best_solution, cost_history, best_iteration = tabu_search(500, map.drones, map.clients, depot_node[0], depot_node[1], depot_node[2])
        end_time = time.time()

        execution_time = end_time - start_time
        best_cost = cost_history[-1]

        execution_times.append(execution_time)
        best_costs.append(best_cost)

        total_execution_time += execution_time
        total_best_cost += best_cost
        total_best_iteration += best_iteration

        print(f"Iteration {i+1}: Execution time = {execution_time:.4f} sec, Best cost = {best_cost} at {best_iteration} iteration")

    avg_execution_time = total_execution_time / num_iterations
    avg_best_cost = total_best_cost / num_iterations
    avg_best_iter = total_best_iteration / num_iterations

    print(f"\nAverage execution time over {num_iterations} iterations: {avg_execution_time:.4f} sec")
    print(f"Average best cost over {num_iterations} iterations: {avg_best_cost}")
    print(f"Average best cost iteration: {avg_best_iter}")

    plt.title('Cost history (Last iteration)')
    plt.xlabel('iteration')
    plt.ylabel('cost')
    plt.grid(True)
    plt.plot(cost_history)
    plt.show()

    print(best_solution)
    map.plot_node_distribution(best_solution)




