

class Drone:
    def __init__(self, id, start_node, capacity):
        self.id = id
        self.current_capacity = capacity
        self.start_capacity = capacity
        self.temp_client_id = None
        self.depot_x = start_node[1]
        self.depot_y = start_node[2]
        self.x,self.y = start_node[1],start_node[2]
        self.x_client, self.y_client = None,None
        self.client_weight = 0
        self.prev_x_client, self.prev_y_client = None, None

    def __str__(self):
        return f"id: {self.id}, x: {self.x}, y {self.y}, current_capacity: {self.current_capacity}"

    # def add_route(self,node):
    #     print(f"Adding route: {node}")
    #     self.x_client = node.x
    #     self.y_client = node.y

    def move_to_next_node(self):
        self.y = self.y_client
        self.x = self.x_client
        if self.y is not self.depot_y and self.x is not self.depot_x:
            self.current_capacity -= self.client_weight
        else:
            self.visit_depot()

    def is_full(self,client_weight):
        if client_weight > self.current_capacity:
            return True
        return False

    def visit_depot(self):
        self.current_capacity = self.start_capacity












