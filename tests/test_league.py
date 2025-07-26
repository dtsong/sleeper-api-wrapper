from sleeper_wrapper import get_sport_state, League 

def test_get_league() -> None:
	""" Tests the get_league method"""
	league = League(355526480094113792)
	league_info = league.get_league()

	assert isinstance(league_info, dict)
	assert league_info["league_id"] == "355526480094113792"

def test_get_rosters() -> None:
	""" Tests the get_rosters method"""
	league = League(355526480094113792)
	rosters = league.get_rosters()
	
	assert isinstance(rosters, list) 
	assert len(rosters)>5

def test_get_users() -> None:
	""" Tests the get_users method"""
	league = League(355526480094113792)
	users = league.get_users()

	assert isinstance(users, list)
	assert isinstance(users[0]["user_id"], str)
	#I guess username is not a thing

def test_get_matchups() -> None:
	""" Tests the get_matchups method"""
	league = League(355526480094113792)
	matchup_info = league.get_matchups(4)
	first_item = matchup_info[0]
	assert isinstance(matchup_info, list)
	assert isinstance(first_item, dict)

	matchup_info = league.get_matchups(20)

	assert len(matchup_info) == 0

def test_get_playoff_winners_bracket() -> None:
	""" Tests the get_playoff_winners_bracket method"""
	league = League(355526480094113792)
	bracket = league.get_playoff_winners_bracket()
	first_item = bracket[0]

	assert isinstance(bracket, list)
	assert isinstance(first_item, dict)

def test_get_playoff_losers_bracket() -> None:
	""" Tests the get_playoff_losers method"""
	league = League(355526480094113792)
	bracket = league.get_playoff_losers_bracket()
	first_item = bracket[0]

	assert isinstance(bracket, list)
	assert isinstance(first_item, dict)

def test_get_transactions() -> None:
	""" Tests the get_transactions method
	Note: Not really sure wether this method works or what its supposed to do yet because the season has not fully started.
	"""
	league = League(355526480094113792)
	transactions = league.get_transactions(4)
	assert isinstance(transactions, list)

	transactions = league.get_transactions("4")
	assert isinstance(transactions, list)

def test_get_trades() -> None:
	""" Tests the get_trades method.
	Note: It would be better if we had trades to verify!"""
	league = League(355526480094113792)
	trades = league.get_trades(4)
	assert isinstance(trades, list)
	assert len(trades) == 0

def test_get_waivers() -> None:
	"""Tests the get_waivers method.
	Note: It would be better if we had waivers to verify!"""
	league = League(355526480094113792)
	waivers = league.get_waivers(4)
	assert isinstance(waivers, list)
	assert len(waivers) == 0

def test_get_free_agents() -> None:
	"""Tests the get_free_agents method.
	Note: It would be better if we had free agents to verify!"""
	league = League(355526480094113792)
	free_agents = league.get_free_agents(4)
	assert isinstance(free_agents, list)
	assert len(free_agents) == 0

def test_get_traded_picks() -> None:
	""" Tests the get_traded_picks method"""
	league = League(355526480094113792)
	traded_picks = league.get_traded_picks()
	first_item = traded_picks[0]

	assert isinstance(traded_picks, list)
	assert isinstance(first_item, dict)

def test_get_all_drafts() -> None:
	league = League(355526480094113792)
	drafts = league.get_all_drafts()
	first_item = drafts[0]

	assert isinstance(drafts, list)
	assert isinstance(first_item, dict)

def test_get_standings() -> None:
	""" Tests the get_standings method"""
	league = League(355526480094113792)
	rosters = league.get_rosters()
	users = league.get_users()
	standings = league.get_standings(rosters,users)
	first_item = standings[0]

	assert isinstance(first_item, tuple)
	assert len(standings)==12

def test_get_scoreboards() -> None:
	"""Tests the get_scoreoards method 
	-Needs more testing after the season starts"""
	league = League(442724598706860032)
	matchups = league.get_matchups(1)
	users = league.get_users()
	rosters = league.get_rosters()
	scoreboards = league.get_scoreboards(rosters, matchups, users, "pts_half_ppr", 2019, 1)
	print(scoreboards)
	assert isinstance(scoreboards, dict)

def test_get_close_games() -> None:
	""" 
	Tests the get_close_games method
	-Notes: Need to test more. 
	"""
	league = League(442724598706860032)
	matchups = league.get_matchups(1)
	users = league.get_users()
	rosters = league.get_rosters()
	scoreboards = league.get_scoreboards(rosters, matchups, users, "pts_half_ppr", 2019, 1)
	close_games = league.get_close_games(scoreboards, 10)
	assert isinstance(close_games, dict)

def test_empty_roster_spots() -> None:
	"""
	Tests the empty_roster_spots method

	Assertion 1: ensures that our function returns an integer for all league users (and not None)

	Assertion 2: ensures that our function returns None when an invalid user id is sent
	"""
	league = League(442724598706860032)
	users = league.get_users()
	rosters = league.get_rosters()
	# Assertion 1
	for user in users:
		user_id = user["user_id"]
		for roster in rosters:
			if user_id == roster["owner_id"]:
				assert league.empty_roster_spots(user_id) is not None
	
	# Assertion 2
	assert league.empty_roster_spots(-10000) is None

def test_get_negative_scores() -> None:
	pass

def test_get_sport_state(mocker) -> None:
	mock_data = {
		"week": 1, 
		"season_type": "regular"
		}
	mock_base_api_call = mocker.patch(
		"sleeper_wrapper.league.BaseApi._call", return_value=mock_data
		)
	response = get_sport_state("nfl")
	assert response == mock_data
	mock_base_api_call.assert_called_once_with(
		"https://api.sleeper.app/v1/state/nfl"
		)
