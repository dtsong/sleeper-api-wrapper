from sleeper_wrapper import League 

def test_get_league(capsys):
	""" Tests the get_league method"""
	league = League(355526480094113792)
	league_info = league.get_league()

	assert isinstance(league_info, dict)
	assert league_info["league_id"] == "355526480094113792"

def test_get_rosters():
	""" Tests the get_rosters method"""
	league = League(355526480094113792)
	rosters = league.get_rosters()
	
	assert isinstance(rosters, list) 
	assert len(rosters)>5

def test_get_users():
	""" Tests the get_users method"""
	league = League(355526480094113792)
	users = league.get_users()

	assert isinstance(users, list)
	assert isinstance(users[0]["user_id"], str)
	#I guess username is not a thing

def test_get_matchups(capsys):
	""" Tests the get_matchups method"""
	league = League(355526480094113792)
	matchup_info = league.get_matchups(4)
	first_item = matchup_info[0]
	assert isinstance(matchup_info, list)
	assert isinstance(first_item, dict)

	matchup_info = league.get_matchups(20)

	assert len(matchup_info) == 0

def test_get_playoff_winners_bracket():
	""" Tests the get_playoff_winners_bracket method"""
	league = League(355526480094113792)
	bracket = league.get_playoff_winners_bracket()
	first_item = bracket[0]

	assert isinstance(bracket, list)
	assert isinstance(first_item, dict)

def test_get_playoff_losers_bracket():
	""" Tests the get_playoff_losers method"""
	league = League(355526480094113792)
	bracket = league.get_playoff_losers_bracket()
	first_item = bracket[0]

	assert isinstance(bracket, list)
	assert isinstance(first_item, dict)

def test_get_transactions():
	""" Tests the get_transactions method
	Note: Not really sure wether this method works or what its supposed to do yet because the season has not fully started.
	"""
	league = League(355526480094113792)
	transactions = league.get_transactions(4)
	assert isinstance(transactions, list)

	transactions = league.get_transactions("4")
	assert isinstance(transactions, list)

def test_get_traded_picks():
	""" Tests the get_traded_picks method"""
	league = League(355526480094113792)
	traded_picks = league.get_traded_picks()
	first_item = traded_picks[0]

	assert isinstance(traded_picks, list)
	assert isinstance(first_item, dict)

def test_get_all_drafts():
	league = League(355526480094113792)
	drafts = league.get_all_drafts()
	first_item = drafts[0]

	assert isinstance(drafts, list)
	assert isinstance(first_item, dict)
def test_get_standings(capsys):
	""" Tests the get_standings method"""
	league = League(355526480094113792)
	rosters = league.get_rosters()
	users = league.get_users()
	standings = league.get_standings(rosters,users)
	first_item = standings[0]

	assert isinstance(first_item, tuple)
	assert len(standings)==12

def test_get_scoreboards(capsys):
	"""Tests the get_scoreoards method 
	-Needs more testing after the season starts"""
	league = League(442724598706860032)
	matchups = league.get_matchups(1)
	users = league.get_users()
	rosters = league.get_rosters()
	scoreboards = league.get_scoreboards(rosters, matchups, users, "pts_half_ppr", 1)
	print(scoreboards)
	assert isinstance(scoreboards, dict)

def test_get_close_games(capsys):
	""" 
	Tests the get_close_games method
	-Notes: Need to test more. 
	"""
	league = League(442724598706860032)
	matchups = league.get_matchups(1)
	users = league.get_users()
	rosters = league.get_rosters()
	scoreboards = league.get_scoreboards(rosters, matchups, users, "pts_half_ppr", 1)
	close_games = league.get_close_games(scoreboards, 10)
	assert isinstance(close_games, dict)

def test_empty_roster_spots():
	pass

def test_get_negative_scores():
	pass