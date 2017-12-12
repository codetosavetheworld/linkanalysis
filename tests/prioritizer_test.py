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
    
    # Add nodes from a sample sestion
    test_network = network.Network()
    test_network.add_node(webpage,date_last_updated,frequency)
    test_network.add_edge(network.get_node(webpage),outlinks_webpage,relationship)


#Test number_of_inlinks function
def test_number_of_inlinks():
    # Create 3 nodes. node1, node2 links to nodes 3. node1 also links to node2.
    network.add_node("www.node1.com","","")
    network.add_edge(network.get_node("www.node1.com"),"www.node3.com","h2")
    network.add_edge(network.get_node("www.node1.com"),"www.node2.com","h1")
    network.add_edge(network.get_node("www.node2.com"),"www.node3.com","p")
    assert(network.number_of_inlinks("www.node1.com") == 0)
    assert(network.number_of_inlinks("www.node2.com") == -1)
    assert(network.number_of_inlinks("www.node3.com") == -2)
    # Clear data for other test
    network.graph_instance.delete_all()


#Test prioritizer function and priority
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
    test_number_of_inlinks()
    test_remaining_time()  
    test_prioritizer()

main()










