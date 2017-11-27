
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

    def add_edge(self, node_u, node_v_link, relationship):
        #if the relationship not exist create new edge
        #else update the tag
        self.add_node(node_v_link, "","")
        node_v = self.get_node(node_v_link)
        self.graph_instance.create(Relationship(node_u, "links to", node_v, tag = relationship))



    def delete_failed_webpages(self,link):
        node = self.get_node(link)
        self.delete_relationship(node)
        self.delete_incoming_relationship(node)
        self.graph_instance.delete(node)
    

    def check_node_exist(self, link):
        return len(list(self.graph_instance.find(link))) != 0

 
    def delete_relationship(self,node_u):
        rels = list(self.graph_instance.match(rel_type="links to",start_node= node_u,end_node = None))
        for r in rels:
            self.graph_instance.separate(r)


    def delete_incoming_relationship(self,node_u):
        rels = list(self.graph_instance.match(rel_type="links to",end_node= node_u,start_node = None))
        for r in rels:
            self.graph_instance.separate(r)

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


