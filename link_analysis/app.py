from flask import Flask, render_template, request, jsonify
import sys
import json
import requests
import network

app = Flask(__name__)
crawling_url = ""
ranking_url = ""

@app.route("/prioritizedOutlinks", methods=["POST"])
def send_prioritized_outlinks():
	if request.data:
		json_data = request.get_json()
		parse_session_information(json_data)

		prioritized_links = []

		response_data = {}
		response_data["prioritizedLinks"] = prioritized_links
		response = app.response_class(
			response = json.dumps(response_data),
			status = 200,
			mimetype='application/json'
		)
		return response
	else:
		sys.stderr.write("ERROR: Cannot get POSTed data from ranking\n")
		response_message = {}
		response_message["text"] = "Cannot retrieve POSTed data"
		response = app.response_class(
			response = json.dumps(response_message),
			status = 400,
			mimetype = "application/json"
		)
		return response

def parse_session_information(session_information):
    graph = network.Network()
    failed_webpages = session_information["failedWebpages"]
    graph.delete_failed_webpages(failed_webpages)
    for w in session_information["webpages"]:
        try:
            link = w["link"]
            date_last_updated = w["date_last_updated"]
            frequency = w["frequency"]
            outlinks = w["outlinks"]
            node_u = graph.get_node(link)
            graph.add_node(link,date_last_updated,frequency)
            graph.delete_relationship(node_u)
            for o in outlinks:
                graph.add_edge(node_u,o["links"],o["tags"])
        except:
                send_incorrect_json_error()



def send_incorrect_json_error():
	response_message = {}
	response_message["text"] = "Incorrect JSON format"
	response = app.response_class(
		response = json.dumps(response_message),
		status = 400,
		mimetype = "application/json"
	)
	return response


if __name__ == "__main__":
	app.config['DEBUG'] = True
	app.run(host="127.0.0.1", port=80, threaded=True)
