from flask import Flask, render_template, request
import sys
import json
import requests
execfile("../link_analysis/network.py")
network = Network()


def parse_session_information(session_info):
    sessionID = session_info["sessionID"]
    webpage = session_info["webpages"][0]["link"]
    date_last_updated = session_info["webpages"][0]["date_last_updated"]
    frequency = session_info["webpages"][0]["frequency"]
    outlinks = session_info["webpages"][0]["outlinks"]
    outlinks_webpage = outlinks[0]["link"]
    relationship = outlinks[0]["tags"]
    failed_webpages = session_info["failed_webpages"][0]
    
    
    #add nodes
    test_network = network.Network()
    test_network.add_node(webpage,date_last_updated,frequency)
    test_network.add_edge(network.get_node(webpage),outlinks_webpage,relationship)


#Test number_of_inlinks function
def test_number_of_inlinks():
    #Create 3 nodes. node1, node2 links to nodes 3. node1 also links to node2.
    network.add_node("www.node1.com","","")
    network.add_edge(network.get_node("www.node1.com"),"www.node3.com","h2")
    network.add_edge(network.get_node("www.node1.com"),"www.node2.com","h1")
    network.add_edge(network.get_node("www.node2.com"),"www.node3.com","p")
    assert(network.number_of_inlinks("www.node1.com") == 0)
    assert(network.number_of_inlinks("www.node2.com") == -1)
    assert(network.number_of_inlinks("www.node3.com") == -2)
    #clear data for other test
    network.graph_instance.delete_all()


#Test remaining_time function
'''def test_remaining_time():
    network.add_node("n1","","always")
    n1 = network.get_node("n1")
    n1["last_crawled_time"] = "2017-11-16 10:50:00"
    n1.push()
    network.remaining_time("n1")
    assert(n1["time_remaining"] == -1)
    network.add_node("n2","","hourly")
    n2 = network.get_node("n2")
    n2["last_crawled_time"] = "2017-11-16 10:50:00"
    n2.push()
    network.remaining_time("n2")
    assert(n2["time_remaining"] == 0)
    network.add_node("n3","","")
    n3 = network.get_node("n3")
    network.remaining_time("n3")
    assert(n3["time_remaining"] == 0)
    n2["last_crawled_time"] = "2017-11-16 12:40:00"
    n2.push()
    network.remaining_time("n2", "2017-11-16 12:50:00")
    assert(n3["time_remaining"] == float(50/60))'''

#Test prioritizer function
def test_prioritizer():
    network.add_edge(network.get_node("n1"),"n4","h4")
    network.add_node("n4","","always")
    n4 = network.get_node("n4")
    n4["last_crawled_time"] = "2017-11-16 10:50:00"
    n4.push()
    outlinks = ["n1","n2","n3"]
    network.prioritizer(outlinks)
    for o in outlinks:
        print o



    


def main():
    #test_network = network.Network()
    test_number_of_inlinks()
    test_remaining_time()
     #outlinks = ["www.example1.com","www.example3.com","www.example5.com","www.example4.com","www.exmapledelete.com"]
    #test_network.prioritizer(outlinks)
    
    test_prioritizer()



main()










