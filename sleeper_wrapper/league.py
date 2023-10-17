from typing import Union

from .base_api import BaseApi
from .stats import Stats

class League(BaseApi):
	"""The data associated with the given Sleeper league.

	Can retrieve data for the league such as matchups, transactions, brackets,
	drafts, scoreboards, and more. Some of these are simple calls to the 
	Sleeper API while others add on a layer of data transformation or include
	multiple calls.

	Attributes:
	  league_id: Union[str, int]
	    The Sleeper ID for the league. May be provided as a string or int.
	"""

	def __init__(self, league_id: Union[str, int]) -> None:
		"""Initializes the instance based on league ID.

		Args:
		  league_id: Union[str, int]
		    Defines the league ID for data retrieval.
		"""
		self.league_id = league_id
		self._base_url = "https://api.sleeper.app/v1/league/{}".format(self.league_id)
		self._league = self._call(self._base_url)

	def get_league(self) -> dict:
		"""Returns the league data."""
		return self._league

	def get_rosters(self) -> list:
		"""Retrieves the league's rosters."""
		return self._call("{}/{}".format(self._base_url,"rosters"))

	def get_users(self) -> list:
		"""Retrieves the league's users."""
		return self._call("{}/{}".format(self._base_url,"users"))

	def get_matchups(self, week: Union[str, int]) -> list:
		"""Retrieves the league's matchups for the given week."""
		return self._call("{}/{}/{}".format(self._base_url,"matchups", week))

	def get_playoff_winners_bracket(self) -> list:
		"""Retrieves the winner's playoff bracket."""
		return self._call("{}/{}".format(self._base_url,"winners_bracket"))

	def get_playoff_losers_bracket(self) -> list:
		"""Retrieves the loser's playoff bracket."""
		return self._call("{}/{}".format(self._base_url,"losers_bracket"))

	def get_transactions(self, week: Union[str, int]) -> list:
		"""Retrieves all of a league's transactions for the given week."""
		return self._call("{}/{}/{}".format(self._base_url,"transactions", week))

	def get_trades(self, week: Union[str, int]) -> list:
		"""Retrieves the league's trades for the given week."""
		transactions = self.get_transactions(week)
		return [t for t in transactions if t["type"] == "trade"]

	def get_waivers(self, week: Union[str, int]) -> list:
		"""Retrieves the league's waiver transactions for the given week."""
		transactions = self.get_transactions(week)
		return [t for t in transactions if t["type"] == "waiver"]

	def get_free_agents(self, week: Union[str, int]) -> list:
		"""Retrieves the league's free agent transactions for the given week."""
		transactions = self.get_transactions(week)
		return [t for t in transactions if t["type"] == "free_agent"]

	def get_traded_picks(self) -> list:
		"""Retrieves the league's traded draft picks."""
		return self._call("{}/{}".format(self._base_url,"traded_picks"))

	def get_all_drafts(self) -> list:
		"""Retrieves all of a league's drafts.

		This will typically return only one draft. 
		"""
		return self._call("{}/{}".format(self._base_url, "drafts"))

	def map_users_to_team_name(self, users: list) -> dict:
		"""Creates a mapping from user ID to team name.
		
		Args:
		  users: list
		    List of user IDs for the league.

		Returns:
		  A dict mapping the user ID to team name for each user / team
		  combination in the league.
		"""
		users_dict = {}
		
		# Maps the user_id to team name for easy lookup
		for user in users:
			try:
				users_dict[user["user_id"]] = user["metadata"]["team_name"]
			except:
				users_dict[user["user_id"]] = user["display_name"]
		return users_dict

	def get_standings(self, rosters: list, users: list) -> dict:
		"""Creates standings based on the team's wins, losses, and ties.

		Args:
		  rosters: 
		    List of rosters for the league.
		  users: list
		    List of user IDs for the league.

		Returns:
		  List of tuples (team_name, wins, losses, points) sorted by wins in
		  descending order.
		"""
		users_dict = self.map_users_to_team_name(users)

		roster_standings_list = []
		for roster in rosters:
			wins = roster["settings"]["wins"]
			points = roster["settings"]["fpts"]
			name = roster["owner_id"]
			losses = roster["settings"]["losses"]
			if name is not None:
				roster_tuple = (wins, losses, points, users_dict[name])
			else:
				roster_tuple = (wins, losses, points, None)
			roster_standings_list.append(roster_tuple)

		roster_standings_list.sort(reverse = 1)

		clean_standings_list = []
		for item in roster_standings_list:
			clean_standings_list.append((item[3], str(item[0]), str(item[1]), str(item[2])))
		
		return clean_standings_list

	def map_rosterid_to_ownerid(self, rosters: list) -> dict:
		"""Creates a mapping from roster ID to owner ID.
		
		Args:
		  rosters: list
		    List of rosters for the league.

		Returns:
		  A dict mapping the roster ID to owner ID for each roster / owner
		  combination in the league.
		"""
		result_dict = {}
		for roster in rosters:
			roster_id = roster["roster_id"]
			owner_id = roster["owner_id"]
			result_dict[roster_id] = owner_id

		return result_dict

	def get_scoreboards(self, rosters: list, matchups: list, users: list, score_type: str, season: Union[str, int], week: Union[str, int]) -> Union[dict, None]:
		"""Returns the team names and scores from each matchup.

		Uses the provided information about the league to create a scoreboard
		for the given week. It pulls data from the rosters and users to find
		the team name and then pulls the team's score. It does not currently
		support leagues with custom scoring options and relies on the `Stats()`
		class, which is no longer officially documented by Sleeper.

		Args:
		  rosters: list
		    List of rosters for the league.
		  matchups: list
		    List of matchups for that week.
		  users: list
		    List of users for the league.
		  score_type: str
		    Scoring type for the league, eg "pts_std", "pts_ppr", or "pts_half_ppr"
		  season: Union[str, int]
		    The season to retrieve the scoreboards. May be provided as either a
		    str or an int.
		  week: Union[str, int]
		    The week to retrieve the scoreboards. May be provided as either a
		    str or an int.

		Returns:
		  A dict with the matchup ID as key and the corresponding teams' names
		  and scores for that matchup.
		"""
		roster_id_dict = self.map_rosterid_to_ownerid(rosters)

		if len(matchups) == 0:
			return None

		# Get the users to team name stats
		users_dict = self.map_users_to_team_name(users)

		# Map roster_id to points
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
		"""Returns scoreboard's games where final margin is beneath given number.

		Args:
		  scoreboards: list
		    List of scoreboards, which can be retrieved with the
		    `get_scoreboards()` method.
		  close_num: float
		    The final margin to use as a threshold for determining close games.

		Returns:
		  A dict of matchups qualifying as close.
		"""
		close_games_dict = {}
		for key in scoreboards:
			team_one_score = scoreboards[key][0][1]
			team_two_score = scoreboards[key][1][1]

			if abs(team_one_score-team_two_score) < close_num:
				close_games_dict[key] = scoreboards[key]
		return close_games_dict

	def get_team_score(self, starters: list, score_type: str, season: Union[str, int], week: Union[str, int]) -> float:
		"""Retrieves a team's scores for a week based on the score type.

		Uses the provided list of starters to pull their stats for that week
		with the given score type. It does not currently support leagues with
		custom scoring options because it pulls the pre-calculated score based
		on score type and does not calculate the score based on the league's
		scoring setting. It relies on the `Stats()` class to do this, which is 
		no longer officially documented by Sleeper.

		Args:
		  starters: list
		    A list of starters for the team.
		  score_type: str
		    Scoring type for the league, eg "pts_std", "pts_ppr", or "pts_half_ppr"
		  season: Union[str, int]
		    The season to retrieve the scores. May be provided as either a str 
		    or an int.
		  week: Union[str, int]
		    The week to retrieve the scores. May be provided as either a str or
		    an int.

		Returns:
		  The total score as a float for the team in that week.
		"""
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

	def empty_roster_spots(self, user_id: Union[str, int]) -> Union[int, None]:
		"""Returns the number of empty roster spots on a user's team.

		Args:
		  user_id: Union[str, int]
		    The user's ID to check for empty roster spots.

		Returns:
		  The number of empty roster spots assuming the user was found. Otherwise
		  returns `None`.
		"""
		# get size of maximum roster
		max_roster_size = len(self._league["roster_positions"])

		# finds roster of user, returns max size - size of user roster
		rosters = self.get_rosters()
		for roster in rosters:
			if user_id == roster["owner_id"]:
				return max_roster_size - len(roster["players"])

		# returns None if user was not found
		return None

	
	def get_league_name(self) -> str:
		"""Returns name of league."""
		return self._league["name"]

	def get_negative_scores(self, week: Union[str, int]) -> None:
		pass

	def get_rosters_players(self) -> None:
		pass
