# NOTES: calculatedFrequency is going to be in terms of hours or days? currently in hours

from py2neo import Graph, Node, Relationship
from py2neo.server import GraphSever
class Network():
	def __init__(self):
                self.server = GraphSever()
                self.server.start()
		self.graphInstance = Graph()
		self.tx = self.graphInstance.begin()

	def addNode(self, link, dateLastUpdated, frequency):
		calculatedFrequency = convertFrequencyToHours(frequency)
		n = Node(link, dateLastUpdated = dateLastUpdated, frequency = frequency, calculatedFrequency = calculatedFrequency)
		self.tx.create(n)
        
        def addEdge(self, nodeu, nodev, relation):
                self.tx.create(Relationship(nodeu,"links to",nodev,tag = relation))


            


	# def addOutlink()
        # We can use 0 to indicate always and -1 to indicate never
	def convertFrequencyToHours(frequency):
		if (frequency == "always" or frequency == ""):		# Unsure what to do for this?
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
		if (frequency == "never"):	 						# Also this
			return float("inf")


n = Network()
# n.addNode("www.example.com", "2015-05-02", "daily")
