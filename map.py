
import numpy as np
from client import Client
from drone import Drone
import matplotlib.pyplot as plt

class Map:
    def __init__(self):
        self.clients = []
        self.drone = None


    def add_clients(self,node_modules):
        for node_module in node_modules:
            self.clients.append(Client(node_module[0],node_module[1],node_module[2]))


    def print_cilents(self):
        for client in self.clients:
            print(client)

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
        plt.title('Geographical Distribution of Nodes for CVRP')
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.grid(True)
        plt.show()

    def add_drone(self,client_node):
        self.drone = Drone(self.clients)





