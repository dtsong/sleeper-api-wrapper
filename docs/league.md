# League

## League
`sleeper_wrapper.League(league_id)`

Instantiating a `League` object will allow interaction with Sleeper's [Leagues endpoint](https://docs.sleeper.com/#leagues) by pulling data for the league specified by the `league_id`. Examples for how the data is structured for methods hitting the API directly may be found in their documentation for the endpoint.


### Attributes
`league_id` _(Union[int, str])_: The Sleeper ID for the league. May be provided as a string or int.

### Methods
`get_league()`: Returns the league's data.

`get_rosters()`: Retrieves the league's rosters.

`get_users()`: Retrieves the league's users.

`get_matchups(week)`: Retrieves the league's matchups for the given week.

`get_playoff_winners_bracket()`: Retrieves the winner's playoff bracket.

`get_playoff_losers_bracket()`: Retrieves the loser's playoff bracket.

`get_transactions(week)`: Retrieves all of a league's transactions for the given week.

`get_trades(week)`: Retrieves the league's trades for the given week.

`get_waivers(week)`: Retrieves the league's waiver transactions for the given week.

`get_free_agents(week)`: Retrieves the league's free agent transactions for the given week.

`get_traded_picks()`: Retrieves the league's traded draft picks.

`get_all_drafts()`: Retrieves all of a league's drafts. This will typically return only one draft.

`map_users_to_team_name(users)`: Creates and returns a mapping from user ID to team name.

`get_standings(rosters, users)`: Creates and returns standings based on the team's wins, losses, and ties.

`map_rosterid_to_ownerid(rosters)`: Creates and returns a mapping from roster ID to owner ID.

`get_scoreboards(rosters, matchups, users, score_type, season, week)`: Returns the team names and scores from each matchup.

Uses the provided information about the league to create a scoreboard
for the given week. It pulls data from the rosters and users to find
the team name and then pulls the team's score. It does not currently
support leagues with custom scoring options and relies on the `Stats()`
class, which is no longer officially documented by Sleeper.

`get_close_games(scoreboards, close_num)`: Returns scoreboard's games where final margin is beneath given number.

`get_team_score(starters, score_type, season, week)`: Retrieves a team's scores for a week based on the score type.

Uses the provided list of starters to pull their stats for that week
with the given score type. It does not currently support leagues with
custom scoring options because it pulls the pre-calculated score based
on score type and does not calculate the score based on the league's
scoring setting. It relies on the `Stats()` class to do this, which is 
no longer officially documented by Sleeper.

`empty_roster_spots(user_id)`: Returns the number of empty roster spots on a user's team.

`get_league_name()`: Returns name of league.


## Functions

`get_sport_state()`: Returns current state for the given sport.


## Examples
```
from sleeper_wrapper import League

# creates the league object and stores its basic data
league = League(league_id)
rosters = league.get_rosters()
users = league.get_users()

# gets the matchups for the first week
matchups = league.get_matchups(week=1)

# retrieves the standings and returns them with user information
standings = league.get_standings(rosters=rosters, users=users)

# retrieves the scoreboard for the given week and returns it with user information
scoreboards = league.get_scoreboards(rosters=rosters, matchups=matchups, users=users, score_type="pts_std", season=2023, week=1)

# gets current NFL state, e.g. current week
state = get_sport_state(sport="nfl")
```