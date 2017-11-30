import requests
import json
import urllib

link_analysis_base_url = "http://127.0.0.1"
prioritized_links_endpoint = link_analysis_base_url + "/prioritizedOutlinks"
page_rank_endpoint = link_analysis_base_url + "/pageRank"
headers = {"Content-Type": "application/json", "Accept":"application/json"}

def test_sample_session_create():
	# Send sample POST session information
	create_json = session_create_json()
	r = requests.post(prioritized_links_endpoint, data=create_json, headers=headers)
	assert (r.status_code == 200)

	# Verify relationships and attributes
	params = {}
	params["link"] = "example.com"
	r = requests.get(link_analysis_base_url + "/getWebpageData" + "?" + urllib.urlencode(params))
	json_data = json.loads(r.text)
	assert(json_data["inlinks"] == [])
	assert(json_data["date_last_updated"] == "2017-05-20")
	assert(json_data["frequency"] == "daily")
	assert("example2.com" in json_data["outlinks"])
	assert("example3.com" in json_data["outlinks"])

	params["link"] = "example2.com"
	r = requests.get(link_analysis_base_url + "/getWebpageData" + "?" + urllib.urlencode(params))
	json_data = json.loads(r.text)
	assert(json_data["inlinks"] == ["example.com"])
	assert(json_data["date_last_updated"] == "")
	assert(json_data["frequency"] == "")
	assert(json_data["outlinks"] == [])
	assert(json_data["calculated_frequency"] == 0)

	params["link"] = "example3.com"
	r = requests.get(link_analysis_base_url + "/getWebpageData" + "?" + urllib.urlencode(params))
	assert(json_data["inlinks"] == ["example.com"])
	assert(json_data["date_last_updated"] == "")
	assert(json_data["frequency"] == "")
	assert(json_data["outlinks"] == [])
	assert(json_data["calculated_frequency"] == 0)

def test_page_rank():
	params = {}
	params["webpages"] = ["example.com", "example2.com", "example3.com"]
	r = requests.get(page_rank_endpoint + "?" + urllib.urlencode(params))
	print r.text

def test_sample_session_edit():
	# Send sample POST session information with changes to webpage metadata
	create_json = session_create_json2()
	r = requests.post(prioritized_links_endpoint, data=create_json, headers=headers)
	assert (r.status_code == 200)

	# Verify relationships and attributes
	params = {}
	params["link"] = "example.com"
	r = requests.get(link_analysis_base_url + "/getWebpageData" + "?" + urllib.urlencode(params))
	json_data = json.loads(r.text)
	assert(json_data["date_last_updated"] == "2017-06-02")
	assert(json_data["frequency"] == "never")
	assert(json_data["calculated_frequency"] == 312.0)

def test_sample_session_delete():
	# Test the correct deletion of resources
	delete_json = session_delete_json()
	r = requests.post(prioritized_links_endpoint, data=delete_json, headers=headers)
	assert(r.status_code == 200)

	params = {}
	params["link"] = "example.com"
	r = requests.get(link_analysis_base_url + "/getWebpageData" + "?" + urllib.urlencode(params))
	json_data = json.loads(r.text)
	assert(r.text == "{}")

	params["link"] = "example2.com"
	r = requests.get(link_analysis_base_url + "/getWebpageData" + "?" + urllib.urlencode(params))
	json_data = json.loads(r.text)
	assert(json_data["inlinks"] == [])
	assert(json_data["date_last_updated"] == "")
	assert(json_data["frequency"] == "")
	assert(json_data["outlinks"] == [])
	assert(json_data["calculated_frequency"] == 0)

	params["link"] = "example3.com"
	r = requests.get(link_analysis_base_url + "/getWebpageData" + "?" + urllib.urlencode(params))
	assert(json_data["inlinks"] == [])
	assert(json_data["date_last_updated"] == "")
	assert(json_data["frequency"] == "")
	assert(json_data["outlinks"] == [])
	assert(json_data["calculated_frequency"] == 0)

def session_create_json():
	sample_json = '''
	{	"webpages":
		[
			{
				"link": "example.com",
				"dateLastUpdated": "2017-05-20",
				"frequency": "daily",
				"outlinks":
				[
					{
						"link": "example2.com",
						"tags": ["h1", "h2"]
					},
					{
						"link": "example3.com",
						"tags": ["p"]
					}
				]
			},
			{
				"link": "example4.com",
				"dateLastUpdated": "2017-05-21",
				"frequency": "never",
				"outlinks": []
			}
		],
		"failedWebpages": ["example5.com"]
	} '''
	return sample_json

def session_create_json2():
	sample_json = '''
	{	"webpages":
		[
			{
				"link": "example.com",
				"dateLastUpdated": "2017-06-02",
				"frequency": "never",
				"outlinks": [] 
			}
		
		],
		"failedWebpages": []
	}
	'''
	return sample_json

def session_delete_json():
	sample_json = '''
	{
		"webpages": [],
		"failedWebpages": ["example.com"]
	}
	'''
	return sample_json

if __name__ == "__main__":
	test_sample_session_create()
	test_page_rank()
	test_sample_session_edit()
	test_sample_session_delete()