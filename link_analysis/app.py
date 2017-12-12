from flask import Flask, render_template, request, jsonify
import sys
import json
import requests
import network
import ast
from datetime import datetime

app = Flask(__name__)
graph = network.Network()

# API used by crawling to POST session information and receive new links to crawl
@app.route("/prioritizedOutlinks", methods=["POST"])
def send_prioritized_outlinks():
    if request.data:
        json_data = request.get_json()
        outlinks = parse_session_information(json_data)
        if (outlinks == -1):
            return send_incorrect_json_error()

        prioritized_outlinks = graph.prioritize_dic(outlinks)
        print prioritized_outlinks
        return send_outlinks_response(prioritized_outlinks)
        
    else:
        return send_no_json_error()

# Parses session information sent by crawling and adds it to network graph
def parse_session_information(session_information):
    try:
        outlink_links = []
        failed_webpages = session_information["failedWebpages"]
        for w in failed_webpages:
            graph.delete_failed_webpages(w)
        for w in session_information["webpages"]:
            link = w["link"]
            date_last_updated = w["dateLastUpdated"]
            frequency = w["frequency"]
            outlinks = w["outlinks"]
            node_u = graph.add_node(link,date_last_updated,frequency)
            for o in outlinks:
                print "o:", o
                graph.add_edge(node_u,o["link"],o["tags"])
                outlink_links.append(o["link"])
        graph.update_time(str(datetime.now()))
        return outlink_links
    except:
      return -1

# Returns prioritized list of links to crawling as a response to their POST request
def send_outlinks_response(prioritized_outlinks):
    response_data = {}
    response_data["prioritizedLinks"] = prioritized_outlinks
    response = app.response_class(
        response = json.dumps(response_data),
        status = 200,
        mimetype='application/json'
    )
    return response

# Returns an error if the JSON sent by crawling is not formatted correctly
def send_incorrect_json_error():
    sys.stderr.write("ERROR: Incorrect JSON format from crawling\n")
    text = "Incorrect JSON format"
    response = app.response_class(
        response = text,
        status = 400,
        mimetype = "application/json"
    )
    return response

# Returns an error if crawling does not send a JSON with their request
def send_no_json_error():
    sys.stderr.write("ERROR: Cannot get POSTed data from crawling\n")
    text = "Cannot retrieve POSTed data"
    response = app.response_class(
        response = text,
        status = 400,
        mimetype = "application/json"
    )
    return response

# Updates page rank and retrieves page rank for requested web pages
@app.route("/pageRank", methods=["GET"])
def send_page_rank():
    try:
        webpages = ast.literal_eval(request.args.get("webpages"))
        if (len(webpages) == 0):
            return send_empty_list_error()
        graph.update_pagerank()
        page_rank_data = graph.get_ranking_data(webpages)
        return send_page_rank_response(page_rank_data)
    except:
        return send_no_arguments_error()

# Returns a successful page rank response to /pageRank GET request
def send_page_rank_response(page_rank_data):
    response = app.response_class(
        response = json.dumps(page_rank_data),
        status = 200,
        mimetype='application/json'
    )
    return response

# Returns an error in response if no webpages are requested in /pageRank GET request
def send_empty_list_error():
    sys.stderr.write("ERROR: Empty webpages list from ranking\n")
    text = "Empty webpages list"
    response = app.response_class(
        response = text,
        status = 400,
        mimetype = "application/json"
    )
    return response

# Returns an error in response if no URL parameters are given in /pageRank GET request
def send_no_arguments_error():
    sys.stderr.write("ERROR: Cannot get URL parameters from ranking\n")
    text = "Cannot retrieve URL parameters"
    response = app.response_class(
        response = text,
        status = 400,
        mimetype = "application/json"
    )
    return response

# --- Internal Testing APIs ---

# Returns all relevant information for a web page for internal testing - this includes inlinks and internal variables
@app.route("/getWebpageData", methods=["GET"])
def send_webpage_data():
    link = request.args.get("link")

    webpage_data = graph.get_node_information(link)
    response = app.response_class(
        response = json.dumps(webpage_data),
        status = 200,
        mimetype = "application/json"
    )
    return response


if __name__ == "__main__":
    app.config['DEBUG'] = True
    app.run(host="127.0.0.1", port=80, threaded=True)
