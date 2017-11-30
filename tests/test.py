from flask import Flask, render_template, request
import sys
import json
import requests
import network


from flask import Flask, render_template, request
import sys
import json
import requests
import network






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
    test_network.add_edge(test_network.get_node(webpage),outlinks_webpage,relationship)








# --- Functions for premilimary testing (will be removed) ---
def make_sample_session_info():
    sample_session_info = {}
    sample_session_info["sessionID"] = 2
    
    sample_link = {}
    sample_link["link"] = "www.example5.com"
    sample_link["date_last_updated"] = "2017-01-22"
    sample_link["frequency"] = "daily"

    
    sample_outlink = {}
    sample_outlink["link"] = "www.example3.com"
    sample_outlink["tags"] = ["h2"]
    sample_link["outlinks"] = [sample_outlink]
    
    sample_session_info["webpages"] = [sample_link]
    sample_session_info["failed_webpages"] = ["www.example4.com"]
    
    json_data = json.dumps(sample_session_info)
    return json_data




def main():
     test_network = network.Network()
     outlinks = ["www.example1.com","www.example3.com","www.example5.com","www.example4.com","www.exmapledelete.com"]
     test_network.prioritizer(outlinks)


main()










