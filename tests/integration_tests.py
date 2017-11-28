import requests
import json
import urllib

link_analysis_base_url = "http://127.0.0.1"

def test_sample_session_create():
	prioritized_links_endpoint = link_analysis_base_url + "/prioritizedOutlinks"
	headers = {"Content-Type": "application/json", "Accept":"application/json"}
	
	# Test the correct creation/edit of resources
	create_json = session_create_json()
	r = requests.post(prioritized_links_endpoint, data=create_json, headers=headers)
	assert (r.status_code == 200)

	create_json = session_create_json2()
	r = requests.post(prioritized_links_endpoint, data=create_json, headers=headers)
	assert (r.status_code == 200)

	# Test the correct deletion of resources
	delete_json = session_delete_json()
	r = requests.post(prioritized_links_endpoint, data=delete_json, headers=headers)
	assert(r.status_code == 200)


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