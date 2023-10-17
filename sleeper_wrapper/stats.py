import logging
from typing import Union

from sleeper_wrapper.base_api import BaseApi

logging.basicConfig(level=logging.WARN)

warning_message = "The Stats API is no longer included in Sleeper's documentation, therefore we cannot guarantee that this class will continue working."

class Stats(BaseApi):
	"""Retrieves stats and projections from Sleeper's stats provider.

	Can retrieve stats and projections for Sleeper, though it is no longer
	officially documented and supported. Both stats and projections include
	box score and detailed stats as well as rollups to fantasy scores in
	standard scoring formats (standard, ppr, half ppr).
	"""

	def __init__(self):
		"""Initializes the instance for getting the stats."""
		logging.warning(warning_message)
		self._base_url = "https://api.sleeper.app/v1/stats/{}".format("nfl")
		self._projections_base_url = "https://api.sleeper.app/v1/projections/{}".format("nfl")

	def get_all_stats(self, season_type: str, season: Union[str, int]) -> dict:
		"""Retrieves all statistics for the given season.

		It supports detailed data going back until 2010 before only providing
		ranks for the various scoring formats. The detailed data contains information
		such as passing yards per attempt, field goal makes and misses by 10 yard
		buckets, snaps played, red zone statistics, and more.

		Arguments:
		  season_type: str
		    The type of season for pulling the stats. Supports "regular", "pre",
		    and "post".
		  season: Union[str, int]
		    The year of the season for pulling the stats.

		Returns:
		  A dictionary with each player and their statistics for the season.
		"""
		# season_type: "regular" works..."reg", "regular_season", "playoffs", and "preseason" don't seem to work
		return self._call("{}/{}/{}".format(self._base_url, season_type, season))

	def get_week_stats(self, season_type: str, season: Union[str, int], week: str) -> dict:
		"""Retrieves all statistics for the given season and week.

		It supports detailed data going back until 2010 before only providing
		ranks for the various scoring formats. The detailed data contains information
		such as passing yards per attempt, field goal makes and misses by 10 yard
		buckets, snaps played, red zone statistics, and more.

		Arguments:
		  season_type: str
		    The type of season for pulling the stats. Supports "regular", "pre",
		    and "post".
		  season: Union[str, int]
		    The year of the season for pulling the stats.
		  week: Union[str, int]
		    The week of the season for pulling the stats.

		Returns:
		  A dictionary with each player and their statistics for the season's week.
		"""
		return self._call("{}/{}/{}/{}".format(self._base_url, season_type, season, week))

	def get_all_projections(self, season_type: str, season: Union[str, int]) -> dict:
		"""Retrieves all projections for the given season.

		It supports data going back until 2018 and contains information such as
		passing yards per attempt, field goal makes and misses by 10 yard buckets,
		ADP, games played, and more.

		Arguments:
		  season_type: str
		    The type of season for pulling the projections. Supports "regular",
		    "pre", and "post".
		  season: Union[str, int]
		    The year of the season for pulling the projections.

		Returns:
		  A dictionary with each player and their projections for the year.
		"""
		return self._call("{}/{}/{}".format(self._projections_base_url, season_type, season))

	def get_week_projections(self, season_type: str, season: Union[str, int], week: str) -> dict:
		"""Retrieves all projections for the given season and week.

		It supports data going back until 2018 and contains information such as
		passing yards per attempt, field goal makes and misses by 10 yard buckets,
		ADP, games played, and more.

		Arguments:
		  season_type: str
		    The type of season for pulling the projections. Supports "regular", 
		    "pre", and "post".
		  season: Union[str, int]
		    The year of the season for pulling the projections.
		  week: Union[str, int]
		    The week of the season for pulling the projections.

		Returns:
		  A dictionary with each player and their projections for the year.
		"""
		return self._call("{}/{}/{}/{}".format(self._projections_base_url, season_type, season, week))

	def get_player_week_stats(self, stats: dict, player_id: str) -> Union[dict, None]:
		"""Gets a player's stats or projections from the given dictionary.

		Arguments:
		  stats: dict
		    Either stats or projections returned by the API. Can be for the whole
		    season or a single week.
		  player_id: str
		    The ID for the player of interest.

		Returns:
		  A dictionary of the player's stats or projections for the time period
		  associated with the dictionary provided to the function.
		"""

		return stats.get(player_id, None)


	def get_player_week_score(self, stats: dict, player_id: str) -> Union[dict, None]:
		"""Retrieves a player's points scored for the primary scoring formats.

		Arguments:
		  stats: dict
		    Either stats or projections returned by the API. Can be for the whole
		    season or a single week.
		  player_id: str
		    The ID for the player of interest.

		Returns:
		  A dictionary with the points scored for standard, PPR, and half PPR
		  scoring formats.
		"""
		result_dict = {}
		player_stats = stats.get(player_id, None)

		if player_stats:
			result_dict["pts_ppr"] = player_stats.get("pts_ppr", None)
			result_dict["pts_std"] = player_stats.get("pts_std", None)
			result_dict["pts_half_ppr"] = player_stats.get("pts_half_ppr", None)

		return result_dict

