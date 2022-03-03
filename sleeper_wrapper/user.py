from .base_api import BaseApi

class User(BaseApi):
	def __init__(self, initial_user_input):
		self.user_id = ""
		self._base_url = "https://api.sleeper.app/v1/user"
		self._user = self._call("{}/{}".format(self._base_url,initial_user_input))
		self._username = self._user["username"]
		self._user_id = self._user["user_id"]

	def get_user(self):
		return self._user

	def get_all_leagues(self, sport, season):
		return self._call("{}/{}/{}/{}/{}".format(self._base_url, self._user_id, "leagues", sport, season))

	def get_all_drafts(self, sport, season):
		return self._call("{}/{}/{}/{}/{}".format(self._base_url, self._user_id, "drafts",sport, season ))

	def get_username(self):
		"""A method that might be useful to convert user_id to username. For example a user can initialize with a user_id and get a username"""
		return self._username

	def get_user_id(self):
		"""A method that might be useful to convert username to user_id. For example a user can initialize with a username and get a userid"""
		return self._user_id
