import logging

from .base_api import BaseApi

logger = logging.getLogger(__name__)

AVAILABLE_SPORTS = ["nfl", "nba", "mlb", "lcs"]

NFL_POSITIONS = ['TE', 'OL', 'CB', 'LB', 'RB', 'QB', 'K', 'DE', 'WR', 'DT', 'DL',
       'DB', 'OT', 'G', 'C', 'SS', 'LS', 'T', 'P', 'ILB', 'FB', 'FS',
       'OLB', 'NT', 'S', 'OG', 'K/P', 'DEF']

NBA_POSITIONS = ['SG', 'SF', 'PF', 'PG', 'C', 'DEF']

MLB_POSITIONS = ['1B', '2B', 'RP', 'SP', 'LF', 'RF', 'SS', '3B', 'CF', 'DH', 'C',
       'DEF']

LCS_POSITIONS = ['MID', 'TOP', 'JUN', 'ADC', 'SUP', 'DEF']

class Players(BaseApi):
	"""Retrieves player data from Sleeper.

	Attributes:
	  sport: str
		The sport to retrieve the players. Options include "nfl",
		"nba", "mlb", and "lcs".
	"""
	
	def __init__(self, sport: str = "nfl"):
		"""Initializes the instance based on the sport.

		Args:
		  sport: str
			The sport to retrieve the players. Options include "nfl",
			"nba", "mlb", and "lcs".
		"""
		if sport not in AVAILABLE_SPORTS:
			raise ValueError(f"Sport must be in {', '.join(AVAILABLE_SPORTS)}")
		self.sport = sport
		self._base_url = "https://api.sleeper.app/v1/players/{}".format(self.sport)

	def get_all_players(self, active: str = "", position: str = "") -> dict:
		"""Gets players from Sleeper.

		Retrieves data pertaining to each player in the Sleeper, including
		positions, biographical data, height / weight, team, and more.

		Args:
		  active: str
		    Set to true to only return active players; any other value is 
		    ignored - optional.
		  position: str
		    Only return players whose fantasy positions include this position,
		    such as QB - optional. Possible positions checked against what
		    appears in the data.

		Returns:
		  A dict of dicts where the keys are the player IDs and the values
		  contain all of the player information.
		"""

		message = """Please use this call sparingly, as it is intended only to be used once per day at most to keep your player IDs updated.

		Save the information to your own servers, if possible.
		"""
		logger.info(message)

		params = {}
		if active == "true":
			params["active"] = "true"
		else:
			active = ""

		if position != "":
			if self.sport == "nfl" and position not in NFL_POSITIONS:
				raise ValueError(f"Not a valid position for the {self.sport}. Please choose from {', '.join(NFL_POSITIONS)}")
			elif self.sport == "nba" and position not in NBA_POSITIONS:
				raise ValueError(f"Not a valid position for the {self.sport}. Please choose from {', '.join(NBA_POSITIONS)}")
			elif self.sport == "mlb" and position not in MLB_POSITIONS:
				raise ValueError(f"Not a valid position for the {self.sport}. Please choose from {', '.join(MLB_POSITIONS)}")
			elif self.sport == "lcs" and position not in LCS_POSITIONS:
				raise ValueError(f"Not a valid position for the {self.sport}. Please choose from {', '.join(LCS_POSITIONS)}")
			params["position"] = position

		return self._call("https://api.sleeper.app/v1/players/{}".format(sport), params=params)

	def get_trending_players(self, sport: str, add_drop: str = "add", hours: int = 24, limit: int = 25) -> list:
		"""Gets trending players from Sleeper.

		Retrieves the player ID and number of adds / drops for that player
		during the specified lookback hours.

		Args:
		  sport: str
			The sport to retrieve the players. Options include "nfl",
			"nba", "mlb", and "lcs".
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
		logger.info(message)
		return self._call("https://api.sleeper.app/v1/players/{}/trending/{}?lookback_hours={}&limit={}".format(sport, add_drop, hours, limit))
