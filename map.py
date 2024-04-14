
import numpy as np
from client import Client
from drone import Drone
import matplotlib.pyplot as plt

class Map:
    def __init__(self, depot_node):
        self.depot_node = depot_node
        self.clients = []
        self.drones = []


    def add_clients(self,node_modules):
        for node_module in node_modules:
            self.clients.append(Client(node_module[0],node_module[1],node_module[2]))

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
        # Extract coordinates
        x_coords = []
        y_coords = []
        for client in self.clients:
            x_coords.append(client.x)
            y_coords.append(client.y)

        # Create a plot
        plt.figure(figsize=(10, 8))
        plt.scatter(x_coords, y_coords, color='blue', marker='o')
        plt.scatter(self.depot_node[1], self.depot_node[2], color='red', marker='o')
        plt.title('Geographical Distribution of Nodes for CVRP')
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.grid(True)
        plt.show()






