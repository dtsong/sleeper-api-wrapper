import requests
import json


class BaseApi():
	def _call(self, url):
		result_json_string = requests.get(url);
		try:
			result_json_string.raise_for_status()
		except requests.exceptions.HTTPError as e:
			return e
			#return SleeperWrapperException("Empty value returned")

		result = result_json_string.json()
		return result;