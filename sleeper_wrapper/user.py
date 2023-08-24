from typing import Union

from .base_api import BaseApi

class User(BaseApi):
	"""The data associated with a given Sleeper user."""

	def __init__(self, initial_user_input: Union[str, int]) -> None:
		"""Initializes the instance based on either username or user ID.

		Args:
		  initial_user_input: Union[str, int]
		    The Sleeper user ID or username for the user. May be provided as a
		    string or int.
		"""
		self._base_url = "https://api.sleeper.app/v1/user"
		self._user = self._call("{}/{}".format(self._base_url, initial_user_input))
		self._username = self._user["username"]
		self._user_id = self._user["user_id"]

	def get_user(self) -> dict:
		"""Returns the user's data."""
		return self._user

	def get_all_leagues(self, sport: str, season: Union[str, int]) -> list:
		"""Returns every league the user is in for that sport and season.

		Args:
		  sport: str
		    The sport to retrieve the leagues. Options include "nfl",
			"nba", and "lcs".
		  season: Union[str, int]
		    The season to retrieve the leagues. May be provided as either a
		    str or an int.

		Returns:
		  A list of dicts corresponding to the leagues a user is in. Each entry
		  will look akin to a specific League().get_league() call.
		"""
		return self._call("{}/{}/{}/{}/{}".format(self._base_url, self._user_id, "leagues", sport, season))

	def get_all_drafts(self, sport: str, season: Union[str, int]) -> list:
		"""Returns every draft the user is in for that sport and season.

		Args:
		  sport: str
		    The sport to retrieve the drafts. Options include "nfl",
			"nba", and "lcs".
		  season: Union[str, int]
		    The season to retrieve the drafts. May be provided as either a
		    str or an int.

		Returns:
		  A list of dicts corresponding to the drafts a user completed.
		"""
		return self._call("{}/{}/{}/{}/{}".format(self._base_url, self._user_id, "drafts", sport, season))

	def get_username(self) -> str:
		"""Retrieves username."""
		return self._username

	def get_user_id(self) -> str:
		"""Retrieves user_id."""
		return self._user_id

	def get_display_name(self) -> str:
		"""Retrieves display name."""
		return self._user["display_name"]
