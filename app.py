from flask import Flask, render_template, request
import sys
import json
import requests

app = Flask(__name__)
crawling_baseURL = ""

@app.route("/receiveSessionID")
def receive_sessionID():
    # Gets the session ID from request data
    sessionID = request.args.get("sessionID")
    if (sessionID == None):
        sys.stderr.write("ERROR: No session ID received\n")

        response = {}
        response["message"] = "No session ID given"

        response = app.response_class(
            response = json.dumps(response),
            status = 400,
            mimetype = 'application/json'
            )

        return response


    else:
        # Makes request to crawling for session information
        # sessionInfo = getSessionInformation(sessionID)

        session_info = make_sample_session_info()
        session_info = json.loads(session_info)
        parse_session_information(session_info)


def get_session_information(sessionID):

    endpoint = crawling_baseURL + "/sessionInformation"
    params = {
        "sessionID": sessionID
    }
    r = requests.get(endpoint, params=params)
    if (r.status_code != 200):
        sys.stderr.write("ERROR: Session information not received for session %d\n", sessionID)
    else:
        return r.json

def parse_session_information(session_info):
    sessionID = session_info["sessionID"]
    webpage = session_info["link"]
    date_last_updated = session_info["date_last_updated"]
    frequency = session_info["frequency"]
    outlinks = session_info["outlinks"]
    failed_webpages = session_info["failed_webpages"]
#for o in outlinks:




# --- Functions for premilimary testing (will be removed) ---
def make_sample_session_info():
    sample_session_info = {}
    sample_session_info["sessionID"] = 1

    sample_link = {}
    sample_link["link"] = "www.example.com"
    sample_link["date_last_updated"] = "2017-05-20"
    sample_link["frequency"] = "daily"

    sample_outlink = {}
    sample_outlink["link"] = "www.example2.com"
    sample_outlink["tags"] = ["h1"]
    sample_link["outlinks"] = [sample_outlink]

    sample_session_info["webpages"] = [sample_link]
    sample_session["failedWebpages"] = ["www.example3.com"]

    json_data = json.dumps(sampleSessionInfo)
    return json_data

if __name__ == "__main__":
    app.config['DEBUG'] = True
    app.run(host="127.0.0.1", port=80)







