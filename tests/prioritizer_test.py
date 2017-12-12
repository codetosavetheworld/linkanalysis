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
    network.graph_instance.delete_all()

#Test if priorizter function return error when webpage is not exist
def failed_test_nonexist_webpage():
    outlinks = ["www.one.com"]
    output_link = []
    assert(network.prioritizer(outlinks) != output_link)
    network.graph_instance.delete_all()

#Test if priorizter value if out of range
def failed_test_valid_prioritizing_value():
    tmp_string = ["one","two","three","four","five","six","seven","eight","nine","ten","wrong"]
    for x in range (0, 11):
        network.add_node(tmp_string[x], "2017-12-21","daily")
    new = network.prioritize_dic(tmp_string);
    for l in new["prioritizedLinks"]:
        assert(["priority_value"]<=100)
    network.graph_instance.delete_all()

def main():
    test_number_of_inlinks()
    failed_test_nonexist_webpage()
    failed_test_valid_prioritizing_value()
    
main()










