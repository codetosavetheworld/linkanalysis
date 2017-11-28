
from py2neo import Graph, Node, Relationship
# from py2neo.server import GraphSever
import numpy as np
import scipy
import scipy.sparse

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
        return n


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

    
   def delete_failed_webpages(self,link):
       node = self.get_node(link)
       self.delete_relationship(node)
       self.delete_incoming_relationship(node)
       self.graph_instance.delete(node)

    
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

    def _to_matrix(self):
        #Get adjacency matrix of the neo4j graph
        #to be used for pagerank
        # Get the nodes from py2neo
        nodes = list(self.graph_instance.node_selector.select())
        N = len(nodes)
        mat = np.zeros((N,N))
        # Populate the adjacency matrix
        for i, a in enumerate(nodes):
            for j, b in enumerate(nodes):
                # Use existing function to check for link
                mat[i,j] = self.check_relationship_exist(a, b)
        return mat


    def update_pagerank(self):
        #Iterate over nodes and add pagerank
        
        # Get all the nodes
        nodes = self.graph_instance.node_selector.select()
        # Iterate over the result of _pagerank and the nodes
        for pr, node in zip(self._pagerank(), nodes):
            # Update the node's pagerank and push back to neo4j
            node.update(page_rank= pr)
            self.graph_instance.push(node)


    def show_pagerank(self, selector=None, link=None):
        #Simple show function to get nodes and display their pagerank
        
        if selector:
            nodes = self.graph_instance.node_selector.select(selector)
        elif link:
            nodes = [ self.graph_instance.find_one(link) ]
        else:
            nodes = self.graph_instance.node_selector.select()
        for node in nodes:
            print(list(node.labels())[0], node.get('page_rank'))


    def get_pagerank_dict(self, links=[]):
        #Get the pageranks for any given list of links (or all)
        
        if links:
            nodes = [self.graph_instance.find_one(link) for link in links]
        else:
            nodes = self.graph_instance.node_selector.select()
        return { list(node.labels())[0] : node.get('page_rank') for node in nodes}


    def _pagerank(
            self,
            alpha=0.85,
            max_iter=100,   # Increase this if we get the non-convergence error
            tol=1.0e-6,
            ):
        
        #Perform pagerank on the adjacency matrix, using the power method
        # Create a sparse matrix rep. of adjacency matrix
        mat = scipy.sparse.csr_matrix(self._to_matrix())
        n,m = mat.shape
        # Make a sum matrix
        S = scipy.array(mat.sum(axis=1)).flatten()
        # Get non-zero rows
        index=scipy.where(S<>0)[0]
        for i in index:
            # We need to normlize (divide by sum)
            mat[i,:]*=1.0/S[i]
        #
        pr = scipy.ones((n))/n  # initial guess
        # Get dangling nodes
        dangling = scipy.array(scipy.where(mat.sum(axis=1)==0,1.0/n,0)).flatten()
        for i in range(max_iter):
            prlast=pr
            pr=alpha*(pr*mat+scipy.dot(dangling,prlast))+(1-alpha)*prlast.sum()/n
            # check if we're done
            err=scipy.absolute(pr-prlast).sum()
            if err < n*tol:
                return pr
        raise Exception("pagerank failed to converge [%d iterations]"%(i+1))

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


#more test cases in test.py
# n = Network()
# #just for test
# n.add_node("www.example.com", "2015-05-02", "daily")
# n.add_node("www.example2.com", "2017-07-02", "hourly")
# n.add_node("www.example3.com", "2017-07-01", "hourly")

# n1 = n.get_node("www.example.com")
# n2 = n.get_node("www.example2.com")
# n3 = n.get_node("www.example3.com")

# n.add_edge(n1,n2,"<h1>")
# n.add_edge(n3,n2,"<h1>")
# n.add_edge(n1,n2,"<h3>")

