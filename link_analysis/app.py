from flask import Flask, render_template, request, jsonify
import sys
import json
import requests

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
	failed_webpages = session_information["failedWebpages"]
	print "Need to remove failed webpage node and edges here"
	for w in session_information["webpages"]:
		try:
			link = w["link"]
			date_last_updated = w["date_last_updated"]
			frequency = w["frequency"]
			outlinks = w["outlinks"]
			print "Need to add node here"
			for o in outlinks:
				print "Need to add node here"
				print "Need to add edge here"
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