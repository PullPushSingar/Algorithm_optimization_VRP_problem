

class Drone:
    def __init__(self,start_node):
        self.id = start_node[0]
        self.capacity = 0
        self.num_of_packages = 0
        self.temp_cleint_id = None
        self.x,self.y = start_node[1],start_node[2]
        self.x_client, self.y_client = None,None
        self.prev_x_client, self.prev_y_client = None, None


    def set_depot_location(self,x,y):
        self.x,self.y = x,y

    def set_capacity(self,capacity):
        self.capacity = capacity


