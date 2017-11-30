from flask import Flask, render_template, request, jsonify
import sys
import json
import requests
import network
import ast

app = Flask(__name__)
graph = network.Network()

@app.route("/")
def welcomePage():
  return "<html><body><h1>Team QQ: Link Analysis</h1><p>Team Members: Sara Khedr, Xini Yang, Enosh Neupane</p></body></html>"

@app.route("/prioritizedOutlinks", methods=["POST"])
def send_prioritized_outlinks():
	if request.data:
		json_data = request.get_json()
		parse_success = parse_session_information(json_data)
		if (parse_success == -1):
			return send_incorrect_json_error()

		prioritized_outlinks = []
		return send_outlinks_response(prioritized_outlinks)
		
	else:
		return send_no_json_error()

def parse_session_information(session_information):
  try:
  	failed_webpages = session_information["failedWebpages"]
  	for w in failed_webpages:
  		graph.delete_failed_webpages(w)
  	for w in session_information["webpages"]:
  		link = w["link"]
  		date_last_updated = w["dateLastUpdated"]
  		frequency = w["frequency"]
  		outlinks = w["outlinks"]
  		# node_u = graph.get_node(link)
  		node_u = graph.add_node(link,date_last_updated,frequency)
  		# graph.delete_relationship(node_u)
  		for o in outlinks:
  			node_v = graph.add_node(o["link"], "", "")
  			graph.add_edge(node_u,node_v,o["tags"])
  		return 0
  except:
	  return -1

def send_outlinks_response(prioritized_outlinks):
	response_data = {}
	response_data["prioritizedLinks"] = prioritized_outlinks
	response = app.response_class(
		response = json.dumps(response_data),
		status = 200,
		mimetype='application/json'
	)
	return response

def send_incorrect_json_error():
	sys.stderr.write("ERROR: Incorrect JSON format from crawling\n")
	text = "Incorrect JSON format"
	response = app.response_class(
		response = text,
		status = 400,
		mimetype = "application/json"
	)
	return response

def send_no_json_error():
	sys.stderr.write("ERROR: Cannot get POSTed data from crawling\n")
	text = "Cannot retrieve POSTed data"
	response = app.response_class(
		response = text,
		status = 400,
		mimetype = "application/json"
	)
	return response

@app.route("/pageRank", methods=["GET"])
def send_page_rank():
	print request
	try:
		webpages = ast.literal_eval(request.args.get("webpages"))
		if (len(webpages) == 0):
			return send_empty_list_error()
		
		page_rank_data = {}
		return send_page_rank_response(page_rank_data)
	except:
		return send_no_arguments_error()

def send_page_rank_response(page_rank_data):
	response = app.response_class(
		response = json.dumps(page_rank_data),
		status = 200,
		mimetype='application/json'
	)
	return response

def send_empty_list_error():
	sys.stderr.write("ERROR: Empty webpages list from ranking\n")
	text = "Empty webpages list"
	response = app.response_class(
		response = text,
		status = 400,
		mimetype = "application/json"
	)
	return response

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
	app.run(host="0.0.0.0", port=80, threaded=True)
