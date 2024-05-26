import time

import numpy as np

import drone
from client import Client
from drone import Drone
import matplotlib.pyplot as plt
import math

class Map:
    def __init__(self, depot_node):
        self.depot_node = depot_node
        self.clients = []
        self.drones = []
        self.map_range = []
        self.map_range_calculated = False



    def add_clients(self,node_modules,capacity):
        for node_module,capacity in zip(node_modules,capacity):

            self.clients.append(Client(node_module[0],node_module[1],node_module[2],capacity[1]))

    def add_drones(self, num, capacity):
        for i in range(num):
            self.drones.append(Drone(i+1, self.depot_node, capacity))


    def print_clients(self):
        print("Clients: ")
        for client in self.clients:
            print(client)

    def print_drones(self):
        print("Drones: ")
        for drone in self.drones:
            print(drone)

    def calculate_map_range(self):
        self.map_range.append(min([client.x for client in self.clients] + [drone.x for drone in self.drones] + [self.depot_node[1]])-100)
        self.map_range.append(max([client.x for client in self.clients] + [drone.x for drone in self.drones] + [self.depot_node[1]])+100)
        self.map_range.append(min([client.y for client in self.clients] + [drone.y for drone in self.drones] + [self.depot_node[2]])-100)
        self.map_range.append(max([client.y for client in self.clients] + [drone.y for drone in self.drones] + [self.depot_node[2]])+100)
        self.map_range_calculated = True


    def plot_node_distribution(self, best_solution):
        if not self.map_range_calculated:
            self.calculate_map_range()

        x_coords = []
        y_coords = []
        x_drone = []
        y_drone = []
        client_ids = []

        for client in self.clients:
            x_coords.append(client.x)
            y_coords.append(client.y)
            client_ids.append(client.id)

        for drone in self.drones:
            x_drone.append(drone.x)
            y_drone.append(drone.y)

        plt.figure(figsize=(10, 8))
        plt.scatter(x_coords, y_coords, color='blue', marker='o')
        plt.scatter(self.depot_node[1], self.depot_node[2], color='red', marker='o')

        colors = ['magenta', 'orange', 'yellow', 'green', 'cyan', 'purple']
        for i, (x, y) in enumerate(zip(x_drone, y_drone)):
            plt.scatter(x, y, color=colors[i % len(colors)], marker='o')

        for i, txt in enumerate(client_ids):
            plt.annotate(txt, (x_coords[i], y_coords[i]), textcoords="offset points", xytext=(0, 5), ha='center')

        # Rysowanie ścieżek
        for color_idx, (key, routes) in enumerate(best_solution.items()):
            for route in routes:
                route_x = [self.depot_node[1] if node == 1 else self.clients[node - 2].x for node in route]
                route_y = [self.depot_node[2] if node == 1 else self.clients[node - 2].y for node in route]
                plt.plot(route_x, route_y, color=colors[color_idx % len(colors)], linewidth=2)

        plt.title('Geographical Distribution of Nodes for CVRP')
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.grid(True)
        plt.xlim(self.map_range[0], self.map_range[1])
        plt.ylim(self.map_range[2], self.map_range[3])
        plt.show()

    def move_drones(self):

        for drone in self.drones:
            self.choose_nearest_node(drone)
            drone.move_to_next_node()
            visited_client = self.find_visited_client(drone)
            if visited_client is not None:
                self.clients.remove(visited_client)


    def choose_nearest_node(self, drone):
            nearest_distance = float('inf')
            nearest_x = None
            nearest_y = None
            for node in self.clients:
                distance = math.sqrt((drone.x - node.x)**2 + (drone.y - node.y)**2)
                if distance < nearest_distance and not drone.is_full(node.capacity):
                    nearest_distance = distance
                    nearest_x = node.x
                    nearest_y = node.y
                    nearest_node_weight= node.capacity
                elif drone.is_full(node.capacity):
                    drone.x_client = self.depot_node[1]
                    drone.y_client = self.depot_node[2]

            if nearest_x is not None and nearest_y is not None:
                drone.x_client = nearest_x
                drone.y_client = nearest_y
                drone.client_weight = nearest_node_weight
            else:
                drone.x_client = self.depot_node[1]
                drone.y_client = self.depot_node[2]

    def find_visited_client(self, drone):
        for client in self.clients:
            if client.x == drone.x and client.y == drone.y:
                return client
        return None

















