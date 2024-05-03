

class Drone:
    def __init__(self, id, start_node, capacity):
        self.id = id
        self.capacity = capacity
        self.num_of_packages = 0
        self.temp_client_id = None
        self.depot_x = start_node[1]
        self.depot_y = start_node[2]
        self.x,self.y = start_node[1],start_node[2]
        self.x_client, self.y_client = None,None
        self.prev_x_client, self.prev_y_client = None, None
        self.distance = 0

    def __str__(self):
        return f"id: {self.id}, x: {self.x}, y {self.y}, capacity: {self.capacity}"

    def add_route(self,node):
        print(f"Adding route: {node}")
        self.x_client = node.x
        self.y_client = node.y

    def move(self,x,y):
        if x > self.x:
            self.x += 1
        elif x < self.x:
            self.x -= 1
        elif y > self.y:
            self.y +=1
        elif y < self.y:
            self.y -=1
        self.distance += 1












