import requests



API_URl = "https://bitcoinfees.earn.com/api/v1/"


def recommended():
	path = "fees/recommended"
	return request(path)

def request(path, params=None, method="get", json=None):
	url = API_URl + path

	request_method = getattr(requests, method)  # Метод get или post
	response = request_method(url, params=params, json=json)

	return response.json()
	 
