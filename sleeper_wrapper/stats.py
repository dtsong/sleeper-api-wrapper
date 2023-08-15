import logging
from typing import Union

from sleeper_wrapper.base_api import BaseApi

logging.basicConfig(level=logging.WARN)

warning_message = "The Stats API is no longer included in Sleeper's documentation, therefore we cannot guarantee that this class will continue working."

class Stats(BaseApi):
	
	def __init__(self):
		logging.warning(warning_message)
		self._base_url = "https://api.sleeper.app/v1/stats/{}".format("nfl")
		self._projections_base_url = "https://api.sleeper.app/v1/projections/{}".format("nfl")
		self._full_stats = None
		self._weekly_stats = dict.fromkeys([str(x) for x in range(1, 19)])

	def get_all_stats(self, season_type: str, season: Union[str, int]) -> dict:
		# season_type: "regular" works..."reg", "regular_season", "playoffs", and "preseason" don't seem to work
		self._full_stats = self._call("{}/{}/{}".format(self._base_url, season_type, season))
		return self._full_stats

	def get_week_stats(self, season_type: str, season: Union[str, int], week: str) -> dict:
		self._weekly_stats[week] = self._call("{}/{}/{}/{}".format(self._base_url, season_type, season, week))
		return self._weekly_stats[week]

	def get_all_projections(self, season_type: str, season: Union[str, int]) -> dict:
		return self._call("{}/{}/{}".format(self._projections_base_url, season_type, season))

	def get_week_projections(self, season_type: str, season: Union[str, int], week: str) -> dict:
		return self._call("{}/{}/{}/{}".format(self._projections_base_url, season_type, season, week))

	def get_player_stats(self, player_id: str) -> Union[dict, None]:
		try:
			return self._full_stats[player_id]
		except KeyError:
			return None

	def get_player_score(self, player_id: str) -> Union[dict, None]:
		scoring_formats = ["pts_ppr", "pts_half_ppr", "pts_std"]
		try:
			player_stats = self.get_player_stats(player_id)
			return {
				stat: value 
				for stat, value
				in player_stats.items()
				if stat in scoring_formats
			}
		except KeyError:
			return None

	def get_player_week_stats(self, player_id: str, week: str) -> Union[dict, None]:
		try:
			return self._weekly_stats[week][player_id]
		except KeyError:
			return None

	def get_player_week_score(self, player_id: str, week: str) -> Union[dict, None]:
		scoring_formats = ["pts_ppr", "pts_half_ppr", "pts_std"]
		try:
			player_stats = self.get_player_week_stats(player_id, week)
			return {
				stat: value
				for stat, value
				in player_stats.items()
				if stat in scoring_formats
			}
		except KeyError:
			return None
		