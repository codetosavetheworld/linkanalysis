
from py2neo import Graph, Node, Relationship
# from py2neo.server import GraphSever

class Network():
    def __init__(self):
        # self.server = GraphSever()
        # self.server.start()
        self.graph_instance = Graph()
    
    
    def add_node(self, link, date_last_updated, frequency):
        print("here")
        calculated_frequency = convert_frequency_to_hours(frequency)
        n = Node(link, date_last_updated = date_last_updated, frequency = frequency, calculated_frequency = calculated_frequency)
        self.graph_instance.create(n)
    
    def add_edge(self, node_u, node_v, relation):
        self.graph_instance.create(Relationship(node_u, "links to", node_v, tag = relation))

def convert_frequency_to_hours(frequency):
    if (frequency == "always" or frequency == ""):
        return 0
    if (frequency == "hourly"):
        return 1
    if (frequency == "daily"):
        return 24
    if (frequency == "weekly"):
        return 7*24
    if (frequency == "monthly"):
        return 30*24
    if (frequency == "yearly"):
        return 365*24
    if (frequency == "never"):
        return -1


n = Network()
n.add_node("www.example.com", "2015-05-02", "daily")
