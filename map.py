import time

import numpy as np

import drone
from client import Client
from drone import Drone
import matplotlib.pyplot as plt

class Map:
    def __init__(self, depot_node):
        self.depot_node = depot_node
        self.clients = []
        self.drones = []


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

    def plot_node_distribution(self):

        x_coords = []
        y_coords = []
        x_drone = []
        y_drone= []


        for client in self.clients:
            x_coords.append(client.x)
            y_coords.append(client.y)

        for drone in self.drones:
            x_drone.append(drone.x)
            y_drone.append(drone.y)


        plt.figure(figsize=(10, 8))
        plt.scatter(x_coords, y_coords, color='blue', marker='o')
        plt.scatter(self.depot_node[1], self.depot_node[2], color='red', marker='o')
        plt.scatter(x_drone, y_drone, color='green', marker='o')
        plt.title('Geographical Distribution of Nodes for CVRP')
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.grid(True)
        plt.show()

    def add_route(self):

        self.choose_nearest_node()
        print("Adding route")

    def move_drone(self):
        if self.is_drone_visit_client():
            visited_client = self.visit_drone()
            if visited_client in self.clients:
                self.clients.remove(visited_client)
                print("remove Client")
                self.plot_node_distribution()
                time.sleep(5)
            self.choose_nearest_node()
        for drone in self.drones:
            drone.move(drone.x_client, drone.y_client)

    def choose_nearest_node(self):
        for drone in self.drones:
            nearest_distance = float('inf')
            nearest_x = None
            nearest_y = None
            for node in self.clients:
                distance = abs(drone.x - node.x) + abs(
                    drone.y - node.y)
                if distance < nearest_distance:
                    nearest_distance = distance
                    nearest_x = node.x
                    nearest_y = node.y
            if nearest_x is not None and nearest_y is not None:
                drone.x_client = nearest_x
                drone.y_client = nearest_y

    def is_drone_visit_client(self):
        for drone in self.drones:
            if drone.y == drone.y_client and drone.x == drone.x_client:
                return True
        return False

    def visit_drone(self):
        for client in self.clients:
            for drone in self.drones:
                if client.x == drone.x and client.y == drone.y:
                    return client















