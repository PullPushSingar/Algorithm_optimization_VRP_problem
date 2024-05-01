import numpy as np


class Client:
    """
    id Identifier
    x, y Coordinates
    """

    def __init__(self,id,x,y,capacity):
        self.id = id
        self.x,self.y = x,y
        self.capacity = capacity


    def __str__(self):
        return f"id: {self.id}, x: {self.x},y {self.y}, capacity: {self.capacity}"

    def __repr__(self, other):
        return self.id == other.id

    def get_distance_from(self,other):
        return np.sqrt((self.x-other.x)**2+(self.y-other.y)**2)
