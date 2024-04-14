

class Drone:
    def __init__(self, id, start_node, capacity):
        self.id = id
        self.capacity = capacity
        self.num_of_packages = 0
        self.temp_client_id = None
        self.x,self.y = start_node[1],start_node[2]
        self.x_client, self.y_client = None,None
        self.prev_x_client, self.prev_y_client = None, None

    def __str__(self):
        return f"id: {self.id}, x: {self.x}, y {self.y}, capacity: {self.capacity}"



