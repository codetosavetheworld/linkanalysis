# NOTES: calculatedFrequency is going to be in terms of hours or days? currently in hours

from py2neo import Graph, Node, Relationship

class Network():
	def __init__(self):
		self.graphInstance = Graph()
		self.tx = self.graphInstance.begin()

	def addNode(self, link, dateLastUpdated, frequency):
		calculatedFrequency = convertFrequencyToHours(frequency)
		n = Node(link, dateLastUpdated = dateLastUpdated, frequency = frequency, calculatedFrequency = calculatedFrequency)
		tx.create(n)

	# def addOutlink()
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