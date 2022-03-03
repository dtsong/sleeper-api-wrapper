from sleeper_wrapper import Stats
import pytest

def test_get_all_stats(capsys):
	stats = Stats()
	all_stats = stats.get_all_stats('regular', 2018)
	assert isinstance(all_stats, dict)

def test_get_week_stats():
	stats = Stats()
	week_stats = stats.get_week_stats('regular', 2018, '2')
	assert isinstance(week_stats, dict)

def test_get_all_projections():
	stats = Stats()
	projections = stats.get_all_projections("regular", "2019")
	assert isinstance(projections, dict)

def test_get_week_projections():
	stats = Stats()
	week_projections = stats.get_week_projections("regular", 2018, "4")
	assert isinstance(week_projections, dict)

def test_get_player_week_score(capsys):
	stats = Stats()
	week_stats = stats.get_week_stats("regular",2018, 5)
	score = stats.get_player_week_score(week_stats, "GB")


	assert isinstance(score, dict)
	assert score["pts_ppr"] == None

	score = stats.get_player_week_score(week_stats, "1262")
	assert isinstance(score, dict)
	assert score["pts_ppr"] == None

	score = stats.get_player_week_score(week_stats, "5170")

	assert isinstance(score, dict)
	assert score["pts_ppr"] != None

	
	score = stats.get_player_week_score(week_stats, "30000000000")
	assert score is None

def test_get_player_week_stats():
	stats = Stats()
	week_stats = stats.get_week_stats("regular", 2018, 5)
	player_week_stats = stats.get_player_week_stats(week_stats, "1262")

	assert isinstance(player_week_stats, dict)

	player_week_stats = stats.get_player_week_stats(week_stats, "300000000")
	assert player_week_stats is None
