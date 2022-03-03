from .base_api import BaseApi 

class Players(BaseApi):
	def __init__(self):
		pass

	def get_all_players(self):
		return self._call("https://api.sleeper.app/v1/players/nfl")

	def get_trending_players(self,sport, add_drop, hours=24, limit=25 ):
		return self._call("https://api.sleeper.app/v1/players/{}/trending/{}?lookback_hours={}&limit={}".format(sport, add_drop, hours, limit))