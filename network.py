
from py2neo import Graph, Node, Relationship
# from py2neo.server import GraphSever

class Network():
    def __init__(self):
        # self.server = GraphSever()
        # self.server.start()
        self.graph_instance = Graph()


    def add_node(self, link, date_last_updated, frequency):
        # check if the node exist
        # if node not exist create a new node
        # if node exist update the node
        calculated_frequency = convert_frequency_to_hours(frequency)
      
        if (not self.check_node_exist(link)):
            n = Node(link, date_last_updated = date_last_updated, frequency = frequency, calculated_frequency = calculated_frequency)
            self.graph_instance.create(n)
        else:
            n = self.graph_instance.find_one(link)
            n["date_last_updated"] = date_last_updated
            n["calculated_frequency"] = calculated_frequency
            n["frequency"] = frequency
            n.push()

    
    def add_edge(self, node_u, node_v, relationship):
        #if the relationship not exist create new edge
        #else update the tag
        if not self.check_relationship_exist(node_u,node_v):
            self.graph_instance.create(Relationship(node_u, "links to", node_v, tag = relationship))
        else:
            for l in list(self.graph_instance.match(start_node = node_u, end_node = node_v, rel_type = "links to")):
                l["tag"] = relationship
                l.push()


    def check_node_exist(self, link):
        return len(list(self.graph_instance.find(link))) != 0

    def check_relationship_exist(self,node_u, node_v):
        return len(list(self.graph_instance.match(start_node = node_u, end_node = node_v, rel_type = "links to"))) > 0
    
    def get_node(self,link):
        return self.graph_instance.find_one(link)



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
#just for test
n.add_node("www.example.com", "2015-05-02", "daily")
n.add_node("www.example2.com", "2017-07-02", "hourly")

n1 = n.get_node("www.example.com")
n2 = n.get_node("www.example2.com")

n.add_edge(n1,n2,"<h1>")


n.check_relationship_exist(n1,n2)
n.add_edge(n1,n2,"<h3>")




