from sleeper_wrapper import Players

def test_get_trending_players() -> None:
	players = Players()
	added = players.get_trending_players("nfl","add", 1, 4)

	dropped = players.get_trending_players("nfl","drop")
