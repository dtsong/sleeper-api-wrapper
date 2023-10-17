from typing import Union

from .base_api import BaseApi
from .stats import Stats

class League(BaseApi):
	def __init__(self, league_id: Union[str, int]) -> None:
		self.league_id = league_id
		self._base_url = "https://api.sleeper.app/v1/league/{}".format(self.league_id)
		self._league = self._call(self._base_url)

	def get_league(self) -> dict:
		return self._league

	def get_rosters(self) -> list:
		return self._call("{}/{}".format(self._base_url,"rosters"))

	def get_users(self) -> list:
		return self._call("{}/{}".format(self._base_url,"users"))

	def get_matchups(self, week: Union[str, int]) -> list:
		return self._call("{}/{}/{}".format(self._base_url,"matchups", week))

	def get_playoff_winners_bracket(self) -> list:
		return self._call("{}/{}".format(self._base_url,"winners_bracket"))

	def get_playoff_losers_bracket(self) -> list:
		return self._call("{}/{}".format(self._base_url,"losers_bracket"))

	def get_transactions(self, week: Union[str, int]) -> list:
		return self._call("{}/{}/{}".format(self._base_url,"transactions", week))

	def get_trades(self, week: Union[str, int]) -> list:
		transactions = self.get_transactions(week)
		return [t for t in transactions if t["type"] == "trade"]

	def get_waivers(self, week: Union[str, int]) -> list:
		transactions = self.get_transactions(week)
		return [t for t in transactions if t["type"] == "waiver"]

	def get_free_agents(self, week: Union[str, int]) -> list:
		transactions = self.get_transactions(week)
		return [t for t in transactions if t["type"] == "free_agent"]

	def get_traded_picks(self) -> list:
		return self._call("{}/{}".format(self._base_url,"traded_picks"))

	def get_all_drafts(self) -> list:
		return self._call("{}/{}".format(self._base_url, "drafts"))

	def map_users_to_team_name(self, users: list) -> dict:
		"""returns dict {user_id:team_name}"""
		users_dict = {}

		#Maps the user_id to team name for easy lookup
		for user in users:
			try:
				users_dict[user["user_id"]] = user["metadata"]["team_name"]
			except:
				users_dict[user["user_id"]] = user["display_name"]
		return users_dict

	def get_standings(self, rosters: list, users: list) -> dict:
		"""returns list of tuples (team_name, wins, losses, points)"""
		users_dict = self.map_users_to_team_name(users)

		roster_standings_list = []
		for roster in rosters:
			wins = roster["settings"]["wins"]
			points = roster["settings"]["fpts"]
			name = roster["owner_id"]
			losses = roster["settings"]["losses"]
			ties = roster["settings"]["ties"]
			if name is not None:
				roster_tuple = (wins, losses, ties, points, users_dict[name])
			else:
				roster_tuple = (wins, losses, ties, points, None)
			roster_standings_list.append(roster_tuple)

		roster_standings_list.sort(reverse = 1)

		clean_standings_list = []
		for item in roster_standings_list:
			clean_standings_list.append((item[4], str(item[0]), str(item[1]), str(item[2]), str(item[3])))
		
		return clean_standings_list

	def map_rosterid_to_ownerid(self, rosters: list) -> dict:
		"""returns dict {roster_id:[owner_id,pts]}"""
		result_dict = {}
		for roster in rosters:
			roster_id = roster["roster_id"]
			owner_id = roster["owner_id"]
			result_dict[roster_id] = owner_id

		return result_dict

	def get_scoreboards(self, rosters: list, matchups: list, users: list, score_type: str, season: Union[str, int], week: Union[str, int]) -> Union[dict, None]:
		"""returns dict {matchup_id:[(team_name,score), (team_name, score)]}"""
		roster_id_dict = self.map_rosterid_to_ownerid(rosters)

		if len(matchups) == 0:
			return None

		#Get the users to team name stats
		users_dict = self.map_users_to_team_name(users)

		#map roster_id to points
		scoreboards_dict = {}

		for team in matchups:
			matchup_id = team["matchup_id"]
			current_roster_id = team["roster_id"]
			owner_id = roster_id_dict[current_roster_id]
			if owner_id is not None:
				team_name = users_dict[owner_id]
			else:
				team_name = "Team name not available"

			team_score = self.get_team_score(team["starters"], score_type, season, week)
			if team_score is None:
				team_score = 0

			team_score_tuple = (team_name, team_score)
			if matchup_id not in scoreboards_dict:
				scoreboards_dict[matchup_id] = [team_score_tuple]
			else:
				scoreboards_dict[matchup_id].append(team_score_tuple)
		return scoreboards_dict

	def get_close_games(self, scoreboards: list, close_num: float) -> dict:
		""" -Notes: Need to find a better way to compare scores rather than abs value of the difference of floats. """
		close_games_dict = {}
		for key in scoreboards:
			team_one_score = scoreboards[key][0][1]
			team_two_score = scoreboards[key][1][1]

			if abs(team_one_score-team_two_score) < close_num:
				close_games_dict[key] = scoreboards[key]
		return close_games_dict

	def get_team_score(self, starters: list, score_type: str, season: Union[str, int], week: Union[str, int]) -> float:
		total_score = 0
		stats = Stats()
		week_stats = stats.get_week_stats("regular", season, week)
		for starter in starters:
			if stats.get_player_week_stats(week_stats, starter) is not None:
				try:
					total_score += stats.get_player_week_stats(week_stats, starter)[score_type]
				except KeyError:
					total_score += 0

		return total_score

	def empty_roster_spots(self, user_id: str) -> Union[int, None]:
		"""takes a user id and returns the number of empty roster spots on that team"""
		# get league JSON
		league = self.get_league()
		# get size of maximum roster
		max_roster_size = len(league["roster_positions"])

		# finds roster of user, returns max size - size of user roster
		rosters = self.get_rosters()
		for roster in rosters:
			if user_id == roster["owner_id"]:
				return max_roster_size - len(roster["players"])

		# returns None if user was not found
		return None

	
	def get_league_name(self) -> str:
		"""# returns name of league"""
		return self.get_league()["name"]

	def get_negative_scores(self, week: Union[str, int]) -> None:
		pass

	def get_rosters_players(self) -> None:
		pass
