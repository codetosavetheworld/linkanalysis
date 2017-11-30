import requests
import json
import urllib

link_analysis_base_url = "http://127.0.0.1"

def test_prioritized_outlinks_API():
	# Test no POSTed data
	prioritized_links_endpoint = link_analysis_base_url + "/prioritizedOutlinks"
	headers = {"Content-Type": "application/json", "Accept":"application/json"}
	# r = requests.post(prioritized_links_endpoint, headers=headers)
	# assert(r.status_code == 400)
	# assert(r.text == "Cannot retrieve POSTed data")

	# Test incorrectly POSTed data
	# data = make_incorrect_session_info()
	# r = requests.post(prioritized_links_endpoint, data=data, headers=headers)
	# assert(r.status_code == 400)
	# assert(r.text == "Incorrect JSON format")

	# Test correctly POSTed data
	data = make_sample_session_info()
	r = requests.post(prioritized_links_endpoint, data=data, headers=headers)
	assert(r.status_code == 200)
	

# Makes incorrectly formatted JSON to post to /prioritizedOutlinks; incorrect 'webpage' key
def make_incorrect_session_info():
	sample_session_info = {}
	sample_session_info["webpage"] = []
	sample_session_info["failedWebpages"] = []
	json_data = json.dumps(sample_session_info)
	return json_data


# Makes a correctly formatted JSON to post to /prioritizedOutlinks
def make_sample_session_info():
    sample_session_info = {}

    sample_link = {}
    sample_link["link"] = "www.example.com"
    sample_link["dateLastUpdated"] = "2017-05-20"
    sample_link["frequency"] = "daily"

    sample_outlink = {}
    sample_outlink["link"] = "www.example2.com"
    sample_outlink["tags"] = ["h1"]
    sample_link["outlinks"] = [sample_outlink]

    sample_session_info["webpages"] = [sample_link]
    sample_session_info["failedWebpages"] = ["www.example3.com"]

    json_data = json.dumps(sample_session_info)
    return json_data

def test_page_rank_API():
	# Test no URL parameters
	page_rank_endpoint = link_analysis_base_url + "/pageRank"
	r = requests.get(page_rank_endpoint)
	assert(r.status_code == 400)
	assert(r.text == "Cannot retrieve URL parameters")
	
	# Test empty webpages list
	params = {}
	params["webpages"] = []
	r = requests.get(page_rank_endpoint + "?" + urllib.urlencode(params))
	assert(r.status_code == 400)
	assert(r.text == "Empty webpages list")

	# Test correctly formatted parameters
	params["webpages"] = ["www.example.com"]
	r = requests.get(page_rank_endpoint + "?" + urllib.urlencode(params))
	assert(r.status_code == 200)

if __name__ == "__main__":
	test_prioritized_outlinks_API()
	test_page_rank_API()

