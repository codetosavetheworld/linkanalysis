from py2neo import Graph, Node, Relationship
import sys
import os
execfile("../link_analysis/network.py")
network = Network()

def test_calculated_frequency():
	assert(network._update_calculated_frequency("2017-05-20", "2017-05-20") == 0.0)
	assert(network._update_calculated_frequency("2017-05-20", "2017_05-20") == -1)
	assert(network._update_calculated_frequency("2017-05-20", "2017-05-21") == 24.0)

if __name__ == "__main__":
	test_calculated_frequency()