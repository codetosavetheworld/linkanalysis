
from py2neo import Graph, Node, Relationship
# from py2neo.server import GraphSever
import numpy as np
import scipy
import scipy.sparse
import datetime

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
            # Calculate initial calculated frequency
            n = Node(link, date_last_updated = date_last_updated, frequency = frequency, calculated_frequency = calculated_frequency, link=link)
            self.graph_instance.create(n)
        else:
            n = self.graph_instance.find_one(link)
            if (n["date_last_updated"] != ""):
                calculated_frequency = self._update_calculated_frequency(n["date_last_updated"], date_last_updated)
            n["date_last_updated"] = date_last_updated
            n["calculated_frequency"] = calculated_frequency
            n["frequency"] = frequency
            n.push()
        return n


    # Measures calculated frequency from subtracting previous date_last_updated to current date_last_updated (returns time in hours)
    def _update_calculated_frequency(self, prev_date_updated, new_date_updated):
        try:
            prev_date = datetime.datetime.strptime(prev_date_updated, "%Y-%m-%d")
            new_date = datetime.datetime.strptime(new_date_updated, "%Y-%m-%d")
            td = new_date - prev_date
            return td.total_seconds() // 3600
        except:
            return -1


    def add_edge(self, node_u, node_v, relationship):
        #if the relationship not exist create new edge
        #else update the tag
        if not self.check_relationship_exist(node_u,node_v):
            self.graph_instance.create(Relationship(node_u, "links_to", node_v, tag = relationship))
        else:
            for l in list(self.graph_instance.match(start_node = node_u, end_node = node_v, rel_type = "links_to")):
                l["tag"] = relationship
                l.push()

    def check_node_exist(self, link):
        return len(list(self.graph_instance.find(link))) != 0

    def check_relationship_exist(self,node_u, node_v):
        return len(list(self.graph_instance.match(start_node = node_u, end_node = node_v, rel_type = "links_to"))) > 0

    
    def delete_failed_webpages(self,link):
       if (self.check_node_exist(link) == False):
           return 
       node = self.get_node(link)
       self.delete_relationship(node)
       self.delete_incoming_relationship(node)
       self.graph_instance.delete(node)

    
    def delete_relationship(self,node_u):
        rels = list(self.graph_instance.match(rel_type="links_to",start_node= node_u,end_node = None))
        for r in rels:
            self.graph_instance.separate(r)


    def delete_incoming_relationship(self,node_u):
        rels = list(self.graph_instance.match(rel_type="links_to",end_node= node_u,start_node = None))
        for r in rels:
            self.graph_instance.separate(r)


    def get_node(self,link):
        return self.graph_instance.find_one(link)

    def get_node_information(self, link):
        check_node = self.graph_instance.data("MATCH (n {link: '" + link + "'} ) RETURN n")
        if len(check_node) == 0:
            return {}

        n = self.get_node(link)
        date_last_updated = n["date_last_updated"]
        calculated_frequency = n["calculated_frequency"]
        frequency = n["frequency"]

        node_data = {}
        node_data["date_last_updated"] = date_last_updated
        node_data["calculated_frequency"] = calculated_frequency
        node_data["frequency"] = frequency
        node_data["outlinks"] = self.get_outlinks(link)
        node_data["inlinks"] = self.get_inlinks(link)

        return node_data

    def get_outlinks(self, link):
        outlink_data = self.graph_instance.data("MATCH (n {link: '" + link + "'} )-->(node) RETURN node")
        outlinks = []
        for o in outlink_data:
            outlinks.append(o["node"]["link"])
        return outlinks

    def get_inlinks(self, link):
        inlink_data = self.graph_instance.data("MATCH (n {link: '" + link + "'} )<--(node) RETURN node")
        inlinks = []
        for o in inlink_data:
            inlinks.append(o["node"]["link"])
        return inlinks

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
        
        nodes = list(self.graph_instance.node_selector.select())
        for node in nodes:
            if isinstance(link, str):
                if not list(node.labels())[0] == link:
                    continue
            elif isinstance(link, (list, tuple)):
                if not list(node.labels())[0] in link:
                    continue
            print(list(node.labels())[0], node.get('page_rank'))


    def get_pagerank_dict(self, links=[]):
        #Get the pageranks for any given list of links (or all)
        
        nodes = list(self.graph_instance.node_selector.select())
        dct = {}
        for node in nodes:
            if isinstance(links, str):
                if not list(node.labels())[0] == links:
                    continue
            elif isinstance(links, (list, tuple)):
                if not list(node.labels())[0] in links:
                    continue
            #print(list(node.labels())[0], node.get('page_rank'))
            dct[list(node.labels())[0]] = node.get('page_rank')
        return dct

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



    #Prioritizer
    def prioritizer(self,outlinks):
        #get remaining time and number of inlink
        for ol in outlinks:
            if (self.check_node_exist(ol)):
                node = self.get_node(ol)
                number_inlinks = len(list(self.graph_instance.match(rel_type="links to",end_node= node,start_node = None)))
                node["number_inlink"] = number_inlinks
                node.push()

        new_links = sorted(outlinks, key = lambda k: -self.get_node(k)["number_inlink"])
        for ol in new_links:
            print(ol)













def convert_frequency_to_hours(frequency):
    if (frequency == "always"):
        return 0
    elif (frequency == "hourly"):
        return 1
    elif (frequency == "daily"):
        return 24
    elif (frequency == "weekly"):
        return 7*24
    elif (frequency == "monthly"):
        return 30*24
    elif (frequency == "yearly"):
        return 365*24
    elif (frequency == "never"):
        return -1
    elif (frequency == ""):
        return ""


