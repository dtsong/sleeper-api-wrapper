from sleeper_wrapper import User

def test_get_user() -> None:
	user = User("swa")
	user = user.get_user()
	assert isinstance(user, dict)
	assert user['username'] == "swa"

def test_get_all_leagues() -> None:
	user = User("78623389212098560")
	leagues = user.get_all_leagues("nfl", 2019)

	assert isinstance(leagues, list)
	assert isinstance(leagues[0], dict)

	user = User("swa")
	leagues = user.get_all_leagues("nfl", 2019)
	assert isinstance(leagues, list)
	assert isinstance(leagues[0], dict)

def test_get_all_drafts() -> None:
	user = User("swa")
	drafts = user.get_all_drafts("nfl", 2019)
	assert isinstance(drafts, list)
	assert isinstance(drafts[0], dict)