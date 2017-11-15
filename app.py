from flask import Flask, render_template, request
import sys
import json
import requests

app = Flask(__name__)
crawlingBaseURL = ""

@app.route("/receiveSessionID")
def receiveSessionID():
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

        sessionInfo = makeSampleSessionInfo()
        sessionInfo = json.loads(sessionInfo)
        parseSessionInformation(sessionInfo)


def getSessionInformation(sessionID):

    endpoint = crawlingBaseURL + "/sessionInformation"
    params = {
        "sessionID": sessionID
    }
    r = requests.get(endpoint, params=params)
    if (r.status_code != 200):
        sys.stderr.write("ERROR: Session information not received for session %d\n", sessionID)
    else:
        return r.json

def parseSessionInformation(sessionInfo):
    sessionID = sessionInfo["sessionID"]
    webpage = sessionInfo["link"]
    dateLastUpdated = sessionInfo["dateLastUpdated"]
    frequency = sessionInfo["frequency"]
    outlinks = sessionInfo["outlinks"]
    failedWebpages = sessionInfo["failedWebpages"]
    for o in outlinks:




# --- Functions for premilimary testing (will be removed) ---
def makeSampleSessionInfo():
    sampleSessionInfo = {}
    sampleSessionInfo["sessionID"] = 1

    sampleLink = {}
    sampleLink["link"] = "www.example.com"
    sampleLink["dateLastUpdated"] = "2017-05-20"
    sampleLink["frequency"] = "daily"

    sampleOutlink = {}
    sampleOutlink["link"] = "www.example2.com"
    sampleOutlink["tags"] = ["h1"]
    sampleLink["outlinks"] = [sampleOutlink]

    sampleSessionInfo["webpages"] = [sampleLink]
    sampleSession["failedWebpages"] = ["www.example3.com"]

    jsonData = json.dumps(sampleSessionInfo)
    return jsonData

if __name__ == "__main__":
    app.config['DEBUG'] = True
    app.run(host="127.0.0.1", port=80)







