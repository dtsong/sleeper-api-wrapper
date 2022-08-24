[![Build Status](https://travis-ci.org/SwapnikKatkoori/sleeper-api-wrapper.svg?branch=master)](https://travis-ci.org/SwapnikKatkoori/sleeper-api-wrapper)
![GitHub](https://img.shields.io/github/license/SwapnikKatkoori/sleeper-api-wrapper.svg?color=blue)
![GitHub issues](https://img.shields.io/github/issues/SwapnikKatkoori/sleeper-api-wrapper.svg?color=orange)
![PyPI](https://img.shields.io/pypi/v/sleeper-api-wrapper)
# sleeper-api-wrapper
A Python API wrapper for Sleeper Fantasy Football, as well as tools to simplify data received. It makes all endpoints found in the sleeper api docs: https://docs.sleeper.app/ available and turns the JSON response received into Python types for easy usage.

Ownership was transferred from @SwapnikKatkoori to @dtsong in March 2022 to continue efforts.
Original Repository: https://github.com/SwapnikKatkoori/sleeper-api-wrapper

# Table of Contents
1. [RoadMap](#roadmap)

2. [Installation](#install)

3. [Usage](#usage)

    * [League](#league)
        * [Initialize](#league_initialize)
        * [get_league()](#get_league)
        * [get_rosters()](#get_rosters)
        * [get_users()](#get_users)
        * [get_matchups()](#get_matchups)
        * [get_playoff_winners_bracket()](#get_playoff_winners_racket)
        * [get_playoff_losers_bracket()](#get_playoff_losers_racket)
        * [get_transactions()](#get_transactions)
        * [get_traded_picks()](#get_traded_picks)
        * [get_all_drafts()](#get_all_drafts)
        * [get_standings()](#get_standings)
        * [get_scoreboards()](#get_scoreboards)
        * [get_close_games()](#get_close_games)
    * [User](#user)
        * [Initialize](#user_initialize)
        * [get_user()](#get_user)
        * [get_all_leagues()](#get_all_leagues)
        * [get_all_drafts()](#get_all_drafts)
        * [get_username()](#get_username)
        * [get_user_id()](#get_user_id)
    * [Stats](#stats)
        * [Initialize](#stats_initialize)
        * [get_all_stats()](#get_all_stats)
        * [get_week_stats()](#get_week_stats)
        * [get_all_projections()](#get_all_projections)
        * [get_week_projections()](#get_week_projections)
        * [get_player_week_score()](#get_player_week_score)
    * [Players](#players)
        * [Initialize](#players_initialize)
        * [get_all_players()](#get_all_players)
        * [get_trending_players()](#get_trending_players)
4. [Notes](#notes)
5. [Dependencies](#depends)
6. [License](#license)

<a name="roadmap"></a>
# Project Roadmap
* Establish solid CICD practices with automated testing and validation of pull requests via GitHub Actions
* Ensure libraries are up to date and secure.
* Update endpoints and logic with the current Sleeper API docs
* Investigate performance optimization (effort, implementation, etc)

Want to help? Send me a message to @dtsong

<a name="install"></a>
# Install
~~~
pip install sleeper-api-wrapper
~~~

<a name="usage"></a>
# Usage
There are five objects that get data from the Sleeper API specified below. Most of them are intuitive based on the Sleeper Api docs.  

<a name="league"></a>

## League

<a name="league_initialize"></a>
### Initiaize
~~~
from sleeper_wrapper import League

league = League(league_id)
~~~
- league_id: (str)The id of your sleeper league

<a name="get_league"></a>
### League.get_league()
Gets data for the league that was specified when the League object was initialized. Data returned looks like: https://docs.sleeper.app/#get-a-specific-league

<a name="get_rosters"></a>
### League.get_rosters()
Gets all of the rosters in the league. Data returned looks like: https://docs.sleeper.app/#getting-rosters-in-a-league

<a name="get_users"></a>
### League.get_users()
Gets all of the users in the league. Data returned looks like: https://docs.sleeper.app/#getting-users-in-a-league

<a name="get_matchups"></a>
### League.get_matchups(week)
Gets all of the users in the league. Data returned looks like: https://docs.sleeper.app/#getting-matchups-in-a-league

- week:(int or string) week of the matchups to be returned.

<a name="get_playoff_winners_bracket"></a>
### League.get_playoff_winners_bracket()
Gets the playoff winners bracket for the league. Data returned looks like: https://docs.sleeper.app/#getting-the-playoff-bracket

<a name="get_playoff_losers_bracket"></a>
### League.get_playoff_losers_bracket()
Gets the playoff losers bracket for the league. Data returned looks like: https://docs.sleeper.app/#getting-the-playoff-bracket

<a name="get_transactions"></a>
### League.get_transactions(week)
Gets all of the transactions data in the league. Data returned looks like: https://docs.sleeper.app/#get-transactions

- week:(int or str) week of the matchups to be returned.

<a name="get_traded_picks"></a>
### League.get_traded_picks()
Gets all of the traded picks in the league. Data returned looks like: https://docs.sleeper.app/#get-traded-picks

<a name="get_all_drafts"></a>
### League.get_all_drafts()
Gets all of the draft data in the league. Data returned looks like: https://docs.sleeper.app/#get-all-drafts-for-a-league

<a name="get_standings"></a>
### League.get_standings(rosters, users)
Gets the standings in a league. Returns a list of the standings in order of most wins to least wins.
- rosters: (list)The data returned by the get_rosters() method.
- users: (list)The data returned by the get_standings() method.

Data returned looks like:

~~~
[(username, number_of_wins, number_of_losses, total_points), (username, number_of_wins, number_of_losses, total_points),...]
~~~
- types: username(str), number_of_wins(int), number_of_losses(int), total_points(int)
- "username" could be None if a user does not have a username.

Example usage:

~~~
    	league = League(league_id)
	rosters = league.get_rosters()
	users = league.get_users()
	standings = league.get_standings(rosters,users)
~~~

<a name="get_scoreboards"></a>
### League.get_scoreboards(rosters, matchups, users, score_type, week)
Gets the scoreboards of the league. Returns a dict of league mathups and scores.
- rosters: (list)The data returned by the get_rosters() method.
- matchups: (list)The data returned by the get_mathcups() method.
- users: (list)The data returned by the get_standings() method.
- score_type: (string) either "pts_std", "pts_half_ppr", or "pts_ppr".
- week: (int) week

Data returned looks like:

~~~
{matchup_id:[(team_name,score), (team_name, score)], matchup_id:[(team_name,score), (team_name, score)], ... }
~~~
- types: matchup_id(int), team_name(str), score(float)

Example usage:

~~~
    	league = League(league_id)
	matchups = league.get_matchups(11)
	users = league.get_users()
	rosters = league.get_rosters()
	scoreboards = league.get_scoreboards(rosters, matchups, users)
~~~
<a name="get_close_games"></a>
### League.get_close_games(scoreboards, close_num)
Gets all of the close games in a league. Returns a dict.
- scoreboards: (dict)The data returned by the get_scoreboards() method.
- close_num: (int)How close the games need to be considered a close game. For example, if the close num is 5, the data returned would only include matchups that are within 5 points of each other.

Data returned looks like:

~~~
{matchup_id:[(team_name,score), (team_name, score)], matchup_id:[(team_name,score), (team_name, score)], ... }
~~~
- types: matchup_id(int), team_name(str), score(float)

Example usage:

~~~
    league = League(league_id)
	matchups = league.get_matchups(11)
	users = league.get_users()
	rosters = league.get_rosters()
	scoreboards = league.get_scoreboards(rosters, matchups, users)
	close_games = league.get_close_games(scoreboards, 10)
~~~
<a name="user"></a>
## User

<a name="user_initialize"></a>
### Initialize
~~~
from sleeper_wrapper import User

user = User(user_id)
~~~
- user_id: (str)The id of a user. It can also be a username.

<a name="get_user"></a>
### User.get_user()
Gets data for the user that was specified by the user_id or username when the User object was initialized. Data returned looks like: https://docs.sleeper.app/#user

<a name="get_all_leagues"></a>
### User.get_all_leagues(sport, season)
Gets the data of all of the leagues that a user belongs to. Data returned looks like: https://docs.sleeper.app/#get-all-leagues-for-user

- sport: (str)The sport of the leagues. Currently, it can only be "nfl".
- season: (int or str)The season of the leagues. ex. 2018,2019, etc.

<a name="get_all_drafts"></a>
### User.get_all_drafts(sport, season)
Gets the data of all of the drafts of a user in the specified season. Data returned looks like: https://docs.sleeper.app/#get-all-drafts-for-user

- sport: (str)The sport of the leagues. Currently, it can only be "nfl".
- season: (int or str)The season of the leagues. ex. 2018,2019, etc.

<a name="get_username"></a>
### User.get_username()
Returns the username of the User. This can be useful if the User was initialized with a user_id.

<a name="get_user_id"></a>
### User.get_user_id()
Returns the user_id of the User. This can be useful if the User was initialized with a username.

<a name="stats"></a>
## Stats

<a name="stats_initialize"></a>
### Initialize
~~~
from sleeper_wrapper import Stats

stats = Stats()
~~~
<a name="get_all_stats"></a>
### Stats.get_all_stats(season_type, season)
Gets all of the stats in a season. Data returned looks like: https://docs.sleeper.app/#stats-and-projections

- season_type: (str) The type of the season. Supports "regular", "pre", "post".
- season: (int or str) The season of the leagues. ex. 2018,2019, etc.

<a name="get_week_stats"></a>
### Stats.get_week_stats(season_type, season, week)
Gets all of the stats for a specific week in a season. Data returned looks like: https://docs.sleeper.app/#stats-and-projections

- season_type: (str) The type of the season. Supports "regular", "pre", "post".
- season: (int or str) The season of the leagues. ex. 2018,2019, etc.
- week: (int or str) The week of the stats to get.

<a name="get_all_projections"></a>
### Stats.get_all_projections(season_type, season)
Gets all of the projections in a season. Data returned looks like: https://docs.sleeper.app/#stats-and-projections

- season_type: (str) The type of the season. Supports "regular", "pre", "post".
- season: (int or str) The season of the leagues. ex. 2018,2019, etc.

<a name="get_week_projections"></a>
### Stats.get_week_projections(season_type, season, week)
Gets all of the projections for a specific week in a season. Data returned looks like: https://docs.sleeper.app/#stats-and-projections

- season_type: (str) The type of the season. Supports "regular", "pre", "post".
- season: (int or str) The season of the leagues. ex. 2018,2019, etc.
- week: (int or str) The week of the stats to get.

<a name="get_player_week_score"></a>
### Stats.get_player_week_score(week_stats, player_id)
Gets the player score of a specified week.

- week_stats: (dict) The result of the method get_week_stats().
- player_id: (str) The player_id of the player to get the stats of. ex. 2018,2019, etc.

Data returned looks like:
~~~
{'pts_ppr':score_float, 'pts_std': score_float, 'pts_half_ppr': score_float}
~~~
- types: score_float(float)
- If the score is not available for a format, the value will be None.

Example usage:

~~~
    	stats = Stats()
	week_stats = stats.get_week_stats("regular",2018, 5)
	score = stats.get_player_week_score(week_stats, "DET")
~~~
<a name="players"></a>
## Players

<a name="players_initialize"></a>
### Initiaize
~~~
from sleeper_wrapper import Players

players = Players()
~~~
<a name="get_all_players"></a>
### Players.get_all_players()
Gets all of the players in fantasy football. Data returned looks like: https://docs.sleeper.app/#fetch-all-players

<a name="get_trending_players"></a>
### Players.get_trending_players(sport, add_drop, hours, limit)
Gets all of the players in fantasy football. Data returned looks like: https://docs.sleeper.app/#trending-players

- sport: (str) The sport to get. Supports only "nfl" right now.
- add_drop: (str) Either "add" or "drop".
- hours: (int or str) Number of hours to look back. Default is 24 hours.
- limit: (int or str) Number of results you want. Default is 25.

<a name="notes"></a>
# Notes
This package is intended to be used by Python version 3.5 and higher. There might be some wacky results for previous versions.

<a name="depends"></a>
# Dependencies

[requests](https://github.com/kennethreitz/requests)
- Used for all http requests in sleeper_wrapper

[pytest](https://github.com/pytest-dev/pytest)
- Used for all testing in sleeper_wrapper

<a name="license"></a>
# License
This project is licensed under the terms of the MIT license.
