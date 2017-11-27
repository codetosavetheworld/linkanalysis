import requests
import json

link_analysis_base_url = "http://127.0.0.1"

def test_prioritized_outlinks():
	# Test no POSTed data
	prioritized_links_endpoint = link_analysis_base_url + "/prioritizedOutlinks"
	headers = {"Content-Type": "application/json", "Accept":"application/json"}
	r = requests.post(prioritized_links_endpoint, headers=headers)
	status_code = r.status_code
	assert(status_code == 400)

	data = make_sample_session_info()
	r = requests.post(prioritized_links_endpoint, data=data, headers=headers)
	status_code = r.status_code
	assert(status_code == 200)


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
    sample_session_info["failedWebpages"] = ["www.example3.com"]

    json_data = json.dumps(sample_session_info)
    return json_data



if __name__ == "__main__":
	test_prioritized_outlinks()

