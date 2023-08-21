import logging

from .base_api import BaseApi

logging.basicConfig(level=logging.INFO)

class Players(BaseApi):
	"""Retrieves player data from Sleeper."""
	
	def __init__(self):
		pass

	def get_all_players(self, sport: str = "nfl") -> dict:
		"""Gets all players from Sleeper.

		Retrieves data pertaining to each player in the Sleeper, including
		positions, biographical data, height / weight, team, and more.

		Args:
		  sport: str
			The sport to retrieve the players. Options include "nfl",
			"nba", and "lcs".

		Returns:
		  A dict of dicts where the keys are the player IDs and the values
		  contain all of the player information.
		"""

		message = """Please use this call sparingly, as it is intended only to be used once per day at most to keep your player IDs updated.

		Save the information to your own servers, if possible.
		"""
		logging.info(message)
		return self._call("https://api.sleeper.app/v1/players/nfl")

	def get_trending_players(self, sport: str, add_drop: str = "add", hours: int = 24, limit: int = 25) -> list:
		"""Gets trending players from Sleeper.

		Retrieves the player ID and number of adds / drops for that player
		during the specified lookback hours.

		Args:
		  sport: str
			The sport to retrieve the players. Options include "nfl",
			"nba", and "lcs".
		  add_drop: str
		    Type of action to retreive. Either "add" or "drop".
		  hours: int
		    The number of hours to look back.
		  limit: int
		    The number of players to retrieve.

		Returns:
		  A list of dicts containing the player ID and a count of the adds /
		  drops.
		"""


		message = """If you use this trending data, please attribute Sleeper.

		Copy the code below to embed it in your app:
		<iframe src="https://sleeper.app/embed/players/nfl/trending/add?lookback_hours=24&limit=25" width="350" height="500" allowtransparency="true" frameborder="0"></iframe>
		"""
		logging.info(message)
		return self._call("https://api.sleeper.app/v1/players/{}/trending/{}?lookback_hours={}&limit={}".format(sport, add_drop, hours, limit))
