from flask import Flask, render_template, request
import sys
import json
import requests
execfile("../link_analysis/network.py")

# Unit tests for network functions
def parse_session_information(session_info):
    # Gets information from sample session
    sessionID = session_info["sessionID"]
    webpage = session_info["webpages"][0]["link"]
    date_last_updated = session_info["webpages"][0]["date_last_updated"]
    frequency = session_info["webpages"][0]["frequency"]
    outlinks = session_info["webpages"][0]["outlinks"]
    outlinks_webpage = outlinks[0]["link"]
    relationship = outlinks[0]["tags"]
    failed_webpages = session_info["failed_webpages"][0]

    # Initialize a network
    test_network = Network()
    # Test add node
    test_network.add_node(webpage,date_last_updated,frequency)
    # Test delete node
    test_network.delete_relationship(test_network.get_node(webpage))
    # Test add edge
    test_network.add_edge(test_network.get_node(webpage),outlinks_webpage,relationship)
    # Test deleting a failed webpage
    test_network.delete_failed_webpages(failed_webpages)

# Creates a sample session
def make_sample_session_info():
    sample_session_info = {}
    sample_session_info["sessionID"] = 1

    sample_link = {}
    sample_link["link"] = "www.example2.com"
    sample_link["date_last_updated"] = "2018-01-22"
    sample_link["frequency"] = "daily"

    sample_outlink = {}
    sample_outlink["link"] = "www.example4.com"
    sample_outlink["tags"] = ["h1"]
    sample_link["outlinks"] = [sample_outlink]

    sample_session_info["webpages"] = [sample_link]
    sample_session_info["failed_webpages"] = ["www.example4.com"]

    json_data = json.dumps(sample_session_info)
    return json_data

def main():
    session_info = make_sample_session_info()
    session_info = json.loads(session_info)
    parse_session_information(session_info)

main()
